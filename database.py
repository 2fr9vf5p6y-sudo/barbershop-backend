from pathlib import Path

from sqlalchemy import Float, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

DB_PATH = Path(__file__).resolve().parent / "barbershop.db"
engine = create_engine(
    f"sqlite:///{DB_PATH.as_posix()}",
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column("category_id", nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    desc: Mapped[str] = mapped_column(String(100), nullable=False)
    duration: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)


class Master(Base):
    __tablename__ = "masters"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    specialization: Mapped[str] = mapped_column(nullable=False)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        if session.scalar(select(Master.id).limit(1)) is None:
            session.add_all([
                Master(id=1, name="Анна", specialization="Парикмахер"),
                Master(id=2, name="Мария", specialization="Визажист"),
            ])
            session.commit()


def get_db():
    with SessionLocal() as session:
        yield session


def find_master(master_id: int) -> Master | None:
    with SessionLocal() as session:
        return session.get(Master, master_id)


init_db()
