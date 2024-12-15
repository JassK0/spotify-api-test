import os
from dotenv import load_dotenv
from requests import get
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask, request, render_template

# Load environment variables
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Set up Spotipy with client credentials
sp = Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))


#setup for flask
app = Flask(__name__)



# Search for an artist
def search_for_artist(artist_name):
    results = sp.search(q=f"artist:{artist_name}", type="artist", limit=1)
    items = results["artists"]["items"]
    if not items:
        print("No artist with this name exists...")
        return None
    return items[0]

# Get top songs for an artist
def get_songs_by_artist(artist_id, top_choice):
    results = sp.artist_top_tracks(artist_id, country="US")
    return results["tracks"][:top_choice]

@app.route("/", methods=["GET", "POST"])
def home():
    
    songs = []
    artist_name = ""
    error_message = ""
    
    
    if request.method == "POST":
        artist_name = request.form.get("artist_name")
        top_choice = int(request.form.get("top_choice"))
        
        artist = search_for_artist(artist_name)
        
        if artist:
            songs = get_songs_by_artist(artist["id"], top_choice)
        else:
            error_message = "Artist Not Found :/"
            
    return render_template("/pages/index.html", songs=songs, artist_name=artist_name, error_message=error_message)