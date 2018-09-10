import sys
import binascii
import argparse
import json
from collections import Counter
import string
import base64

stripped = lambda s: "".join(i for i in s if 32 < ord(i) < 127)

parser = argparse.ArgumentParser(description = 'Cryptopals cmd tools. Reads from stdin by default.')
parser.add_argument('--x2b64', action='store_true', help = "Convert hexadecimal string to base64 encoded string.")
parser.add_argument('--fixed_xor', action='store_true',  help = "Return the xor of two strings of same length.")
parser.add_argument('--xor', action='store_true', help = 'Return the xor of string and key. Key specified in input2.')
parser.add_argument('--crack_xor', action='store_true', help = 'Guesses the 1-byte xor key of input according to english letter frequency.')
parser.add_argument('-i', '--input', type = str, help = "Read input from file.")
parser.add_argument('-i2', '--input2', type = str, help = "Read input from (another) file.")
args = parser.parse_args()

with open('engl_letter_freq.json') as f:
    engl_letter_freq = json.load(f)


# Conversion Primitives

def hexstr2raw(hexstr):
    return binascii.unhexlify(hexstr)

def raw2base64(raw):
    return binascii.b2a_base64(raw)

def raw2hexstr(raw):
    return binascii.hexlify(raw)

# XOR Operations
def fixed_xor(str1, str2):
    if len(str1) != len(str2):
        print "Strings must be of same length."
    else:
        strlen = len(str1)
        result = bytearray(strlen)
        for i in range(strlen):
            result[i] = chr(ord(str1[i]) ^ ord(str2[i]))
        return result

def xor(data, key):
    result = bytearray(data)
    for i in range(len(data)):
        result[i] = chr(ord(data[i]) ^ ord(key[i % len(key)]))
    return result

# Get hamming distance
def hamming_dist(a, b):
    a = bytearray(a)
    b = bytearray(b)
    if len(a) < len(b):
        print "First string must be equal or longer than second string."
        return
    n = 0
    for i in range(len(a)):
        result = a[i] ^ b[i % len(b)]
        n += bin(result).count("1")
    return n

# Guess metric distance
def xor_metric(decoded, letter_freq_default):
    letter_freq = Counter(decoded.lower())
    nletters = len(decoded)
    for key in letter_freq:
        letter_freq[key] /= float(nletters)
    metric = 0.0
    for key in letter_freq_default:
        try:
            metric += (letter_freq[ord(key)] - letter_freq_default[key]/100)**2
        except KeyError:
            metric += (letter_freq_default[key]/100)**2
    return metric


def main():
    data = ""
    if not args.input:
        data = raw_input()
    else:
        with open(args.input, 'r') as f:
            data = f.read()

    if args.input2:
        with open(args.input2, 'r') as f:
            data2 = f.read().rstrip()

    if args.x2b64:
        result = raw2base64(hexstr2raw(data.rstrip()))
        print result.rstrip()
        return

    if args.fixed_xor:
        if not args.input2:
            print "Please specify two inputs."
            return
        else:
            n1 = hexstr2raw(data)
            n2 = hexstr2raw(data2)
            print raw2hexstr(fixed_xor(n1,n2))
            return
        
    if args.xor:
        if not args.input2:
            print "Please specify two inputs."
            return
        else:
            n1 = base64.b64decode(data)
            n2 = data2.rstrip()
            print len(n2)
            print xor(n1,n2)
            return
        
    if args.crack_xor:
        for line in data.splitlines():
            d = {}
            for i in range(256):
                guess = xor(hexstr2raw(line.rstrip()), chr(i))
                metric = xor_metric(guess, engl_letter_freq)
                intab = "\a\b\t\n\v\f\r"
                outtab = "       "
                trantab = string.maketrans(intab, outtab)
                guess = guess.translate(trantab)
                for i in list(guess):
                    if i  < 32 or i > 127:
                        guess = ""
                d[str(guess)] = metric
            for key, value in sorted(d.iteritems(), key = lambda (k,v): (v,k)):
                if value < 0.04:
                    print "%s, %s" % (value, key)
            




if __name__ == "__main__":
    main()
