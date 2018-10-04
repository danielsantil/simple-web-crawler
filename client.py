from xmlrpc import client
from urllib import request

print('**Buscador PUCMM**')

def valid_url(url):
    try:
        request.urlopen(url)
        return True
    except:
        return False

url = input('URL: ')
while not valid_url(url):
    url = input('URL: ')
max_depth = int(input('Profundidad: ') or  0)
search = 'PUCMM'

server = client.ServerProxy('http://localhost:9080/server')
response = server.PutWork(url, search, max_depth)
print(response)