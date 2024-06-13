from datetime import datetime

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Boolean,
    DateTime,
    func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    plants: Mapped['Plants'] = relationship(back_populates='user')


class Plants(Base):
    __tablename__ = 'plants'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    name: Mapped[str]
    plant_type: Mapped[str]
    image: Mapped[str]
    temperature: Mapped[float]
    humidity: Mapped[float]
    soil_type: Mapped[str]
    soil_acidity_type: Mapped[str]

    user: Mapped['User'] = relationship(back_populates='plants')
