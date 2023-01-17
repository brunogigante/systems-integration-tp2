import psycopg2
from functions.db_connection import db_xml_connection


def execute_queries(query):
    connection = None
    cursor = None
    result = None

    try:
        with db_xml_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()

    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

    finally:
        cursor.close()
        connection.close()

    return result
