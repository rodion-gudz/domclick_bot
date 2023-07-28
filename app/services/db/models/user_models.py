from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.services.db.models import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    lang: Mapped[str] = mapped_column(nullable=True, server_default="ru")
