from urllib import parse, request
import json

def get_data(city, state, country):
    params = parse.urlencode({
        'state': state,
        'country': country,
        'city': city,
        'format': 'jsonv2'
    })
    with request.urlopen(f'https://nominatim.openstreetmap.org/search?{params}') as req:
        data = json.loads(req.read())
        return data
