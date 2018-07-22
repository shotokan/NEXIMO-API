"""
    author: ivan sabido
    date: 19/07/2018
    email: <isc_86@hotmail.com>
"""

from sqlalchemy import text
from sqlalchemy import Column, String, Integer, DateTime, func, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.sqlalchemy.connection import Base


class RoleModel(Base):
    __tablename__ = 'roles'

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column(String)
    active = Column(Boolean, default=True)
    user = relationship("UserModel", back_populates="role", uselist=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
