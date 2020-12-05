import cv2
import numpy as np

import matplotlib.pyplot as plt


def process(loaded, position_data):
    level = 0
    index = 0
    last_layer = None
    pos = 0
    m = 0
    this_data = loaded

    while index < len(loaded):
        n = (1 << level)
        this_layer = np.zeros((n, n), dtype=np.uint8)
        # this_data = loaded[index:index + n*n]

        def valid_coord(x, y):
            return n>x>=0 and n>y>=0


        for l in range(0, n, 2):
            for h in range(0, n, 2):
                xx = -1
                yy = -1

                if last_layer is not None:
                    xx = position_data[pos] & 2

                    if xx > 0:
                        xx = 1

                    yy = position_data[pos] & 1
                    this_layer[l + xx, h + yy] = last_layer[(l + xx) // 2, (h+yy) // 2]
                    pos += 1

                for t in [False, True]:
                    for k in [False, True]:
                        if int(t) == xx and int(k) == yy:
                            continue

                        i = l + int(t)
                        j = h + int(k)
                        if not valid_coord(i, j):
                            continue

                        assert m < len(this_data), print(len(this_data), m)
                        this_layer[i, j] = this_data[m]

                        m += 1

        fig = plt.figure()
        fig.set_size_inches(8.5, 8.5)

        plt.imshow(this_layer)
        plt.show()
        print(this_layer)
        level += 1
        last_layer = this_layer
        index += n*n