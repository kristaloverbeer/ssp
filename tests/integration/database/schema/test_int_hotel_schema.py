from src.database.models.hotel import Hotel
from src.database.schemas.hotel_schema import HotelSchema


def test_insert_one_hotel(db_session):
    # Given
    hotel_schema = HotelSchema()
    hotel = {
        'name': 'hotel 1',
        'address': '1 boulevard du test',
    }
    # When
    deserialized_hotel, errors = hotel_schema.load(hotel)
    db_session.add(deserialized_hotel)
    db_session.commit()

    # Then
    inserted_hotel = db_session.query(Hotel).first()
    serialized_inserted_hotel, new_errors = hotel_schema.dump(inserted_hotel)
    serialized_inserted_hotel.pop('id')

    assert hotel == serialized_inserted_hotel


def test_insert_several_hotels(db_session):
    # Given
    hotel_schema = HotelSchema()

    hotels = [
        {
            'name': 'hotel 1',
            'address': '1 boulevard du test',
        },
        {
            'name': 'hotel 2',
            'address': '2 boulevard du test',
        }
    ]
    # When
    deserialized_hotels, errorss = hotel_schema.load(hotels, many=True)
    db_session.add_all(deserialized_hotels)
    db_session.commit()

    # Then
    inserted_hotels = db_session.query(Hotel).all()
    serialized_inserted_hotel, new_errors = hotel_schema.dump(inserted_hotels, many=True)
    for hotel in serialized_inserted_hotel:
        hotel.pop('id')

    assert hotels == serialized_inserted_hotel

