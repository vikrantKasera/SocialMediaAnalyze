"""Fetch, filter, persist, and export YouTube creators asynchronously."""

import argparse
import asyncio
import io
import json
import os
import re
import socket
from datetime import datetime, timezone
from typing import Any

import django
import openpyxl
import requests
from django.core.files.base import ContentFile
from django.utils import timezone as django_timezone
from googleapiclient.errors import HttpError
from openpyxl.styles import Font


class ApiKeysExhausted(RuntimeError):
    pass


class InvalidApiKey(RuntimeError):
    pass


class YouTubeNetworkError(RuntimeError):
    pass


class RotatingYouTubeApi:
    """Retry quota errors with the next active key from the database."""

    def __init__(self, keys: list[str], progress_callback=None):
        self.keys = keys
        self.index = 0
        self.clients = {}
        self.progress_callback = progress_callback

    def _report(self, message: str) -> None:
        if self.progress_callback:
            self.progress_callback(message)

    @staticmethod
    def _is_quota_error(error: HttpError) -> bool:
        if error.resp.status not in {403, 429}:
            return False
        try:
            reasons = [item.get("reason") for item in json.loads(error.content).get("error", {}).get("errors", [])]
        except (TypeError, ValueError, AttributeError):
            reasons = []
        return any(reason in {"quotaExceeded", "dailyLimitExceeded", "userRateLimitExceeded", "rateLimitExceeded"} for reason in reasons)

    @staticmethod
    def _is_invalid_key_error(error: HttpError) -> bool:
        try:
            payload = json.loads(error.content)
            reasons = [item.get("reason") for item in payload.get("error", {}).get("errors", [])]
            message = payload.get("error", {}).get("message", "").lower()
        except (TypeError, ValueError, AttributeError):
            reasons = []
            message = str(error).lower()
        return "keyInvalid" in reasons or "api key not valid" in message

    def request(self, resource: str, method: str, **params: Any) -> dict[str, Any]:
        endpoint = f"https://youtube.googleapis.com/youtube/v3/{resource}"
        for _ in range(len(self.keys)):
            key = self.keys[self.index]
            request_params = {**params, "key": key}
            try:
                response = requests.request(method, endpoint, params=request_params, timeout=30)
                if response.ok:
                    return response.json()
                error = HttpError(
                    type("Response", (), {"status": response.status_code, "reason": response.reason})(),
                    response.content,
                )
                if self._is_quota_error(error):
                    self._report("YouTube API key quota reached; switching to the next key...")
                elif self._is_invalid_key_error(error):
                    self._report("YouTube API key is invalid; switching to the next key...")
                else:
                    response.raise_for_status()
                self.index = (self.index + 1) % len(self.keys)
            except (requests.RequestException, OSError, socket.timeout) as error:
                self._report("Network error connecting to YouTube. Check production outbound HTTPS access and proxy settings.")
                raise YouTubeNetworkError(
                    "Cannot connect to YouTube API. Verify HTTPS proxy settings and outbound access on port 443."
                ) from error
        raise ApiKeysExhausted("All active YouTube API keys are invalid or have reached their quota.")


def setup_django() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SocialMediaAnalizer.settings")
    django.setup()


def load_inputs(progress_callback=None) -> tuple[RotatingYouTubeApi, list[str], list[str], dict[str, Any]]:
    setup_django()
    from apps.access_keys.models import AccessKey
    from apps.countries.models import Country
    from apps.posting_criteria.models import PostingCriteria
    from apps.relevance_keywords.models import RelevanceKeyword
    from apps.search_keywords.models import SearchKeyword
    from apps.results.models import Creator

    keys = list(AccessKey.objects.filter(is_active=True).values_list("key", flat=True))
    if not keys:
        raise RuntimeError("No active YouTube API keys are configured.")
    keywords = list(SearchKeyword.objects.filter(is_active=True).values_list("keyword", flat=True))
    relevance = [value.lower() for value in RelevanceKeyword.objects.filter(is_active=True).values_list("keyword", flat=True)]
    excluded_countries = {value.upper() for value in Country.objects.filter(is_active=True).values_list("code", flat=True)}
    criteria = PostingCriteria.objects.filter(is_active=True).order_by("-updated_at").first()
    settings = {
        "result_limit": criteria.result_per_keyword if criteria else 10,
        "pages": criteria.per_page_keyword if criteria else 1,
        "videos_to_check": criteria.video_to_check if criteria else 4,
        "recent_days": criteria.recent_days if criteria else 100,
        "shorts_max_seconds": criteria.shorts_max_second if criteria else 180,
        "min_views": criteria.min_views if criteria else 0,
        "min_subscribers": criteria.min_subscribers if criteria else 0,
        "max_subscribers": criteria.max_subscribers if criteria else 1_000_000,
        "max_creators": criteria.max_creators if criteria else 1000,
        "excluded_countries": excluded_countries,
    }
    existing = set(Creator.objects.values_list("channel_id", flat=True))
    return RotatingYouTubeApi(keys, progress_callback=progress_callback), keywords, relevance, {**settings, "existing": existing}


