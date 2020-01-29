#!/usr/bin/env python
# coding: utf-8
import glob

print("Files in the current folder")
print(glob.glob("*"))
print("Files in the child folders")
print(glob.glob("*/*"))