from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from fuzzywuzzy import fuzz

from dotenv import load_dotenv
import os
load_dotenv()

api_keys = [
    os.getenv("YOUT_secret1"), 
    os.getenv("YOUT_secret2"), 
    os.getenv("YOUT_secret3"), 
    os.getenv("YOUT_secret4"), 
    os.getenv("YOUT_secret5"), 
    os.getenv("YOUT_secret6"), 
    os.getenv("YOUT_secret7"), 
    os.getenv("YOUT_secret8"), 
    os.getenv("YOUT_secret9"),
    os.getenv("YOUT_secret10"), 
    os.getenv("YOUT_secret11"), 
    os.getenv("YOUT_secret12")
]

def yout_search(song, artist):
    if (song=="not found"): 
        track_info = {
            "view_count": -1,
            "like_count": -1,
            "comment_count": -1,
            "youtube_url": "https://www.youtube.com/"
        }           
        return track_info

        
    song_artist= song + " " + artist
    def search_music_video(youtube, song_artist):
        search_response = youtube.search().list(
            q=song_artist,
            part='id,snippet',
            maxResults=3,
            type='video'
        ).execute()

        video_ids = [item['id']['videoId'] for item in search_response['items']]
        return video_ids

    def get_video_details(youtube, video_ids):
        video_response = youtube.videos().list(
            id=','.join(video_ids),
            part='snippet,contentDetails,statistics'
        ).execute()

        video_details = video_response['items']
        return video_details

    for api_key in api_keys:
        try:
            youtube = build('youtube', 'v3', developerKey=api_key)
            video_ids = search_music_video(youtube, song_artist)

            if video_ids:
                video_details = get_video_details(youtube, video_ids)

                # Calculate engagement for each video and find the most engaged one
                
                most_engaged_video = max(
                    video_details,
                    key=lambda video: (
                        int(video['statistics']['viewCount']) +
                        int(video['statistics'].get('commentCount', 0)) +
                        int(video['statistics'].get('likeCount', 0)) 
                    )
                )

                track_info = {
                    "view_count": int(most_engaged_video['statistics']['viewCount']),
                    "like_count": int(most_engaged_video['statistics'].get('likeCount', -1)),  # Handle videos without likeCount
                    "comment_count": int(most_engaged_video['statistics'].get('commentCount', -1)),  # Handle videos without commentCount
                }

                video_id = most_engaged_video['id']
                track_info.update({
                    'youtube_url' : f'https://www.youtube.com/watch?v={video_id}'
                })
                return track_info
            else:
                track_info = {
                    "view_count": -1,
                    "like_count": -1,
                    "comment_count": -1,
                    "youtube_url": "https://www.youtube.com/"
                }
                return track_info
        except HttpError as e:
            error_content = e.content.decode()
            if 'quotaExceeded' in error_content:
                continue
            else:
                raise e  
             
    track_info = {
        "view_count": -1,
        "like_count": -1,
        "comment_count": -1,
        "youtube_url": "https://www.youtube.com/"
    }           
    return track_info
