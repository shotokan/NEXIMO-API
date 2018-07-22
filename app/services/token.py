import logging
import time

import pygogo as gogo

from datetime import datetime, timedelta

from marshmallow import ValidationError

from app.api.exceptions.exceptions import SerializerException
from app.api.serializers.auth import AuthSchema
from app.utils.tokens import create_token, read_token, get_data_for_access_token, get_data_for_refresh_token
from app.model.token import TokenModel
from app.repository.token import TokenRepository
from app.repository.user import UserRepository
from app.api.serializers.token import TokenSchema

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(log_format)
logger = gogo.Gogo(__name__, low_formatter=formatter).logger


class TokenService:

    def __init__(self):
        self.token_rep = TokenRepository()
        self.user_rep = UserRepository()

    def create_token(self, data, session):
        try:
            try:
                print("schema")
                _auth = AuthSchema().load(data)
                print(_auth)
            except ValidationError as err:
                raise err
            if _auth.get('grant_type', 'password') != 'password':
                raise Exception("grant_type incorrecto")
            email = _auth.get('email', ''),
            password = _auth.get('password', '')
            user = self.user_rep.get_by_email(email, session)
            if user.check_password(password, user.password):
                data = self._generate_token(user)
                token = self.token_rep.save(data, session)
                if not token:
                    raise Exception("No se ha podido iniciar la sesión.")
                token_schema = TokenSchema()
                try:
                    result = token_schema.load(data)
                except ValidationError as err:
                    raise err
                print(result)
                return result
            return {}
        except Exception as err:
            logger.error("create_token-Exception")
            logger.error(err)
            raise err

    def _read_token(self, refresh_token):
        try:
            read_token(refresh_token)
            return True
        except Exception as exc:
            print(exc)
            return False

    def refresh_token(self, data, session):
        try:
            if data.get('grant_type', '') != 'refresh_token':
                raise Exception("grant_type incorrecto para refresh token")

            refresh_token = data.get('refresh_token', '')
            if not self._read_token(refresh_token):
                raise Exception("El tiempo para el refresh token ha expirado.")
            actual_token = self.token_rep.exist_refresh(refresh_token, session)
            if not actual_token:
                raise Exception("No existe el token.")
            user = self.user_rep.get(actual_token.user_id, session)
            data = self._generate_token(user)
            token = self.token_rep.save(data, session)
            if not token:
                raise Exception("No se ha podido iniciar la sesión.")
            print('en refresh')
            print(data)
            token_schema = TokenSchema()
            result = token_schema.load(data)
            print(result)
            return result
        except SerializerException as err:
            logger.error("refresh_token-SerializerException")
            logger.error(err)
            raise err
        except Exception as err:
            logger.error("refresh_token-Exception")
            logger.error(err)
            raise err

    def _generate_token(self, user):
        try:
            # generates datetime for expirations
            now = datetime.now()
            epoch = int(time.mktime(now.timetuple()))
            expires_in = now + timedelta(minutes=15)
            expires_in = int(time.mktime(expires_in.timetuple()))
            refresh_expires = now + timedelta(days=2)
            refresh_expires = int(time.mktime(refresh_expires.timetuple()))
            data = {
                'user_id': user.id,
                'role_id': user.role_id,
                'role_name': user.role.name,
                'access_token_expires_at': expires_in,
                'refresh_token_expires_in': refresh_expires,
                'issued_at': epoch
            }
            # generates access and refresh tokens
            access_token = create_token(get_data_for_access_token(data)).decode("utf-8")
            refresh_token = create_token(get_data_for_refresh_token(data)).decode("utf-8")
            data.update({
                'access_token': access_token,
                'refresh_token': refresh_token
            })
            return data
        except Exception as exc:
            print("Generate token")
            print(exc)
            print(exc)

    def _verify_credentials(self, data, session):
        try:
            email = data.get('email', '')
            password = data.get('password', '')
            user = self.user_rep.get_by_email(email, session=session)

            if user is None:
                raise Exception("Credenciales incorrectas")
            if not user.check_password(password, user.password):
                raise Exception("Credenciales incorrectas")

            return user
        except Exception as exc:
            print(exc)
            raise exc

