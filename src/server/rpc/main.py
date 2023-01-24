import signal, sys
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from functions.execute_queries import execute_queries
from functions.queries import *


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


with SimpleXMLRPCServer(('0.0.0.0', 9000), requestHandler=RequestHandler, allow_none=True) as server:
    server.register_introspection_functions()


    def signal_handler(signum, frame):
        print("received signal")
        server.server_close()

        # perform clean up, etc. here...

        print("exiting, gracefully")
        sys.exit(0)


    # signals
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGHUP, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # register functions
    server.register_function(execute_queries)
    server.register_function(list_stores)
    server.register_function(list_countries_stores)
    server.register_function(list_ownership_stores)
    server.register_function(list_portuguese_cities_stores)
    server.register_function(list_stores_contacts)
    server.register_function(list_cities)
    server.register_function(list_stores_cities)

    # start the server
    print("Starting the RPC Server...")
    server.serve_forever()
