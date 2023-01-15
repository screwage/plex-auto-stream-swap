#!/usr/bin/python3
import sys
import os
import time
import logging
import configparser
from plexapi.server import PlexServer
from clients import clients, check_client, update_client

plex = None


def load_config(file_path):
    global plex

    config = configparser.ConfigParser(os.environ)
    if len(config.read(file_path)) == 0:
        sys.exit(f"No config file named \"{file_path}\" could be found.")

    enable_debugging = config['APP']['debug']

    # Configure Logging
    logging_level = logging.DEBUG if enable_debugging == 'True' else logging.INFO
    logging.basicConfig(level=logging_level,
                        format='[%(asctime)s][%(levelname)s] %(message)s', datefmt='%H:%M:%S %d-%m-20%y')

    # Configure Plex Connection
    plex_ip = config['PLEX']['host']
    plex_port = config['PLEX']['port']
    base_url = f'http://{plex_ip}:{plex_port}'
    try:
        plex_api_token = config['PLEX']['api_token']
    except:
        sys.exit("Missing Plex API Token. Modifiy config.ini or set environment variable PLEX_API_TOKEN.")

    plex = PlexServer(base_url, plex_api_token)
    logging.info(
        f"Connected to Plex Server at {plex_ip}:{plex_port}.")


def process_playing(data):
    global clients

    if data['type'] != 'playing':
        return

    # Get the rating key for this corresponding callback.
    # A rating key will uniquely identify an episode in the case of a show.
    data = data['PlaySessionStateNotification'][0]
    rating_key = int(data['ratingKey'])
    episode = plex.fetchItem(rating_key)

    if episode.type != 'episode':
        return

    # Whenever a new client starts watching,
    # start tracking what they're watching.
    client_id = data['clientIdentifier']
    if client_id not in clients:
        logging.info(f'Adding new client with ID {client_id}')
        update_client(client_id, rating_key, episode=episode)
        return

    check_client(client_id, rating_key, episode)


def handle_error(error):
    sys.exit('Listener ran into an error. Stopping script. Error: ' + error)

def main():
    load_config("config.ini")

    try:
        listener = plex.startAlertListener(callback=process_playing, callbackError=handle_error)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info('Shutting down Listener.')
        listener.stop()


if __name__ == '__main__':
    main()
