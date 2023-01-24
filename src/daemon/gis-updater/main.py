import sys
import time

import psycopg2
from get_api_data import get_data

POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 60
ENTITIES_PER_ITERATION = int(sys.argv[2]) if len(sys.argv) >= 3 else 10

connection_rel = psycopg2.connect(user="is",
                              password="is",
                              host="db-rel",
                              database="is")

def get_cities_without_coordinates(entities_per_iteration):
    with connection_rel.cursor() as cur:
        cur.execute(f'select id, name, country, state_province from city where city_coordinates is null limit {entities_per_iteration}')
        result = cur.fetchall()
    return result

if __name__ == "__main__":

    while True:
        print(f"Getting up to {ENTITIES_PER_ITERATION} entities without coordinates..")
        # !TODO: 1- Use api-gis to retrieve a fixed amount of entities without coordinates (e.g. 100 entities per iteration, use ENTITIES_PER_ITERATION)
        data = get_cities_without_coordinates(ENTITIES_PER_ITERATION)
        # !TODO: 2- Use the entity information to retrieve coordinates from an external API
        coordinates = {}
        for i in range(len(data)):
            api_data = get_data(data[i][1], data[i][3], data[i][2])
            if len(api_data) > 0:
                coordinates[data[i][0]] = [api_data[0]['lon'], api_data[0]['lat']]
        # !TODO: 3- Submit the changes
        with connection_rel.cursor() as cursor:
            for key in coordinates.keys():
                cursor.execute(f"update city set city_coordinates = ST_GeomFromText('POINT({coordinates[key][1]} {coordinates[key][0]})', 4326) where id = {key}")
                connection_rel.commit()
        time.sleep(POLLING_FREQ)
