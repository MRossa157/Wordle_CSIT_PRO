from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, Integer, MetaData, String, Table

metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String, nullable=False),
    Column('password', String, nullable=False),
    Column('registered_at', TIMESTAMP, default=datetime.utcnow),
)
