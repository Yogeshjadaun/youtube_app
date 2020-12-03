from datetime import datetime, timedelta

from celery import shared_task
import requests

from django.conf import settings
from youtube_engine.models import YoutubeVideo, YoutubeApiKey


@shared_task
def youtube_engine():
    '''
    Background server task which fetches the latest videos from youtube
    using youtube data api and update the new videos in database effectively.
    Also it fetches the youtube api key which is working from database once
    it got expired it will make it to failed status.
    :return:
    '''
    youtube_search_url = "https://www.googleapis.com/youtube/v3/search"
    published_after = datetime.now()-timedelta(minutes=1)
    published_after = str(published_after.date()) + 'T' + str(published_after.time())[:8] + 'Z'
    api_keys = YoutubeApiKey.objects.filter(status=YoutubeApiKey.SUCCESS).order_by('created_at')
    for api_key in api_keys:
        params = {
            'part': "snippet",
            'q': settings.SEARCH_KEYWORD,
            'type': "video",
            'key': api_key.key,
            'publishedAfter': published_after,
            'maxResults': settings.MAX_RESULTS
        }
        response = requests.get(youtube_search_url, params)
        response = response.json()
        if response.get('error'):
            api_key.status = YoutubeApiKey.FAILED
            api_key.save()
            print("Valid API Key not Present")
        else:
            response = response.get('items', None)
            for video in response:
                video_id = video['id']['videoId']
                channel_id = video['snippet']['channelId']
                title = video['snippet']['title']
                description = video['snippet']['description']
                channel_title = video['snippet']['channelTitle']
                publishing_date = video['snippet']['publishTime']
                thumbnail_url = video['snippet']['thumbnails']["default"]["url"]
                obj, created = YoutubeVideo.objects.get_or_create(title=title, description=description,
                                                                  channel_title=channel_title, thumbnails_url=thumbnail_url,
                                                                  publishing_date=publishing_date, channel_id=channel_id,
                                                                  defaults={"video_id": video_id})

            break

    print("Database Updated after fetching data from youtube apis")