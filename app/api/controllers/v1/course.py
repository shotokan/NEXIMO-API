import falcon
from marshmallow import ValidationError

from app.api.exceptions.exceptions import SerializerException
from app.api.hooks.auth import validate_token
from app.services.course import CourseService
from app.utils.api_response import response_ok, response_error
from app.api.hooks.validate_role import validate_scope_professor, validate_scope_student, validate_scope_both

@falcon.before(validate_token)
class Course:
    def __init__(self):
        self.course_service = CourseService()

    @falcon.before(validate_scope_both)
    def on_get(self, req, resp):
        """Obtiene los cursos y si es un estudiante marca a cuales tiene acceso"""
        try:
            result = self.course_service.get_all(req.context['user'], self.session)
            resp.status = falcon.HTTP_200  # This is the default status
            resp.context['result'] = response_ok(result, "ok", 'list of courses', 'get', req.path)
        except ValidationError as err:
            resp.status = falcon.HTTP_400
            resp.context['result'] = response_error(err.messages, str("Validation Error"), 'get', req.path)
        except SerializerException as exc:
            resp.status = falcon.HTTP_500
            resp.context['result'] = response_error({}, "Internal Error. Contact the Admin.", 'get', req.path)
        except Exception as exc:
            resp.status = falcon.HTTP_400
            resp.context['result'] = response_error({}, str(exc), 'post', req.path)

    @falcon.before(validate_scope_professor)
    def on_post(self, req, resp):
        """Crea un curso"""
        try:
            result = self.course_service.create(req.context['data'], req.context['user'], self.session)
            resp.status = falcon.HTTP_201  # This is the default status
            resp.context['result'] = response_ok(result, "ok", 'created', 'post', req.path)
        except ValidationError as err:
            resp.status = falcon.HTTP_400
            resp.context['result'] = response_error(err.messages, str("Validation Error"), 'post', req.path)
        except SerializerException as exc:
            resp.status = falcon.HTTP_500
            resp.context['result'] = response_error(str(exc), "Internal Error. Contact the Admin.", 'post', req.path)
        except Exception as exc:
            resp.status = falcon.HTTP_400
            resp.context['result'] = response_error(str(exc), "Error", 'post', req.path)

    @falcon.before(validate_scope_professor)
    def on_put(self, req, resp):
        """Actualiza un curso"""
        try:
            result = self.course_service.create(req.context['data'], req.context['user'], self.session)
            resp.status = falcon.HTTP_201  # This is the default status
            resp.context['result'] = response_ok(result, "ok", 'created', 'put', req.path)
        except ValidationError as err:
            resp.status = falcon.HTTP_400
            resp.context['result'] = response_error(err.messages, str("Validation Error"), 'put', req.path)
        except SerializerException as exc:
            resp.status = falcon.HTTP_500
            resp.context['result'] = response_error(str(exc), "Internal Error. Contact the Admin.", 'put', req.path)
        except Exception as exc:
            resp.status = falcon.HTTP_400
            resp.context['result'] = response_error(str(exc), "Error", 'put', req.path)


@falcon.before(validate_token)
class CourseResource:
    def __init__(self):
        self.course_service = CourseService()

    @falcon.before(validate_scope_both)
    def on_get(self, req, resp, uuid):
        """Obtiene un curso por su id"""
        try:
            result = self.course_service.get_by_id(uuid, self.session)
            resp.status = falcon.HTTP_201  # This is the default status
            resp.context['result'] = response_ok(result, "ok", 'created', 'get', req.path)
        except ValidationError as err:
            resp.status = falcon.HTTP_400
            resp.context['result'] = response_error(err.messages, str("Validation Error"), 'get', req.path)
        except SerializerException as exc:
            resp.status = falcon.HTTP_500
            resp.context['result'] = response_error({}, "Error interno", 'get', req.path)
        except Exception as exc:
            resp.status = falcon.HTTP_400
            resp.context['result'] = response_error({}, str(exc), 'get', req.path)
