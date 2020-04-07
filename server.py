import asyncio, socket
import os
import re

from aiofile import AIOFile
from async_lru import alru_cache

PORT = 8000
CHUNK_LIMIT = 50
RESPONSE = 'HTTP/1.1 {status} {status_msg}\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Encoding: UTF-8\r\nAccept-Ranges: bytes\r\nConnection: closed\r\n\r\n{html}'
STATIC_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'static'
)


def url_to_path(url):
    if url in ('/index.html', '/'):
        path = 'index.html'
    else:
        path = re.sub(r'(^/)(.+)(/$)', r'\2', url)

    return path


def parse_request(request_str):
    part_one, part_two = request_str.split('\r\n\r\n')
    http_lines = part_one.split('\r\n')
    method, url, _ = http_lines[0].split(' ')
    # TODO: catch this with exception
    if method != 'GET':
        status, status_msg = 405, 'Not allowed'
    else:
        status, status_msg = 200, 'OK'

    return status, status_msg, url


@alru_cache(maxsize=512)
async def load_response(path):
    try:
        async with AIOFile(f"{STATIC_DIR}/{path}", 'r') as afp:
            html = await afp.read()
    except FileNotFoundError:
        async with AIOFile(f"{STATIC_DIR}/not_found.html", 'r') as afp:
            html = await afp.read()

    return html


async def build_response(request):
    status, status_msg, url = parse_request(request)
    html = await load_response(url_to_path(url))
    response = RESPONSE.format(
        status=status,
        status_msg=status_msg,
        html=html
    ).encode('utf-8')

    return response


async def read_request(client):
    request = ''
    while True:
        chunk = (await loop.sock_recv(client, CHUNK_LIMIT)).decode('utf8')
        request += chunk
        if len(chunk) < CHUNK_LIMIT:
            break

    return request


async def handle_client(client):
    request = await read_request(client)
    response = await build_response(request)
    await loop.sock_sendall(client, response)
    client.close()


async def run_server(selected_server):
    while True:
        client, _ = await loop.sock_accept(selected_server)
        loop.create_task(handle_client(client))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', PORT))
server.listen(1)
server.setblocking(False)

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(run_server(server))
except KeyboardInterrupt:
    server.close()
