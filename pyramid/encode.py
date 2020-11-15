import cv2
import matplotlib.pyplot as plt
import numpy as np

from pyramid.utils import *


def get_median(in_list):
    """
    Args
        in_list: list of tuples (value, coordinate)
    """
    return sorted(in_list)[len(in_list) // 2]


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

    new_im = np.zeros(((im.shape[0] + 1) // 2, (im.shape[1] + 1) // 2), np.uint8)
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

            median, coord = get_median(this_im)

            compressed_group = list()
            for t in [False, True]:
                for k in [False, True]:
                    if valid_coord(i + int(t), j + int(k)):
                        # if (t, k) == coord:
                        #     compressed_group.append((t, k))
                        # else:

                        compressed_group.append((im[i + int(t), j + int(k)]))

            print(i, j)
            print(compressed_group)

            compressed_layer += compressed_group
            new_im[i // 2, j // 2] = median

    cv2.imwrite("output/{}.jpg".format(level), new_im)
    plt.imshow(new_im)
    plt.show()

    if im.shape == (1, 1):
        return [im[0, 0]]
    print("compressed layer:\n ", compressed_layer)
    print("im: \n", im)
    return process(new_im, level + 1) + compressed_layer


if __name__ == "__main__":
    im = cv2.imread('data/sample.jpg', 0)

    compressed = process(im, 1)
    # print(bytes(compressed))
    save_obj(compressed, "compressed")
