"""
Resources for creating maps
"""
import shapely.geometry
from flask import g, request
from flask_restful import Resource
from geoalchemy2.shape import to_shape
from geojson import Point, FeatureCollection, Feature
from sqlalchemy import func, Float, or_

from meerkat_abacus import model
from meerkat_abacus.model import Data, Locations
from meerkat_abacus.util import is_child, get_locations
from meerkat_api.authentication import authenticate, is_allowed_location
from meerkat_api.extensions import db, api
from meerkat_api.resources.incidence import IncidenceRate
from meerkat_api.util import fix_dates


class Clinics(Resource):
    """
    Geojson for all clinics that are sublocation of location.

    Args:\n
        location_id: location that all other locations should be under\n
        clinic_type: If we should only get a specific clinic type (default=None)\n

    Returns:\n
        points: A geojson FeatureCollection of points\n
    """
    def get(self, location_id, clinic_type=None, require_case_report="yes"):
        locations = get_locations(db.session)
        other_conditions = {}
        for arg in request.args:
            other_conditions[arg] = request.args.get(arg)
        points = []
        if not is_allowed_location(location_id, g.allowed_location):
            return FeatureCollection(points)

        for l in locations:
            if ((locations[l].case_report or require_case_report == "no") and is_child(
                    location_id, l, locations) and locations[l].point_location is not None
                and (not clinic_type or locations[l].clinic_type == clinic_type)):
                other_cond = True
                for cond in other_conditions:
                    if locations[l].other.get(cond, None) != other_conditions[cond]:
                        other_cond = False
                        break
                if not other_cond:
                    continue
                geo = to_shape(locations[l].point_location)
                p = Point((float(geo.x), float(geo.y))) # Note that this is the specified order for geojson
                points.append(Feature(geometry=p,
                                      properties={"name":
                                                  locations[l].name,
                                                  "other": locations[l].other}))
        return FeatureCollection(points)



class MapVariable(Resource):
    """
    Want to map a variable id by clinic (only include case reporting clinics)

    Args:\n
       variable_id: variable to map\n
       interval: the time interval to aggregate over (default=year)\n
       location: If we should restrict on location\n
       include_all_clinics: If true we include all clinics even with no cases\n

    Returns:\n
        map_data: [{value:0, geolocation: .., clinic:name},...]\n
    """
    decorators = [authenticate]

    def get(self, variable_id, location=1,
            start_date=None, end_date=None, include_all_clinics=False):

        start_date, end_date = fix_dates(start_date, end_date)
        location = int(location)

        allowed_location = 1
        if g:
            allowed_location = g.allowed_location
        if not is_allowed_location(location, allowed_location):
            return {}
        vi = str(variable_id)
        results = db.session.query(
            func.sum(Data.variables[vi].astext.cast(Float)).label('value'),
            Data.geolocation,
            Data.clinic
        ).filter(
            Data.variables.has_key(variable_id),
            Data.date >= start_date,
            Data.date < end_date,
            or_(
                loc == location for loc in (Data.country,
                                            Data.region,
                                            Data.district,
                                            Data.clinic)
            )
        ).group_by("clinic", "geolocation")

        locations = get_locations(db.session)
        ret = {}
        for r in results.all():
            if r[1] is not None:
                geo = to_shape(r[1])
                if r[2]:
                    # Leaflet uses LatLng
                    ret[str(r[2])] = {"value": r[0], "geolocation": [geo.y, geo.x],
                                 "clinic": locations[r[2]].name}
                else:
                    if not include_all_clinics:
                        cords = [geo.y, geo.x]  # Leaflet uses LatLng
                        ret[str(cords)] = {"value": r[0], "geolocation": cords,
                                           "clinic": "Outbreak Investigation"}


        if include_all_clinics:
            results = db.session.query(model.Locations)
            for row in results.all():
                if is_allowed_location(row.id, location):
                    if row.case_report and row.point_location is not None and str(row.id) not in ret.keys():
                        geo = to_shape(row.point_location)
                        ret[str(row.id)] = {"value": 0,
                                            "geolocation": [geo.y, geo.x],
                                            "clinic": row.name}
        return ret


