import logging
import pygogo as gogo

from app.api.exceptions.exceptions import SerializerException
from app.repository.user import UserRepository
from app.api.serializers.user import UserSchema
from marshmallow import pprint, ValidationError

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(log_format)
logger = gogo.Gogo(__name__, low_formatter=formatter).logger


class UserService:
    def __init__(self):
        self.user_rep = UserRepository()
        self.user_schema = UserSchema()

    def create(self, data, session):
        """crea un usuario y devuelve un diccionario con los datos del usuario y rol"""
        try:
            print("En service user")
            if isinstance(data, dict) and data:
                _user = {}
                try:
                    _user = UserSchema().load(data)
                except ValidationError as err:
                    raise err
                user = self.user_rep.save(_user, session)
                result = self.user_schema.dump(user)
                print(result)
                print(type(result))
                return result
        except ValidationError as err:
            logger.error("ValidationError")
            logger.error(err)
            raise err
        except SerializerException as err:
            logger.error("SerializerException")
            logger.error(err)
            raise err
        except Exception as err:
            logger.error("Exception")
            logger.error(err)
            raise err
