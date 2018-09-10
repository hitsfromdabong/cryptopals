import sys
import binascii
import argparse
from collections import Counter
import string
import base64
import math
import matplotlib.pyplot as plt
import numpy as np
import json


def hexstr2raw(hexstr):
    return binascii.unhexlify(hexstr)

def raw2base64(raw):
    return binascii.b2a_base64(raw)

def raw2hexstr(raw):
    return binascii.hexlify(raw)

def split_len(seq, length):
    return [seq[i:i+length] for i in range(0, len(seq), length)]

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

def guess_xor_keysize(ciphertext):
    raw = ciphertext
    avg = np.zeros(int(math.floor(len(raw)/2)))
    for i in range(1, int(math.floor(len(raw)/2))):
        for j in range(0, int(math.floor(len(raw) / i) - 1)):
            avg[i] += normalized_hamming_dist(raw[j*i:(j + 1)*i], raw[(j + 1)*i:(j + 2)*i], i)
        avg[i] /= (math.floor(len(raw)/i) - 1)
    s = {}
    for i in range(2,20):
        s[score(avg, i)] = i
    minkey = min(s.keys())
    print "Detected most probable keysize: " + str(s[minkey])
    return s[minkey]


def normalized_hamming_dist(a, b, keysize):
    return hamming_dist(a, b) / keysize

def score(avg, keysize):
    n = 0
    k = int(math.floor(len(avg)/keysize))
    for i in (1,k - 1):
        n += avg[i*keysize]
    n /= (k - 1)
    return n

with open('engl_letter_freq.json') as f:
    letter_freq_engl = json.load(f)

with open('test', 'r') as f:
    raw = base64.b64decode(f.read())

keysize = guess_xor_keysize(raw)

for i in range(keysize):
    data = ""
    for j in range(int(math.floor(len(raw)/keysize))):
        data += raw[keysize*j + i]
    d = dict()
    for i in range(0, 256):
        guess = xor(data, chr(i))
        metric = xor_metric(guess, letter_freq_engl)
        intab = "\a\b\t\n\v\f\r"
        outtab = "       "
        trantab = string.maketrans(intab, outtab)
        guess = guess.translate(trantab)
        d[chr(i)] = metric
    for key, value in sorted(d.iteritems(), key = lambda (k,v): (v,k)):
        if value < 0.04:
            print "%s, %s" % (value, key)

