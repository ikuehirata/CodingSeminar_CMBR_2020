#!/usr/bin/env python
# coding: utf-8
from random import sample
import string
import re

# generate key
original = list(string.ascii_lowercase) # list of original alphabets
key = sample(string.ascii_uppercase, len(original)) # cipher
print(f"original: {''.join(original)}")
print(f'key: {"".join(key)}')
# make translation dictionary
dic = {}
for (k, v) in zip(original, key):
    dic.update({k: v})

# open file and read txt
with open("ilprincipe_original.txt", "r", encoding="utf8") as f:
    txt = f.read()

txt2 = re.sub(r"\W", "", txt) # remove non-alphabets
txt2 = txt2.lower() # make all lower case
txt2 = txt2.translate(str.maketrans(dic)) # cipher

# save
with open("cipher.txt", "w", encoding="utf8") as o:
    o.write(txt2)
with open("key.txt", "w", encoding="utf8") as o:
    o.write(f"original: {''.join(original)}")
    o.write(f"key: {''.join(original)}")
