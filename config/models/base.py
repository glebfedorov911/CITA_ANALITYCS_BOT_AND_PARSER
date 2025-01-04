from sqlalchemy.orm import declared_attr, DeclarativeBase, Mapped, mapped_column

from typing import TypeVar


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)

type_base = TypeVar("type_base", bound=Base)