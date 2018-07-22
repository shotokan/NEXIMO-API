"""
    author: ivan sabido
    date: 19/07/2018
    email: <isc_86@hotmail.com>
"""

# Se importan los modelos para que sqlalchemy pueda generar las tablas, si estas no existen
from .user import UserModel
from .role import RoleModel
from .token import TokenModel
from .course import CourseModel
from .lesson import LessonModel
from .question import QuestionModel
from .enrollment import EnrollmentModel
from .lesson_score import LessonScoreModel
from .choices import ChoiceModel

from app.database.sqlalchemy.connection import engine, Base, Session

Session = Session


def db_init():
    """ Initialize database """
    # Recreate database each time for demo
    # #Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
