from .youtube_client import YouTubeClient

class ChannelSearchService:
    def __init__(self, api_key):
        self.client = YouTubeClient(api_key)

    def search(self, keyword, max_results=50):
        return self.client.search_channels(keyword, max_results=max_results)
