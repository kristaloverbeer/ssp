from typing import Optional, Union, List, Tuple

from src.database.models import db
from src.database.models.person import Person
from src.logging.mixin import LoggingMixin


class PersonRepository(LoggingMixin):
    def __init__(self, person_schema):
        self.person_schema = person_schema

    def insert(self, persons_to_add: dict) -> Tuple[dict, int]:
        self.logger.debug('Inserting person: {}'.format(persons_to_add))

        deserialized_person, errors = self.person_schema.load(persons_to_add)
        if errors:
            return errors, 400

        db.session.add(deserialized_person)
        db.session.commit()

        return {'message': 'Success'}, 201

    def get(self, person_id: Optional[int] = None) -> Tuple[Union[dict, List[dict]], int]:
        if person_id is not None:
            deserialized_person = Person.query.get(person_id)
            if not deserialized_person:
                return {'message': 'Person not found'}, 404
            serialized_person, errors = self.person_schema.dump(deserialized_person)
            if errors:
                return errors, 400
            return serialized_person, 200
        else:
            deserialized_persons = Person.query.all()
            serialized_persons, errors = self.person_schema.dump(deserialized_persons, many=True)
            if errors:
                return errors, 400
            return serialized_persons, 200

    def update(self, person_id: int, updates: dict) -> Tuple[Union[dict, List[dict]], int]:
        validate_updates, validation_errors = self.person_schema.load(updates)
        if validation_errors:
            return validation_errors, 400
        updated_person = Person.query.filter_by(id=person_id).update(updates)
        db.session.commit()
        serialized_updated_person, status_code = self.get(person_id)
        return serialized_updated_person, status_code

    def delete(self, person_id: int) -> Tuple[dict, int]:
        deserialized_person = Person.query.get(person_id)
        if not deserialized_person:
            return {'message': 'Person not found'}, 404

        db.session.delete(deserialized_person)
        db.session.commit()

        return {'message': 'Success'}, 200
