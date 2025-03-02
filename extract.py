import mysql.connector
from sqlalchemy import create_engine
import os
import pandas as pd
import requests
import datetime
from datetime import timedelta
import logging
from configparser import ConfigParser
from spotipy.oauth2 import SpotifyOAuth

# Logger initialization
logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.DEBUG)

# Read config.ini file
config = ConfigParser()
config.read('C:/Users/dilee/Downloads/spotify_etl-20250127T140840Z-001/spotify_etl/utils/config.ini')

# Spotify credentials from config.ini
CLIENT_ID = config.get('SPOTIFY', 'CLIENT_ID')
CLIENT_SECRET = config.get('SPOTIFY', 'CLIENT_SECRET')
REDIRECT_URI = config.get('SPOTIFY', 'REDIRECT_URI')
SCOPE = config.get('SPOTIFY', 'SCOPE')

# Initialize Spotipy OAuth
sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPE)

# MySQL Database connection details
DB_USER = 'dileep_pothula'
DB_PASSWORD = '1999'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'spotify_db'


def get_token():
    """
    Function to retrieve or refresh the Spotify API token.
    """
    token_info = sp_oauth.get_cached_token()

    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        print(f'Please navigate to {auth_url} and authorize access, then paste the URL you are redirected to here:')
        response = input('Enter the URL: ')
        code = sp_oauth.parse_response_code(response)
        token_info = sp_oauth.get_access_token(code)

    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info['access_token']


def extract_data():
    """
    Extracts recently played tracks from Spotify and stores them in MySQL.
    """
    try:
        # Get token
        token = get_token()

        # Prepare the headers
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        # Perform the request
        r = requests.get("https://api.spotify.com/v1/me/player/recently-played", headers=headers)
        r.raise_for_status()  # Raises an error if request fails

        # Grab the data
        data = r.json()

        # The fields we are looking for
        song_names = []
        artist_names = []
        played_at_list = []
        timestamps = []

        # Calculate the period for the last 60 days
        today = datetime.datetime.now()
        last_60_days = today - timedelta(days=60)

        # Loop through each song to get the info we want
        for song in data.get('items', []):
            # Check if the song was played in the last 60 days
            if song['played_at'][0:10] >= last_60_days.strftime('%Y-%m-%d'):
                song_names.append(song['track']['name'])
                artist_names.append(", ".join([artist['name'] for artist in song['track']['artists']]))
                played_at_list.append(song['played_at'])
                timestamps.append(song['played_at'][0:10])

        # Create the dict in order to create the pandas dataframe
        song_dict = {
            'song_name': song_names,
            'artist_name': artist_names,
            'played_at': played_at_list,
            'timestamp': timestamps
        }

        # Songs dataframe
        song_df = pd.DataFrame(song_dict, columns=['song_name', 'artist_name', 'played_at', 'timestamp'])

        logging.info(song_df)

        # Save DataFrame to MySQL
        engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        song_df.to_sql(name="spotify_tracks", con=engine, if_exists="replace", index=False)

        logging.info("✅ Data successfully stored in MySQL database.")
        return song_df

    except requests.exceptions.RequestException as req_err:
        logging.error(f"⚠️ Request error: {req_err}")
    except mysql.connector.Error as db_err:
        logging.error(f"❌ MySQL error: {db_err}")
    except Exception as e:
        logging.error(f"🔥 An unexpected error occurred: {e}")


if __name__ == '__main__':
    extract_data()
