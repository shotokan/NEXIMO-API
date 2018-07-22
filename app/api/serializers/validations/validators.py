from uuid import UUID
from marshmallow import ValidationError
from app.utils.type_question import TYPE_QUESTIONS


def validate_password(n):
    if len(n) < 8:
        raise ValidationError('Password must be greater than 7 characters')
    if len(n) > 50:
        raise ValidationError('Password must not be greater than 50 characters')


def validate_mandatory_courses(n):
    for element in n:
        try:
            UUID(element, version=4)
        except ValueError:
            # If it's a value error, then the string
            # is not a valid hex code for a UUID.
            raise ValidationError('elements in mandatory_courses must be of type uuid version 4.')


def validate_mandatory_courses_code(n):
    for element in n:
        if not isinstance(element, str):
            raise ValidationError('elements in mandatory_courses must be a string.')


def validate_type_question(n):
    if n not in TYPE_QUESTIONS:
        types = ",".join(TYPE_QUESTIONS.values())
        raise ValidationError('You can only pass this types {}. See instructions.'.format(types))

