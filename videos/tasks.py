import os
import requests
from datetime import datetime, timedelta, timezone
from django.utils.dateparse import parse_datetime
from .models import YouTubeVideo
from celery import shared_task

API_KEYS = os.getenv('YOUTUBE_API_KEYS').split(',')
API_KEY_INDEX = 0
QUERY = os.getenv('YOUTUBE_QUERY', 'official')
YOUTUBE_SEARCH_BASE_URL = os.getenv('YOUTUBE_SEARCH_BASE_URL')
last_checked_str = os.getenv('RECENT_THRESHOLD_DATE', "2024-05-23T00:00:00Z")
LAST_CHECKED = parse_datetime(last_checked_str)
if LAST_CHECKED.tzinfo is None:
    LAST_CHECKED = LAST_CHECKED.replace(tzinfo=timezone.utc)

@shared_task(bind=True)
def fetch_youtube_videos(self):
    global LAST_CHECKED
    global API_KEY_INDEX
    print(f"Fetching YouTube videos since {LAST_CHECKED.replace(tzinfo=None).isoformat('T') + 'Z'} with query '{QUERY}'")

    print('API Keys:', API_KEYS)

    try:
        while API_KEY_INDEX < len(API_KEYS):
            params = {
                'part': 'snippet',
                'q': QUERY,
                'type': 'video',
                'order': 'date',
                'publishedAfter': LAST_CHECKED.replace(tzinfo=None).isoformat("T") + "Z",
                'maxResults': 50,
                'key': API_KEYS[API_KEY_INDEX],
            }
            resp = requests.get(YOUTUBE_SEARCH_BASE_URL, params=params)
            print("YouTube API Request URL:", resp.url)
            print("Status Code:", resp.status_code)

            if resp.status_code != 200:
                print("Error response:", resp.text)
                
            if (resp.status_code == 403):
                print("Quota exceeded for API key:", API_KEYS[API_KEY_INDEX])
                
                API_KEY_INDEX += 1
                continue
            
            data = resp.json()
            print("Items received:", len(data.get("items", [])))

            LAST_CHECKED = datetime.now(timezone.utc)

            for item in data.get('items', []):
                snippet = item['snippet']
                YouTubeVideo.objects.get_or_create(
                    video_id=item['id']['videoId'],
                    defaults={
                        'title': snippet['title'],
                        'description': snippet['description'],
                        'published_at': parse_datetime(snippet['publishedAt']),
                        'thumbnail_url': snippet['thumbnails']['default']['url'],
                    }
                )

            next_page_token = data.get('nextPageToken')
            while next_page_token:
                params['pageToken'] = next_page_token
                resp = requests.get(YOUTUBE_SEARCH_BASE_URL, params=params)
                if resp.status_code != 200:
                    print("Error on pagination page:", resp.text)
                    break
                page_data = resp.json()
                for item in page_data.get('items', []):
                    snippet = item['snippet']
                    YouTubeVideo.objects.get_or_create(
                        video_id=item['id']['videoId'],
                        defaults={
                            'title': snippet['title'],
                            'description': snippet['description'],
                            'published_at': parse_datetime(snippet['publishedAt']),
                            'thumbnail_url': snippet['thumbnails']['default']['url'],
                        }
                    )
                next_page_token = page_data.get('nextPageToken')
            break
        
        if API_KEY_INDEX >= len(API_KEYS):
            print("All API keys exhausted. Stopping task.")
            return
        
    except Exception as e:
        print(f"Exception in celery task: {e}")
