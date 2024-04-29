import abc

from bson import ObjectId
from django.db.models import QuerySet
from django.forms.models import model_to_dict
from injector import inject

from appmeasure.components.unitmeasure_ops import UnitMeasureOps
from appmeasure.models import UnitMeasure
from unitmeasure.logger import logger


class UnitMeasureService(abc.ABC):
    """
    This interface defines the methods of the business logic.
    """

    @inject
    def __init__(self, unit_measure_ops: UnitMeasureOps):
        self.unit_measure_ops = unit_measure_ops

    @abc.abstractmethod
    def query_all(self) -> QuerySet[UnitMeasure]:
        """
        This method retrieves all unit measures from the UnitMeasureOpsMongo concrete class
        """
        raise NotImplementedError

    @abc.abstractmethod
    def query_by_id(self, unit_measure_id: str):
        """
        This method retrieves a unit measure by ID from the
        UnitMeasureOpsMongo concrete class.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def query_by_name(self, name: str) -> QuerySet[UnitMeasure]:
        """
        This method retrieves unit measures by name from the UnitMeasureOpsMongo concrete class.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, data: dict) -> bool:
        """
        This method executes the business logic to create a new unit
        measure record using the UnitMeasureOpsMongo concrete class.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, unit_measure_id: str) -> bool:
        """
        This method execute the business logic to delete a record by ID using
        the UnitMeasureOpsMongo concrete class
        """
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, data: dict, id: str) -> UnitMeasure:
        """
        This method execute the business logic to update a record by ID
        using the UnitMeasureOpsMongo concrete class

        """
        raise NotImplementedError


class UnitMeasureMongoService(UnitMeasureService):
    def query_all(self) -> QuerySet[UnitMeasure]:
        logger.info("Service Layer - querry_all method:::")
        unit_measures = self.unit_measure_ops.query_all()
        return unit_measures

    def query_by_id(self, unit_measure_id: str) -> UnitMeasure:
        logger.info("Service Layer - query_by_id method:::")
        unit_measure_oid = ObjectId(unit_measure_id)
        return self.unit_measure_ops.query_by_id(unit_measure_oid)

    def query_by_name(self, name: str) -> QuerySet[UnitMeasure]:
        logger.info("Service Layer - query_by_name method:::")
        return self.unit_measure_ops.query_by_name(name)

    def create(self, data: dict) -> bool:
        logger.info("Service Layer - create method:::")
        self.unit_measure_ops.create(data)
        return True

    def delete(self, unit_measure_id: str) -> bool:
        logger.info("Service Layer - delete method:::")
        unit_measure_oid = ObjectId(unit_measure_id)
        self.unit_measure_ops.delete(unit_measure_oid)
        return True

    def update(self, data: dict, id: str) -> UnitMeasure:
        logger.info("Service Layer - update method:::")
        unit_measure_oid = ObjectId(id)
        unit_measure = self.unit_measure_ops.query_by_id(unit_measure_oid)
        name = data.get("name")
        if name is not None:
            unit_measure.name = name
        abbreviation = data.get("abbreviation")
        if abbreviation is not None:
            unit_measure.abbreviation = abbreviation
        description = data.get("description")
        if description is not None:
            unit_measure.description = data.get("description")
        unit_measure_update = self.unit_measure_ops.update(unit_measure)
        unit_measure_update._id = str(unit_measure_update._id)
        return model_to_dict(unit_measure_update)
