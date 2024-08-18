from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from fuzzywuzzy import fuzz

# List of API keys
api_keys = [
    'AIzaSyD5ejr1Ol545fSRgAECOjtj8-GznjTTdv0',
    'AIzaSyBNbinY51LczOi3p5-QF75phEy0x6kUqPc',
    'AIzaSyDIwZ1OidwEtGxNV5Iy08kq0AvjBSyBZDI',
    'AIzaSyC6I6yDQ9M5Gzp_hRv0PNGns2hECVAiZR0',
    'AIzaSyBrU-KK3Tq4EAvYkPdb4XAEiguPy5l1lwo',
    'AIzaSyC4--pK-xnWxP3XbeG1mYMlBbM084S4DDM',
    'AIzaSyDSmsELdf_0CdXKBfFbJfTg_msAZAwCLYs',
    'AIzaSyAdkVrg8VilHQOaINS3Tf9XPLPCduED2yg',
    'AIzaSyCuy5Gj4aFhElnZiOdpw1VV8G8kA2tCaFk',
    'AIzaSyBT9fj4JNVHdtl-RvHJe29IRngKPiMRdcM',
    'AIzaSyC_8gnUDNv5WB3GOyyVYDSdq-pc_SZWD8g',
    'AIzaSyDMtVrB5jkBekGVzmuwfpLp8DhwQ4cw0Yc'
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
            maxResults=5,
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
