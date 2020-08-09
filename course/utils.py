from django.conf import settings
from django.core.files.base import ContentFile

import urllib.parse
import urllib.request
import requests

from googleapiclient.discovery import build

# arguments to be passed to build function 
DEVELOPER_KEY = settings.YOUTUBE_API_ACCESS_KEY
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# creating youtube resource object 
# for interacting with API 
youtube = build(YOUTUBE_API_SERVICE_NAME,
                YOUTUBE_API_VERSION,
                developerKey=DEVELOPER_KEY)


def video_details(video_id):
    # Call the videos.list method
    # to retrieve video info 
    list_videos_byid = youtube.videos().list(id=video_id,
                                             part="id, snippet, contentDetails, statistics",
                                             ).execute()

    # extracting the results from search response (getting first item)
    data = list_videos_byid.get("items", [])[0]

    return data


def extract_video_id(video_url):
    """extract youtube video id from its url"""
    url_data = urllib.parse.urlparse("http://www.youtube.com/watch?v=z_AbfPXTKms&NR=1")
    query = urllib.parse.parse_qs(url_data.query)
    video_id = query["v"][0]
    return video_id


def create_video_details(sender, instance, **kwargs):

    video_id = extract_video_id(instance.path)
    if video_id is not None:
        data = video_details(video_id)
        instance.title = data["snippet"]["title"]
        image_url = data['snippet']['thumbnails']['default']['url']
        instance.description = data['snippet']['description']

        name = urllib.parse.urlparse(image_url).path.split('/')[-1]
        response = requests.get(image_url)

        if response.status_code == 200:
            instance.thumbnail.save(name, ContentFile(response.content), save=False)
