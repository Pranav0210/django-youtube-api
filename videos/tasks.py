import os
import requests
from datetime import datetime, timedelta
from django.utils.dateparse import parse_datetime
from .models import YouTubeVideo
from celery import shared_task

API_KEYS = os.getenv('YOUTUBE_API_KEYS').split(',')
QUERY = os.getenv('YOUTUBE_QUERY', 'official')
BASE_URL = 'https://www.googleapis.com/youtube/v3/search'

last_checked = datetime.utcnow() - timedelta(seconds=15)

@shared_task
def fetch_youtube_videos():
    global last_checked
    for key in API_KEYS:
        params = {
            'part': 'snippet',
            'q': QUERY,
            'type': 'video',
            'order': 'date',
            # 'publishedAfter': last_checked.isoformat("T") + "Z",
            'publishedAfter': "2025-05-23T00:00:00Z",
            'maxResults': 10,
            'key': key,
        }
        try:
            resp = requests.get(BASE_URL, params=params)
            print("YouTube API Request URL:", resp.url)
            print("Status Code:", resp.status_code)
            
            if resp.status_code != 200:
                print("Error response:", resp.text)
                return
    
            data = resp.json()
            print("Items received:", len(data.get("items", [])))

            if 'items' not in data:
                continue  # try next key

            for item in data['items']:
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
            last_checked = datetime.utcnow()
            break
        except Exception as e:
            continue
