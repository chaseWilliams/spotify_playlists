import requests as http
import os
import json
from collections import Counter

library_tracks_url = 'https://api.spotify.com/v1/me/tracks?limit=50&offset='
artists_info_url = 'https://api.spotify.com/v1/artists?ids='
me_info_url = 'https://api.spotify.com/v1/me'

def get_request(url, access_token):
    return http.get(url, headers={'Authorization': 'Bearer ' + access_token})

def construct_user_library(access_token, db):
    first_response = get_request(library_tracks_url + '0', access_token).json()
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

def create_playlist(genre, user_id, db):
    library = json.loads(db.get(user_id).decode('utf-8'))
    access_token = os.environ[user_id]
    user_id = get_request(me_info_url, access_token).json()['id']

    create_playlist_url = 'https://api.spotify.com/v1/users/{0}/playlists'.format(user_id)

    create_response = http.post(create_playlist_url, data=json.dumps({'name': genre}), headers={'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}).json()

    playlist_id = create_response['id']
    add_tracks_playlist_url = 'https://api.spotify.com/v1/playlists/{0}/tracks'.format(playlist_id)

    playlist_track_ids = []
    for track_obj in library:
        if genre in track_obj['genres']:
            playlist_track_ids.append(track_obj['id'])

    ## TODO:
    # randomize the playlist tracks? right now it is in chronological order (added date)
    for i in range(0, len(playlist_track_ids), 100):
        request_ids = playlist_track_ids[i:i + 100]
        add_tracks_response = http.post(add_tracks_playlist_url, data=json.dumps({
            'uris': ['spotify:track:' + x for x in request_ids]
        }), headers={'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}).json()
        print(add_tracks_response)

def get_genre_counts(user_id, db):
    # this function returns the user's genre count, but it also stores the user's 
    # library in redis
    access_token = os.environ[user_id]
    library, genre_counter = construct_user_library(access_token, db)
    db.set(user_id, json.dumps(library))
    return genre_counter
    