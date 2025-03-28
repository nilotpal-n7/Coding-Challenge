import numpy as np

a = np.arange(3)
print(a)
b = np.arange(1, 3, 0.1, dtype=int)
print(b)
c = np.array([[1,2,3]])
print(c.T)
print(c.shape, c.T.shape)
print(c.dot(c.T))