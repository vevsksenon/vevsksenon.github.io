#!/usr/bin/env python3
import base64
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8090
TIMEOUT = 30
IP_PREFIX = re.compile(r'^ip[0-9a-fA-F.:]*/')
HOP = ('content-type', 'content-length', 'content-range', 'accept-ranges')


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
    return parts.scheme in ('http', 'https') and bool(parts.hostname)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS')
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

    def upstream_headers(self, headers):
        upstream = {}
        client_xhr = self.headers.get('X-Requested-With')
        if client_xhr:
            upstream['X-Requested-With'] = client_xhr
        upstream.update(headers)
        if not any(name.lower() == 'user-agent' for name in upstream):
            upstream['User-Agent'] = 'Mozilla/5.0'
        range_header = self.headers.get('Range')
        if range_header:
            upstream['Range'] = range_header
        return upstream

    def do_GET(self):
        try:
            url, headers = parse(self.path.lstrip('/'))
        except (ValueError, UnicodeDecodeError, IndexError):
            return self.reply(400, b'Malformed proxy path')
        parts = urllib.parse.urlsplit(url)
        if 'filmix' in (parts.hostname or '') and not any(name.lower() == 'x-requested-with' for name in headers):
            headers['X-Requested-With'] = 'XMLHttpRequest'
        if not is_allowed(url):
            return self.reply(403, b'Only http and https URLs are allowed')
        request = urllib.request.Request(url, headers=self.upstream_headers(headers))
        try:
            response = urllib.request.urlopen(request, timeout=TIMEOUT)
        except urllib.error.HTTPError as error:
            return self.reply(error.code, error.read(), error.headers.get('Content-Type', 'text/plain'))
        except Exception as error:
            return self.reply(502, str(error).encode('utf-8'))
        try:
            self.send_response(response.status)
            self.cors()
            self.send_header('Accept-Ranges', 'bytes')
            for name in HOP:
                value = response.headers.get(name)
                if value and name != 'accept-ranges':
                    self.send_header(name, value)
            self.end_headers()
            while True:
                chunk = response.read(64 * 1024)
                if not chunk:
                    break
                self.wfile.write(chunk)
        except (BrokenPipeError, ConnectionResetError):
            pass
        finally:
            response.close()


ThreadingHTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
