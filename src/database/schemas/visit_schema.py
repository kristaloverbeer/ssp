from marshmallow import Schema, fields, validates, ValidationError, post_load

from src.database.models.visit import Visit


class VisitSchema(Schema):
    id = fields.Integer(required=True, allow_none=False)
    type = fields.String(required=True, allow_none=False)

    @post_load
    def make_visit(self, visit_data: dict) -> Visit:
        return Visit(**visit_data)
