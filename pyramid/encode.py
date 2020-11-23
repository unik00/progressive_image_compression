import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import cdist, euclidean

from pyramid.utils import *


def geometric_median(in_list):
    chosen = in_list[0]
    ans_sum = 1e9

    for val, coord in in_list:
        sum = 0
        for val2, coord2 in in_list:
            sum += euclidean(val, val2)
        if sum < ans_sum:
            chosen = (val, coord)
            ans_sum = sum

    return chosen


def process(im, level):
    """
    Args:
        im: numpy 2D array, type np.uint8
        level: integer
    Returns:
        new_im
    """
    if level == 1:
        cv2.imwrite("output/0.jpg", im)

        plt.imshow(im)
        plt.show()

    print("im shape: ", im.shape)

    new_im = np.zeros(((im.shape[0] + 1) // 2, (im.shape[1] + 1) // 2, 3), np.uint8)
    compressed_layer = list()

    def valid_coord(x, y):
        return im.shape[0] > x >= 0 and im.shape[1] > y >= 0

    for i in range(0, im.shape[0], 2):
        for j in range(0, im.shape[1], 2):
            this_im = list()
            for t in [False, True]:
                for k in [False, True]:
                    if valid_coord(i + int(t), j + int(k)):
                        this_im.append((im[i + int(t), j + int(k)], (t, k)))

            median, coord = geometric_median(this_im)

            compressed_group = list()
            for t in [False, True]:
                for k in [False, True]:
                    if valid_coord(i + int(t), j + int(k)):
                        if (t, k) == coord:
                            compressed_group.append((t, k))
                        else:
                            compressed_group.append((im[i + int(t), j + int(k)]))

            # print(i, j)
            # print(compressed_group)

            compressed_layer += compressed_group
            new_im[i // 2, j // 2, :] = median

    cv2.imwrite("output/{}.jpg".format(level), new_im)
    plt.imshow(new_im)
    plt.show()

    if im.shape == (1, 1, 3):
        return [im[0, 0]]
    print("compressed layer:\n ", compressed_layer)
    print("im: \n", im)
    return process(new_im, level + 1) + compressed_layer


if __name__ == "__main__":
    im = cv2.imread('data/lena_color.jpg')
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    compressed = process(im, 1)
    # print(bytes(compressed))
    save_obj(compressed, "compressed")
