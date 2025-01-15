from datetime import datetime

from sqlalchemy import VARCHAR, TEXT, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column

from core.database.models import Base, TableNameMixin


class Aplication(TableNameMixin, Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_name: Mapped[str] = mapped_column(VARCHAR(128))
    description: Mapped[str] = mapped_column(TEXT)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), nullable=False
    )

    def __repr__(self):
        return f"{self.user_name}"
