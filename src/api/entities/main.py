import sys

import psycopg2
from flask import Flask, jsonify, request

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

# set of all teams
# !TODO: replace by database access
connection_rel = psycopg2.connect(user="is",
                              password="is",
                              host="db-rel",
                              database="is")

connection_xml = psycopg2.connect(user="is",
                              password="is",
                              host="db-xml",
                              database="is")

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/cities_xml/<path:file>', methods=['GET'])
def get_cities_xml(file):
    file_name = str(file)
    with connection_xml.cursor() as cursor:
        cursor.execute(f"""SELECT unnest(xpath('/Dataset/Cities/City//@id', xml))::text as city_id,
            unnest(xpath('/Dataset/Cities/City/Name/text()', xml))::text as city_name,
            unnest(xpath('/Dataset/Cities/City/Country/text()', xml))::text as city_country,
            unnest(xpath('/Dataset/Cities/City/State_Province/text()', xml))::text as city_state
            FROM imported_documents
            WHERE is_deleted = false AND file_name = concat('/','{file_name}');""")
        result = cursor.fetchall()
    return jsonify(result)

@app.route('/api/stores_xml/<path:file>', methods=['GET'])
def get_stores_xml(file):
    file_name = str(file)
    with connection_xml.cursor() as cursor:
        cursor.execute(f"""SELECT unnest(xpath('/Dataset/Store//@number', xml))::text as store_number,
            unnest(xpath('/Dataset/Store/Brand/text()', xml))::text as brand,
            unnest(xpath('/Dataset/Store/Store_name/text()', xml))::text as store_name,
            unnest(xpath('/Dataset/Store/Ownership_type/text()', xml))::text as ownership,
            unnest(xpath('/Dataset/Store/Address/Street/text()', xml))::text as street,
            unnest(xpath('/Dataset/Store/Address/City//@ref', xml))::text as city_ref,
            unnest(xpath('/Dataset/Store/Address/City/text()', xml))::text as city_name,
            unnest(xpath('/Dataset/Store/Address/Postcode/text()', xml))::text as postcode,
            unnest(xpath('/Dataset/Store/Phone_number/text()', xml))::text as phone,
            point(unnest(xpath('/Dataset/Store/Coordinates//@Longitude', xml))::text::float, 
            unnest(xpath('/Dataset/Store/Coordinates//@Latitude', xml))::text::float) as coordinates
            FROM imported_documents
            WHERE is_deleted = false AND file_name = concat('/','{file_name}');""")
        result = cursor.fetchall()
    return jsonify(result)

@app.route('/api/cities/', methods=['POST'])
def set_cities():
    data = {}
    cities = request.get_json()
    var_names = ["ids", "names", "countries", "states"]
    for i in range(len(var_names)):
        data[var_names[i]] = list(map(lambda x: x[i], cities))

    data_to_insert = tuple(zip(data['ids'], data['names'], data['countries'], data['states']))

    with connection_rel.cursor() as cursor:
        cursor.executemany("""insert into city (id, name, country, state_province)
    values (%s,%s,%s,%s)""", data_to_insert)
    connection_rel.commit()
    return jsonify(data_to_insert), 201

@app.route('/api/stores/', methods=['POST'])
def set_stores():
    data = {}
    stores = request.get_json()
    var_names = ["numbers", "brands", "store_names", "ownerships", "streets", "city_refs", "city_names", "postcodes",
                 "phone_numbers", "coordinates"]

    for i in range(len(var_names)):
        data[var_names[i]] = list(map(lambda x: x[i], stores))

    data_to_insert = tuple(zip(data['numbers'], data['brands'], data['ownerships'], data['store_names'], data['streets'],
            data['city_refs'], data['city_names'], data['postcodes'], data['phone_numbers'], data['coordinates']))

    with connection_rel.cursor() as cursor:
        cursor.executemany(f"""insert into store (number, brand, ownership_type, store_name, street, city_ref, city_name, postcode, phone_number, store_coordinates)
        values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", data_to_insert)
    connection_rel.commit()
    return jsonify(data_to_insert), 201

@app.route('/api/stores/', methods=['GET'])
def get_stores():
    with connection_rel.cursor() as cursor:
        cursor.execute("""select * from store""")
        result = cursor.fetchall()
    return jsonify(result)

@app.route('/api/cities/', methods=['GET'])
def get_cities():
    with connection_rel.cursor() as cursor:
        cursor.execute("""select * from city""")
        result = cursor.fetchall()
    return jsonify(result)

@app.route('/api/stores/<store_number>', methods=['GET'])
def get_stores_by_number(store_number):
    with connection_rel.cursor() as cursor:
        cursor.execute(f"""select * from store where id = {store_number}""")
        result = cursor.fetchall()
    return jsonify(result)

@app.route('/api/cities/<city_id>', methods=['GET'])
def get_cities_by_id(city_id):
    with connection_rel.cursor() as cursor:
        cursor.execute(f"""select * from city where id = {city_id}""")
        result = cursor.fetchall()
    return jsonify(result)

@app.route('/api/stores/', methods=['PUT'])
def update_stores():
    data = request.get_json()
    for i in range(len(data)):
        if not data[i]:
            return 400
    with connection_rel.cursor() as cursor:
        cursor.execute(f"""update store set number={data[1]}, brand={data[2]}, ownership_type={data[3]}, store_name={data[4]}, street={data[5]}, postcode={data[6]}, phone_number={data[7]}
        where id = {data[0]}""")
    return 200

@app.route('/api/cities/', methods=['PUT'])
def update_cities():
    data = request.get_json()
    for i in range(len(data)):
        if not data[i]:
            return 400
    with connection_rel.cursor() as cursor:
        cursor.execute(f"""update city set name={data[1]}, country={data[2]}, state_province={data[3]}
        where id = {data[0]}""")
    return 200

@app.route('/api/stores/<store_id>', methods=['DELETE'])
def delete_stores(store_id):
    with connection_rel.cursor() as cursor:
        cursor.execute(f"""delete from store where id = {store_id}""")
    return 200
@app.route('/api/cities/<city_id>', methods=['DELETE'])
def delete_cities(city_id):
    with connection_rel.cursor() as cursor:
        cursor.execute(f"""delete from city where id = {city_id}""")
    return 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
