import json
from flask import Flask, request, jsonify
from threads_downloader import download_media
from ai_nsfw_detection import is_image_nsfw
from ai_captioning import generate_caption

app = Flask(__name__)

@app.route('/process_media', methods=['POST'])
def process_media():
    """
    HTTP endpoint to process media.

    Returns:
        Response object.
    """
    try:
        data = request.get_json()
        media_url = data.get('media_url')
        if not media_url:
            return jsonify({'error': 'media_url is required'}), 400

        # Download media
        media_path = download_media(media_url)

        # Perform NSFW detection
        if is_image_nsfw(media_path):
            return jsonify({'error': 'The provided media contains NSFW content.'}), 403

        # Generate caption
        caption = generate_caption(media_path)

        return jsonify({'caption': caption}), 200

    except Exception as e:
        return jsonify({'error': f'Error processing media: {str(e)}'}), 500
