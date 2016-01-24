#!/usr/bin/env python3

import configparser
import dropbox;
import sys, os
import notify2

APP_KEY = os.getenv('DROPBOX_API_KEY')
APP_SECRET = os.getenv('DROPBOX_API_SECRET')

CONFIG = os.getenv('HOME') + '/.dropshare.conf'

def get_token():
    if not os.path.exists(CONFIG):
        return None

    config = configparser.ConfigParser()
    config.read(CONFIG)

    return config.get('auth', 'access_token')


def write_config(access_token, user_id):
    config = configparser.ConfigParser()
    config.add_section('auth')
    config.set('auth', 'access_token', access_token)
    config.set('auth', 'user_id', user_id)
    with open(CONFIG, 'w') as configfile:
        config.write(configfile)


def authorize():
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)
    authorize_url = flow.start()
    print('1. Go to: ' + authorize_url)
    print('2. Click "Allow" (you might have to log in first)')
    print('3. Copy the authorization code.')

    code = input('Auth token: ').strip()
    return flow.finish(code)


def notify(title, message, type='dialog-information'):
    notify2.init('dropshare')
    notify2.Notification(title, message, type).show()

if __name__ == '__main__':
    try:
        token = get_token()
        if not token:
            try:
                access_token, user_id = authorize()
                write_config(access_token, user_id)
            except dropbox.rest.ErrorResponse as e:
                print("FAILED: " + str(e.body))
        else:
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

            import pyperclip
            pyperclip.copy(link)
            notify('Shared!', 'File "' + file + '" has been shared: ' + link, 'dialog-success')
            print('Shared: ' + link)
    except BaseException as e:
        notify('Error', str(e), 'dialog-error')
        print('Error')
        print(str(e))
