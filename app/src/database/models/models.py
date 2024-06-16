from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Boolean,
    DateTime,
    func,
    JSON
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    reports: Mapped['Report'] = relationship(back_populates='users')


# class Plants(Base):
#     __tablename__ = 'plants'

#     id: Mapped[int] = mapped_column(primary_key=True, index=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

#     name: Mapped[str]
#     plant_type: Mapped[str]
#     image: Mapped[str]
#     temperature: Mapped[float]
#     humidity: Mapped[float]
#     soil_type: Mapped[str]
#     soil_acidity_type: Mapped[str]

#     user: Mapped['User'] = relationship(back_populates='plants')


class Report(Base):
    __tablename__ = 'reports'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    name: Mapped[str]
    report_type: Mapped[str] # template | doc
    create_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    users: Mapped['User'] = relationship(back_populates='reports')
    blocks: Mapped[list['Block']] = relationship(back_populates='reports', uselist=True)
    links: Mapped[list['Link']] = relationship(back_populates='reports', uselist=True)
    report_settings: Mapped['ReportSetting'] = relationship(back_populates='reports', uselist=False)


class Link(Base):
    __tablename__ = 'links'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(ForeignKey('reports.id'))

    content: Mapped[str]

    reports: Mapped['Report'] = relationship(back_populates='links')


class ReportSetting(Base):
    __tablename__ = 'report_settings'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(ForeignKey('reports.id'))

    llm_model: Mapped[str]
    theme: Mapped[str]
    full_theme: Mapped[str]
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    reports: Mapped['Report'] = relationship(back_populates='report_settings')


class Block(Base):
    __tablename__ = 'blocks'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(ForeignKey('reports.id'))

    title: Mapped[str]
    axis_x: Mapped[str]
    axis_y: Mapped[str]

    input_mode_x: Mapped[str] # auto | input | date
    input_mode_y: Mapped[str] # auto | input
    block_type: Mapped[str] # curve chart | bar chart| pie chart | grid | text

    json_data: Mapped[Optional[JSON]] = mapped_column(type_=JSON)

    reports: Mapped['Report'] = relationship(back_populates='blocks')
