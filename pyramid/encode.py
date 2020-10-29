import cv2
import matplotlib.pyplot as plt
import numpy as np


def get_median(in_list):
    """
    Args
        in_list: list
    """
    return sorted(in_list)[len(in_list) // 2]


def process(im):
    # assert im.shape[0] % 2 == 0 and im.shape[1] % 2 == 0
    new_im = np.zeros((im.shape[0]//2,im.shape[1]//2), np.uint8)

    for i in range(0, im.shape[0], 2):
        for j in range(0, im.shape[1], 2):
            median = get_median([im[i,j],im[i,j+1],im[i+1,j],im[i+1,j+1]])
            new_im[i//2, j//2] = median
    plt.imshow(new_im)
    plt.show()
    return new_im


if __name__ == "__main__":
    im = cv2.imread('data/lena.png', 0)
    plt.imshow(im)
    plt.show()
    process(im)
    process(process(im))