import pytesseract
import requests
from PIL import Image
from PIL import ImageFilter
from StringIO import StringIO
import cv2
import numpy as np


def process_image(url):
    image = _get_image(url)
    image.filter(ImageFilter.SHARPEN)
    return pytesseract.image_to_string(image)

def process_image_data(data):
    # convert string of image data to uint8
    nparr = np.fromstring(data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # build a response dict to send back to client
    return {
        'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0]),
        'data': pytesseract.image_to_data(img)
        }


def _get_image(url):
    return Image.open(StringIO(requests.get(url).content))
