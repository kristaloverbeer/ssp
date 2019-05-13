from typing import Optional, Union, List, Tuple

from src.database.models import db
from src.database.models.hotel import Hotel
from src.logging.mixin import LoggingMixin


class HotelRepository(LoggingMixin):
    def __init__(self, hotel_schema):
        self.hotel_schema = hotel_schema

    def insert(self, hotels_to_add: dict) -> Tuple[dict, int]:
        self.logger.debug('Inserting hotel: {}'.format(hotels_to_add))

        deserialized_hotel, errors = self.hotel_schema.load(hotels_to_add)
        if errors:
            return errors, 400

        db.session.add(deserialized_hotel)
        db.session.commit()

        return {'message': 'Success'}, 201

    def get(self, hotel_id: Optional[int] = None) -> Tuple[Union[dict, List[dict]], int]:
        if hotel_id is not None:
            deserialized_hotel = Hotel.query.get(hotel_id)
            if not deserialized_hotel:
                return {'message': 'Hotel not found'}, 404
            serialized_hotel, errors = self.hotel_schema.dump(deserialized_hotel)
            if errors:
                return errors, 400
            return serialized_hotel, 200
        else:
            deserialized_hotels = Hotel.query.all()
            serialized_hotels, errors = self.hotel_schema.dump(deserialized_hotels, many=True)
            if errors:
                return errors, 400
            return serialized_hotels, 200

    def update(self, hotel_id: int, updates: dict) -> Tuple[Union[dict, List[dict]], int]:
        validate_updates, validation_errors = self.hotel_schema.load(updates)
        if validation_errors:
            return validation_errors, 400
        updated_hotel = Hotel.query.filter_by(id=hotel_id).update(updates)
        db.session.commit()
        serialized_updated_hotel, status_code = self.get(hotel_id)
        return serialized_updated_hotel, status_code

    def delete(self, hotel_id: int) -> Tuple[dict, int]:
        deserialized_hotel = Hotel.query.get(hotel_id)
        if not deserialized_hotel:
            return {'message': 'Hotel not found'}, 404

        db.session.delete(deserialized_hotel)
        db.session.commit()

        return {'message': 'Success'}, 200
