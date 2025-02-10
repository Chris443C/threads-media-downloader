import pytest
from src.ai_captioning import generate_caption

def test_generate_caption():
    image_path = "tests/test_image.jpg"
    caption = generate_caption(image_path)
    assert isinstance(caption, str) and len(caption) > 0
