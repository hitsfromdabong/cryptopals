import sys
import json

table = {}
for i in range(256):
    table[i] = 0.0

with open('corpus.txt', 'r') as f:
    line = f.readline()
    while line:
        for char in line:
            table[ord(char)] += 1
        line = f.readline()

total = 0
for i in range(256):
    total += table[i]
for i in range(256):
    table[i] /= total

print json.dumps(table)
            
