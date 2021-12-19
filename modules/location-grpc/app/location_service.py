import logging

from typing import Dict
from models import Location
from schemas import LocationSchema
from geoalchemy2.functions import ST_Point
from database import db

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("location_service")


class LocationService:
    @staticmethod
    def Retrieve(location_id) -> Location:
        with db.Session() as dbs:
            attr = {"id": location_id}
            location = db.s.first(Location, **attr)
            db.s.flush()
            db.s.commit()
            dbs.close()
            return location

    @staticmethod
    def Create(location: Dict) -> Location:
        print("location in svc: before validate = ", location)
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        new_location = Location()
        new_location.person_id = location["person_id"]
        new_location.creation_time = location["creation_time"]
        new_location.coordinate = ST_Point(location["latitude"], location["longitude"])

        with db.Session() as dbs:  # work with the session here
            persisted_location = db.s.add(new_location)
            result = persisted_location
            all_locations = db.s.all(Location)
            print("len(all_locations): ", len(all_locations))
            db.s.flush()
            db.s.commit()
            dbs.close()
