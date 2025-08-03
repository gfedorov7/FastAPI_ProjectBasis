from sqlalchemy.orm import (
    mapped_column, Mapped,
    DeclarativeBase, declared_attr
)


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    def to_dict(self) -> dict:
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )
