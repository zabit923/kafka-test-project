from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.aplications.schemas import AplicationCreate
from config import KAFKA_TOPIC
from core.database.models.aplications import Aplication
from core.kafka.producer import KafkaProducer


kafka_producer = KafkaProducer()


class AplicationService:
    @staticmethod
    async def create_aplication(
        aplication_data: AplicationCreate,
        session: AsyncSession,
    ) -> Aplication:
        new_aplication = Aplication(
            user_name=aplication_data.user_name,
            description=aplication_data.description
        )
        session.add(new_aplication)
        await session.commit()
        await kafka_producer.start()
        try:
            message = {
                "id": new_aplication.id,
                "user_name": new_aplication.user_name,
                "description": new_aplication.description,
                "created_at": new_aplication.created_at.isoformat()
            }
            await kafka_producer.send_message(KAFKA_TOPIC, message)
        finally:
            await kafka_producer.stop()
        return new_aplication

    @staticmethod
    async def get_aplications(
        session: AsyncSession, user_name: Optional[str], page: int, size: int
    ) -> dict:
        statement = select(Aplication)
        if user_name:
            statement = statement.where(Aplication.user_name == user_name)

        statement = statement.offset((page - 1) * size).limit(size)
        result = await session.execute(statement)
        aplications = result.scalars().all()

        return {
            "items": aplications,
            "page": page,
            "size": size,
        }
