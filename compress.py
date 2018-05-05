'''
Compress

Authors: Alexander Ryan

This program compresses a text file. The input is a text file
and the ouput is a compressed version of the text file.

'''

NUM_BYTES = 256

ALL_BYTES = set()
for byte_val in range(NUM_BYTES):
    ALL_BYTES.add(chr(byte_val))

def get_unused_bytes(string):
    '''
    Returns the number of unique bytes 
    that are not being used in the string.
    
    This gives us an indication of how many bytes 
    we can use to substitute n_grams in the string.
    
    For example if a particular string used 200 out of 
    the 256 possible unique bytes, there are only 56 
    different bytes we can use in the compression.
    
    Parameters: 
        
        string: a string of text you want compressed.
    
    Result:
    
        a list of all the unique bytes 
        not present in the string.
    
    '''
    used_bytes = set(string)
    return ALL_BYTES.difference(used_bytes)


def get_ngrams(string, ngram_size):
    '''
    Breaks the string entered into chunks, formally called ngrams, 
    with the size given by the parameter ngram_size.
    These ngrams are then added to a list, result.
    
    Parameters:
    
        string: a string of text you want compressed.
        ngram_size: the size of each ngram of the string. 
                    For example if we broke the string 'apple' 
                    with ngram size of 2 it would be 
                    ['ap', 'pp', 'pl', 'le']
    
    Result:
    
        A list of all the ngrams of text in the string, 
        with size in characters given by the ngram_size.

    '''
    result = []
    upper_index = len(string) - ngram_size
    for index in range(upper_index + 1):
        next_ngram = string[index:index + ngram_size]
        result.append(next_ngram)
    return result


def freqs(seq):
    '''
    Counts the number of times each individual ngram appears in the list.
    This data is mapped to a dictionary.
    Each different ngram will have a number for each 
    time it appears in the sequence
    
    Parameters:
    
        seq: A list of ngrams. 
             An example input could be the get_ngram function result
    
    Result:
    
        A dictionary which lists all the different ngrams 
        and the number of times they appeared in the given seq

    '''
    counters = {}
    for item in seq:
        if item in counters:
            counters[item] += 1
        else:
            counters[item] = 1
    return counters


def get_second_item(seq):
    '''
    Returns the second item in the list
    
    Parameters:
    
        seq: A list of ngrams.
    
    Result:
    
       The second value in the list.

    '''
    return seq[1]


def sorted_ngrams_by_freq(dict):
    '''
    The ngams in the dictionary are sorted by the 
    number associated with them, which represents 
    the number of times they appear in the string.
    This sorted frequency is put into a list called result
    
    Parameters:
    
        dict: A dictionary of ngrams with an associated number 
              which respresents how many times they 
              appeared in the original string.
    
    Result:
    
        A dictionary sorted by the number associated with each ngram.
        The ngrams which appear most frequently 
        will appear towards the start of the dictionary.

    '''
    items = dict.items()
    sorted_items = sorted(items, key=get_second_item, reverse=True)
    result = []
    for ngram, _freq in sorted_items:
        result.append(ngram)
    return result


MAX_MAPPINGS = 255

def make_ngram_encoding(sorted_ngrams, encoding_bytes):
    '''
    For evry ngram in the list of sorted ngrams and encoding byte
    Add the encoding byte to the list of result
    If this list of encoding bytes becomes equal or greater than 255 stop the function

    The result is returned at the end
    
    Parameters:
    
        sorted_ngrams: A list of the ngrams, sorted by their frequency in the original string.
        encoding_bytes:

    '''
    result = {}
    count = 0
    for ngram, encoding_byte in zip(sorted_ngrams, encoding_bytes):
        if count >= MAX_MAPPINGS:
            break
        result[ngram] = encoding_byte 
        count += 1
    return result


def make_header(ngram_size, encoded_ngrams):
    '''
    
    Parameters:
    
        ngram_size:
        encoded_ngrams:
    
    '''
    number_mappings = len(encoded_ngrams)
    number_mappings_as_char = chr(number_mappings)
    ngram_size_as_char = chr(ngram_size)
    result = number_mappings_as_char + ngram_size_as_char 
    for ngram in encoded_ngrams:
        result += ngram + encoded_ngrams[ngram]
    return result


def make_encoded_string(string, ngram_size, encoded_ngrams):
    '''
    
    
    
    Parameters:
    
        string:
        ngram_size:
        encoded_ngrams:
    
    Result
    
    
    '''
    result  = ''
    index = 0
    while index < len(string):
        ngram = string[index:index + ngram_size]
        if ngram in encoded_ngrams:
            result += encoded_ngrams[ngram]
            index += ngram_size
        else:
            result += string[index]
            index += 1
    return result


MINIMUM_ENCODING_BYTES = 1

def compress_file(ngram_size, in_filename, out_filename):
    '''
    
    
    Parameters:
    
        ngram_size:
        in_filename:
        out_filename:
    
    Result:
    
    
    '''
    if ngram_size <= 0:
        print("n-gram size must be greater than 0")
        return

    in_file = open(in_filename)
    contents = in_file.read()
    in_file.close()

    encoding_bytes = list(get_unused_bytes(contents))
    num_encoding_bytes = len(encoding_bytes)

    if num_encoding_bytes <= MINIMUM_ENCODING_BYTES:
        print("Cannot compress file %s" % in_filename)
        print("Insufficient unused bytes in file")
        print("Found %s unused bytes, but %s are required" %
                 (num_encoding_bytes, MINIMUM_ENCODING_BYTES))
        return

    ngrams = get_ngrams(contents, ngram_size)
    num_ngrams = len(ngrams)

    if num_ngrams == 0:
        print("Cannot compress file %s" % in_filename)
        print("Zero ngrams found, perhaps file is too small?")
        return

    ngram_freqs = freqs(ngrams)
    sorted_ngrams = sorted_ngrams_by_freq(ngram_freqs) 
    encoded_ngrams = make_ngram_encoding(sorted_ngrams, encoding_bytes)
    header = make_header(ngram_size, encoded_ngrams)
    encoded_contents = make_encoded_string(contents, ngram_size,
                           encoded_ngrams)

    out_file = open(out_filename, 'w')
    out_file.write(header)
    out_file.write(encoded_contents)
    out_file.close()
