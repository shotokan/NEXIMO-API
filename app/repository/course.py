import sqlalchemy
import logging
import pygogo as gogo

from typing import Dict

from sqlalchemy import and_
from uuid import UUID

from sqlalchemy.dialects import postgresql
from sqlalchemy import or_
from app.model.course import CourseModel
from app.model.enrollment import EnrollmentModel

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(log_format)
logger = gogo.Gogo(__name__, low_formatter=formatter).logger


class CourseRepository:

    def get(self, uuid: str, session=None) -> CourseModel:
        logger.info("Get CourseRepository")
        course = session.query(CourseModel).get(uuid)

        return course

    def get_with_mandatories(self, uuid: str, session=None):
        logger.info("Get CourseRepository")
        course = session.query(CourseModel).get(uuid)
        mandatories = session.query(CourseModel).filter(CourseModel.id.in_(course.mandatory_courses)).all()

        return course, mandatories

    def get_all_active_by_user(self, user_id, session=None):
        logger.info("get_all_active CourseRepository")
        ids = []
        enrollments = session.query(EnrollmentModel.course_id)\
            .filter(EnrollmentModel.user_id == user_id, EnrollmentModel.active, EnrollmentModel.status == 'approved')\
            .all()
        if enrollments is not None:
            ids = [course_id for course_id, in enrollments]
        # can_take = session.query(CourseModel) \
        #     .filter(postgresql.ARRAY.Comparator(CourseModel.mandatory_courses)
        #                 .contained_by(ids)).all()
        courses = session.query(CourseModel).filter(CourseModel.active).all()
        return courses, ids

    def get_all_active(self, session=None):
        logger.info("get_all_active CourseRepository")
        courses = session.query(CourseModel).filter(CourseModel.active).all()
        return courses

    def save(self, data: Dict, user_id: str, session=None) -> CourseModel:
        try:
            course = CourseModel()
            course.name = data['name']
            course.active = True
            course.code = data.get('code', '')
            course.credits = data.get('credits', 0)
            course.description = data.get('description', '')
            course.created_by = user_id
            course.updated_by = user_id
            course.mandatory_courses = data.get('mandatory_courses', [])
            courses_length = len(course.mandatory_courses)
            if courses_length > 0:
                courses = session.query(CourseModel.code).filter(CourseModel.id.in_(course.mandatory_courses)).all()
                if len(courses) != courses_length:
                    raise Exception("Mandatory Courses must exist.")
                codes = [code for code, in courses]
                course.mandatory_courses_code = codes
            session.add(course)
            session.commit()
            return course
        except sqlalchemy.exc.IntegrityError as ie:
            logger.error(str(ie))
            session.rollback()
            raise Exception("El nombre o código del curso ya existe.")
        except Exception as exc:
            logger.error(str(exc))
            session.rollback()
            raise exc

    def update(self, data: Dict, user_id: str, session=None) -> CourseModel:
        try:
            actual_course = self.get(data['id'], session)
            course = CourseModel()

            course.name = actual_course.name if data['name'] == actual_course.name else data['name']
            course.active = True
            course.code = actual_course.code if data['code'] == data['code'] else data['code']
            course.credits = actual_course.credits if data.get('credits', 0) == actual_course.credits else data.get('credits', 0)
            course.description = actual_course.description if data.get('description', '') == actual_course.description else data.get('description', '')
            course.updated_by = user_id
            if data.get('mandatory_courses', []) != actual_course.mandatory_courses:
                course.mandatory_courses = actual_course.mandatory_courses if data.get('mandatory_courses', []) == actual_course.mandatory_courses else data.get('mandatory_courses', [])
                courses_length = len(course.mandatory_courses)
                if courses_length > 0:
                    courses = session.query(CourseModel.code).filter(CourseModel.id.in_(course.mandatory_courses)).all()
                    if len(courses) != courses_length:
                        raise Exception("Mandatory Courses must exist.")
                    codes = [code for code, in courses]
                    print(codes)
                    course.mandatory_courses_code = codes
            session.add(course)
            session.commit()
            return course
        except sqlalchemy.exc.IntegrityError as ie:
            logger.error(str(ie))
            session.rollback()
            raise Exception("El nombre o código del curso ya existe.")
        except Exception as exc:
            logger.error(str(exc))
            session.rollback()
            raise exc
