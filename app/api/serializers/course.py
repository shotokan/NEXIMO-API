from marshmallow import Schema, fields
from .validations.validators import validate_mandatory_courses, validate_mandatory_courses_code


class CourseSchema(Schema):
    id = fields.Str()
    name = fields.Str(required=True)
    description = fields.Str()
    code = fields.Str(required=True)
    mandatory_courses = fields.List(fields.Str(), load_only=True, validate=validate_mandatory_courses)
    mandatory_courses_code = fields.List(fields.Str(), validate=validate_mandatory_courses_code)
    credits = fields.Integer()
    created_at = fields.DateTime()


class CourseUserSchema(Schema):
    id = fields.Str()
    name = fields.Str(required=True)
    description = fields.Str()
    code = fields.Str(required=True)
    mandatory_courses = fields.List(fields.Str(), validate=validate_mandatory_courses)
    mandatory_courses_code = fields.List(fields.Str(), validate=validate_mandatory_courses_code)
    credits = fields.Integer()
    created_at = fields.DateTime()