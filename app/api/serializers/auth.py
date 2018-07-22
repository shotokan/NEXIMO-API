from marshmallow import Schema, fields, validate, ValidationError
from .validations.validators import validate_password


class AuthSchema(Schema):
    grant_type = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate_password)


class RefreshSchema(Schema):
    grant_type = fields.Str(required=True)
    email = fields.Str(required=True)
