import json
import sys
import time

import psycopg2
from psycopg2 import OperationalError
import requests

POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 60


def print_psycopg2_exception(ex):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print("\npsycopg2 ERROR:", ex, "on line number:", line_num)
    print("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print("\nextensions.Diagnostics:", ex.diag)

    # print the pgcode and pgerror exceptions
    print("pgerror:", ex.pgerror)
    print("pgcode:", ex.pgcode, "\n")

def execute_query(query, connection):
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result

def check_db(connection):
    return execute_query("""select file_name from imported_documents where is_migrated = false""", connection)

if __name__ == "__main__":

    db_org = psycopg2.connect(host='db-xml', database='is', user='is', password='is')
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')

    while True:

        # Connect to both databases
        db_org = None
        db_dst = None

        try:
            db_org = psycopg2.connect(host='db-xml', database='is', user='is', password='is')
            db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
        except OperationalError as err:
            print_psycopg2_exception(err)

        if db_dst is None or db_org is None:
            continue

        print("Checking updates...")
        # !TODO: 1- Execute a SELECT query to check for any changes on the table
        new_files = check_db(db_org)
        # !TODO: 2- Execute a SELECT queries with xpath to retrieve the data we want to store in the relational db
        for file in new_files:
            resp_get_cities = requests.get(f"http://api-entities:8080/api/cities_xml/{file[0]}")
            resp_get_stores = requests.get(f"http://api-entities:8080/api/stores_xml/{file[0]}")
            city_data = resp_get_cities.json()
            store_data = resp_get_stores.json()
        # !TODO: 3- Execute INSERT queries in the destination db
            headers = {'Content-type': 'application/json'}
            resp_insert_cities = requests.post(f"http://api-entities:8080/api/cities/", data=json.dumps(city_data), headers=headers)
            resp_insert_stores = requests.post(f"http://api-entities:8080/api/stores/", data=json.dumps(store_data), headers=headers)
        # !TODO: 4- Make sure we store somehow in the origin database that certain records were already migrated.
        #          Change the db structure if needed.
            with db_org.cursor() as cursor:
                cursor.execute(f'update imported_documents set is_migrated = true where file_name = %s', (file[0],))
            db_org.commit()

        db_org.close()
        db_dst.close()

        time.sleep(POLLING_FREQ)
