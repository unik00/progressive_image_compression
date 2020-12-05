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
        cv2.imwrite("output/0.bmp", im)

        # plt.imshow(im)
        # plt.show()

    # print("im shape: ", im.shape)

    new_im = np.zeros(((im.shape[0] + 1) // 2, (im.shape[1] + 1) // 2), np.uint8)
    compressed_layer = list()

    def valid_coord(x, y):
        return im.shape[0] > x >= 0 and im.shape[1] > y >= 0

    positions = list()

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
                        if (t, k) == coord:
                            removed_position = (int(t)<<1) + int(k)
                        else:
                            compressed_group.append((im[i + int(t), j + int(k)]))
            # compressed_group = [removed_position] + compressed_group
            positions.append(removed_position)

            # print(i, j)
            # print(compressed_group)

            compressed_layer += compressed_group
            new_im[i // 2, j // 2] = median

    cv2.imwrite("output/{}.bmp".format(level), new_im)
    # plt.imshow(new_im)
    # plt.show()

    if im.shape == (1, 1):
        return [list([im[0, 0]]), list([])]

    next_level = process(new_im, level + 1)

    print("compressed layer:\n ", compressed_layer)
    print("position:\n", positions)

    # print("im: \n", im)
    print("next level: \n", next_level)
    return list(next_level[0]) + list(compressed_layer), list(next_level[1]) + list(positions)


if __name__ == "__main__":
    im = cv2.imread('data/lena.bmp', 0)

    # rList = []
    # for i in range(im.shape[0]):
    #     for j in range(im.shape[1]):
    #         rList.append(im[i, j])
    #
    # new_file = open("data_bin.bin", "wb")
    # arr = bytearray(rList)
    # new_file.write(arr)

    compressed = process(im, 1)

    # save_obj(compressed, "compressed")
    # print("compressed: \n\n")
    print(*compressed)
    # new_file = open("data_bin.bin", "wb")
    # arr = bytearray(compressed)
    # new_file.write(arr)