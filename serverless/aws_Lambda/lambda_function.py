import json
from threads_downloader import download_media
from ai_nsfw_detection import is_image_nsfw
from ai_captioning import generate_caption

def lambda_handler(event, context):
    """
    AWS Lambda handler function.

    Args:
        event (dict): Input event data.
        context (object): Runtime information.

    Returns:
        dict: Response object.
    """
    try:
        # Extract URL from the event
        media_url = event.get('media_url')
        if not media_url:
            return {
                'statusCode': 400,
                'body': json.dumps('media_url is required in the event')
            }

        # Download media
        media_path = download_media(media_url)

        # Perform NSFW detection
        if is_image_nsfw(media_path):
            return {
                'statusCode': 403,
                'body': json.dumps('The provided media contains NSFW content.')
            }

        # Generate caption
        caption = generate_caption(media_path)

        return {
            'statusCode': 200,
            'body': json.dumps({'caption': caption})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error processing media: {str(e)}')
        }
