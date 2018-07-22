from app.api.exceptions.exceptions import SerializerException
from app.repository.question import QuestionRepository
from app.model.course import CourseModel
from app.api.serializers.question import QuestionRequestSchema, QuestionResponseSchema
from marshmallow import pprint, ValidationError

from app.utils.roles import ROLES
from app.utils.type_question import is_m_one, is_bool, is_m_all, is_m_mtone, TYPE_QUESTIONS


class QuestionService:
    def __init__(self):
        self.question_repo = QuestionRepository()

    def create(self, data, user, lesson_id, session):
        try:

            if isinstance(data, dict) and data:
                _course = {}
                try:
                    print("En service user1")
                    _question = QuestionRequestSchema().load(data)
                    print(_course)
                except ValidationError as err:
                    raise err
                print("En service user2")
                print(_question)
                if _question['type_question'] == TYPE_QUESTIONS[1] and not is_bool(_question['corrects'], _question['wrong']):
                    raise Exception("Boolean type incorrect.")
                elif _question['type_question'] == TYPE_QUESTIONS[2] and not is_m_one(_question['corrects'], _question['wrong']):
                    raise Exception("M-ONE type incorrect.")
                elif _question['type_question'] == TYPE_QUESTIONS[3] and not is_m_mtone(_question['corrects'], _question['wrong']):
                    raise Exception("M-MTONE type incorrect.")
                elif _question['type_question'] == TYPE_QUESTIONS[4] and not is_m_mtone(_question['corrects'], _question['wrong']):
                    raise Exception("M-ALL type incorrect.")
                print("En service user")
                course = self.question_repo.save(_question, lesson_id, user['user_id'], session)
                result = QuestionResponseSchema().dump(course)
                return result
        except ValidationError as err:
            raise err
        except SerializerException as exc:
            print("Service create error serializer {}".format(exc))
            raise exc
        except Exception as exc:
            print("Service create error {}".format(exc))
            raise exc

    def get_all(self, lesson_id, user, session):
        try:
            if user['role_name'].lower() == ROLES['1'].lower():
                pass
            questions = self.question_repo.get_all_active(lesson_id, session)
            print(questions)
            questions = QuestionResponseSchema(many=True).dump(questions)
            return questions
        except Exception as exc:
            print("Service create error {}".format(exc))
            raise exc

    def get_by_id(self, uuid, session):
        try:
            course, mandatories = self.question_repo.get_with_mandatories(uuid, user, session)
            _course = QuestionRequestSchema().dump(course)
            _mandatories = QuestionRequestSchema(many=True).dump(mandatories)
            del _course['mandatory_courses_code']
            _course['mandatory_courses'] = _mandatories
            return _course
        except Exception as exc:
            print("Service create error {}".format(exc))
            raise exc

    def update(self, data, session):
        try:
            print("En service user")
            if isinstance(data, dict) and data:
                _course = {}
                try:
                    _course = QuestionRequestSchema().load(data)
                    print(_course)
                except ValidationError as err:
                    raise err
                return _course
        except ValidationError as err:
            raise err
        except SerializerException as exc:
            print("Service create error serializer {}".format(exc))
            raise exc
        except Exception as exc:
            print("Service create error {}".format(exc))
            raise exc
