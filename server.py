from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from queue import Queue

host = 'localhost'
port = 9080
path = '/server'

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = (path,)

server = SimpleXMLRPCServer((host, port),
                            requestHandler=RequestHandler)

queue = Queue()

def PutWork(url, search, max_depth, current_depth='0'):
    work = url + "|" + search + "|" + str(max_depth) + "|" + current_depth
    queue.put(work)
    print(f'Work {work} received')
    print(f'Queue size: {queue.qsize()}')
    return 'Trabajo recibido'

def GetWork():
    print(f'Queue size: {queue.qsize()}')
    if queue.empty():
        return 'Empty'
    el = queue.get(False, 1)

    # temporary
    queue.put(el)
    # temporary
    return el

server.register_function(PutWork)
server.register_function(GetWork)
print(f'Server started at {host}:{port}{path}')
print(f'Queue size: {queue.qsize()}')
server.serve_forever()
