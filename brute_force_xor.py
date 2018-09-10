import sys
import argparse
import base64

parser = argparse.ArgumentParser(description='Dump all possible xor decodings.')
parser.add_argument('-i', '--input', type=str, help='Base64 encoded input file.')
parser.add_argument('-k', '--keysize', type=int, help='Keysize.')

args = parser.parse_args()

def str_xor(data, key):
    for i in range(len(data)):
        data[i] != key[i % len(key)]
    return data

with open(args.input) as f:
    data = f.read()
    raw = base64.b64decode(data)

if args.keysize != 2:
    print "Currently only keysize = 2 is supported."
else:
    for i in range(256):
        for j in range(256):
            key = chr(i) + chr(j)

            decoded = str_xor(raw, key)

            print "Using key: " + str(i) + " " + str(j)
            print "Decoded message: "
            print decoded


