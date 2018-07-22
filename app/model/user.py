"""
    author: ivan sabido
    date: 19/07/2018
    email: <isc_86@hotmail.com>
"""

from sqlalchemy import text
from sqlalchemy import Column, String, Integer, DateTime, func, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from passlib.hash import pbkdf2_sha256

from app.database.sqlalchemy.connection import Base


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column(String)
    lastname = Column(String)
    password = Column(String)
    cellphone = Column(String)
    email = Column(String, unique=True)
    active = Column(Boolean, default=True)
    status = Column(String)
    role_id = Column(UUID, ForeignKey('roles.id'))
    role = relationship("RoleModel", back_populates="user")
    tokens = relationship("TokenModel", back_populates="user")
    enrollments = relationship("EnrollmentModel", back_populates="user")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())

    @staticmethod
    def get_hashed_password(plain_text_password):
        # Hash a password for the first time
        #   (Using bcrypt, the salt is saved into the hash itself)
        return pbkdf2_sha256.hash(plain_text_password.encode('utf8'))
        # return bcrypt.hashpw(plain_text_password.encode('utf8'), bcrypt.gensalt())

    @staticmethod
    def check_password(plain_text_password, hashed_password):
        # Check hased password. Useing bcrypt, the salt is saved into the hash itself
        return pbkdf2_sha256.verify(plain_text_password.encode('utf8'), hashed_password)
        # return bcrypt.checkpw(plain_text_password.encode('utf8'), hashed_password)
