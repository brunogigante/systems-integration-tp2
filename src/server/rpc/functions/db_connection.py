import psycopg2

def db_xml_connection():
    connection = psycopg2.connect(user="is",
                                  password="is",
                                  host="db-xml",
                                  database="is")

    return connection
