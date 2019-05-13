from typing import Optional, Union, List, Tuple

from src.database.models import db
from src.database.models.visit import Visit
from src.logging.mixin import LoggingMixin


class VisitRepository(LoggingMixin):
    def __init__(self, visit_schema):
        self.visit_schema = visit_schema

    def insert(self, visits_to_add: dict) -> Tuple[dict, int]:
        self.logger.debug('Inserting visit: {}'.format(visits_to_add))

        deserialized_visit, errors = self.visit_schema.load(visits_to_add)
        if errors:
            return errors, 400

        db.session.add(deserialized_visit)
        db.session.commit()

        return {'message': 'Success'}, 201

    def get(self, visit_id: Optional[int] = None) -> Tuple[Union[dict, List[dict]], int]:
        if visit_id is not None:
            deserialized_visit = Visit.query.get(visit_id)
            if not deserialized_visit:
                return {'message': 'Visit not found'}, 404
            serialized_visit, errors = self.visit_schema.dump(deserialized_visit)
            if errors:
                return errors, 400
            return serialized_visit, 200
        else:
            deserialized_visits = Visit.query.all()
            serialized_visits, errors = self.visit_schema.dump(deserialized_visits, many=True)
            if errors:
                return errors, 400
            return serialized_visits, 200

    def update(self, visit_id: int, updates: dict) -> Tuple[Union[dict, List[dict]], int]:
        validate_updates, validation_errors = self.visit_schema.load(updates)
        if validation_errors:
            return validation_errors, 400
        updated_visit = Visit.query.filter_by(id=visit_id).update(updates)
        db.session.commit()
        serialized_updated_visit, status_code = self.get(visit_id)
        return serialized_updated_visit, status_code

    def delete(self, visit_id: int) -> Tuple[dict, int]:
        deserialized_visit = Visit.query.get(visit_id)
        if not deserialized_visit:
            return {'message': 'Visit not found'}, 404

        db.session.delete(deserialized_visit)
        db.session.commit()

        return {'message': 'Success'}, 200