def parse_duration(value: str) -> int:
    match = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", value or "")
    if not match:
        return 0
    hours, minutes, seconds = (int(part or 0) for part in match.groups())
    return hours * 3600 + minutes * 60 + seconds


def search_channels(api: RotatingYouTubeApi, keyword: str, result_limit: int, pages: int) -> list[str]:
    channel_ids = []
    page_token = None
    for _ in range(max(1, pages)):
        params = {"part": "snippet", "q": keyword, "type": "channel", "maxResults": min(result_limit, 50)}
        if page_token:
            params["pageToken"] = page_token
        response = api.request("search", "list", **params)
        channel_ids.extend(item["id"]["channelId"] for item in response.get("items", []) if item.get("id", {}).get("channelId"))
        page_token = response.get("nextPageToken")
        if not page_token:
            break
    return channel_ids


def batches(values: list[str], size: int = 50):
    for index in range(0, len(values), size):
        yield values[index:index + size]


def fetch_details(api: RotatingYouTubeApi, channel_ids: list[str], progress_callback=None) -> list[dict[str, Any]]:
    details = []
    for batch in batches(channel_ids):
        try:
            response = api.request("channels", "list", part="snippet,statistics,contentDetails", id=",".join(batch))
        except ApiKeysExhausted:
            if progress_callback:
                progress_callback("All API keys are exhausted. Finalizing creators processed so far...")
            break
        details.extend(response.get("items", []))
    return details


def fetch_recent_videos(api: RotatingYouTubeApi, playlist_id: str, count: int) -> list[dict[str, Any]]:
    response = api.request("playlistItems", "list", part="contentDetails", playlistId=playlist_id, maxResults=min(max(count, 15), 50))
    ids = [item["contentDetails"]["videoId"] for item in response.get("items", [])]
    videos = []
    for batch in batches(ids):
        response = api.request("videos", "list", part="snippet,statistics,contentDetails", id=",".join(batch))
        videos.extend(response.get("items", []))
    return videos


def evaluate_channel(api: RotatingYouTubeApi, channel: dict[str, Any], settings: dict[str, Any], relevance: list[str]) -> dict[str, Any] | None:
    snippet = channel.get("snippet", {})
    stats = channel.get("statistics", {})
    channel_id = channel["id"]
    title = snippet.get("title", "")
    description = snippet.get("description", "")
    country = snippet.get("country", "")
    subscribers = int(stats.get("subscriberCount", 0)) if stats.get("subscriberCount") else None
    if subscribers is not None and not settings["min_subscribers"] <= subscribers <= settings["max_subscribers"]:
        return None
    if country.upper() in settings["excluded_countries"]:
        return None
    uploads = channel.get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads")
    if not uploads:
        return None
    videos = fetch_recent_videos(api, uploads, settings["videos_to_check"])
    relevant_text = f"{title} {description} " + " ".join(
        f"{video.get('snippet', {}).get('title', '')} {video.get('snippet', {}).get('description', '')}" for video in videos
    )
    if relevance and not any(keyword in relevant_text.lower() for keyword in relevance):
        return None

    now = datetime.now(timezone.utc)
    long_form = []
    for video in videos:
        video_snippet = video.get("snippet", {})
        published = video_snippet.get("publishedAt")
        duration = parse_duration(video.get("contentDetails", {}).get("duration", ""))
        if not published or duration <= settings["shorts_max_seconds"]:
            continue
        published_at = datetime.fromisoformat(published.replace("Z", "+00:00"))
        if (now - published_at).days > settings["recent_days"]:
            continue
        video_stats = video.get("statistics", {})
        long_form.append({
            "title": video_snippet.get("title", "Untitled"),
            "published": published,
            "views": int(video_stats.get("viewCount", 0)),
            "likes": int(video_stats["likeCount"]) if "likeCount" in video_stats else None,
            "comments": int(video_stats["commentCount"]) if "commentCount" in video_stats else None,
        })
    long_form.sort(key=lambda item: item["published"], reverse=True)
    recent = long_form[:settings["videos_to_check"]]
    if len(recent) < settings["videos_to_check"] or any(item["views"] < settings["min_views"] for item in recent):
        return None
    engagement = []
    for video in recent:
        ratio = video["likes"] / video["views"] if video["likes"] is not None and video["views"] else None
        engagement.append("UNKNOWN" if ratio is None else "LOW" if ratio < 0.005 else "HIGH" if ratio > 0.03 else "OK")
    return {
        "channel_id": channel_id,
        "channel_name": title,
        "channel_url": f"https://www.youtube.com/channel/{channel_id}",
        "custom_url": snippet.get("customUrl", ""),
        "description": description,
        "country": country,
        "subscribers": subscribers,
        "average_recent_views": round(sum(item["views"] for item in recent) / len(recent)),
        "days_since_oldest_video": (now - datetime.fromisoformat(recent[-1]["published"].replace("Z", "+00:00"))).days,
        "engagement_flags": engagement,
        "recent_videos": recent,
    }


