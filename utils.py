import numpy as np
import torch
from PIL import Image
import requests
import io

def img_tensor_to_np(img_tensor):
    img_tensor = img_tensor.clone() * 255.0
    return img_tensor.squeeze().numpy().astype(np.uint8)

def img_np_to_tensor(img_np_list):
    return torch.from_numpy(img_np_list.astype(np.float32) / 255.0).unsqueeze(0)


def pillow2bin(image):
    stream = io.BytesIO()
    image.save(stream, format='PNG')
    binary_data = stream.getvalue()
    stream.close()
    return binary_data

def bin_to_pillow(bin_data):
    image_stream = io.BytesIO(bin_data)
    img = Image.open(image_stream)
    return img

def read_image(url):
    response = requests.get(url)
    image = Image.open(io.BytesIO(response.content))
    image = image
    return image

