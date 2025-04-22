import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

def fft_1(x, inv=False):
    N = len(x)
    i = 1 if inv else -1
    if(N <= 1):
        return x
    
    e_k = fft_1(x[0::2], inv)
    o_k = fft_1(x[1::2], inv)

    fac = np.exp(i * 2j * np.pi * np.arange(N // 2) / N)
    return np.r_[e_k + fac * o_k, e_k - fac * o_k]

def fft_2(x, inv=False):
    r_k = np.array([fft_1(r, inv) for r in x])
    return np.array([fft_1(c, inv) for c in r_k.T]).T

def fft2_shift(x, inv=False):
    r, c = x.shape
    shift_r, shift_c = ((r + 1) // 2, (c + 1) // 2) if inv else (r // 2, c // 2)
    return np.roll(np.roll(x, shift_r, axis=0), shift_c, axis=1)

image_o = cv.imread("cat.jpg", cv.IMREAD_GRAYSCALE)
resize_fac_r, resize_fac_c = 4, 4
c_o, r_o = image_o.shape
c_o, r_o = int(c_o / resize_fac_c), int(r_o / resize_fac_r)
image = cv.resize(image_o, (r_o, c_o))

r = 1 if r_o == 0 else 2 ** (r_o - 1).bit_length()
c = 1 if c_o == 0 else 2 ** (c_o - 1).bit_length()
img = np.zeros((c, r), dtype=np.uint8)
img[:c_o, :r_o] = image[:c_o, :r_o]
img = img.astype(float)
print(image_o.shape, image.shape, img.shape)

percent = 2
a = int(r / 20 * percent ** 0.5)
b = int(c / 20 * percent ** 0.5)
r_l, r_r = r // 2 - a, r // 2 + a
c_l, c_r = c // 2 - b, c // 2 + b

img_fft = fft_2(img)
img_fft_shift = fft2_shift(img_fft)
compressed = np.zeros_like(img_fft_shift, dtype=complex)
compressed[c_l:c_r, r_l:r_r] = img_fft_shift[c_l:c_r, r_l:r_r]

img_ifft_shift = fft2_shift(compressed, inv=True)
img_ifft = fft_2(img_ifft_shift, inv=True)
img_ifft = np.real(img_ifft)
img_ifft = cv.normalize(img_ifft, None, 0, 255, cv.NORM_MINMAX).astype(np.uint8)
img_ifft_unp = img_ifft[:c_o, :r_o]

plt.subplot(2, 2, 1)
plt.title(r"Original: 100% of Original")
plt.imshow(image, cmap="gray")
plt.subplot(2, 2, 2)
plt.title(f"Compressed: {percent}% of Original")
plt.imshow(np.real(img_ifft_unp), cmap="gray")
plt.subplot(2, 2, 3)
plt.title("All Frequencies Magnitude")
plt.imshow(np.log(1 + np.abs(img_fft_shift)), cmap="gray")
plt.subplot(2, 2, 4)
plt.title("Masked Frequencies Magnitude")
plt.imshow(np.log(1 + np.abs(compressed)), cmap="gray")
plt.tight_layout()
plt.show()
