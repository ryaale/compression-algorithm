'''
Decompression

Author: Alexander Ryan

This program takes a compressed file and decompresses the file back
to its original state. The input is any compressed .txt file and the
output is the .txt in its decompressed normal form.

'''
# Get header information
def get_header_info(compressed_contents):
    '''
    Retrieves the number of mappings and ngram size from a compressed text file. 
    The number of mappings is the first value of the string compressed contents, 
    so hence we take the slice from the string.
        e.g. compressed_contents[0]
    The ngram size is the second value, so we take the second slice.
        e.g. compressed_contents[1]
    We then use ord() to convert the Unicode object into an integer.
    
    Parameters:
    
        compressed_contents: A file that has been compressed 
        with a particular ngram size, using the function 
        compress_file in the compress.py program.
    
    Result:
    
        A two element tuple of integers. The first integer 
        represents the number of mappings, the number of ngrams 
        that have been swapped with an encoding byte from the 
        original uncompressed text file.
        The second integer represents the size of each 
        ngram that is being represented by each encoding byte.
    
    '''
    number_mappings = ord(compressed_contents[0])
    ngram_size = ord(compressed_contents[1])
    return (number_mappings, ngram_size)


# Parse the header
def parse_header(compressed_contents):
    
    '''
    Parameters:
    
        compressed_contents: A file that has been compressed 
        with a particular ngram size, using the function 
        compress_file in the compress.py program.
    
    Result:
    
        A dictionary that represents the mapping in the header of the compressed contents.
    
    '''
    number_mappings = get_header_info(compressed_contents)[0]
    ngram_size = get_header_info(compressed_contents)[1]
    
    decode_map = {}    #the dictionary is called decode_map
    index1 = 2
    index2 = 2 + ngram_size
    index3 = 2 + ngram_size
    while index3 < (number_mappings * (ngram_size + 1) + ngram_size + 1):
        decode_map[compressed_contents[index3]] = compressed_contents[index1:index2]
        index1 += (ngram_size + 1)
        index2 += (ngram_size + 1)
        index3 += (ngram_size + 1)
    return decode_map
                    
# Get the compressed body
def get_compressed_body(compressed_contents):
    
    '''
    Parameters:
    
        compressed_contents: A file that has been compressed 
        with a particular ngram size, using the function 
        compress_file in the compress.py program.
    
    '''
    number_mappings = get_header_info(compressed_contents)[0]
    ngram_size = get_header_info(compressed_contents)[1]
    
    index = 2 + number_mappings * (ngram_size + 1)
    compressed_body = compressed_contents[index:]
    return compressed_body
    

# Decompress the body
def decompress_body(decode_map, compressed_body):
    '''
    Parameters:
    
        decode_map:
        compressed_body:
    if i.isalpha() == False: 
            decompressed_contents += decode_map[i]
        elif i == ' ':
            decompressed_contents += i
        else:
            decompressed_contents += i
    
    i.isalpha() == True or i == '_' or i == ' ' or i == '.' or i == '"' or i == '0' or i == '1' or i == '2' or i == '3' or i == '4' or i == '5' or i == '6' or i == '7' or i == '8' or i == '9' or i == '\n' or i == ';' or i == "'" or i == '-' or i == '?' or i == '!' or i == ',' or i == '(' or i == ')' or i == ':':
    
     if ord(i) in range(32, 126) or i == '\n':
            decompressed_contents += i
        else:
            decompressed_contents += decode_map[i]
    '''
    decompressed_contents = ''
    for i in compressed_body:
        if i in decode_map.keys():
            decompressed_contents += decode_map[i]
        else:
            decompressed_contents += i
    return decompressed_contents



# Tie it all together
def decompress_file(in_filename, out_filename):
    
    in_file = open(in_filename)
    compressed_contents = in_file.read()
    in_file.close()
    
    decode_map = parse_header(compressed_contents)
    compressed_body = get_compressed_body(compressed_contents)
    uncompressed_contents = decompress_body(decode_map, compressed_body)
    
    out_file = open(out_filename, 'w')    
    out_file.write(uncompressed_contents)
    out_file.close()
    #return compressed_contents
    #return get_header_info(compressed_contents)
    #return decode_map
    #return compressed_body
    #return uncompressed_contents
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
