import falcon
from marshmallow import ValidationError

from app.api.exceptions.exceptions import SerializerException
from app.services.user import UserService
from app.utils.api_response import response_ok, response_error


class User:
    def __init__(self):
        self.user_service = UserService()

    def on_post(self, req, resp):
        """crea un usuario para el sistema con su rol"""
        try:
            result = self.user_service.create(req.context['data'], self.session)
            resp.status = falcon.HTTP_201  # This is the default status
            resp.context['result'] = response_ok(result, "ok", 'created', 'post', req.path)
        except ValidationError as err:
            resp.status = falcon.HTTP_400
            resp.context['result'] = response_error(err.messages, str("Validation Error"), 'post', req.path)
        except SerializerException as exc:
            resp.status = falcon.HTTP_500
            resp.context['result'] = response_error({}, "Internal Error. Contact the Admin.", 'post', req.path)
        except Exception as exc:
            resp.status = falcon.HTTP_400
            resp.context['result'] = response_error({}, str(exc), 'post', req.path)
