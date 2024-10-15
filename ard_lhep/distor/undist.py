import numpy as np
import cv2
import matplotlib.pyplot as plt
# читать входное изображение
img = cv2.imread("lumi.png")
rows, cols, dim = img.shape
# матрица преобразования для перевода
# M = np.float32([ [1, 0, 50],
#                 [0, 1, 50],
#                 [0, 0, 1] ])
# применяем перспективное преобразование к изображению
# translated_img = cv2.warpPerspective(img, M, (cols, rows))
rows, cols = img.shape[:2]
# Define shearing matrix
M = np.float32([[1, 1, 0], [1, 1, 0]])
print("The transformation matrix is:\n", M)
# Apply shearing
sheared_img = cv2.warpAffine(img, M, (cols, rows))
cv2.imwrite('Sheared.png', sheared_img)
