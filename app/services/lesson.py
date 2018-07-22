from marshmallow import ValidationError

from app.api.exceptions.exceptions import SerializerException
from app.api.serializers.question import QuestionResponseSchema
from app.repository.lesson import LessonRepository
from app.api.serializers.lesson import LessonSchema
from app.repository.question import QuestionRepository
from app.repository.enrollment import EnrollmentRepository
from app.repository.lesson_score import LessonScoreRepository
from app.utils.roles import ROLES
from app.utils.type_question import TYPE_QUESTIONS, m_all, m_one, m_mtone, bool_answer


class LessonService:
    def __init__(self):
        self.lesson_repo = LessonRepository()
        self.question_repo = QuestionRepository()
        self.enrollment_repo = EnrollmentRepository()
        self.score_repo = LessonScoreRepository()

    def create(self, data, user, uuid, session):
        """Crea una leccion para un curso (uuid) y devuelve los datos con su id"""
        try:
            print("En service lesson")
            if isinstance(data, dict) and data:
                _lesson = {}
                try:
                    _lesson = LessonSchema().load(data)
                    _lesson['course_id'] = uuid
                    print(_lesson)
                except ValidationError as err:
                    raise err
                lesson = self.lesson_repo.save(_lesson, uuid, user['user_id'], session)
                result = LessonSchema().dump(lesson)
                return result
        except ValidationError as err:
            raise err
        except SerializerException as exc:
            print("Service create error serializer {}".format(exc))
            raise exc
        except Exception as exc:
            print("Service create error {}".format(exc))
            raise exc

    def get_all(self, course_id, user, session):
        """Obtiene las lecciones activas, si el usuario es estudiante le añade a la respuesta access y user_status
        con ello indica si un estudiante tiene acceso al curso y si ya lo ha tomado"""
        try:
            if user['role_name'].lower() == ROLES['1'].lower():
                lessons, ids = self.lesson_repo.get_all_active_with_user_lessons(course_id, session)
                band = True
                lessons = LessonSchema(many=True).dump(lessons)
                for lesson in lessons:
                    if lesson['id'] in ids:
                        lesson['access'] = False
                        lesson['user_status'] = 'Taken'
                    else:
                        if band:
                            lesson['access'] = True
                            band = False
                            lesson['user_status'] = 'not approved'
                        else:
                            lesson['access'] = False
                            lesson['user_status'] = 'not approved'
            else:
                lessons = self.lesson_repo.get_all_active(course_id, session)
                lessons = LessonSchema(many=True).dump(lessons)
            print(lessons)

            print(lessons)
            return lessons
        except Exception as exc:
            print("Service create error {}".format(exc))
            raise exc

    def get_questions(self, lesson_id, user, session):
        """Obtiene las preguntas de una leccion"""
        try:
            #TODO: validar que el usuario pueda tomar la lección
            if user['role_name'].lower() == ROLES['1'].lower():
                lessons_taken = self.score_repo.get_lesson_by_user(lesson_id, user['user_id'], session)
                if lessons_taken is not None:
                    raise Exception("Lesson has already been taken.")
                questions = self.question_repo.get_all_active(lesson_id, session)
            else:
                questions = self.question_repo.get_all_active(lesson_id, session)
            if len(questions) < 1:
                raise Exception("Lesson does not yet have questions.")
            result = QuestionResponseSchema(many=True).dump(questions)
            print(result)
            return result
        except Exception as exc:
            print("Service create error {}".format(exc))
            raise exc

    def get_by_id(self, uuid, session):
        """Obtiene una pregunta por su identificador"""
        try:
            #TODO: no disponible
            course, mandatories = self.lesson_repo.get_with_mandatories(uuid, session)
            _course = LessonSchema().dump(course)
            _mandatories = LessonSchema(many=True).dump(mandatories)
            del _course['mandatory_courses_code']
            _course['mandatory_courses'] = _mandatories
            return _course
        except Exception as exc:
            print("Service create error {}".format(exc))
            raise exc

    def update(self, data, session):
        """Actualiza todos los datos de una leccion"""
        try:
            #TODO: No disponible
            print("En service user")
            if isinstance(data, dict) and data:
                _course = {}
                try:
                    _course = LessonSchema().load(data)
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

    def take_lesson(self, data, user, lesson_uuid, session):
        """Califica las preguntas de una leccion y si la aprueba el estudiante la añade en lesson_score con el puntaje"""
        try:
            print("En service user")
            lesson = self.lesson_repo.get(lesson_uuid, session)

            question_ids = {question['id']: question['answers'] for question in data['questions']}
            corrects = self.question_repo.get_correct_answers(lesson_uuid, session)
            # verifica que las preguntas respondidas sean la misma cantidad que las preguntas de la leccion
            if len(set(question_ids.keys())) != len(corrects):
                raise Exception("You need to answer all questions.")
            total_score = 0
            successful_answers = 0
            unsuccessful_answers = 0
            # se verican las respuestas con las correctas
            for question in corrects:
                # indexes: 0-Question_ID, 1-QUESTION_SCORE, 2-Type_Question, 3-Correct_Answers
                is_correct = self._type_question(question[2], question_ids[question[0]], question[3])
                print(is_correct)
                if is_correct:
                    total_score += question[1]
                    successful_answers += 1
                else:
                    unsuccessful_answers += 1
            score_reached = (100 * total_score)/lesson.score
            lesson_score = {
                'successful_answers': successful_answers,
                'unsuccessful_answers': unsuccessful_answers,
                'score_reached': score_reached,
                'total_score': total_score
            }
            # verifica si el estudiante alcanzo el promedio para pasar la leccion
            if score_reached < lesson.aproval_score:
                raise Exception("No has alcanzado el puntaje necesario.")
            enrollment = self.enrollment_repo.save(lesson_score, lesson.course_id, user['user_id'],
                                                   lesson_uuid, lesson.order, session)
            lessons_taken = [lesson_score.lesson_id for lesson_score in enrollment.lesson_scores]

            missing_lessons = self.lesson_repo.get_all_not_in(lessons_taken, session)
            # si al curso ya no le quedan mas lecciones actualiza el status del curso que esta tomando el estudiante
            if len(missing_lessons) == 0:
                self.enrollment_repo.change_enrollment_status(lesson.course_id, 'approved', session)
            # alade a la respuesta si aprobo o no
            if score_reached < lesson.aproval_score:
                lesson_score['approved'] = False
            else:
                lesson_score['approved'] = True
            return lesson_score
        except ValidationError as err:
            raise err
        except SerializerException as exc:
            print("Service create error serializer {}".format(exc))
            raise exc
        except Exception as exc:
            print("Service create error {}".format(exc))
            raise exc

    def _type_question(self, t_question, user_answers, correct_answers):
        switch = {
            TYPE_QUESTIONS[1]: bool_answer,
            TYPE_QUESTIONS[2]: m_one,
            TYPE_QUESTIONS[3]: m_mtone,
            TYPE_QUESTIONS[4]: m_all,
        }
        func = switch.get(t_question, lambda _: False)
        return func(user_answers, correct_answers)
