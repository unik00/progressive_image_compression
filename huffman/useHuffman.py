from .huffman import HuffmanCoding
import sys


if __name__ == "__main__":
	path = "data.txt"

	with open(path, 'r') as f:
		lines = f.readlines()
		lines = lines[0].strip('\n').split(' ')
		lines = [int(n) for n in lines]


	print(len(lines))

	# new_file = open("data_bin.bin", "wb")
	# arr = bytearray(lines)
	# new_file.write(arr)

	h = HuffmanCoding(path)

	output_path = h.compress()
	print("Compressed file path: " + output_path)

	decom_path = h.decompress(output_path)
	print("Decompressed file path: " + decom_path)