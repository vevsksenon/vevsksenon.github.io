#!/usr/bin/env python3
import base64
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8090
TIMEOUT = 20
IP_PREFIX = re.compile(r'^ip[0-9a-fA-F.:]*/')


def b64decode(value):
    value = urllib.parse.unquote(value)
    return base64.b64decode(value + '=' * (-len(value) % 4)).decode('utf-8')


def parse(path):
    headers = {}
    while True:
        path = IP_PREFIX.sub('', path, count=1)
        if path.startswith('param/'):
            param, path = path[len('param/'):].split('/', 1)
            name, value = param.split('=', 1)
            headers[urllib.parse.unquote(name)] = urllib.parse.unquote(value)
        elif path.startswith(('enc/', 'enc1/')):
            encoded, rest = path.split('/', 2)[1:]
            path = b64decode(encoded) + rest
        elif path.startswith('enc2/'):
            path = b64decode(path.split('/', 2)[1])
        else:
            return path, headers


def is_allowed(url):
    parts = urllib.parse.urlsplit(url)
    return parts.scheme in ('http', 'https') and 'filmix' in (parts.hostname or '')


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')

    def reply(self, status, body=b'', content_type='text/plain; charset=utf-8'):
        self.send_response(status)
        self.cors()
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.reply(204)

    def do_GET(self):
        try:
            url, headers = parse(self.path.lstrip('/'))
        except (ValueError, UnicodeDecodeError):
            return self.reply(400, b'Malformed proxy path')
        if not is_allowed(url):
            return self.reply(403, b'Only filmix hosts are allowed')
        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                self.reply(response.status, response.read(), response.headers.get('Content-Type', 'application/octet-stream'))
        except urllib.error.HTTPError as error:
            self.reply(error.code, error.read(), error.headers.get('Content-Type', 'text/plain'))
        except Exception as error:
            self.reply(502, str(error).encode('utf-8'))


ThreadingHTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
