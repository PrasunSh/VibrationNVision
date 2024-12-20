import cv2
import numpy as np
from ix_iy_it_calc import calcIxIyIt
from scipy.ndimage import convolve
from quiver import draw_quiver


def computeHS(img1, img2, alpha):
    gimg1  = cv2.GaussianBlur(img1, (5, 5), 0)
    gimg2  = cv2.GaussianBlur(img2, (5, 5), 0)

    u = np.zeros((img1.shape[0], img1.shape[1]))
    v = np.zeros((img1.shape[0], img1.shape[1]))
    Ix, Iy, It = calcIxIyIt(gimg1, gimg2)
    avg_kernel = np.array([[1 / 12, 1 / 6, 1 / 12],
                            [1 / 6, 0, 1 / 6],
                            [1 / 12, 1 / 6, 1 / 12]], float)
    
    iter_count = 0

    while True:
        iter_count += 1
        u_avg = convolve(u, avg_kernel)
        v_avg = convolve(v, avg_kernel)
        p = Ix * u_avg + Iy * v_avg + It
        d = alpha**2 + Ix**2 + Iy**2

        u = u_avg - Ix * (p / d)
        v = v_avg - Iy * (p / d)

        if iter_count >50 :
            break

    draw_quiver(u, v , img1)

    
if __name__ == "__main__":
    img1path = r"C:\Users\prasu\Desktop\testthis1.png"
    img2path = r"C:\Users\prasu\Desktop\testthis2.png"
    img1 =cv2.imread(img1path, cv2.IMREAD_GRAYSCALE).astype(float)

    img2 =cv2.imread(img2path, cv2.IMREAD_GRAYSCALE).astype(float)

    computeHS(img1, img2, 25)