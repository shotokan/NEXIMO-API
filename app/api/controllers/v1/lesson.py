import falcon
from marshmallow import ValidationError

from app.api.exceptions.exceptions import SerializerException
from app.api.hooks.auth import validate_token
from app.api.hooks.validate_role import validate_scope_professor, validate_scope_student, validate_scope_both
from app.services.lesson import LessonService
from app.utils.api_response import response_ok, response_error


@falcon.before(validate_token)
class Lesson:
    def __init__(self):
        self.lesson_service = LessonService()

    @falcon.before(validate_scope_both)
    def on_get(self, req, resp, uuid):
        """devuelve las lecciones y si el usuario es estudiante las marca"""
        try:
            result = self.lesson_service.get_all(uuid, req.context['user'], self.session)
            resp.status = falcon.HTTP_201  # This is the default status
            resp.context['result'] = response_ok(result, "ok", 'created', 'get', req.path)
        except ValidationError as err:
            resp.status = falcon.HTTP_400
            resp.context['result'] = response_error(err.messages, str("Validation Error"), 'get', req.path)
        except SerializerException as exc:
            resp.status = falcon.HTTP_500
            resp.context['result'] = response_error({}, "Internal Error. Contact the Admin.", 'get', req.path)
        except Exception as exc:
            resp.status = falcon.HTTP_400
            resp.context['result'] = response_error(str(exc), 'Error', 'get', req.path)

    @falcon.before(validate_scope_professor)
    def on_post(self, req, resp, uuid):
        """crea lecciones"""
        try:
            result = self.lesson_service.create(req.context['data'], req.context['user'], uuid, self.session)
            resp.status = falcon.HTTP_201  # This is the default status
            resp.context['result'] = response_ok(result, "ok", 'created', 'post', req.path)
        except ValidationError as err:
            resp.status = falcon.HTTP_400
            resp.context['result'] = response_error(err.messages, str("Validation Error"), 'post', req.path)
        except SerializerException as exc:
            resp.status = falcon.HTTP_500
            resp.context['result'] = response_error({}, "Error interno", 'post', req.path)
        except Exception as exc:
            resp.status = falcon.HTTP_400
            resp.context['result'] = response_error(str(exc), 'Error', 'post', req.path)


@falcon.before(validate_token)
class LessonTaken:
    def __init__(self):
        self.lesson_service = LessonService()

    @falcon.before(validate_scope_both)
    def on_get(self, req, resp, uuid):
        """obtiene las lecciones tomadas por un usuario"""
        try:
            result = self.lesson_service.get_all(uuid, req.context['user'], self.session)
            resp.status = falcon.HTTP_201  # This is the default status
            resp.context['result'] = response_ok(result, "ok", 'created', 'get', req.path)
        except ValidationError as err:
            resp.status = falcon.HTTP_400
            resp.context['result'] = response_error(err.messages, str("Validation Error"), 'get', req.path)
        except SerializerException as exc:
            resp.status = falcon.HTTP_500
            resp.context['result'] = response_error({}, "Internal Error. Contact the Admin.", 'get', req.path)
        except Exception as exc:
            resp.status = falcon.HTTP_400
            resp.context['result'] = response_error(str(exc), 'Error', 'get', req.path)

    @falcon.before(validate_scope_student)
    def on_post(self, req, resp, lesson_id):
        """Valida las respuestas, calcula el score y si el usuario ha pasado lo añade"""
        try:
            result = self.lesson_service.take_lesson(req.context['data'], req.context['user'], lesson_id, self.session)
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
            resp.context['result'] = response_error(str(exc), 'Error', 'post', req.path)


@falcon.before(validate_token)
class LessonDetails:
    def __init__(self):
        self.lesson_service = LessonService()

    @falcon.before(validate_scope_both)
    def on_get(self, req, resp, lesson_id):
        """obtiene las preguntas de una leccion"""
        try:
            result = self.lesson_service.get_questions(lesson_id, req.context['user'], self.session)
            resp.status = falcon.HTTP_201  # This is the default status
            resp.context['result'] = response_ok(result, "ok", 'created', 'get', req.path)
        except ValidationError as err:
            resp.status = falcon.HTTP_400
            resp.context['result'] = response_error(err.messages, str("Validation Error"), 'get', req.path)
        except SerializerException as exc:
            resp.status = falcon.HTTP_500
            resp.context['result'] = response_error({}, "Internal Error. Contact the Admin.", 'get', req.path)
        except Exception as exc:
            resp.status = falcon.HTTP_400
            resp.context['result'] = response_error(str(exc), 'Error', 'get', req.path)