import sys
import xmlrpc.client

from flask import Flask

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
app.config["DEBUG"] = True

server = xmlrpc.client.ServerProxy('http://rpc-server:9000')

@app.route('/api/stores/', methods=['GET'])
def get_stores():
    result = server.execute_queries(server.list_stores())
    return result

@app.route('/api/countries_stores/', methods=['GET'])
def get_countries_stores():
    result = server.execute_queries(server.list_countries_stores())
    return result

@app.route('/api/ownership_stores/', methods=['GET'])
def get_ownership_stores():
    result = server.execute_queries(server.list_ownership_stores())
    return result

@app.route('/api/portuguese_cities_stores/', methods=['GET'])
def get_portuguese_cities_stores():
    result = server.execute_queries(server.list_portuguese_cities_stores())
    return result

@app.route('/api/stores_contacts/', methods=['GET'])
def get_stores_contacts():
    result = server.execute_queries(server.list_stores_contacts())
    return result

@app.route('/api/stores_cities/<city>', methods=['GET'])
def get_stores_cities(city):
    result = server.execute_queries(server.list_stores_cities(city))
    return result

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
