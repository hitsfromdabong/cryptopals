import sys
import argparse
import base64

parser = argparse.ArgumentParser(description = 'Cryptopals cmd tools. Reads from stdin by default.')
parser.add_argument('-i', '--in', metavar = 'input file', type = str, nargs = '+', help = "Input file.")
parser.add_argument('-e', '--encoding', metavar = 'encoding', type = str, nargs = 1, help = "Encoding of input file. (base64, ...)")
parser.add_argument('-v', '--verbose', action = 'count')

subparsers = parser.add_subparsers(help = 'sub command help')

parser_encode = subparsers.add_parser('encode', help = 'Encoding tools.')
parser_encode.add_argument('hex',  action='store_true')

parser_decode = subparsers.add_parser('decode', help = 'Decoding tools.')

parser_transcode = subparsers.add_parser('transcode', help = 'Decoding tools.')

parser_analyze = subparsers.add_parser('analyze', help = 'Analyzing tools.')

parser_crack = subparsers.add_parser('crack', help = 'Cracking tools.')
parser.add_argument('-l', '--language', help = "Language for letter frequency table. Default: English.")

args = parser.parse_args()
