import requests
from fuzzywuzzy import fuzz

from dotenv import load_dotenv
import os
load_dotenv()

API_KEY = os.getenv("LAST_key")
API_SECRET = os.getenv("LAST_secret")

def list_to_string(listy):
    ans=" "
    for idx in range(len(listy)):
        if idx == 0:
            ans = listy[idx]
        else:
            ans = ans + ", " + listy[idx]
    return ans
        
def last_search(song_name, artist_name):

    def search_song(song_name, artist_name=None):
        search_url = 'http://ws.audioscrobbler.com/2.0/'
        params = {
            'method': 'track.search',
            'track': song_name,
            'api_key': API_KEY,
            'format': 'json',
            'limit': 10  
        }
        if artist_name:
            params['artist'] = artist_name

        response = requests.get(search_url, params=params)
        data = response.json()
        return data

    def get_song_info(artist_name, track_name):
        info_url = 'http://ws.audioscrobbler.com/2.0/'
        params = {
            'method': 'track.getInfo',
            'api_key': API_KEY,
            'artist': artist_name,
            'track': track_name,
            'format': 'json'
        }

        response = requests.get(info_url, params=params)
        data = response.json()
        return data

    def find_most_popular_song(song_name):
        search_results = search_song(song_name)
        if 'results' not in search_results or 'trackmatches' not in search_results['results'] or 'track' not in search_results['results']['trackmatches']:
            return None
        
        tracks = search_results['results']['trackmatches']['track']
        
        possible_artists = {artist_name}
        possible_artists.update(artist_name.split(','))

        most_popular_track = None
        max_playcount = -1

        for artist in possible_artists:
            artist = artist.strip()
            search_results = search_song(song_name, artist)
            if 'results' not in search_results or 'trackmatches' not in search_results['results'] or 'track' not in search_results['results']['trackmatches']:
                continue
            
            tracks = search_results['results']['trackmatches']['track']
            
            for track in tracks:
                track_name = track['name']
                if fuzz.partial_ratio(track_name.lower().split('(')[0], song_name.lower()) > 70:
                    song_info = get_song_info(artist, track_name)
                    if 'track' in song_info:
                        track_info = song_info['track']
                        playcount = int(track_info['playcount'])
                        
                        if playcount > max_playcount:
                            max_playcount = playcount
                            most_popular_track = track_info
                            
        return most_popular_track

    most_popular_track = find_most_popular_song(song_name)

    if most_popular_track:
        tags = [tag['name'] for tag in most_popular_track['toptags']['tag']]
        str_tags=" "
        for idx in range(len(tags)):
            if idx == 0:
                str_tags = tags[idx]
            else:
                str_tags = str_tags + ", " + tags[idx]

        track_info={
            "track_name": most_popular_track['name'],
            "artist_name": most_popular_track['artist']['name'],
            "listeners": int(most_popular_track['listeners']),
            "playcount": int(most_popular_track['playcount']),
            "last_url": most_popular_track['url'],
            "tags": str_tags
        }
        return track_info
    else:
        track_info={
            "listeners": -1,
            "playcount": -1,
            "tags": "none found",
            "last_url": 'https://www.last.fm/home'
        }
        return track_info
