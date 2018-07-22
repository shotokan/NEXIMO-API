import falcon

from falcon_cors import CORS

from app.api.controllers.v1.auth import AuthResource, AuthenticationRefresh
from app.api.middlewares.token_auth import AuthMiddleware
from app.model import db_init, Session
from app.api.middlewares.session_db_manager import SQLAlchemySessionManager
from app.api.middlewares.json_translator import JSONTranslator
from app.api.middlewares.require_json import RequireJSON
from app.api.controllers.v1.user import User
from app.api.controllers.v1.ping import Ping
from app.api.controllers.v1.course import Course, CourseResource
from app.api.controllers.v1.lesson import Lesson, LessonTaken, LessonDetails
from app.api.controllers.v1.question import Question
from app.api.controllers.v1.role import Role


def init_app():
    # Database initialization
    db_init()

    # Middlewares
    public_cors = CORS(allow_all_origins=True)
    middleware = [
        public_cors.middleware,
        RequireJSON(),
        JSONTranslator(),
        SQLAlchemySessionManager(Session)
    ]
    app = falcon.API(middleware=middleware)

    # API V1
    user = User()
    ping = Ping()
    auth = AuthResource()
    refresh = AuthenticationRefresh()
    course = Course()
    course_id = CourseResource()
    lesson = Lesson()
    question = Question()
    lesson_take = LessonTaken()
    lesson_details = LessonDetails()
    role = Role()

    app.add_route('/v1/courses', course)
    app.add_route('/v1/courses/{uuid}', course_id)
    app.add_route('/v1/courses/{uuid}/lessons', lesson)
    app.add_route('/v1/lessons/{lesson_id}/questions', question)
    app.add_route('/v1/lessons/{lesson_id}/details', lesson_details)
    app.add_route('/v1/lessons/{lesson_id}/take', lesson_take)
    app.add_route('/v1/users', user)
    app.add_route('/v1/ping', ping)
    app.add_route('/v1/roles', role)
    app.add_route('/v1/oauth/token', auth)
    app.add_route('/v1/oauth/token/refresh', refresh)

    return app
