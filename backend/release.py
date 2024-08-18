import requests
from datetime import datetime

def get_release_date(song_name, artist_name, entity='song'):
    base_url = 'https://itunes.apple.com/search'
    search_term = f"{song_name} {artist_name}"
    
    params = {
        'term': search_term,
        'entity': entity,
        'limit': 1  # Limit to 1 result for simplicity
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if data['resultCount'] > 0:
        # Extract release date from the first result
        result = data['results'][0]
        iso_date_str = result.get('releaseDate', None)
        
        if iso_date_str:
            # Convert the ISO 8601 date string to a datetime object
            date_object = datetime.fromisoformat(iso_date_str.replace('Z', '+00:00'))
            # Format the datetime object to a string in YYYY-MM-DD format
            formatted_date = date_object.strftime('%Y-%m-%d')
            return formatted_date
        else:
            return '1800-01-01'
    else:
        return '1800-01-01'

