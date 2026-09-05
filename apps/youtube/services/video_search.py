from .youtube_client import YouTubeClient

class VideoSearchService:
    def __init__(self, api_key):
        self.client = YouTubeClient(api_key)

    def get_channel_details(self, channel_ids):
        return self.client.get_channel_details(channel_ids)
