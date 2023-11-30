import numpy as np
import cv2 as cv
from sklearn.cluster import KMeans

IMG_PATH = r"C:\Users\aritr\Downloads\Telegram Desktop\profile_photo.png"

img = cv.imread(IMG_PATH)

img = cv.resize(img, (0, 0), fx=0.5, fy=0.5)
cv.imshow('profile_photo.png', img)

flattened = img.flatten().reshape((-1, 3))

kMeans = KMeans(n_clusters=4, n_init=50, random_state=0).fit(flattened)

colors = [[0, 49, 79], [216, 25, 33], [252, 228, 168], [252, 228, 168]]

new_flattened = np.array([colors[i] for i in kMeans.labels_])
new_image = new_flattened.reshape(img.shape).astype(np.uint8)

new_image = cv.cvtColor(new_image, cv.COLOR_RGB2BGR)
cv.imshow('new_image', new_image)
cv.waitKey(0)
