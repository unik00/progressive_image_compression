import cv2
import matplotlib.pyplot as plt
import numpy as np


def get_median(in_list):
    """
    Args
        in_list: list
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
    print("im shape: ", im.shape)
    if im.shape[0] * im.shape[1] == 0:
        # TODO: mất bit
        return []


    new_im = np.zeros(((im.shape[0] + 1)//2,(im.shape[1]+1)//2), np.uint8)


    for i in range(0, im.shape[0], 2):
        for j in range(0, im.shape[1], 2):
            median_list = []
            median_list.append(im[i,j])
            if j+1 < im.shape[1]: median_list.append(im[i,j+1])
            if i+1 < im.shape[0]: median_list.append(im[i+1,j])
            if i+1<im.shape[0] and j+1<im.shape[1]: median_list.append(im[i+1,j+1])
            median = get_median(median_list)
            new_im[i//2, j//2] = median

    # cv2.imwrite("{}.jpg".format(level), new_im)
    plt.imshow(new_im)
    plt.show()

    if new_im.shape != im.shape:
        process(new_im, level + 1)
    return new_im


if __name__ == "__main__":
    im = cv2.imread('data/sample.jpg', 0)
    # plt.imshow(im)
    # plt.show()
    process(im, 1)
