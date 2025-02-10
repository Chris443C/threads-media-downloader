import os
from nsfw_detector import predict

# Load the pre-trained NSFW model
model_path = os.path.join(os.path.dirname(__file__), 'nsfw_mobilenet2.224x224.h5')
model = predict.load_model(model_path)

def is_image_nsfw(image_path, threshold=0.7):
    """
    Determines if an image contains NSFW content.

    Args:
        image_path (str): Path to the image file.
        threshold (float): Confidence threshold for NSFW classification.

    Returns:
        bool: True if the image is NSFW, False otherwise.
    """
    predictions = predict.classify(model, image_path)
    nsfw_score = predictions[image_path].get('nsfw', 0)
    return nsfw_score >= threshold
