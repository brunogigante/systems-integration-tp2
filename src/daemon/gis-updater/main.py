import sys
import time
import requests
from get_api_data import get_data
from db_connection import db_rel_connection

POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 60
ENTITIES_PER_ITERATION = int(sys.argv[2]) if len(sys.argv) >= 3 else 10

if __name__ == "__main__":

    while True:
        print(f"Getting up to {ENTITIES_PER_ITERATION} entities without coordinates...")
        # !TODO: 1- Use api-gis to retrieve a fixed amount of entities without coordinates (e.g. 100 entities per iteration, use ENTITIES_PER_ITERATION)
        resp = requests.get(f"http://api-entities:8080/api/cities/coordinates/{ENTITIES_PER_ITERATION}")
        data = resp.json()
        # !TODO: 2- Use the entity information to retrieve coordinates from an external API
        coordinates = {}
        for i in range(len(data)):
            api_data = get_data(data[i][1], data[i][3], data[i][2])
            if len(api_data) > 0:
                coordinates[data[i][0]] = [api_data[0]['lon'], api_data[0]['lat']]
        # !TODO: 3- Submit the changes
        connection = db_rel_connection()
        with connection.cursor() as cursor:
            for key in coordinates.keys():
                cursor.execute(f"update city set city_coordinates = ST_GeomFromText('POINT({coordinates[key][0]} {coordinates[key][1]})', 4326) where id = {key}")
                connection.commit()
        time.sleep(POLLING_FREQ)
