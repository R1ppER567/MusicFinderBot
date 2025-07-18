import subprocess
from typing import Optional

from common.consts import DURATION_LIMIT

class AudioDownloadError(Exception):
    """Custom exception for audio download errors."""


def get_audio_info(url: str) -> tuple[str, int]:
    """Retrieves the title and duration of a YouTube video using yt-dlp.

    Args:
        url (str): The URL of the video.

    Returns:
        tuple: (title, duration in seconds)

    Raises:
        AudioDownloadError: If info can't be retrieved or duration is too long.
    """
    info_cmd = ['yt-dlp', '--config-location', 'yt-info.conf', url]
    result = subprocess.run(info_cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise AudioDownloadError('Error retrieving video information.')

    lines = result.stdout.strip().split('\n')
    title = lines[0] if lines else "Unknown"
    duration = int(lines[1]) if len(lines) > 1 and lines[1].isdigit() else 0

    if duration > DURATION_LIMIT:
        raise AudioDownloadError(f'The track is too long (more than {
            seconds_to_ms(DURATION_LIMIT)
        }).')

    return title, duration


def download_audio_stream(url: str) -> bytes:
    """Downloads raw audio data from the given URL using yt-dlp.

    Args:
        url (str): The URL of the video.

    Returns:
        bytes: Raw audio data.

    Raises:
        AudioDownloadError: If download fails.
    """
    download_cmd = ['yt-dlp', '--config-location', 'yt-download.conf', url]
    process = subprocess.Popen(download_cmd, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )
    audio_data, error = process.communicate()

    if process.returncode != 0:
        raise AudioDownloadError(f'Download failed: {error.decode().strip()}')

    return audio_data


def download_audio(url: str) -> tuple[Optional[dict], Optional[str]]:
    """Downloads audio and returns its metadata and binary data.

    Args:
        url (str): The URL of the video.

    Returns:
        tuple: 
            - dict: {'title', 'duration', 'audio'} if successful
            - str: error message if failed
    """
    try:
        title, duration = get_audio_info(url)
        audio_data = download_audio_stream(url)
        return {
            'title': title, 
            'duration': duration, 
            'audio': audio_data
        }, None
    except AudioDownloadError as e:
        return None, str(e)


def seconds_to_ms(seconds: int) -> str:
    minutes, secs = divmod(seconds, 60)
    return f"{minutes}:{secs:02d}"
