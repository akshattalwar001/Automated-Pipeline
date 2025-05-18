from googleapiclient.discovery import build
import yaml
import os


def load_config():
    with open("config/config.yaml", "r") as file:
        return yaml.safe_load(file)


def get_youtube_service():
    config = load_config()
    api_key = config["youtube"]["api_key"]
    return build("youtube", "v3", developerKey=api_key)


def extract_trending_videos(region_code="US", max_results=50):
    youtube = get_youtube_service()
    request = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
         regionCode=region_code,
        maxResults=max_results
    )
    response = request.execute()

    videos = []
    for item in response["items"]:
        video = {
            "video_id": item["id"],
            "title": item["snippet"]["title"],
            "published_at": item["snippet"]["publishedAt"],
            "category_id": item["snippet"]["categoryId"],
            "tags": item["snippet"].get("tags", []),
            "views": item["statistics"].get("viewCount", 0),
            "likes": item["statistics"].get("likeCount", 0),
            "channel_title": item["snippet"]["channelTitle"],
            "region_code": region_code
        }
        videos.append(video)
    return videos