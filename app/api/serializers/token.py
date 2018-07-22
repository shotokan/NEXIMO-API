from marshmallow import Schema, fields


class TokenSchema(Schema):
    user_id = fields.Str()
    access_token = fields.Str()
    refresh_token = fields.Str()
    access_token_expires_at = fields.Integer(data_key="access_token_expires_at")
    issued_at = fields.Integer(data_key="issued_at")
    refresh_token_expires_in = fields.Integer(data_key="refresh_token_expires_in")
    role_name = fields.Str()
    role_id = fields.Str()
    token_type = fields.Str(missing="JWT Token", default="JWT Token")
