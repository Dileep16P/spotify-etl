# `Spotify-etl`

In the following repo, you will find a simple ETL process, using different kinds of tools, but basically, `Python`.

The goal is download yesterday's data from Spotify, check if the validation process is approved and finally, load the information needed into the database.

# `ETL` Concept
**Extract**, **Transform** and **Load** it's the process that allows to move data from multiple sources, clean them and load them into a SQL database, that could be used into a Data warehouse.

# Spotify API
Here we will use the Spotify API. You will need to grab you `USER-ID` and generate a `TOKEN` in order to use it. 

To Activate TOKEN , Please follow below steps:

To create an app on Spotify and get the `client_id`, `client_secret`, and set up redirect URIs, follow these steps:

1. **Create a Spotify Developer Account**:
   - Go to the [Spotify for Developers](https://developer.spotify.com/) website.
   - Click on "Log in" and use your Spotify credentials to log in.

2. **Create a New App**:
   - Once logged in, click on "Create an App" on the dashboard.
   - Fill in the required fields such as App Name and App Description.
   - Check the box for "Developer Terms of Service" and click "CREATE".

3. **Get Client ID and Client Secret**:
   - After creating the app, you will be redirected to the app overview page.
   - Here, you will find your **Client ID** and **Client Secret**.
   - Make sure to keep your Client Secret secure and never share it publicly.

4. **Set Up Redirect URIs**:
   - Click on "Edit Settings" on the app overview page.
   - In the "Redirect URIs" field, add the URI where Spotify should redirect after authentication.
   - For development purposes, you can use `http://localhost:5000/callback`.
   - Click "SAVE" to update your settings.

5. **Use the Client ID and Secret in Your Application**:
   - Use the Client ID and Client Secret to authenticate your application with Spotify's API.
   - Ensure your application handles the redirect URI correctly to complete the authentication flow.


# Installation steps

With pip, you can follow this steps:
1. Install the requirements with `pip install -r requirements.txt`
2.Configure below details in config.ini
[SPOTIFY]
CLIENT_ID = 
CLIENT_SECRET = 
REDIRECT_URI = http://localhost:5000/callback
SCOPE = user-library-read playlist-read-private user-read-recently-played

3.Then, you can execute your code with `python3 main.py`

4.Check your database file using SQLite viewer.

Python version: `3.9.5`
SQL Lite: 3.47.2
SQL Lite Web Viewer: 3.13.1
