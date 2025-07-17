import subprocess

def download_audio(url: str) -> tuple[dict | None, str | None]:
    """Downloads audio from the given URL using yt-dlp and 
    returns its metadata and data.

    This function first retrieves the title and duration of the audio using yt-dlp.
    If the duration exceeds 10 minutes or an error occurs during metadata retrieval or
    downloading, an error message is returned instead.

    Args:
        url (str): The URL of the media to download audio from.

    Returns:
        tuple[dict | None, str | None]: 
            - A dictionary containing:
                - 'title' (str): The title of the audio.
                - 'duration' (int): The duration in seconds.
                - 'audio' (bytes): The raw audio data.
            - An error message (str) if something went wrong, otherwise None.
    """
    info_cmd = ['yt-dlp', '--print', 'title', '--print', 'duration', url]
    info_result = subprocess.run(info_cmd, capture_output=True, text=True)
    
    if info_result.returncode != 0:
        return None, 'Error retrieving information'
    
    lines = info_result.stdout.strip().split('\n')
    title = lines[0] if lines else "Unknown"
    duration = int(lines[1]) if len(lines) > 1 and lines[1].isdigit() else 0
    
    if duration > 600:  # 10 minutes
        return None, 'The track is too long'
    
    download_cmd = ['yt-dlp', '-f', 'bestaudio[ext=m4a]', '-o', '-', url]
    
    process = subprocess.Popen(download_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    audio_data, error = process.communicate()
    
    if process.returncode != 0:
        return None, f'Download error: {error.decode()}'
    
    return {
        'title': title,
        'duration': duration,
        'audio': audio_data
    }, None


# For testing
if __name__ == '__main__':
    url = str(input('Input the track url: ')).strip()
    result, error = download_audio(url)

    if error:
        print(f"Error: {error}")
    else:
        print('Title:', result['title'])
        print('Duration:', result['duration'], 's')
        with open(f'{result['title']}.m4a', 'wb') as f:
            f.write(result['audio'])
        print(f'Audio saved as {result['title']}.m4a')
