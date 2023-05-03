from io import StringIO
import os

import math

import os
import math

dict_size = 256
dictionary = {chr(i): i for i in range(dict_size)}
global_codeLen=0

def int_array_to_binary_string(int_array, codelength = 12):
    
    bitstr = ""
    total_bits = 0
    for num in int_array:
        for n in range(codelength):
            if num & (1 << (codelength - 1 - n)):
                bitstr += "1"
            else:
                bitstr += "0"
            total_bits += 1
    #print("total number of bits: ", total_bits)
    return (bitstr)
def remove_padding(codelength, padded_encoded_text):
    padded_info = padded_encoded_text[:8]
    extra_padding = int(padded_info, 2)
    padded_encoded_text = padded_encoded_text[8:]
    encoded_text = padded_encoded_text[:-1 * extra_padding]
    int_codes = []
    for bits in range(0, len(encoded_text),codelength):
        int_codes.append(int(encoded_text[bits:bits+codelength],2))
    return int_codes

def compress_file(file_path):
    """Compress a file using LZW compression with adaptive code length."""

    import os
    import math

    # Open input file and read content
    with open(file_path, 'r') as file:
        uncompressed = file.read()

    # Initialize the dictionary with the ASCII characters
    global dictionary
    global dict_size
    global global_codeLen

    # Initialize the current code length and the maximum code length
    curr_code_length = 9
    max_code_length = 16

    # Initialize the current string and the output list
    curr_string = ""
    output = []

    # Loop through each character in the uncompressed data
    for c in uncompressed:
        # Get the next string by adding the current character to the current string
        next_string = curr_string + c

        # If the next string is in the dictionary, update the current string and continue
        if next_string in dictionary:
            curr_string = next_string
            continue

        # Add the code for the current string to the output list
        output.append(dictionary[curr_string])

        # Add the next string to the dictionary with a new code
        dictionary[next_string] = dict_size
        dict_size += 1

        # If the dictionary is full, increase the code length
        if dict_size >= 2 ** curr_code_length and curr_code_length < max_code_length:
            curr_code_length += 1

        # Set the current string to the current character
        curr_string = c

    # Add the code for the final string to the output list
    output.append(dictionary[curr_string])
    
    # Pad the output with zeros to make it a multiple of 8 bits
    num_padding_bits = (8 - len(output) % 8) % 8
    output += [0] * num_padding_bits

    # Add the number of padding bits to the beginning of the output
    output = [num_padding_bits] + output
    
    # Convert the output list to a binary string
    binary_str = ''.join([format(code, '0{}b'.format(curr_code_length)) for code in output])
    
    # Convert the binary string to bytes and write it to a binary file
    compressed_file_path = os.path.splitext(file_path)[0] + '.lzw'
    with open(compressed_file_path, 'wb') as file:
        num_bytes = int(math.ceil(len(binary_str) / 8))
        
        for i in range(num_bytes):
            byte_str = binary_str[i*8:(i+1)*8].rjust(8, '0')
            byte = int(byte_str, 2)
            file.write(byte.to_bytes(1, byteorder='big'))
        

    # Calculate code length and compression ratio
    uncompressed_size = os.path.getsize(file_path)
    compressed_size = os.path.getsize(compressed_file_path)
    
    code_length = len(binary_str)
    global_codeLen=code_length
    compression_ratio = compressed_size / uncompressed_size
    print('COMPRESS SIZE:',compressed_size,'code length:',code_length,'compression_ratio:',compression_ratio)

    
    # Return the path to the compressed file, code length, and compression ratio
    return compressed_file_path



def decompress_file(file_path):
    """Decompress a file that was compressed using LZW compression with adaptive code length."""

    # Open the compressed file and read the content
    with open(file_path, 'rb') as file:
        compressed = file.read()
    global dictionary
    global dict_size
    global global_codeLen
    # Convert the compressed data to a binary string
    binary_str = ''.join([format(byte, '08b') for byte in compressed])
    

    int_list = []

    for i in range(0, len(binary_str), 9):
        chunk = binary_str[i:i+9]
        int_value = int(chunk, 2)
        int_list.append(int_value)
    
    

    n = int_list[0]
    int_list = int_list[:-n-1]
    int_list = int_list[1:]
    
    output = ""
    for nums in int_list:
        pair=[key for key, value in dictionary.items() if value == nums]
        output=output+pair[0]
   
   
    # Write the output to a text file
    decompressed_file_path = os.path.splitext(file_path)[0] + '_decompressed.txt'
    with open(decompressed_file_path, 'w') as file:
        file.write(output)

    # Return the path to the decompressed file
    return decompressed_file_path

# Compress a file
compressed_file_path = compress_file('input.txt')
decompressed_file_path=decompress_file('input.lzw')
# Decompress the compressed file


with open('input.txt', 'r') as file1, open(decompressed_file_path, 'r') as file2:
    original_text = file1.read()
    decompressed_text = file2.read()

assert original_text == decompressed_text