import falcon
from marshmallow import ValidationError

from app.api.exceptions.exceptions import SerializerException
from app.api.hooks.auth import validate_token
from app.api.hooks.validate_role import validate_scope_professor, validate_scope_both
from app.services.question import QuestionService
from app.utils.api_response import response_ok, response_error


@falcon.before(validate_token)
class Question:
    def __init__(self):
        self.question_service = QuestionService()

    @falcon.before(validate_scope_both)
    def on_get(self, req, resp, lesson_id):
        """devuelve las preguntas activas"""
        try:
            result = self.question_service.get_all(lesson_id, req.context['user'], self.session)
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
            resp.context['result'] = response_error(str(exc), "Error", 'get', req.path)

    @falcon.before(validate_scope_professor)
    def on_post(self, req, resp, lesson_id):
        """crea una pregunta con sus respuestas par auna leccion"""
        try:
            result = self.question_service.create(req.context['data'], req.context['user'], lesson_id, self.session)
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
            resp.context['result'] = response_error(str(exc), "Error", 'post', req.path)
