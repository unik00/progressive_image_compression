import cv2
import numpy as np

import matplotlib.pyplot as plt

from pyramid.utils import load_obj


if __name__ == '__main__':
    loaded = load_obj('compressed')
    print(loaded[:10])

    level = 0
    index = 0
    last_layer = None

    while index < len(loaded):

        n = (1 << level)
        this_layer = np.zeros((n, n), dtype=np.uint8)
        this_data = loaded[index:index + n*n]
        print("this data")
        print(this_data)

        def valid_coord(x, y):
            return n>x>=0 and n>y>=0

        m = 0
        for l in range(0, n, 2):
            for h in range(0, n, 2):
                for t in [False, True]:
                    for k in [False, True]:
                        i = l + int(t)
                        j = h + int(k)
                        if not valid_coord(i, j):
                            continue

                        print(this_data[m])

                        if type(this_data[m]) == tuple:
                            # use data of previous layer
                            this_layer[i, j] = 255
                        else:
                            this_layer[i, j] = this_data[m]

                        m += 1

        plt.imshow(this_layer)
        plt.show()
        print(this_layer)
        level += 1
        last_layer = this_layer
        index += n*n