import requests as http
import os
import json
from collections import Counter


access_token = 'BQAegI-8BtJPrxv3W-sFoilDTFQQz2nLV2vBHyFl7T54_b9ID_m6S5-aLP59qG-z3O1UJtfV9l5zFiJpqHn2eRIkZwbx9b6ubv_7ysYeoh4k_ky2xJ36QsrcB6Ok8l1XOntUEU9q6gogl25T1UTpuEzVJCfR77ArcjwkuQxH6coziVo-J_r2anArfjPocAUzLpK9lg'
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
print(genre_counter.most_common(20))
print()

PLAYLIST_GENRE = 'electronic trap'
user_id = get_request(me_info_url).json()['id']

create_playlist_url = 'https://api.spotify.com/v1/users/{0}/playlists'.format(user_id)

create_response = http.post(create_playlist_url, data=json.dumps({'name': PLAYLIST_GENRE}), headers={'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}).json()
print(create_response)

playlist_id = create_response['id']
add_tracks_playlist_url = 'https://api.spotify.com/v1/playlists/{0}/tracks'.format(playlist_id)

playlist_track_ids = []
for track_obj in library:
    if PLAYLIST_GENRE in track_obj['genres']:
        playlist_track_ids.append(track_obj['id'])

## TODO:
# randomize the playlist tracks? right now it is in chronological order (added date)
for i in range(0, len(playlist_track_ids), 100):
    request_ids = playlist_track_ids[i:i + 100]
    add_tracks_response = http.post(add_tracks_playlist_url, data=json.dumps({
        'uris': ['spotify:track:' + x for x in request_ids]
    }), headers={'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}).json()
    print(add_tracks_response)