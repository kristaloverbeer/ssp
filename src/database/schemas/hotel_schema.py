from marshmallow import Schema, fields, validates, ValidationError, post_load

from src.database.models.hotel import Hotel


class HotelSchema(Schema):
    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=True, allow_none=False)
    address = fields.String(required=False, allow_none=True)

    @post_load
    def make_hotel(self, hotel_data: dict) -> Hotel:
        return Hotel(**hotel_data)
