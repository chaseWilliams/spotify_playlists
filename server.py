from flask import Flask, redirect, request
import os
import requests as http
import json
from collections import Counter
from base64 import b64encode

app = Flask(__name__)

client_id = '3acb1841e1ff42e784708fe06a5e932e'
client_secret = 'c7ce2a5f57d242ffa0a0c28402ce7377'

redirect_uri = 'http://127.0.0.1:5000/callback'
#redirect_uri = 'https://example-django-app-dude0faw3.c9users.io/callback'

authorize_uri = 'https://accounts.spotify.com/authorize'
token_uri = 'https://accounts.spotify.com/api/token'

play_uri = 'https://api.spotify.com/v1/me/player/play'
pause_uri = 'https://api.spotify.com/v1/me/player/pause'
track_uri = 'https://api.spotify.com/v1/tracks/'

code = ''
token = ''

## API

@app.route('/api/user_library')
def user_library():
    pass

@app.route('/api/genre_count')
def genre_count():
    counter = get_genre_counts()
    response = json.dumps(dict(counter))
    print(response)
    return response
## OAUTH2 

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
    print(data)
    token = data['access_token']
    refresh = data['refresh_token']
    print(token)

    os.environ['REFRESH_TOKEN'] = refresh
    os.environ['ACCESS_TOKEN'] = token

    return redirect('/static/explore.html')
    
@app.route("/authenticate")
def authenticate():
    return redirect(authorize_uri + '?client_id=' + client_id + \
                    '&response_type=code&redirect_uri=' + redirect_uri + '&scope=user-library-read playlist-modify-public')

## Playback Endpoints

@app.route("/resume")
def resume():
    print(get_request(play_uri, call_type='PUT'))
    return 'success'

@app.route("/pause")
def pause():
    print('GOT PAUSE')
    print(get_request(pause_uri, call_type='PUT'))
    return 'success'


def get_request(url, call_type='GET', body=None):
    print(os.environ['ACCESS_TOKEN'])
    print(url)
    if call_type is 'GET':
        response = http.get(url, headers={'Authorization': 'Bearer ' + os.environ['ACCESS_TOKEN']})
        if int(response.status_code) >= 400:
            refresh_access_token()
            response = http.get(url, headers={'Authorization': 'Bearer ' + os.environ['ACCESS_TOKEN']})
    if call_type is 'POST':
        response = http.post(url, data=body, headers={'Authorization': 'Bearer ' + os.environ['ACCESS_TOKEN']})
        print(response.text)
        if int(response.status_code) >= 400:
            refresh_access_token()
            response = http.post(url, data=body, headers={'Authorization': 'Bearer ' + os.environ['ACCESS_TOKEN']})
    if call_type is 'PUT':
        response = http.put(url, data=body, headers={'Authorization': 'Bearer ' + os.environ['ACCESS_TOKEN']})
        print(response.text, response.status_code)
        if int(response.status_code) >= 400:
            refresh_access_token()
            response = http.put(url, data=body, headers={'Authorization': 'Bearer ' + os.environ['ACCESS_TOKEN']})

    return response


def refresh_access_token():
    body = {
        'grant_type': 'refresh_token',
        'refresh_token': os.environ['REFRESH_TOKEN']
    }
    string = (client_id + ':' + client_secret).encode('utf-8')
    encoded_string = str(b64encode(string))
    response = http.post(token_uri, data=body, headers={'Authorization': 'Basic ' + encoded_string})
    data = response.json()
    print(data)
    access_token = data['access_token']
    os.environ['ACCESS_TOKEN'] = access_token

def get_genre_counts():
    access_token = 'BQBci0dO-TMCunFh93_eplKZp4A7hmoy0rEM7bpFN8lSiymkn7NFJ-PLkohxRjqvDS0k0L_V-Sezq2A8u5Se2St5c27NIcAz0HD9kwH423QAWCUWUz3wy2ru4ewsf877U1fpb1uCUOkgn9OV5gYPDfTY9e5la0oZ-enPcG-L9ZwVIpZt5jtg1e1YwCQaVpa1W3DcBg'
    library_tracks_url = 'https://api.spotify.com/v1/me/tracks?limit=50&offset='
    artists_info_url = 'https://api.spotify.com/v1/artists?ids='
    me_info_url = 'https://api.spotify.com/v1/me'

    def get_request(url):
        return http.get(url, headers={'Authorization': 'Bearer ' + access_token})

    first_response = get_request(library_tracks_url + '0').json()

    library = [] # each element will be a dict with keys 'id', 'artists', and 'genres'
    library_artists = [] # list of artist ids
    for track in first_response['items']:
        artists = []
        for artist in track['track']['artists']:
            artists.append(artist['id'])
            # this is a comment 
            # im not actually programming Im' just totally writing random stuff down
            library_artists.append(artist['id'])
        library.append({
            'id': track['track']['id'],
            'artists': artists
        })

    for i in range(50, first_response['total'], 50):
        response = get_request(library_tracks_url + str(i)).json()
        for track in response['items']:
            artists = []
            for artist in track['track']['artists']:
                artists.append(artist['id'])
                library_artists.append(artist['id'])
            library.append({
                'id': track['track']['id'],
                'artists': artists
            })

    artists_counter = Counter(library_artists)
    unique_library_artists = list(artists_counter)

    genres = [] # just a running total of genres in library
    artist_genres = {}
    for i in range(0, len(unique_library_artists), 50):
        response = get_request(artists_info_url + ','.join(unique_library_artists[i:i + 50])).json()
        for artist in response['artists']:
            artist_genres[artist['id']] = artist['genres']

    # iterate through tracks and add their respective unique genres according to associated artists
    for track_obj in library:
        track_genres = []
        for artist in track_obj['artists']:
            for genre in artist_genres[artist]:
                track_genres.append(genre)
                genres.append(genre)
        track_obj['genres'] = track_genres

    genre_counter = Counter(genres)
    return genre_counter