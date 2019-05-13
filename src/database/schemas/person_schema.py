from marshmallow import Schema, fields, validates, ValidationError, post_load

from src.database.models.person import Person


class PersonSchema(Schema):
    id = fields.Integer(required=True, allow_none=False)
    name = fields.String(required=True, allow_none=False)
    address = fields.String(required=False, allow_none=True)
    has_driving_license = fields.Boolean(required=False, allow_none=False)

    @post_load
    def make_person(self, person_data: dict) -> Person:
        return Person(**person_data)

    @validates('name')
    def validate_name(self, name: str) -> None:
        first_and_last_name = name.split()
        if not len(first_and_last_name) > 1:
            raise ValidationError('You must enter your first name AND last name in this field.')
