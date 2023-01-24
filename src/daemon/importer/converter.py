import csv
from xml.etree.ElementTree import SubElement, ElementTree, Element


def convert_to_xml(in_path, out_path):
    with open(in_path) as f:
        csv_f = csv.DictReader(f)
        data = []
        citiesDic = {}

        root = Element('Dataset')

        # Write data into the ET
        for num, row in enumerate(csv_f):
            if num == 5000:
                break
            store = SubElement(root, 'Store', {
                'number': row['Store Number']
            })

            brand = SubElement(store, 'Brand')
            brand.text = row['Brand']

            store_name = SubElement(store, 'Store_name')
            store_name.text = row['Store Name']

            ownership = SubElement(store, 'Ownership_type')
            ownership.text = row['Ownership Type']

            address = SubElement(store, 'Address')

            street = SubElement(address, 'Street')
            street.text = row['Street Address']

            city_name = row['City']

            if city_name not in citiesDic:
                citiesDic[city_name] = {
                    'id': len(citiesDic) + 1,
                    'country': row['Country'],
                    'state_province': row['State/Province'],
                }

            city_ref = SubElement(address, 'City', {
                'ref': str(citiesDic[city_name]['id'])
            })
            city_ref.text = city_name

            code = row['Postcode']
            if code != '':
                postcode = SubElement(address, 'Postcode')
                postcode.text = code

            pnum = row['Phone Number']
            if pnum != '':
                phone = SubElement(store, 'Phone_number')
                phone.text = pnum

            coordinates = SubElement(store, 'Coordinates', {
                'Longitude': row['Longitude'],
                'Latitude': row['Latitude']
            })

        # Write cities into the ET
        cities = SubElement(root, 'Cities')
        for city_name, data in citiesDic.items():
            city = SubElement(cities, 'City', {
                'id': str(data['id']),
            })

            name = SubElement(city, 'Name')
            name.text = city_name

            country = SubElement(city, 'Country')
            country.text = data['country']

            state = SubElement(city, 'State_Province')
            state.text = data['state_province']

            SubElement(city, 'City_coordinates', {
                'Longitude': '0',
                'Latitude': '0'
            })

        # Write to output.xml
        et = ElementTree(root)
        et.write(f'{out_path}')