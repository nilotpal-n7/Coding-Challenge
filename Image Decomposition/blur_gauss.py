import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

def gauss(s):
    a = np.zeros((s,s))
    u = np.array([s//2, s//2])

    def get(index, u):
        idx = np.array([index[0], index[1]])
        exp_t = idx - u
        return np.pow(2 * np.pi, -s / 2) * np.exp(-0.5 * exp_t.dot(exp_t.T))
    
    weight = np.array([[get((x,y), u) for y in range(s)] for x in range(s)])
    return weight / np.sum(weight)

def show(img, s):
    x, y = img.shape
    g = gauss(s)
    blur = img

    for i in range(s//2, x - s//2):
        for j in range(s//2, y - s//2):
            blur[i, j] = np.sum(img[i - s//2:i + s//2 + 1, j - s//2: j + s//2 + 1] * g)

    blur = cv.normalize(blur, None, 0, 255, cv.NORM_MINMAX).astype(np.uint8)
    cv.imshow(f"Blur: {s}", blur)

image = cv.imread("cat.jpg", cv.IMREAD_GRAYSCALE)
image = cv.resize(image, (512, 512))
img = image.astype(float)

cv.imshow("Cat", image)
for s in [3, 5, 9, 13, 23, 27, 51]:
    show(img, s)
cv.waitKey(0)
