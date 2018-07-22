from app.api.exceptions.exceptions import SerializerException
from app.repository.course import CourseRepository
from app.model.course import CourseModel
from app.api.serializers.course import CourseSchema, CourseUserSchema
from marshmallow import pprint, ValidationError
from app.utils.roles import ROLES


class CourseService:
    def __init__(self):
        self.course_repo = CourseRepository()
        self.user_schema = CourseSchema()

    def create(self, data, user, session):
        """crea un curso en el sistema"""
        try:
            if isinstance(data, dict) and data:
                _course = {}
                try:
                    # valida los datos
                    _course = CourseSchema().load(data)
                    print(_course)
                except ValidationError as err:
                    raise err
                course = self.course_repo.save(_course, user['user_id'], session)
                result = CourseSchema().dump(course)
                return result
        except ValidationError as err:
            raise err
        except SerializerException as exc:
            print("Service create error serializer {}".format(exc))
            raise exc
        except Exception as exc:
            print("Service create error {}".format(exc))
            raise exc

    def get_all(self, user, session):
        """devuelve los cursos que se encuentran en el sistema. Si es un usuario estudiante, le añade a la respuesta
        access, para indicar si el usuario tiene acceso al curso"""
        try:
            #TODO: Pagination

            if user['role_name'].lower() == ROLES['1'].lower():
                courses, user_coursers = self.course_repo.get_all_active_by_user(user['user_id'], session)
                # valida los datos
                _courses = CourseUserSchema(many=True).dump(courses)
                for c in _courses:
                    # verifica si el curso tiene cursos obligatorios
                    if len(c['mandatory_courses']) > 0:
                        # Se verifica que el usuario haya tomado los cursos obligatorios para acceder
                        # Si el nuevo conjunto es vacio o el curso no tiene cursos obligatorios, se le permite el acceso
                        new_set = set(c['mandatory_courses']) - set(user_coursers)
                        if len(new_set) == 0:
                            c['access'] = True
                        else:
                            c['access'] = False
                    else:
                        c['access'] = True
                    # elimina los identificadores de los cursos obligatorios de la respuesta
                    del c['mandatory_courses']
            else:
                courses = self.course_repo.get_all_active(session)
                _courses = CourseSchema(many=True).dump(courses)

            print(_courses)
            return _courses
        except Exception as exc:
            print("Service create error {}".format(exc))
            raise exc

    def get_by_id(self, uuid, session):
        """Obtiene un curso mediante su id"""
        try:
            course, mandatories = self.course_repo.get_with_mandatories(uuid, session)
            _course = CourseSchema().dump(course)
            _mandatories = CourseSchema(many=True).dump(mandatories)
            del _course['mandatory_courses_code']
            _course['mandatory_courses'] = _mandatories
            return _course
        except Exception as exc:
            print("Service create error {}".format(exc))
            raise exc

    def update(self, data, session):
        """actualiza los datos del curso"""
        try:
            print("En service user")
            if isinstance(data, dict) and data:
                _course = {}
                try:
                    _course = CourseSchema().load(data)
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
