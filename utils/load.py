import os
import sqlalchemy
import pandas as pd
from sqlalchemy import Table, Column, String, MetaData, create_engine
from sqlalchemy.orm import sessionmaker
import logging

# Logger initialization
logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.DEBUG)

# Env variables
# from dotenv import load_dotenv

# Recover env variables
# load_dotenv()

# Database Location
# DATABASE_LOCATION = os.getenv('DATABASE_LOCATION')
DATABASE_LOCATION = f"sqlite:///{os.path.join(os.getcwd(), 'spotify_data.db')}"
logging.info(f'Database location: {DATABASE_LOCATION}')


def load_data(song_df: pd.DataFrame):
    """
    Function that allows loading data into the database
    """
    # Create the database engine
    engine = create_engine(DATABASE_LOCATION)

    # Create a metadata object
    meta = MetaData()

    # Define the table structure
    my_played_tracks = Table(
        'my_played_tracks',
        meta,
        Column('song_name', String),
        Column('artist_name', String),
        Column('played_at', String, primary_key=True),
        Column('timestamp', String)
    )

    # Create the table if it doesn't exist
    meta.create_all(engine)

    try:
        # Load the data into the database
        song_df.to_sql('my_played_tracks', engine, index=False, if_exists='append')
        logging.info('Data loaded successfully')
    except Exception as e:
        logging.error(f'Error loading data into the database: {e}')

    logging.info('Database connection closed successfully')


if __name__ == '__main__':
    # Example usage
    example_data = {
        'song_name': ['Song1', 'Song2'],
        'artist_name': ['Artist1', 'Artist2'],
        'played_at': ['2024-12-24T10:00:00Z', '2024-12-24T11:00:00Z'],
        'timestamp': ['2024-12-24', '2024-12-24']
    }
    song_df = pd.DataFrame(example_data)
    load_data(song_df)