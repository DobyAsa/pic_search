import torch
import clip
import uuid

from PIL import Image

device = "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def get_image_features(image):
    image = preprocess(Image.open(image)).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image)
    # return a list of image features and image id
    return image_features.squeeze().tolist()
def get_image_id():
    return str(uuid.uuid1())