def export_and_save(creators: list[dict[str, Any]], keywords: dict[str, list[str]]) -> str | None:
    from apps.results.models import Creator, ResultFile

    if not creators:
        return None

    def local_video_date(value: str) -> str:
        published_at = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return django_timezone.localtime(published_at).strftime("%Y-%m-%d %H:%M:%S %Z")

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Creators"
    headers = ["Channel", "Direct YouTube Link", "Subscribers", "Country", "Avg Recent Views", "Video Views", "Latest Upload", "Days Since Oldest Video", "Engagement Flags", "Search Keywords"]
    sheet.append(headers)
    for cell in sheet[1]:
        cell.font = Font(bold=True)
    for item in creators:
        item["search_keywords"] = keywords.get(item["channel_id"], [])
        Creator.objects.create(**item)
        sheet.append([item["channel_name"], item["channel_url"], item["subscribers"], item["country"], item["average_recent_views"], ", ".join(str(video["views"]) for video in item["recent_videos"]), local_video_date(item["recent_videos"][0]["published"]), item["days_since_oldest_video"], ", ".join(item["engagement_flags"]), ", ".join(item["search_keywords"])])
    output = io.BytesIO()
    workbook.save(output)
    filename = f"youtube_creators_{django_timezone.localtime().strftime('%Y%m%d_%H%M%S')}.xlsx"
    ResultFile.objects.create(file=ContentFile(output.getvalue(), name=filename), filename=filename)
    return filename


def run_extraction(progress_callback=None) -> dict[str, Any]:
    def report(message: str) -> None:
        if progress_callback:
            progress_callback(message)

    report("Starting YouTube outreach process...")
    report("Initializing search modules...")
    api, search_keywords, relevance, settings = load_inputs(progress_callback=progress_callback)
    channel_keywords: dict[str, list[str]] = {}
    report("Searching for creators...")
    for keyword in search_keywords:
        try:
            found_channel_ids = search_channels(api, keyword, settings["result_limit"], settings["pages"])
        except ApiKeysExhausted:
            report("All API keys are exhausted. Finalizing creators processed so far...")
            break
        for channel_id in found_channel_ids:
            channel_keywords.setdefault(channel_id, []).append(keyword)
        report(f"{len(channel_keywords)} creators found")
    new_ids = [channel_id for channel_id in channel_keywords if channel_id not in settings["existing"]]
    report("Filtering and validating data...")
    creators = []
    for channel in fetch_details(api, new_ids, progress_callback=progress_callback):
        try:
            creator = evaluate_channel(api, channel, settings, relevance)
        except ApiKeysExhausted:
            report("All API keys are exhausted. Finalizing creators processed so far...")
            break
        if creator:
            creators.append(creator)
            if len(creators) >= settings["max_creators"]:
                report(f"Creator limit reached: {settings['max_creators']}")
                break
    report("Finalizing results...")
    filename = export_and_save(creators, channel_keywords)
    report(f"Found successfully: {len(creators)} new creators")
    if filename is None:
        report("No matching creators found. No result file was created.")
    else:
        report(f"Result file created: {filename}")
    report("Process completed.")
    return {"filename": filename, "found": len(creators), "searched": len(channel_keywords), "skipped_existing": len(channel_keywords) - len(new_ids)}


async def extract_from_database() -> dict[str, Any]:
    return await asyncio.to_thread(run_extraction)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract and save filtered YouTube creators.")
    parser.parse_args()
    print(json.dumps(asyncio.run(extract_from_database()), indent=2))


if __name__ == "__main__":
    main()
