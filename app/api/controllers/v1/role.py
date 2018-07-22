import falcon
from marshmallow import ValidationError

from app.api.exceptions.exceptions import SerializerException
from app.api.hooks.auth import validate_token
from app.api.hooks.validate_role import validate_scope_professor, validate_scope_student
from app.services.role import RoleService
from app.utils.api_response import response_ok, response_error


class Role:
    def __init__(self):
        self.role_service = RoleService()

    def on_get(self, req, resp):
        """obtiene los roles disponibles en el sistema"""
        try:
            result = self.role_service.get_all(self.session)
            resp.status = falcon.HTTP_200  # This is the default status
            resp.context['result'] = response_ok(result, "ok", 'list of roles', 'post', req.path)
        except ValidationError as err:
            resp.status = falcon.HTTP_400
            resp.context['result'] = response_error(err.messages, str("Validation Error"), 'get', req.path)
        except SerializerException as exc:
            resp.status = falcon.HTTP_500
            resp.context['result'] = response_error({}, "Internal Error. Contact the Admin.", 'get', req.path)
        except Exception as exc:
            resp.status = falcon.HTTP_400
            resp.context['result'] = response_error(str(exc), 'Error', 'get', req.path)