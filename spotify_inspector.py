import os
from dotenv import load_dotenv
from flask import (Flask, 
                   session, 
                   redirect,
                   request, 
                   url_for)

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

                    
import pandas as np
from dash import (
                  Dash, 
                  html, 
                  dash_table, 
                  dcc
                  )
import plotly.graph_objects as go
import dash_cytoscape as cyto


##loading keys as environment variables
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("DEV_KEY")
client_id = "c936a7c9a80b49cea5e0e8871e641ce6"
uri = "http://localhost:5000/callback"
scope = ('playlist-read-private,'   
        'user-library-read,'
        'user-top-read,'
        'user-read-recently-played,'
        'user-follow-read'
        )

cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(client_id=client_id,
                        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
                        redirect_uri= uri,
                        cache_handler=cache_handler,
                        show_dialog= True
                        )

sp = Spotify(auth_manager = sp_oauth)

@app.route("/")  
def home():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('get_playlists'))

@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('get_playlists'))

@app.route('/get_playlists')
def get_playlists():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    playls = sp.current_user_playlists()
    playls_info = [(pl['name'], pl['external_urls']['spotify'])\
                                    for pl in playls['items']]
    playls_html = '<br>'.join([f'{name}: {url}' for name, url in playls_info])
    return playls_html

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))





# if __name__ == "__spotify_inspector__":
app.run(debug=True)




app = Dash(__name__)

