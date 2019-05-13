from src.database.models.hotel import Hotel
from src.database.schemas.hotel_schema import HotelSchema
from src.repository.hotel_repository import HotelRepository


def test_insert_one_correct_hotel(db_session):
    # Given
    hotel_schema = HotelSchema()
    hotel_repository = HotelRepository(hotel_schema)
    hotel = {
        'name': 'hotel 1',
        'address': '1 boulevard du test',
    }
    # When
    response, status_code = hotel_repository.insert(hotel)

    # Then
    inserted_hotel = db_session.query(Hotel).first()
    serialized_inserted_hotel, new_errors = hotel_schema.dump(inserted_hotel)
    serialized_inserted_hotel.pop('id')

    assert hotel == serialized_inserted_hotel
    assert (response, status_code) == ({'message': 'Success'}, 201)


def test_insert_one_incorrect_hotel(db_session):
    # Given
    hotel_schema = HotelSchema()
    hotel_repository = HotelRepository(hotel_schema)
    hotel = {
        'address': '1 boulevard du test',
    }
    # When
    response, status_code = hotel_repository.insert(hotel)

    # Then
    assert (response, status_code) == ({'name': ['Missing data for required field.']}, 400)


def test_get_hotel(db_session):
    # Given
    hotel_schema = HotelSchema()
    hotel_repository = HotelRepository(hotel_schema)
    hotel = {
        'name': 'hotel 1',
        'address': '1 boulevard du test',
    }
    _, _ = hotel_repository.insert(hotel)
    # When
    response, status_code = hotel_repository.get()
    # Then
    assert response, status_code == ([hotel], 200)


def test_get_hotel_with_id(db_session):
    # Given
    hotel_schema = HotelSchema()
    hotel_repository = HotelRepository(hotel_schema)
    hotel = {
        'name': 'hotel 1',
        'address': '1 boulevard du test',
    }
    db_session.add(Hotel(**hotel))
    db_session.commit()
    # When
    response, status_code = hotel_repository.get(1)
    response.pop('id')
    # Then
    assert (response, status_code) == (hotel, 200)


def test_get_hotels(db_session):
    # Given
    hotel_schema = HotelSchema()
    hotel_repository = HotelRepository(hotel_schema)
    hotels = [
        {
            'name': 'hotel 1',
            'address': '1 boulevard du test',
        }, {
            'name': 'hotel 1',
            'address': '1 boulevard du test',
        },
    ]
    db_session.add_all([Hotel(**hotel) for hotel in hotels])
    db_session.commit()
    # When
    response, status_code = hotel_repository.get()
    for hotel in response:
        hotel.pop('id')
    # Then
    assert (response, status_code) == (hotels, 200)


def test_get_non_existing_hotel(db_session):
    # Given
    hotel_schema = HotelSchema()
    hotel_repository = HotelRepository(hotel_schema)
    # When
    response, status_code = hotel_repository.get(1)
    # Then
    assert (response, status_code) == ({'message': 'Hotel not found'}, 404)


def test_update_hotel_name(db_session):
    # Given
    hotel_schema = HotelSchema()
    hotel_repository = HotelRepository(hotel_schema)
    hotel = {
        'name': 'hotel 1',
        'address': '1 boulevard du test',
    }
    db_session.add(Hotel(**hotel))
    db_session.commit()
    updates = {'name': 'hotel 2'}
    # When
    response, status_code = hotel_repository.update(1, updates)
    # Then
    assert (response['name'], status_code) == ('hotel 2', 200)


def test_update_hotel_with_wrong_data(db_session):
    # Given
    hotel_schema = HotelSchema()
    hotel_repository = HotelRepository(hotel_schema)
    hotel = {
        'name': 'hotel 1',
        'address': '1 boulevard du test',
    }
    db_session.add(Hotel(**hotel))
    db_session.commit()
    updates = {'name': None}
    # When
    response, status_code = hotel_repository.update(1, updates)
    # Then
    assert (response, status_code) == ({'name': ['Field may not be null.']}, 400)


def test_update_non_existing_hotel(db_session):
    # Given
    hotel_schema = HotelSchema()
    hotel_repository = HotelRepository(hotel_schema)
    updates = {'name': 'hotel 2'}
    # When
    response, status_code = hotel_repository.update(1, updates)
    # Then
    assert (response, status_code) == ({'message': 'Hotel not found'}, 404)


def test_delete_hotel(db_session):
    # Given
    hotel_schema = HotelSchema()
    hotel_repository = HotelRepository(hotel_schema)
    hotel = {
        'name': 'hotel 1',
        'address': '1 boulevard du test',
    }
    db_session.add(Hotel(**hotel))
    db_session.commit()
    # When
    response, status_code = hotel_repository.delete(1)
    # Then
    assert (response, status_code) == ({'message': 'Success'}, 200)

    deleted_hotel = Hotel.query.first()
    assert deleted_hotel is None


def test_delete_non_existing_hotel(db_session):
    # Given
    hotel_schema = HotelSchema()
    hotel_repository = HotelRepository(hotel_schema)
    # When
    response, status_code = hotel_repository.delete(1)
    # Then
    assert (response, status_code) == ({'message': 'Hotel not found'}, 404)
