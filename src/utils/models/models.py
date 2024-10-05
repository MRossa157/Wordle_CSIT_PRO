from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="ID записи",
    )
    username = Column(
        String(32),
        nullable=False,
        comment="Имя пользователя",
    )
    password_hash = Column(
        BYTEA,
        nullable=False,
        comment="Hash пароля пользователя",
    )
