import sqlalchemy
import logging
import pygogo as gogo

from typing import Dict

from sqlalchemy import and_
from uuid import UUID

from app.model.user import UserModel

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(log_format)
logger = gogo.Gogo(__name__, low_formatter=formatter).logger


class UserRepository:

    def get(self, uuid: str, session=None):
        logger.info("Get UserRepository")
        user = session.query(UserModel).get(uuid)
        return user

    def get_by_email(self, email, session=None):
        try:
            print("en reposiroty user get by email")
            user = session.query(UserModel).filter(and_(UserModel.email == email, UserModel.active)).first()
            print(user)
            if user is None:
                return None
            return user
        except Exception as exc:
            logger.error(str(exc))
            session.rollback()
            raise exc

    def save(self, data: Dict, session=None) -> UserModel:
        try:
            user = UserModel()
            user.email = data['email']
            user.role_id = data['role_id']
            user.name = data['name']
            user.password = UserModel.get_hashed_password(data['password'])
            user.cellphone = data.get('cellphone', '')
            user.lastname = data['lastname']
            user.status = 'active'
            user.active = True
            session.add(user)
            session.commit()
            print(user)
            return user
        except sqlalchemy.exc.IntegrityError as ie:
            logger.error(str(ie))
            session.rollback()
            raise Exception("El email ya existe")
        except Exception as exc:
            logger.error(str(exc))
            session.rollback()
            raise exc
