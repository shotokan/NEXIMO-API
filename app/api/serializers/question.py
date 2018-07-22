from marshmallow import Schema, fields
from .validations.validators import validate_type_question


class CorrectChoicesSchema(Schema):
    answer = fields.Str()


class WrongChoicesSchema(Schema):
    answer = fields.Str()


class QuestionRequestSchema(Schema):
    question = fields.Str()
    code = fields.Str()
    score = fields.Integer()
    lesson_id = fields.Str()
    type_question = fields.Str()
    corrects = fields.Nested(CorrectChoicesSchema, many=True)
    wrong = fields.Nested(CorrectChoicesSchema, many=True)


class AnswerResponseSchema(Schema):
    id = fields.Str()
    answer = fields.Str()


class QuestionResponseSchema(Schema):
    question = fields.Str()
    code = fields.Str()
    score = fields.Integer()
    lesson_id = fields.Str()
    type_question = fields.Str(validate=validate_type_question)
    choices = fields.Nested(AnswerResponseSchema, many=True)
