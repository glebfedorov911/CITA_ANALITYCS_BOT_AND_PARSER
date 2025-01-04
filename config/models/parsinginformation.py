from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime

from .base import Base


class ParsingInformation(Base):
    name: Mapped[str] = mapped_column(nullable=True)
    region: Mapped[str] = mapped_column(nullable=False)
    office: Mapped[str] = mapped_column(nullable=False)
    service: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    was_get: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        if self.name:
            return self.name 
        return f"{self.region} - {self.office} - {self.service}"