"""
    author: ivan sabido
    date: 19/07/2018
    email: <isc_86@hotmail.com>
"""

from sqlalchemy import text
from sqlalchemy import Column, String, Integer, DateTime, func, Boolean, ForeignKey, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.sqlalchemy.connection import Base


class TokenModel(Base):
    __tablename__ = 'tokens'

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    user_id = Column(UUID, ForeignKey('users.id'))
    access_token = Column(String)
    refresh_token = Column(String)
    access_token_expires_at = Column(BigInteger)
    issued_at = Column(BigInteger)
    refresh_token_expires_in = Column(BigInteger)
    user = relationship("UserModel", back_populates="tokens")
    created_at = Column(DateTime, default=func.now())
