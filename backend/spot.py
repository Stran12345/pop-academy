import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from fuzzywuzzy import fuzz
from datetime import datetime
import re

from dotenv import load_dotenv
import os
load_dotenv()


def extract_first_part(input_string):
    pattern = r'( +[Ff]eaturing +| +[Xx] +| +& +| +[Ww]ith +| +[Aa]nd +| +, +)'
    result = re.split(pattern, input_string)[0]
    return result

def list_to_string(listy):
    ans=" "
    for idx in range(len(listy)):
        if idx == 0:
            ans = listy[idx]
        else:
            ans = ans + ", " + listy[idx]
    return ans

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def spot_search(song_name,artist_name):
    results = sp.search(q=f"{song_name} {artist_name}", type='track', limit=10)
    
    best_match = None
    highest_popularity = -1
    
    for track in results['tracks']['items']:
        track_name = track['name']
        artists_names=list_to_string([artist['name'] for artist in track['artists']])

        if '-' in song_name or '(' in song_name or '[' in song_name:
            similarity_song= fuzz.ratio(track_name.lower(), song_name.lower())
        else:
            similarity_song= fuzz.ratio(track_name.lower().split('(')[0].split('-')[0].split('[')[0], song_name.lower())
        similarity_artist= fuzz.partial_ratio(extract_first_part(artist_name.lower()), artists_names.lower())
        if similarity_song> 80 and similarity_artist > 70:  
            if track['popularity'] > highest_popularity:
                highest_popularity = track['popularity']
                best_match = track

    if best_match:
        track = best_match
        track_id = track['id']
        
        track_info = {
            'name': track['name'],
            'album': track['album']['name'],
            'artists': [artist['name'] for artist in track['artists']],
            'release_date': track['album']['release_date'],
            'popularity': int(track['popularity']),
            'image_url': track['album']['images'][0]['url'],
            'spotify_url': track['external_urls']['spotify']
        }
        
        audio_features = sp.audio_features(track_id)[0]
        if audio_features:
            track_info.update({
                'danceability': float(audio_features['danceability']),
                'energy': float(audio_features['energy']),
                'loudness': float(audio_features['loudness']),
                'speechiness': float(audio_features['speechiness']),
                'acousticness': float(audio_features['acousticness']),
                'instrumentalness': float(audio_features['instrumentalness']),
                'liveness': float(audio_features['liveness']),
                'valence': float(audio_features['valence']),
                'tempo': float(audio_features['tempo'])
            })
        
        artist_id = track['artists'][0]['id']
        artist_info = sp.artist(artist_id)
        tags = artist_info.get('genres', [])
        track_info['genres']=""
        for idx in range(len(tags)):
            if idx == 0:
                track_info['genres'] = tags[idx]
            else:
                track_info['genres'] = track_info['genres'] + ", " + tags[idx]
        return(track_info)
    else:
        track_info = {
            'name': "not found",
            'album': "not found",
            'artists': "not found",
            'release_date': '1800-01-01',
            'popularity': -1,
            'danceability': -1,
            'energy': -1,
            'loudness': -1,
            'speechiness': -1,
            'acousticness': -1,
            'instrumentalness': -1,
            'liveness': -1,
            'valence': -1,
            'tempo': -1,
            'image_url': 'https://img.freepik.com/free-vector/sad-emoji_53876-25516.jpg?t=st=1723746821~exp=1723750421~hmac=4977a4f5444e3a4b3d9613db676ef042f74483c95265fa937afc3434207b7bb8&w=1800',
            'spotify_url': 'https://open.spotify.com/',
            'genres':'none'

        }
        return track_info
