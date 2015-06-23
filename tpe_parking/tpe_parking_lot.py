#!/usr/bin/env python3

import json
import os
import sys
import json
import requests

from geopy.distance import vincenty

import twd97
import logging
logger = logging.getLogger(__name__)


DB_DIR = 'db'
PARKING_LOT_DB_FILE = 'alldescriptions.json'
AVAILABLE_PARKING_PLACE_DB_FILE = 'allavailable.json'


class ParkingLotDb:
    UPDATE_URL = 'http://opendata.dot.taipei.gov.tw/opendata/'
    def __init__(self):
        self._jsParkingInfo = None
        self._jsAvailableParkingPlace = None

    def load(self):
        self._load_db()

    def update(self):
        for db_file_path in [PARKING_LOT_DB_FILE, AVAILABLE_PARKING_PLACE_DB_FILE]:
            response = requests.get(ParkingLotDb.UPDATE_URL + db_file_path)
            with open(os.path.join(DB_DIR, db_file_path), 'w') as outfile:
                json.dump(response.json(), outfile)
        
        self._load_db()

    def _load_db(self):
        try:
            jsParkingInfo_path = os.path.join(DB_DIR, PARKING_LOT_DB_FILE)
            jsAvailableParkingPlace_path = os.path.join(DB_DIR, AVAILABLE_PARKING_PLACE_DB_FILE)
    
            fp = open(os.path.join(DB_DIR, PARKING_LOT_DB_FILE))
            self._jsParkingInfo = json.load(fp)
            fp.close()

            fp = open(os.path.join(DB_DIR, AVAILABLE_PARKING_PLACE_DB_FILE))
            self._jsAvailableParkingPlace = json.load(fp)
            fp.close()

        except OSError as err:
            print("OS error: {0}".format(err))
        except:
            print("Unexpected error:", sys.exc_info()[0])

    def find_parking_lot(self, area):
        for park in self._jsParkingInfo['data']['park']:
            if park['area'] == area:
                yield park

    def find_parking_lot_by_coordinate(self, location, within_meters):
        x, y = location
        for park in self._jsParkingInfo['data']['park']:
            if 'Entrancecoord' in park:
                for entrance in park['Entrancecoord']['EntrancecoordInfo']:
                    entrance_x, entrance_y = float(entrance['Xcod']), float(entrance['Ycod'])
                    if vincenty((x, y), (entrance_x, entrance_y)).meters < within_meters:
                        yield park
                        break
            elif 'tw97x' in park and 'tw97y' in park:
                entrance_x, entrance_y = twd97.towgs84(float(park['tw97x']), float(park['tw97y']))
                if vincenty((x, y), (entrance_x, entrance_y)).meters < within_meters:
                    yield park
            else:
                logger.warning('No location info for ' + park['name'])

    def find_available_parking_space(self, park_id):
        for park in self._jsAvailableParkingPlace['data']['park']:
            if park['id'] == park_id:
                return park
                

class ParkingLotInfoProvider:
    def __init__(self):
        self._db = ParkingLotDb()
        self._db.load()

    def update_db(self):
        self._db.update()

    def find_parking_lot(self, area):
        return self._db.find_parking_lot(area)

    def find_parking_lot_by_coordinate(self, location, within_meters):
        return self._db.find_parking_lot_by_coordinate(location, within_meters)

    def find_available_parking_space(self, park_id):
        return self._db.find_available_parking_space(park_id)

