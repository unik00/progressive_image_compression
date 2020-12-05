import matplotlib.pyplot as plt
import cv2

from huffman.huffman import HuffmanCoding
from pyramid import encode, decode


def data_from_txt(path):
    with open(path, "r") as decoded_f:
        decoded_data = decoded_f.readlines()[0].strip('\n')
        print(decoded_data.split(' '))
        decoded_data = [int(a) for a in decoded_data.split(' ') if a != '']
        return decoded_data


def run_huffman(path):
    compressor_im = HuffmanCoding(path)

    output_path = compressor_im.compress()
    print("Compressed file path: " + output_path)

    decom_path = compressor_im.decompress(output_path)
    print("Decompressed file path: " + decom_path)
    return decom_path


if __name__ == "__main__":
    im = cv2.imread('data/lena.bmp', 0)
    layers, positions = encode.process(im, 1)

    im_data_path = "im_data.txt"
    pos_data_path = "pos_data.txt"

    with open(im_data_path, "w") as tmp_file:
        tmp_file.write(' '.join([str(num) for num in layers]))

    with open(pos_data_path, "w") as tmp_file:
        tmp_file.write(' '.join([str(num) for num in positions]))

    decom_path = run_huffman(im_data_path)
    decoded_im_data = data_from_txt(decom_path)

    decom_path = run_huffman(pos_data_path)
    decoded_pos_data = data_from_txt(decom_path)

    print(decoded_im_data)
    print(decoded_pos_data)
    print(len(decoded_im_data))

    print(len(decoded_pos_data))
    decode.process(decoded_im_data, decoded_pos_data)