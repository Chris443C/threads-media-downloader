import pytest
from src.threads_downloader import download_file

def test_download_file():
    url = "https://example.com/test.jpg"
    output_folder = "tests_output"
    assert download_file(url, output_folder) is True
