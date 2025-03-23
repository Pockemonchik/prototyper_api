from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseSqlAlchemyModel(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
