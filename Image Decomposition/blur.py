import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

def gauss(s):
    sigma = s / 6
    sz = np.linspace(-(s // 2), s // 2, s)
    x, y = np.meshgrid(sz, sz)
    ker = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    return ker / np.sum(ker)

def show(img, s, p):
    x, y = img.shape
    g = gauss(s)
    blur = img[:,:]

    for i in range(s//2, x - s//2):
        for j in range(s//2, y - s//2):
            blur[i, j] = np.sum(img[i - s//2:i + s//2 + 1, j - s//2: j + s//2 + 1] * g)

    plt.subplot(2,3,p)
    plt.title(f"Blur: {s}")
    plt.imshow(blur, cmap="gray")

image = cv.imread("cat.jpg", cv.IMREAD_GRAYSCALE)
img = image.astype(float)

for i, s in enumerate([1, 17, 39, 63, 87, 101]):
    show(img, s, i + 1)
plt.show()
