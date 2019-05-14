from flask import Flask, redirect, request, g
from redis import Redis
from lib.spotify import get_genre_counts, create_playlist, get_song_genre, refresh_master_access_token, \
    search_artist, get_artist_genre
from lib.database import get_db
import requests as http
import os
import sys
import json
import random

app = Flask(__name__)

###
# INITIAL SET UP
###

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

cred_file = open('private.json')
creds = json.loads(cred_file.read())
client_id = creds['client_id']
client_secret = creds['client_secret']
cred_file.close()

######
## API
######

@app.route('/api/create_playlist')
def api_create_playlist():
    user_id = request.args.get('u')
    genres = request.args.get('genres')
    db = get_db()
    create_playlist(genres.split(','), user_id)
    return 'success'

###
# this is the expected first API call - this kicks off the exploration
# of the user's library and ultimately returns the genre counts
@app.route('/api/genre_count')
def genre_count():
    user_id = request.args.get('u')
    counter = get_genre_counts(user_id)
    response = json.dumps(dict(counter))
    return response

@app.route('/api/song_genre')
def song_genre():
    user_id = request.args.get('u')
    song_id = request.args.get('song_id')
    genres = get_song_genre(user_id, song_id)
    return json.dumps(list(genres))

@app.route('/api/search_artist')
def _search_artist(): # underscore to avoid naming conflict
    artist_query = request.args.get('q')
    result = search_artist(artist_query)
    return json.dumps(result)

@app.route('/api/artist_genres')
def artist_genres():
    artist_id = request.args.get('id')
    result = get_artist_genre(artist_id)
    return json.dumps(result)

#########
## OAUTH2
######### 

@app.route("/")
def home():
    return redirect('/authenticate')

@app.route("/callback")
def callback():
    code = request.args.get('code')
    cred_file = open('private.json')
    creds = json.loads(cred_file.read())
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
    db = get_db()
    db.set(user_id, token)

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