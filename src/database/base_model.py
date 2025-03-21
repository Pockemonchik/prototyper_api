from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseSqlAchemyModel(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
