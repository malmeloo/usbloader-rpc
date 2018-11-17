import logging
import sys
import time
import threading
import socket
import requests
from pypresence import Presence
from flask import Flask, request
import bs4

CLIENT_ID = '509746785447706624'

RPC = Presence(CLIENT_ID)
app = Flask(__name__)

flask_log = logging.getLogger('werkzeug')
flask_log.disabled = True
app.logger.disabled = True

logging.basicConfig(level=logging.INFO)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IP = s.getsockname()[0]
    s.close()
except OSError:
    logger.warning('No internet connection available!\
    Please connect to a network and try again.')
    sys.exit()


class Tasks:
    """Performs various tasks to set everything up"""
    @staticmethod
    def check_connection():
        """Checks the connection to the GameTDB website"""
        print('Checking connection to GameTDB...', end='')

        url = 'https://gametdb.com'
        r = requests.get(url)
        r.raise_for_status()

    @staticmethod
    def connect():
        """Init the connection to discord"""
        print('Connecting to Discord...', end='')

        RPC.connect()

    @staticmethod
    def create_config():
        """Creates the config file for USB Loader GX"""
        print('Creating Wiinnertag.xml...', end='')

        with open('Wiinnertag.xml', 'w+') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write(f'<Tag URL="http://{IP}/wiinnertag?game_id={{ID6}}" Key="1234567890"/>')

    @staticmethod
    def start_server():
        """Starts the Flask web server to handle incoming requests"""
        print(f'Starting web server at {IP}...', end='')

        # app.run() is blocking so we're running it in a thread
        def delay_start():
            time.sleep(0.5)
            app.run(host='0.0.0.0', port='80', debug=False)

        thread = threading.Thread(target=delay_start)
        thread.start()


def get_game_name(game_id):
    """Retrieves a game's name by title ID using gametdb"""
    url = f'https://www.gametdb.com/Wii/{game_id.upper()}'
    r = requests.get(url)

    if not r.status_code == 200:
        logger.warning('Could not resolve game name!')
        return game_id

    soup = bs4.BeautifulSoup(r.text)
    table = soup.find('table', {'class': 'DQedit'})
    cols = table.find_all('tr')

    for c in cols:
        fields = c.find_all('td')
        if fields[0].text.startswith('title'):
            # finds first game name listed, prioritizes english
            return fields[1].text
    return game_id


@app.route('/submit', methods=['GET'])
def submit():
    game_id = request.args.get('game_id')
    logging.info(f'Game started with ID: {game_id}')

    game = get_game_name(game_id)
    usb_loader = request.headers.get('User-Agent')
    started = int(time.time())

    logging.info(f'{usb_loader} - {game}')

    payload = {
        'state': usb_loader,
        'details': game,
        'start': started,
        'large_image': 'wii_console',
        'large_text': 'Nintendo Wii',
    }
    RPC.update(**payload)

    logging.info('Successfully set presence')
    print('------------------------------------------')

    return 'Hello there! If you\'re reading this for whatever reason, \
           I hope you\'re having a nice day! :)'


def main():
    tasks = ['check_connection', 'connect', 'create_config', 'start_server']

    for t in tasks:
        task = getattr(Tasks, t)
        try:
            task()
            print('Success!')
        except Exception as e:
            # TODO: print detailed message describing the error
            print('Failed!')
            sys.exit()

    print('------------------------------------------')
    time.sleep(1)  # letting flask boot up
    print('------- Ready to receive requests! -------')


if __name__ == '__main__':
    main()
