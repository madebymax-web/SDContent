"""Stage 10: publish the finished render to YouTube and Instagram.

YouTube: resumable upload via the YouTube Data API v3 (requires OAuth —
config/youtube_client_secret.json + a stored token, see .env.example and
docs/09 Phase 0 setup).

Instagram: Graph API publishing requires the finished video to already be
reachable at a PUBLIC URL (Instagram fetches it server-side, it does not
accept a raw file upload) — see MEDIA_HOST_* in .env.example. Requires a
Business/Creator IG account linked to a Facebook Page and an approved app
(Meta's review process — start early, see docs/09).
"""
from __future__ import annotations

import time
from pathlib import Path

import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from pipeline.config import Config

YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
GRAPH_API_BASE = "https://graph.facebook.com/v19.0"


# --- YouTube -----------------------------------------------------------------

def _youtube_client(config: Config):
    token_path = Path(config.raw["publishing"].get("youtube_token_file", "config/youtube_token.json"))
    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), YOUTUBE_SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            config.env("YOUTUBE_CLIENT_SECRETS_FILE"), YOUTUBE_SCOPES
        )
        creds = flow.run_local_server(port=0)  # one-time interactive auth
        token_path.write_text(creds.to_json())
    return build("youtube", "v3", credentials=creds)


def upload_to_youtube(
    config: Config,
    video_path: Path,
    title: str,
    description: str,
    tags: list[str],
    is_short: bool,
    publish_at_iso: str | None = None,
) -> str:
    youtube = _youtube_client(config)
    body = {
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": tags,
            "categoryId": "27",  # Education
        },
        "status": {
            "privacyStatus": "private" if publish_at_iso else "public",
            "selfDeclaredMadeForKids": False,
        },
    }
    if publish_at_iso:
        body["status"]["publishAt"] = publish_at_iso

    media = MediaFileUpload(str(video_path), chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = None
    while response is None:
        status, response = request.next_chunk()
    return response["id"]


# --- Instagram -----------------------------------------------------------------

def publish_to_instagram(config: Config, public_video_url: str, caption: str) -> str:
    ig_account_id = config.env("IG_BUSINESS_ACCOUNT_ID")
    access_token = config.env("IG_ACCESS_TOKEN")

    create_resp = requests.post(
        f"{GRAPH_API_BASE}/{ig_account_id}/media",
        data={
            "media_type": "REELS",
            "video_url": public_video_url,
            "caption": caption,
            "access_token": access_token,
        },
        timeout=60,
    )
    create_resp.raise_for_status()
    container_id = create_resp.json()["id"]

    # Poll until the container finishes processing before publishing.
    for _ in range(30):
        status_resp = requests.get(
            f"{GRAPH_API_BASE}/{container_id}",
            params={"fields": "status_code", "access_token": access_token},
            timeout=30,
        )
        status_resp.raise_for_status()
        if status_resp.json().get("status_code") == "FINISHED":
            break
        time.sleep(10)
    else:
        raise RuntimeError("Instagram media container never finished processing.")

    publish_resp = requests.post(
        f"{GRAPH_API_BASE}/{ig_account_id}/media_publish",
        data={"creation_id": container_id, "access_token": access_token},
        timeout=60,
    )
    publish_resp.raise_for_status()
    return publish_resp.json()["id"]


if __name__ == "__main__":
    print("Run via pipeline.orchestrator — needs a finished render + upload target as inputs.")
