import numpy as np
import cv2 as cv
from sklearn.cluster import KMeans

def get_file_ext(filename: str):
    return filename.split('.')[-1]


darkBlue = (0, 51, 76)
red = (217, 26, 33)
lightBlue = (112, 150, 158)
yellow = (252, 227, 166)


def filter_obama(img_arr):
    img = np.asarray((img_arr), dtype="uint8")
    img = cv.imdecode(img, cv.IMREAD_COLOR)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if sum(img[i, j]) < 182:
                img[i, j] = darkBlue
            elif sum(img[i, j]) < 364:
                img[i, j] = red
            elif sum(img[i, j]) < 460:
                img[i, j] = lightBlue
            else:
                img[i, j] = yellow
    img = cv.cvtColor(img, cv.COLOR_RGB2BGR)
    img = cv.imencode('.jpg', img)[1].tobytes()
    return img

def filter_gray():
    pass

image_filters = {
    'obama': filter_obama,
    'gray': filter_gray,
}

