from flask import Flask, redirect, request
from redis import Redis
import os
import sys
import requests as http
import json
import random
from collections import Counter
from base64 import b64encode
from lib.spotify import get_genre_counts, create_playlist, get_song_genre
from urllib.parse import urlparse

app = Flask(__name__)

client_id = '3acb1841e1ff42e784708fe06a5e932e'
client_secret = 'c7ce2a5f57d242ffa0a0c28402ce7377'


redirect_uri = 'https://pure-escarpment-60201.herokuapp.com/callback'
# debug or prod mode
LOCAL = False
if len(sys.argv) > 1:
    if sys.argv[1] == 'debug':
        print('LOCAL VERSION')
        redirect_uri = 'http://127.0.0.1:5000/callback'
        LOCAL = True

authorize_uri = 'https://accounts.spotify.com/authorize'
token_uri = 'https://accounts.spotify.com/api/token'

if LOCAL:
    db = Redis()
else:
    url = urlparse(os.environ.get('REDISCLOUD_URL'))
    db = Redis(host=url.hostname, port=url.port, password=url.password)
## API

@app.route('/api/create_playlist')
def api_create_playlist():
    user_id = request.args.get('u')
    genre = request.args.get('genre')
    create_playlist(genre, user_id, db)
    return 'success'

@app.route('/api/genre_count')
def genre_count():
    user_id = request.args.get('u')
    counter = get_genre_counts(user_id, db)
    response = json.dumps(dict(counter))
    return response

@app.route('/api/song_genre')
def song_genre():
    user_id = request.args.get('u')
    song_id = request.args.get('song_id')
    genres = get_song_genre(user_id, song_id)
    return json.dumps(list(genres))


## OAUTH2 

@app.route("/")
def home():
    return redirect('/authenticate')

@app.route("/callback")
def callback():
    code = request.args.get('code')
    result = http.post(token_uri, data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    })
    data = result.json()
    token = data['access_token']
    user_id = str(random.randint(1e5, 1e6 - 1))
    os.environ[user_id] = token

    return redirect('/explore?u=' + user_id)
    
@app.route("/authenticate")
def authenticate():
    return redirect(authorize_uri + '?client_id=' + client_id + \
                    '&response_type=code&redirect_uri=' + redirect_uri + '&scope=user-library-read playlist-modify-public')

@app.route("/explore")
def explore():
    return app.send_static_file('explore.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=LOCAL)