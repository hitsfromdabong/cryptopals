import string
import sys
import base64
import binascii
import matplotlib.pyplot as plt
import math
import json
import langdetect

def single_byte_xor(a, b):
    result = ""
    for i in range(len(a)):
        result += chr(ord(a[i]) ^ b)
    return result

def score_key(freq, lang):
    score = 0.0
    for i in range(256):
        try:
            score += freq[i]*lang[str(i)] 
        except KeyError:
            score += 0.0
    return score


def crack_single_byte_xor(cipher, lang):
    score = []
    for i in range(256):
        decoded = single_byte_xor(cipher, i)
        freq = get_sym_freq(decoded)
        score.append(score_key(freq, lang))
        print "Key: " + str(i) + " Score: " + str(score[i])
        if all(ord(char) < 128 for char in decoded):
            try:
                print "Probable language: " + str(langdetect.detect(decoded))
                print decoded
            except:
                print "No language detected."
    print min(score)
    return

def get_sym_freq(data):
    table = dict()
    for i in range(256):
        table[i] = 0.
    for char in data:
        table[ord(char)] += 1
    for i in range(256):
        table[i] /= len(data)
    return table



def main():
    with open('single-byte-xor-cipher', 'r') as f:
        data = binascii.unhexlify(f.read().rstrip())
    with open('engl_letter_freq.json', 'r') as f:
        letter_freq_engl = json.load(f)

    crack_single_byte_xor(data.rstrip(), letter_freq_engl)






if __name__ == '__main__':
    main()
