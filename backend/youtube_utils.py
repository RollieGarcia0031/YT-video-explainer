import re
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url: str):

    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url)

    if not match:
        raise ValueError("Invalid YouTube URL")

    return match.group(1)


def get_transcript(url: str):

    video_id = extract_video_id(url)

    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    text = " ".join([item["text"] for item in transcript])

    return text

