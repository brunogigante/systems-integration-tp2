import asyncio
import time
import uuid
import psycopg2

import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent
from converter import convert_to_xml
from db_connection import db_xml_connection


def get_csv_files_in_input_folder():
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(CSV_INPUT_PATH) for f in filenames if
            os.path.splitext(f)[1] == '.csv']


def generate_unique_file_name(directory):
    return f"{directory}/{str(uuid.uuid4())}.xml"


def convert_csv_to_xml(in_path, out_path):
    convert_to_xml(in_path, out_path)


class CSVHandler(FileSystemEventHandler):

    def __init__(self, input_path, output_path, connection):
        self._output_path = output_path
        self._input_path = input_path
        self._connection = connection

        # generate file creation events for existing files
        for file in [os.path.join(dp, f) for dp, dn, filenames in os.walk(input_path) for f in filenames]:
            event = FileCreatedEvent(os.path.join(CSV_INPUT_PATH, file))
            event.event_type = "created"
            self.dispatch(event)

    async def convert_csv(self, csv_path):
        # here we avoid converting the same file again
        # !TODO: check converted files in the database
        if csv_path in await self.get_converted_files():
            print("Already exists")
            return

        print(f"new file to convert: '{csv_path}'")

        # we generate a unique file name for the XML file
        xml_path = generate_unique_file_name(self._output_path)

        # we do the conversion
        convert_csv_to_xml(csv_path, xml_path)
        print(f"new xml file generated: '{xml_path}'")

        # !TODO: once the conversion is done, we should updated the converted_documents tables
        with self._connection.cursor() as cursor:
            cursor.execute('insert into converted_documents (src, file_size, dst) values (%s, %s, %s)',
                           (csv_path, os.path.getsize(csv_path), xml_path))
            self._connection.commit()

        # !TODO: we should store the XML document into the imported_documents table
        with self._connection.cursor() as cursor:
            with open(xml_path) as f:
                file_data = f.read()
                cursor.execute('insert into imported_documents (file_name, xml, is_deleted) values (%s, %s, false)',
                               (xml_path, file_data))
                self._connection.commit()

    async def get_converted_files(self):
        with self._connection.cursor() as cursor:
            cursor.execute('select src from converted_documents')
            result = cursor.fetchall()
            return map(lambda x: x[0], result)


    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".csv"):
            asyncio.run(self.convert_csv(event.src_path))


if __name__ == "__main__":

    CSV_INPUT_PATH = "/csv"
    XML_OUTPUT_PATH = "/shared/output"
    CONNECTION = db_xml_connection()

    # create the file observer
    observer = Observer()
    observer.schedule(
        CSVHandler(CSV_INPUT_PATH, XML_OUTPUT_PATH, CONNECTION),
        path=CSV_INPUT_PATH,
        recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
