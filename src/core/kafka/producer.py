from aiokafka import AIOKafkaProducer
import json
from config import KAFKA_BOOTSTRAP_SERVERS


class KafkaProducer:
    def __init__(self, bootstrap_servers: str = KAFKA_BOOTSTRAP_SERVERS):
        self.bootstrap_servers = bootstrap_servers
        self.producer = None

    async def start(self):
        self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
        await self.producer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def send_message(self, topic: str, message: dict):
        payload = json.dumps(message).encode("utf-8")
        await self.producer.send_and_wait(topic, payload)
