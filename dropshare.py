#!/usr/bin/env python3
import configparser
from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import threading
from PyQt5.QtCore import QUrl, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
import atexit
import dropbox
import sys, os
import notify2

APP_KEY = 'cyuugboyrbyqx8t'
CONFIG = os.getenv('HOME') + '/.dropshare.conf'

def write_config(params):
    config = configparser.ConfigParser()
    config.add_section('auth')
    config.set('auth', 'access_token', params['access_token'])
    config.set('auth', 'user_id', params['uid'])
    with open(CONFIG, 'w') as configfile:
        config.write(configfile)

def get_token():
    if not os.path.exists(CONFIG):
        return None

    config = configparser.ConfigParser()
    config.read(CONFIG)

    return config.get('auth', 'access_token')

def notify(title, message, type='dialog-information'):
    notify2.init('dropshare')
    notify2.Notification(title, message, type).show()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200, 'OK')
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Connected!')

class AuthWindow(QMainWindow):
    def __init__(self, server):
        QMainWindow.__init__(self)
        self.initUI()
        self.server = server

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
            self.server.kill()
            self.close()

def http_server():
    server = HTTPServer(('localhost', 30000), RequestHandler)
    server.serve_forever()

    atexit.register(lambda : (
        print ('Stop server'),
        server.shutdown()
    ))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        notify('Error', 'No file to share')
        print('No file to share')
        sys.exit()

    if sys.argv[1] == 'server':
        print('Started server')
        thread = threading.Thread(target=http_server)
        thread.start()
    elif sys.argv[1] == 'auth':
        def on_exit():
            process.kill()

        print('Spawning server')
        process = subprocess.Popen([sys.argv[0], 'server'])
        print('Server pid: %d' % process.pid)

        app = QApplication(sys.argv)
        app.aboutToQuit.connect(on_exit)
        window = AuthWindow(process)
        window.show()

        sys.exit(app.exec_())
    else:
        token = get_token()
        if not token:
            process = subprocess.Popen([sys.argv[0], 'auth'])
            process.wait()
            token = get_token()
            if not token:
                print('Token still not provided. Exit')
                sys.exit()

        file = sys.argv[1]
        if not os.path.exists(file):
            message = 'dropshare: file does not exist: ' + file
            notify('Error', message, 'dialog-error')
            print(message)
            sys.exit(1)

        share_path = '/' + os.path.basename(file)
        client = dropbox.Dropbox(token)
        handle = open(file, 'rb')
        response = client.files_upload(handle, share_path)
        link = client.sharing_create_shared_link(share_path, True).url

        p = subprocess.Popen(['xclip', '-selection', 'c'], stdin=subprocess.PIPE, close_fds=True)
        p.communicate(input=link.encode('utf-8'))

        notify('Shared!', 'File "' + file + '" has been shared: ' + link, 'dialog-success')
        print('Shared: ' + link)
        sys.exit()