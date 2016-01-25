#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import threading
import atexit
import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi

APP_KEY = 'cyuugboyrbyqx8t'
CONFIG = os.getenv('HOME') + '/.dropshare.conf'

def write_config(params):
    config = configparser.ConfigParser()
    config.add_section('auth')
    config.set('auth', 'access_token', params['access_token'])
    config.set('auth', 'user_id', params['uid'])
    with open(CONFIG, 'w') as configfile:
        config.write(configfile)

def http_server():
    server = HTTPServer(('localhost', 30000), RequestHandler)
    server.serve_forever()

    atexit.register(lambda : (
        print ('Stop server'),
        server.shutdown()
    ))

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200, 'OK')
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write('Connected!')
        self.wfile.close()
        print('Connected')

class AuthWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        loadUi('authwindow.ui', self)
        url = QUrl('https://www.dropbox.com/1/oauth2/authorize?redirect_uri=http://localhost:30000&response_type=token&client_id=%s' % APP_KEY)
        self.webView.load(url)
        self.webView.urlChanged.connect(self.onUrlChange)

    def onUrlChange(self):
        url = self.webView.url()
        if url.host() == 'localhost':
            fragment = url.fragment()
            params = {}
            pairs = fragment.split('&')
            for pair in pairs:
                key, value = pair.split('=')
                params[key] = value
            write_config(params)
            self.close()
            self.destroy()

if __name__ == '__main__':
    def on_stop():
        thread._stop()

    thread = threading.Thread(target=http_server)
    thread.start()
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(on_stop)

    window = AuthWindow()
    window.show()
    thread._stop()
    sys.exit(app.exec_())