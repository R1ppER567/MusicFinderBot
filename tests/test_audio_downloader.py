import unittest
from unittest.mock import patch, MagicMock
from services.audio_downloader import (
    get_audio_info, 
    download_audio_stream, 
    download_audio, 
    AudioDownloadError
)


class TestAudioDownloader(unittest.TestCase):
    @patch('services.audio_downloader.subprocess.run')
    def test_get_audio_info_success(self, mock_run):
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "Test Title\n120"

        title, duration = get_audio_info("http://example.com")
        self.assertEqual(title, "Test Title")
        self.assertEqual(duration, 120)

    @patch('services.audio_downloader.subprocess.run')
    def test_get_audio_info_failure(self, mock_run):
        mock_run.return_value.returncode = 1
        with self.assertRaises(AudioDownloadError):
            get_audio_info("http://example.com")

    @patch('services.audio_downloader.subprocess.run')
    def test_get_audio_info_too_long(self, mock_run):
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "Test Title\n1000"
        with self.assertRaises(AudioDownloadError):
            get_audio_info("http://example.com")

    @patch('services.audio_downloader.subprocess.Popen')
    def test_download_audio_stream_success(self, mock_popen):
        mock_process = MagicMock()
        mock_process.communicate.return_value = (b'binarydata', b'')
        mock_process.returncode = 0
        mock_popen.return_value = mock_process

        result = download_audio_stream("http://example.com")
        self.assertEqual(result, b'binarydata')

    @patch('services.audio_downloader.subprocess.Popen')
    def test_download_audio_stream_failure(self, mock_popen):
        mock_process = MagicMock()
        mock_process.communicate.return_value = (b'', b'Error message')
        mock_process.returncode = 1
        mock_popen.return_value = mock_process

        with self.assertRaises(AudioDownloadError):
            download_audio_stream("http://example.com")

    @patch('services.audio_downloader.download_audio_stream')
    @patch('services.audio_downloader.get_audio_info')
    def test_download_audio_success(self, mock_info, mock_stream):
        mock_info.return_value = ("Test Song", 100)
        mock_stream.return_value = b'binarydata'

        data, error = download_audio("http://example.com")
        self.assertIsNone(error)
        self.assertEqual(data['title'], "Test Song")
        self.assertEqual(data['duration'], 100)
        self.assertEqual(data['audio'], b'binarydata')

    @patch('services.audio_downloader.get_audio_info')
    def test_download_audio_info_error(self, mock_info):
        mock_info.side_effect = AudioDownloadError("bad info")
        data, error = download_audio("http://example.com")
        self.assertIsNone(data)
        self.assertEqual(error, "bad info")

    @patch('services.audio_downloader.get_audio_info')
    @patch('services.audio_downloader.download_audio_stream')
    def test_download_audio_stream_error(self, mock_stream, mock_info):
        mock_info.return_value = ("Test Song", 100)
        mock_stream.side_effect = AudioDownloadError("stream fail")
        data, error = download_audio("http://example.com")
        self.assertIsNone(data)
        self.assertEqual(error, "stream fail")


if __name__ == '__main__':
    unittest.main()
