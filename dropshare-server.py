#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from dropshare import RequestHandler

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200, 'OK')
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Connected!')

server = HTTPServer(('localhost', 30000), RequestHandler)
server.serve_forever()

