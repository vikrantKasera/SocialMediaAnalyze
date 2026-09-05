from googleapiclient.discovery import build

class YouTubeClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.youtube = build("youtube", "v3", developerKey=api_key, cache_discovery=False)

    def search_channels(self, keyword, max_results=50):
        response = self.youtube.search().list(
            part="snippet",
            q=keyword,
            type="channel",
            maxResults=min(max_results, 50),
        ).execute()

        return response.get("items", [])

    def get_channel_details(self, channel_ids):
        if not channel_ids:
            return []

        response = self.youtube.channels().list(
            part="snippet,statistics,contentDetails",
            id=",".join(channel_ids),
        ).execute()

        return response.get("items", [])
