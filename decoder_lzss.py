"""
Author: Kevin Lew
StudentID: 29677475
"""

import sys
from datetime import datetime

maxElias_len = 100 # max length of elias encoding

def decode_header(s):
    """Decodes the header section of the encoded string by finding the 
        huffman code words and its respective symbols

    Args:
        s (Str): Binary string of entire encoded string including header and data

    Returns:
        Tuple: Code words paired with its respective symbol and the length of header
    """
    codes = []
    unique_symbols, t = decode_elias(s) 
    skip = t
    for _ in range( to_decimal(unique_symbols) ):
        b_ascii = copy_section(s, skip, skip+7) # obtain symbol
        skip += 7
        symbol = chr( to_decimal(b_ascii) )
        # obtain code word for symbol
        n_s = copy_section(s, skip, skip+maxElias_len)
        code_len, t = decode_elias(n_s) 
        code = copy_section(n_s, t, t+to_decimal(code_len))
        skip += to_decimal(code_len) + t
        codes.append( (code, symbol) )
    return codes, skip

def copy_section(string, s, e):
    """Creates new copy of string's subsection bounded by s and e

    Args:
        string (Str): Reference string to copy from
        s (Int): Lower boundary for subsection (start position)
        e (Int): Upper boundary for subsection (end position)

    Returns:
        Str: Desired subsection of string
    """
    section = []
    for i in range(s, e):
        if i < len(string):
            section.append(string[i])
        else:
            break
    return "".join(section)

def decode_elias(s):
    """Decodes the first occurence of elias encoding in binary string

    Args:
        s (Str): Binary string encoded with elias omega 

    Returns:
        Tuple: First occurence of data for and size of encoded elias string
    """
    c = 0 # pointer for traversing through encoded binary string
    t = 1 # tracks total size of encoded binarys string
    read = 1 # amount of bits to read in next block
    while s[c] == "0":
        temp = ["1"]
        c += 1
        for _ in range(1, read):
            temp.append(s[c])
            c += 1
        temp = "".join(temp)
        read = to_decimal(temp) + 1 # size of next block
        t += read
    data = []
    # obtain data component of encoding
    for i in range(read):
        data.append(s[i+c])
    return "".join(data), t

def to_decimal(b):
    """Converts binary representation to decimal representation

    Args:
        b (Str): Binary string for converting into decimal

    Returns:
        Int: Decimal representation of binary string
    """
    r = 0
    p = 0
    for i in range(len(b)-1, -1, -1):
        if b[i] == "1":
            r += 2**p
        p+=1
    return r

def takeLength(n):
    return len(n[0])

def decode_lzss(s):
    """Decode encoded binary string into symbols

    Args:
        s (Str): Encoded binary string for decoding

    Returns:
        Str: Original text before encoding
    """
    size = len(s)
    decoded = []
    codes, header_len = decode_header(s)
    maxCode_len = len(max(codes, key=takeLength)[0])
    data = copy_section(s, header_len, size)
    fields_n, t = decode_elias(data)
    skip = t
    for _ in range( to_decimal(fields_n) ):
        n_s = copy_section(data, skip, skip+1) # first bit of block within data 
        # match > 3 case
        if n_s[0] == "0":
            n_s = copy_section(data, skip+1, skip+1+maxElias_len) # get look back section
            look_back, t1 = decode_elias(n_s) # find look back value 
            n_s = copy_section(data, skip+t1+1, skip+t1+1+maxElias_len) # get match length section
            length, t2 = decode_elias(n_s) # find length of match
            start = len(decoded)-to_decimal(look_back)
            # add matched sequence into decoded string
            for i in range(start, start + to_decimal(length)):
                decoded.append(decoded[i])
            skip += t1 + t2 + 1 # compute amount of skips for next triple block
        # match < 3 case
        else:
            n_s = copy_section(data, skip+1, skip+1+maxCode_len) # Get bits representing code word
            symbol, length = find_symbol(codes, n_s) # find symbol based on huffman code
            decoded.append(symbol) # add symbol into decoded string
            skip += length+1 # compute amount of skips for next triple block
    decoded = "".join(decoded)
    output_txt(decoded)
    return decoded
    
def find_symbol(codes, s):
    """Finds corresponding symbol for code word in binary string

    Args:
        codes (List): Code word and its corresponding symbol
        s (Str): Binary string that contains code word

    Returns:
        Tuple: Corresponding symbol for code word and length of code word
    """
    for i in range(len(codes)):
        code_word = codes[i][0]
        counter = 0
        for j in range(len(code_word)):
            if j < len(s):
                if code_word[j] == s[j]:
                    counter += 1
        if counter == len(code_word):
            return codes[i][1], len(code_word)
    raise KeyError

def output_txt(s):
    """Writes string s into file output_decoder_lzss.txt

    Args:
        s (Str): String to be written into text file
    """
    file = open("output_decoder_lzss.txt", "w")
    file.write(s)
    file.close()

def open_txt(filename):
    """Reads string inside text file specified by filename

    Args:
        filename (Str): Name of text file

    Returns:
        Str: String inside text file
    """
    file = open(filename, "r")
    s = file.read()
    file.close()
    return s

def test():
    """Tests decoding 
    """
    inputFiles = []
    outputFiles = []
    for i in range(8):
        if i+1 != 4 and i+1 != 6:
            inputFiles.append( "encoder_output"+str(i+1)+".txt" )
            outputFiles.append( "output_lzss_decoder"+str(i+1)+".txt")
    for i in range(len(inputFiles)):
        decode_lzss(open_txt(inputFiles[i]))
        try:
            print("Test Input File:", inputFiles[i])
            assert open_txt("output_decoder_lzss.txt") == open_txt(outputFiles[i])
            print("TEST PASSED\n")
        except AssertionError:
            print("Test Failed")

def main():
    #print(to_decimal("1010"))
    #print(decode_elias("00000010000"))
    #print(decode_lzss("01111000011111000100100011000110100100011111111010011000100100001101111") == "aacaacabcaba")
    #print(len("011110000111110001001000110001101001"))
    #print(chr(to_decimal("1100001")))
    #print(decode_lzss(open_txt(sys.argv[1])) == "aacaacabcaba")
    #timeStart = datetime.now()
    decode_lzss(open_txt(sys.argv[1]))
    #timeEnd = datetime.now()
    #print("run time: ", timeEnd-timeStart)
    #test()


if __name__ == "__main__":
    main()