class IncidenceMap(Resource):
    """
    Want to map a variable id by clinic (only include case reporting clinics)

    Args:\n
       variable_id: variable to map\n
       interval: the time interval to aggregate over (default=year)\n
       location: If we should restrict on location\n
       include_all_clinics: If true we include all clinics even with no cases\n

    Returns:\n
        map_data: [{value:0, geolocation: .., clinic:name},...]\n
    """
    decorators = [authenticate]

    def get(self, variable_id):

        ir = IncidenceRate()

        incidence_rates = ir.get(variable_id, "clinic")

        locations = get_locations(db.session)
        ret = {}
        for clinic in incidence_rates.keys():
            if incidence_rates[clinic]:
                print(clinic)

                if locations[clinic].point_location is not None:
                    geo = to_shape(locations[clinic].point_location)
                    ret[clinic] = {"value": incidence_rates[clinic],
                                   "geolocation": [geo.y, geo.x],
                                   # Leaflet uses LatLng
                                   "clinic": locations[clinic].name}

        return ret


class Shapes(Resource):
    """
    Returns the shapes for the given level

    Args:\n
       level: region, district or clinic
    """

    def get(self, level):
        results = db.session.query(
            Locations.point_location,
            Locations.area,
            Locations.name
        ).filter(
            Locations.level == level
        )
        features = []
        for r in results:
            feature = {"type": "Feature", "properties": {"Name": r[2]}}
            if level == "clinic" and r[0] is not None:
                shape = to_shape(r[0])
                feature["geometry"] = shapely.geometry.mapping(shape)
                features.append(feature)
            elif r[1] is not None:
                shape = to_shape(r[1])
                feature["geometry"] = shapely.geometry.mapping(shape)
                features.append(feature)
        return {"type": "FeatureCollection", "features": features}


class SafeShape(Resource):
    """
    Returns the shape for the given locID.
    If there is no shape data stored for the given loc id, it will return
    the nearest parent for which there is a shape stored.

    Args:\n
       location_id (int): The location id for the desired shape
    """
    def get(self, location_id):
        locID = int(location_id)
        results = db.session.query(
            Locations.id,
            Locations.name,
            Locations.parent_location,
            Locations.level,
            Locations.point_location,
            Locations.area
        )

        def get_location(locID):
            locations = list(filter(lambda r: r[0] == locID, list(results)))
            if len(locations) == 1:
                return locations[0]
            else:
                return None

        location_ancestors = [get_location(locID)]
        while location_ancestors[-1][2] is not None:
            parent = get_location(location_ancestors[-1][2])
            location_ancestors.append(parent)

        for location in location_ancestors:

            has_area = location[5] is not None
            is_point = location[3] == "clinic" and location[4] is not None
            if has_area or is_point:
                feature = {
                    "type": "Feature",
                    "properties": {
                        "Name": location[1],
                        "id": location[0],
                        "parent": location[2]
                    }
                }
                if location[3] == "clinic" and location[4] is not None:
                    shape = to_shape(location[4])
                    feature["geometry"] = shapely.geometry.mapping(shape)
                elif location[5] is not None:
                    shape = to_shape(location[5])
                    feature["geometry"] = shapely.geometry.mapping(shape)
                return feature

        # Return nothing if there is no valid shape data for any parents.
        return {}


api.add_resource(Clinics, "/clinics/<location_id>",
                 "/clinics/<location_id>/<clinic_type>",
                 "/clinics/<location_id>/<clinic_type>/<require_case_report>")
api.add_resource(Shapes, "/geo_shapes/<level>")
api.add_resource(SafeShape, "/geo_shape/<location_id>")
api.add_resource(MapVariable, "/map/<variable_id>",
                 "/map/<variable_id>/<location>",
                 "/map/<variable_id>/<location>/<end_date>",
                 "/map/<variable_id>/<location>/<end_date>/<start_date>")
api.add_resource(IncidenceMap, "/incidence_map/<variable_id>")
