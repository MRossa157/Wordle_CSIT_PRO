import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment='ID записи',
    )
    username = Column(
        String(32),
        nullable=False,
        comment='Имя пользователя',
    )
    password_hash = Column(
        BYTEA,
        nullable=False,
        comment='Hash пароля пользователя',
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment='Дата создания пользователя',
    )


class GameSession(Base):
    __tablename__ = 'game_sessions'

    session_id = Column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    owner_id = Column(
        Integer,
        nullable=False,
        comment='Владелец сессии',
    )
    guess_word_id = Column(
        Integer,
        ForeignKey('words.id', ondelete='CASCADE'),
        nullable=False,
        comment='ID слова для отгадывания',
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment='Дата создания сессии',
    )
    finished_at = Column(
        DateTime,
        nullable=True,
        comment='Дата окончания сессии',
    )


class Word(Base):
    __tablename__ = 'words'

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    word = Column(String, nullable=False, unique=True)
