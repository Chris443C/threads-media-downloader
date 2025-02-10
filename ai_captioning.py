import torch
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
from PIL import Image

# Load the pre-trained model
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

# Set the model to evaluation mode
model.eval()

def generate_caption(image_path, max_length=16, num_beams=4):
    """
    Generates a caption for the given image.

    Args:
        image_path (str): Path to the image file.
        max_length (int): Maximum length of the generated caption.
        num_beams (int): Number of beams for beam search.

    Returns:
        str: Generated caption for the image.
    """
    # Load and preprocess the image
    image = Image.open(image_path)
    if image.mode != "RGB":
        image = image.convert(mode="RGB")
    pixel_values = feature_extractor(images=image, return_tensors="pt").pixel_values

    # Generate caption
    with torch.no_grad():
        output_ids = model.generate(pixel_values, max_length=max_length, num_beams=num_beams)
    caption = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return caption
