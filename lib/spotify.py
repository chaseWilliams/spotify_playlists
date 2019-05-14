from collections import Counter
from base64 import b64encode
from lib.database import get_db
import requests as http
import os
import json

library_tracks_url = 'https://api.spotify.com/v1/me/tracks?limit=50&offset='
single_track_url = 'https://api.spotify.com/v1/tracks/'
artists_info_url = 'https://api.spotify.com/v1/artists?ids='
single_artist_info_url = 'https://api.spotify.com/v1/artists/'
me_info_url = 'https://api.spotify.com/v1/me'
token_uri = 'https://accounts.spotify.com/api/token'
search_url = 'https://api.spotify.com/v1/search'

def get_request(url, access_token):
    return http.get(url, headers={'Authorization': 'Bearer ' + access_token})

def refresh_master_access_token():
    db = get_db()
    cred_file = open('private.json')
    creds = json.loads(cred_file.read())
    creds_string = creds['client_id'] + ':' + creds['client_secret']
    creds_encoded = b64encode(creds_string.encode('utf-8')).decode('utf-8')

    auth_response = http.post(token_uri, data = {
        'grant_type': 'client_credentials'
    }, headers = {
        'Authorization': 'Basic ' + creds_encoded
    }).json()

    print(auth_response)

    db.set('master_access_token', auth_response['access_token'])
    cred_file.close()

def get_request_master_token(url):
    db = get_db()
    access_token = db.get('master_access_token')
    if access_token == None:
        refresh_master_access_token()
        access_token = db.get('master_access_token')
    access_token = access_token.decode('utf-8')
    response = http.get(url, headers={'Authorization': 'Bearer ' + access_token})
    if response.status_code >= 300:
        refresh_master_access_token()
        access_token = db.get('master_access_token').decode('utf-8')
        response = http.get(url, headers={'Authorization': 'Bearer ' + access_token})
    return response

def get_access_token(user_id):
    db = get_db()
    return db.get(user_id).decode('utf-8')

def get_song_genre(user_id, song_id):
    db = get_db()
    access_token = get_access_token(user_id)
    track = get_request(single_track_url + song_id, access_token).json()

    artists = []
    for artist_obj in track['artists']:
        artists.append(artist_obj['id'])

    artists_data = get_request(artists_info_url + ','.join(artists), access_token).json()
    print(artists_data)
    genres = []
    for artist in artists_data['artists']:
        print(artist)
        genres += artist['genres']
    
    return set(genres)

def get_artist_genre(artist_id):
    return get_request_master_token(single_artist_info_url + artist_id).json()['genres']

def search_artist(artist_query):
    data = get_request_master_token(search_url + 
                    '?q={0}&type=artist&limit=5'.format(artist_query)).json()
    print(data)
    return data['artists']['items']

def construct_user_library(access_token):
    first_response = get_request(library_tracks_url + '0', access_token).json()
    library = [] # each element is a track object, a dict with keys 'id', 'artists', and 'genres'
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
    # this does the same thing as above, only difference is program knows how many 
    # songs are in the library
    for i in range(50, first_response['total'], 50):
        response = get_request(library_tracks_url + str(i), access_token).json()
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
        response = get_request(artists_info_url + ','.join(unique_library_artists[i:i + 50]), access_token).json()
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
    return library, Counter(genres)


## TODO
# title can be too long - maybe custom title as well?
def create_playlist(genres, user_id):
    db = get_db()
    library = json.loads(db.get(user_id + '_library').decode('utf-8'))
    access_token = get_access_token(user_id)
    user_id = get_request(me_info_url, access_token).json()['id']

    create_playlist_url = 'https://api.spotify.com/v1/users/{0}/playlists'.format(user_id)
    playlist_name = ','.join(genres)
    if len(playlist_name) > 50:
        playlist_name = playlist_name[:47] + '...'
    create_response = http.post(create_playlist_url, data=json.dumps({'name': playlist_name}), headers={'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}).json()

    playlist_id = create_response['id']
    add_tracks_playlist_url = 'https://api.spotify.com/v1/playlists/{0}/tracks'.format(playlist_id)

    playlist_track_ids = []
    for track_obj in library:
        for genre in genres:
            # if genre in track obj and not already added
            if genre in track_obj['genres'] and track_obj['id'] not in playlist_track_ids:
                playlist_track_ids.append(track_obj['id'])

    ## TODO:
    # randomize the playlist tracks? right now it is in chronological order (added date)
    for i in range(0, len(playlist_track_ids), 100):
        request_ids = playlist_track_ids[i:i + 100]
        add_tracks_response = http.post(add_tracks_playlist_url, data=json.dumps({
            'uris': ['spotify:track:' + x for x in request_ids]
        }), headers={'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}).json()

def get_genre_counts(user_id):
    db = get_db()
    # this function returns the user's genre count, but it also stores the user's 
    # library in redis
    access_token = get_access_token(user_id)
    library, genre_counter = construct_user_library(access_token)
    db.set(user_id + '_library', json.dumps(library))
    return genre_counter
    