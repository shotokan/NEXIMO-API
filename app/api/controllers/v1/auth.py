
import time

import falcon

from datetime import datetime

from marshmallow import ValidationError

from app.api.exceptions.exceptions import SerializerException
from app.services.token import TokenService
from app.utils.api_response import response_ok, response_error


class AuthResource:

    def __init__(self):
        self.token_service = TokenService()

    def on_post(self, req, resp):
        """Genera un token si las credenciales son las adecuadas"""
        try:
            result = self.token_service.create_token(req.context['data'], self.session)
            resp.status = falcon.HTTP_201  # This is the default status
            resp.context['result'] = response_ok(result, "ok", "token created", 'post', req.path)
        except ValidationError as err:
            resp.status = falcon.HTTP_401  # This is the default status
            resp.context['result'] = response_error(err.messages, "authentication failed", 'post', req.path)
        except Exception as exc:
            resp.status = falcon.HTTP_401  # This is the default status
            result = {
                'error': str(exc)
            }
            resp.context['result'] = response_error(result, "authentication failed", 'post', req.path)


class AuthenticationRefresh:

    def __init__(self):
        self.token_service = TokenService()

    def on_post(self, req, resp):
        """Genera un token sin las credenciales pero pasando el token de refresh"""
        try:
            result = self.token_service.refresh_token(req.context['data'], self.session)
            resp.status = falcon.HTTP_201  # This is the default status
            resp.context['result'] = response_ok(result, "ok", "token created", 'post', req.path)
        except SerializerException as exc:
            resp.status = falcon.HTTP_500  # This is the default status
            resp.context['result'] = response_error(str(exc), "Internal Error. Contact the Admin.", 'post', req.path)
        except Exception as exc:
            resp.status = falcon.HTTP_401  # This is the default status
            result = {
                'error': str(exc)
            }
            resp.context['result'] = response_error(result, "authentication failed", 'post', req.path)