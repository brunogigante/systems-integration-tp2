import sys

import psycopg2
from flask import Flask, request

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
app.config["DEBUG"] = True

connection_rel = psycopg2.connect(user="is",
                              password="is",
                              host="db-rel",
                              database="is")

@app.route('/api/markers', methods=['GET'])
def get_markers():
    with connection_rel.cursor() as cursor:
        cursor.execute(f'select id, name, ST_AsText(ST_Point(ST_X(city_coordinates), ST_Y(city_coordinates))) from city where city_coordinates is not null;')
        cities = cursor.fetchall()

    result = []
    for i in range(len(cities)):
        with connection_rel.cursor() as cursor:
            cursor.execute(f"SELECT jsonb_build_object( 'type', 'feature', 'imgUrl', 'https://w7.pngwing.com/pngs/633/366/png-transparent-starbucks.png',"
                           f" 'id', id, 'geometry', ST_AsGeoJSON(geom)::jsonb, 'properties', to_jsonb( t.* ) - 'id' - 'geom')"
                           f" AS json FROM (VALUES ({cities[i][0]}, '{cities[i][1]}', '{cities[i][2]}'::geometry))"
                           f" AS t(id, name, geom);")
            result.append(cursor.fetchall())

    return result


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
