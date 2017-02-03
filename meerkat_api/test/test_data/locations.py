from meerkat_abacus.model import Locations
from datetime import datetime


testshire = [
    Locations(**{"id":1,
                 "name":"Testshire",
                 "parent_location":None,
                 'geolocation':'0,0',
                 "other":None,
                 "deviceid":None,
                 "clinic_type":None,
                 "case_report":None,
                 "level": "country",
                 "start_date": None,
                 "case_type":None,
                 "population":1000}),
    Locations(**{"id":2,
                 "name":"Region Major",
                 "parent_location":1,
                 'geolocation':'1,0',
                 "other":None,
                 "deviceid":None,
                 "clinic_type":None,
                 "case_report":None,
                 "level": "region",
                 "start_date": None,
                 "case_type":None,
                 "population":750}),
    Locations(**{"id":3,
                 "name":"Region Minor",
                 "parent_location":1,
                 'geolocation':'1,1',
                 "other":None,
                 "deviceid":None,
                 "clinic_type":None,
                 "case_report":None,
                 "level": "region",
                 "start_date": None,
                 "case_type":None,
                 "population":250}),
    Locations(**{"id":4,
                 "name":"District Blue",
                 "parent_location":2,
                 'geolocation':'2,0',
                 "other":None,
                 "deviceid":None,
                 "clinic_type":None,
                 "case_report":None,
                 "level": "district",
                 "start_date": None,
                 "case_type":None,
                 "population":500}),
    Locations(**{"id":5,
                 "name":"District Red",
                 "parent_location":2,
                 'geolocation':'2,1',
                 "other":None,
                 "deviceid":None,
                 "clinic_type":None,
                 "case_report":None,
                 "level": "district",
                 "start_date": None,
                 "case_type":None,
                 "population":250}),
    Locations(**{"id":6,
                 "name":"District Green",
                 "parent_location":3,
                 'geolocation':'2,2',
                 "other":None,
                 "deviceid":None,
                 "clinic_type":None,
                 "case_report":None,
                 "level": "district",
                 "start_date": None,
                 "case_type":None,
                 "population":250}),
    Locations(**{"id":7,
                 "name":"Clinic A",
                 "parent_location":4,
                 'geolocation':'3,0',
                 "other":None,
                 "deviceid":"1111",
                 "clinic_type":"test",
                 "case_report":1,
                 "level": "clinic",
                 "start_date": "2016-08-01T00:00:00",
                 "case_type":None,
                 "population":250}),
    Locations(**{"id":8,
                 "name":"Clinic B",
                 "parent_location":4,
                 'geolocation':'3,1',
                 "other":None,
                 "deviceid":"2222",
                 "clinic_type":"test",
                 "case_report":1,
                 "level": "clinic",
                 "start_date": "2016-08-01T00:00:00",
                 "case_type":None,
                 "population":250}),
    Locations(**{"id":9,
                 "name":"Clinic C",
                 "parent_location":5,
                 'geolocation':'3,2',
                 "other":None,
                 "deviceid":"3333",
                 "clinic_type":"test",
                 "case_report":1,
                 "level": "clinic",
                 "start_date": "2016-08-01T00:00:00",
                 "case_type":None,
                 "population":250}),
    Locations(**{"id":10,
                 "name":"Clinic D",
                 "parent_location":6,
                 'geolocation':'3,3',
                 "other":None,
                 "deviceid":"4444",
                 "clinic_type":"test",
                 "case_report":1,
                 "level": "clinic",
                 "start_date": "2016-08-01T00:00:00",
                 "case_type":None,
                 "population":250})
]

locations = [


    
    Locations(**{'population': 10000, 'clinic_type': None,
                 'deviceid': None, 'case_report': None, 'point_location': None, 
                 'parent_location': None, 'level': "country", 
                 'name': 'Demo', 'id': 1, 'other': None}),
    Locations(**{'population': 7000,'clinic_type': None, 'deviceid': None, 'case_report': None, 'point_location': None, 'parent_location': 1, 'level': 'region', 'name': 'Region 1', 'id': 2, 'other': None}),
    Locations(**{'population': 3000,'clinic_type': None, 'deviceid': None, 'case_report': None, 'point_location': None, 'parent_location': 1, 'level': 'region', 'name': 'Region 2', 'id': 3, 'other': None}),
    Locations(**{'population': 5000,'clinic_type': None, 'deviceid': None, 'case_report': None, 'point_location': None, 'parent_location': 2, 'level': 'district', 'name': 'District 1', 'id': 4, 'other': None}),
    Locations(**{'population': 2000,'clinic_type': None, 'deviceid': None, 'case_report': None, 'point_location': None, 'parent_location': 2, 'level': 'district', 'name': 'District 2', 'id': 5, 'other': None}),
    Locations(**{'population': 3000,'clinic_type': None, 'deviceid': None, 'case_report': None, 'point_location': None, 'parent_location': 3, 'level': 'district', 'name': 'District 3', 'id': 6, 'other': None}),
    Locations(**{'population': 1000,'clinic_type': 'SARI', 'deviceid': '2', 'case_report': 1, 'point_location': 'POINT(0.2 0.2)', 'parent_location': 4, 'level': 'clinic', 'name': 'Clinic 2', 'id': 8, 'start_date': datetime(2016, 1, 1), 'other': None}),
    Locations(**{'clinic_type': 'Focal', 'deviceid': '3', 'case_report': 0, 'point_location': 'POINT(0.2 0.3)', 'parent_location': 4, 'start_date': datetime(2016, 1, 1), 'level': 'clinic', 'name': 'Clinic 3', 'id': 9, 'other': None}),
    Locations(**{'population': 1000,'clinic_type': 'SARI', 'deviceid': '4', 'case_report': 1, 'point_location': 'POINT(0.3 0.2)', 'parent_location': 5, 'start_date': datetime(2016, 1, 1), 'level': 'clinic', 'name': 'Clinic 4', 'id': 10, 'other': None}),
    Locations(**{'population': 3000,'clinic_type': 'Refugee', 'deviceid': '5', 'case_report': 1, 'point_location': 'POINT(-0.1 0.4)', 'parent_location': 6, 'start_date': datetime(2016, 1, 1), 'level': 'clinic', 'name': 'Clinic 5', 'id': 11, 'other': None}),
    Locations(**{'population': 3000,'clinic_type': 'Refugee', 'deviceid': '1,6', 'case_report': 1, 'point_location': 'POINT(0.1 0.1)', 'parent_location': 4, 'start_date': datetime(datetime.now().year, 2, 1), 'level': 'clinic', 'name': 'Clinic 1', 'id': 7, 'other': None})
]

