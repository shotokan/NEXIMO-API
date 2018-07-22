from marshmallow import Schema, fields
from .validations.validators import validate_mandatory_courses, validate_mandatory_courses_code


class LessonSchema(Schema):
    id = fields.Str()
    name = fields.Str(required=True)
    course_id = fields.Str()
    description = fields.Str()
    question_details = fields.Str()
    code = fields.Str(required=True)
    order = fields.Integer()
    hours = fields.Integer()
    score = fields.Integer(required=True)
    aproval_score = fields.Integer(required=True)
