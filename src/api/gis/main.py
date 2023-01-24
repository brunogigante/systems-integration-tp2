import sys

import psycopg2
from flask import Flask, request
from flask_cors import CORS

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

connection_rel = psycopg2.connect(user="is",
                              password="is",
                              host="db-rel",
                              database="is")

@app.route('/api/markers', methods=['GET'])
def get_markers():
    args = request.args

    with connection_rel.cursor() as cursor:
        cursor.execute("SELECT jsonb_build_object('type', 'Feature', 'geometry', st_asgeojson(city_coordinates)::jsonb, "
                       "'properties', to_jsonb(marker_data.*) - 'geom') "
                       "AS json FROM (SELECT s.id, city.name as city, city_coordinates, s.store_name, s.number,"
                       " 'https://mcdonough.com/wp-content/uploads/2020/09/starbucks-logo-png-transparent.png' as image "
                       "FROM city INNER JOIN store s on city.id = s.city_ref "
                       "WHERE city_coordinates is not null AND city.city_coordinates && ST_MakeEnvelope(%s, %s, %s, %s, 4326)) "
                       "AS marker_data(id, city, city_coordinates, store, number, image)",
                       [args['neLat'], args['neLng'], args['swLat'], args['swLng']])

        result = cursor.fetchall()

    return result

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
