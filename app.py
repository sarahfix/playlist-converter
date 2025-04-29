from flask import Flask, redirect, url_for, request, render_template
import os
from spotipy import Spotify
#from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

#load_dotenv()

#set up Flask app
app = Flask(__name__)

# Spotify API credentials
CLIENT_ID = "your_spotify_client_id"
CLIENT_SECRET = "your_spotify_client_secret"
REDIRECT_URI = "http://localhost:5000/callback"

# Initialize Spotify OAuth
sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URI,
                        scope="user-library-read playlist-read-private playlist-modify-public playlist-modify-private")

@app.route('/')
def index():
    # Main page where users can either log in or paste playlist links
    return render_template('index.html')

@app.route('/login')
def login():
    # Redirect to Spotify login
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    # Handle the Spotify OAuth callback and get the access token
    token_info = sp_oauth.get_access_token(request.args['code'])
    session['token_info'] = token_info  # Store the token in the session
    return redirect(url_for('index'))

@app.route('/transfer', methods=['POST'])
def transfer_playlist():
    # Transfer playlist from Spotify to Apple Music
    spotify_url = request.form.get('spotify_playlist_url')
    # Extract playlist ID from the URL
    playlist_id = extract_playlist_id(spotify_url)

    if not playlist_id:
        return "Invalid Spotify URL", 400
    
    # Use Spotify API to fetch playlist details
    token_info = session.get('token_info')
    sp = Spotify(auth=token_info['access_token'])

    # Get playlist songs
    playlist_tracks = sp.playlist_tracks(playlist_id)

    # TODO: integrate apple music api and implement method to transfer
    # For now, print song names
    tracks = [track['track']['name'] for track in playlist_tracks['items']]
    print(f"Tracks to transfer: {tracks}")
    return f"Playlist transfer initiated! Tracks: {', '.join(tracks)}"

def extract_playlist_id(spotify_url):
    # Simple function to extract playlist ID from Spotify URL
    if 'spotify.com/playlist/' in spotify_url:
        return spotify_url.split('/')[-1]
    return None

if __name__ == '__main__':
    app.secret_key = os.urandom(24) # Secret key for sessions
    app.run(debug=True)
