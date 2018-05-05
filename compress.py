VERSION = 1.0

NUM_BYTES = 256

ALL_BYTES = set()
for byte_val in range(NUM_BYTES):
    ALL_BYTES.add(chr(byte_val))

def get_unused_bytes(string):
    used_bytes = set(string)
    return ALL_BYTES.difference(used_bytes)

def get_ngrams(string, ngram_size):
    result = []
    upper_index = len(string) - ngram_size
    for index in range(upper_index + 1):
        next_ngram = string[index:index + ngram_size]
        result.append(next_ngram)
    return result

def freqs(seq):
    counters = {}
    for item in seq:
        if item in counters:
            counters[item] += 1
        else:
            counters[item] = 1
    return counters

def get_second_item(seq):
    return seq[1]

def sorted_ngrams_by_freq(dict):
    items = dict.items()
    sorted_items = sorted(items, key=get_second_item, reverse=True)
    result = []
    for ngram, _freq in sorted_items:
        result.append(ngram)
    return result

MAX_MAPPINGS = 255

def make_ngram_encoding(sorted_ngrams, encoding_bytes):
    result = {}
    count = 0
    for ngram, encoding_byte in zip(sorted_ngrams, encoding_bytes):
        if count >= MAX_MAPPINGS:
            break
        result[ngram] = encoding_byte 
        count += 1
    return result

def make_header(ngram_size, encoded_ngrams):
    number_mappings = len(encoded_ngrams)
    number_mappings_as_char = chr(number_mappings)
    ngram_size_as_char = chr(ngram_size)
    result = number_mappings_as_char + ngram_size_as_char 
    for ngram in encoded_ngrams:
        result += ngram + encoded_ngrams[ngram]
    return result

def make_encoded_string(string, ngram_size, encoded_ngrams):
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
