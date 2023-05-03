from lzw import compress_file,decompress_file
import os


# Compress a file
compressed_file_path = compress_file('input.txt')

# Decompress the compressed file
decompressed_file_path = decompress_file(compressed_file_path)

# Compare the original and restored text
with open(os.path.splitext('input')[0] + '.txt', 'r') as original_file:
    with open(decompressed_file_path, 'r') as decompressed_file:
        original = original_file.read()
        decompressed = decompressed_file.read()
        if original != decompressed:
            print("Decompressed file is different from the original file.")
        else:
            print('Decompressed file is same from the original file.')


