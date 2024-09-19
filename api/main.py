from flask import Flask, request, jsonify
from backend.release import get_release_date
from backend.spot import spot_search, extract_first_part
from backend.last import last_search, list_to_string
from backend.yout import yout_search
from flask_cors import CORS
from flask_caching import Cache
from datetime import datetime
import re

app = Flask(__name__)
CORS(app)

cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

def format_date_to_words(date_string):
    try:
        date = datetime.strptime(date_string, '%Y-%m-%d')
        return date.strftime('%B %d, %Y')
    except ValueError:
        return date_string

@app.route('/api/process', methods=['POST'])

def process():
    data = request.json
    title = data['song_name']
    artist = data['artist_name']
    
    song_artist=title + " " + artist

    cache_key = f'{title}_{artist}'

    cached_result = cache.get(cache_key)
    if cached_result:
        return jsonify(cached_result)
    

    spot_info = spot_search(title, artist)
    last_info=last_search(spot_info['name'],list_to_string(spot_info['artists']))
    yout_info=yout_search(spot_info['name'],list_to_string(spot_info['artists']))

    real_release=""
    if len(spot_info['release_date']) < 10:
        real_release=get_release_date(spot_info['name'],list_to_string(spot_info['artists']))
    else:
        real_release=spot_info['release_date']

    result = {  
        "titley": spot_info['name'],
        "artisty": list_to_string(spot_info['artists']),
        "picy": spot_info['image_url'],
        "spotify_urly": spot_info['spotify_url'],
        "release_datey": format_date_to_words(real_release),
        "popularityy": spot_info['popularity'],
        "danceabilityy": spot_info['danceability'],
        "energyy": spot_info['energy'],
        "loudnessy": spot_info['loudness'],
        "speechinessy": spot_info['speechiness'],
        "acousticnessy": spot_info['acousticness'],
        "instrumentalnessy": spot_info['instrumentalness'],
        "livenessy": spot_info['liveness'],
        "valencey": spot_info['valence'],
        "tempoy": spot_info['tempo'],
        "spot_tagsy": spot_info['genres'],
        "listenersy": last_info['listeners'],
        "playcounty": last_info['playcount'],
        "last_urly": last_info['last_url'],
        "last_tagsy": last_info['tags'],
        "youtube_urly": yout_info['youtube_url'],
        "commentsy": yout_info['comment_count'],
        "likesy": yout_info['like_count'],
        "viewsy": yout_info['view_count'], 
    }

    cache.set(cache_key, result, timeout=5 * 60) 

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

