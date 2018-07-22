from marshmallow import Schema, fields, validate


class RoleSchema(Schema):
    id = fields.Str()
    name = fields.Str()
