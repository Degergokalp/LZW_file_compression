# LZW_file_compression
LZW file compression and decompression

The compress_file(file_path) function takes a file path as an input and compresses the file using LZW compression with adaptive code length. The function reads the contents of the file, initializes a dictionary with ASCII characters, and compresses the data using LZW algorithm.

The function then pads the output with zeros to make it a multiple of 8 bits, adds the number of padding bits to the beginning of the output, converts the output list to a binary string, and writes it to a binary file. Finally, the function calculates the code length and compression ratio and returns the path to the compressed file, code length, and compression ratio.

The decompress_file(file_path) function takes a file path as an input and decompresses the file that was compressed using LZW compression with adaptive code length. The function reads the contents of the compressed file, converts the compressed data to a binary string, extracts the number of padding bits from the beginning of the binary string, removes the padding bits, and decompresses the data using LZW algorithm. The function then writes the output to a text file.
