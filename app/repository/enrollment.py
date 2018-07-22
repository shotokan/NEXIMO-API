from datetime import datetime

import sqlalchemy
import logging
import pygogo as gogo

from typing import Dict

from sqlalchemy import text

from app.model.lesson import LessonModel
from app.model.enrollment import EnrollmentModel
from app.model.lesson_score import LessonScoreModel

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(log_format)
logger = gogo.Gogo(__name__, low_formatter=formatter).logger


class EnrollmentRepository:

    def get(self, uuid: str, session=None) -> LessonModel:
        logger.info("Get EnrollmentRepository")
        lesson = session.query(LessonModel).get(uuid)

        return lesson

    def get_all_active_with_user_lessons(self, course_id, session=None):
        logger.info("get_all_active EnrollmentRepository")
        ids = []
        lesson_scores = session.query(LessonScoreModel.lesson_id)\
            .filter(LessonScoreModel.enrollment_id == EnrollmentModel.id)\
            .filter(EnrollmentModel.course_id == course_id)\
            .all()
        if lesson_scores is not None:
            ids = [lesson_id for lesson_id, in lesson_scores]
        print(ids)
        lessons = session.query(LessonModel).filter(LessonModel.active).order_by(LessonModel.order).all()
        return lessons, ids

    def get_all_active(self, course_id, session=None):
        logger.info("get_all_active CourseRepository")
        lessons = session.query(LessonModel).filter(LessonModel.course_id == course_id, LessonModel.active).all()
        return lessons

    def change_enrollment_status(self, course_id, status, session):
        try:
            logger.info("change_enrollment_status EnrollmentRepository")
            enrollment = session.query(EnrollmentModel)\
                .filter(EnrollmentModel.course_id == course_id)\
                .update({"status": status, "date_of_completation": datetime.now()})
            session.commit()
            return enrollment
        except sqlalchemy.exc.IntegrityError as ie:
            logger.error(str(ie))
            session.rollback()
            raise Exception("El nombre o código del curso ya existe.")
        except Exception as exc:
            logger.error(str(exc))
            session.rollback()
            raise exc

    def save(self, lesson_score: Dict, course_id: str, user_id: str, lesson_id, lesson_order, session=None) -> EnrollmentModel:
        try:
            logger.info("save EnrollmentRepository")
            print(session)
            enrollment = session.query(EnrollmentModel).filter(EnrollmentModel.course_id == course_id).first()

            user_score = session.query(LessonScoreModel).filter(LessonScoreModel.lesson_id == lesson_id).first()
            if user_score is not None:
                raise Exception("Lesson has already been taken")
            if enrollment is None:
                # al ser la primera prueba, se verifica que sea la primera de la lección
                if lesson_order > 1:
                    raise Exception("You need to take the first lesson firstly.")
                enrollment = EnrollmentModel()
                enrollment.course_id = course_id
                enrollment.total_score = lesson_score['total_score']
                enrollment.user_id = user_id
                enrollment.active = True
                enrollment.status = 'Not aproved'
            else:
                query = """select
                            lessons.order
                            from public.lesson_scores
                            left join public.lessons on public.lesson_scores.lesson_id = lessons.id
                            where lessons.course_id = '{0}'""".format(course_id)
                lsql = text(query)
                lessons = session.execute(lsql)
                print(lessons)
                print(lessons.rowcount)
                print(lesson_order)
                if lessons.rowcount >= 1 and lesson_order > 1:
                    print("en rowcoun 1")
                    orders = [lesson[0] for lesson in lessons]
                    print(orders)
                    last = max(orders)
                    print(last)
                    if (last + 1) != lesson_order:
                        raise Exception("You can't take this lesson because, you need to pass one or more before this.")
                elif lesson_order > 1:
                    raise Exception("You can't take this lesson because, you need to pass one or more before this.")
            user_lesson = LessonScoreModel()
            user_lesson.lesson_id = lesson_id
            user_lesson.lesson_result = lesson_score['total_score']
            user_lesson.unsuccessful_answers = lesson_score['unsuccessful_answers']
            user_lesson.successful_answers = lesson_score['successful_answers']
            enrollment.lesson_scores.append(user_lesson)
            print("before commit")
            session.add(enrollment)
            session.add(user_lesson)
            session.commit()
            return enrollment
        except sqlalchemy.exc.IntegrityError as ie:
            logger.error(str(ie))
            session.rollback()
            raise Exception("El nombre o código del curso ya existe.")
        except Exception as exc:
            logger.error(str(exc))
            session.rollback()
            raise exc
