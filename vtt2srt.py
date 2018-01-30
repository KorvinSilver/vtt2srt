#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Project: WebVTT Document to SubRib Subtitle converter

Copyright 2018, Korvin F. Ezüst

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import argparse
import re

__author__ = "Korvin F. Ezüst"
__copyright__ = "Copyright (c) 2018, Korvin F. Ezüst"
__license__ = "Apache 2.0"
__version__ = "1.0"
__email__ = "dev@korvin.eu"
__status__ = "Working"

parser = argparse.ArgumentParser(
    description="Convert a WebVTT Document to a SubRip Subtitle")
parser.add_argument("file", help="vtt file to convert")
args = parser.parse_args()

# Read VRT file
with open(args.file) as f:
    lines = f.readlines()

# Find a dot in a string matching e.g. 12:34:56.789
# and replace it with a comma
regex = r"(?<=\d\d:\d\d:\d\d)\.(?=\d\d\d)"
lines = [re.sub(regex, ",", i.rstrip()) for i in lines]

# Find everything in line after a string matching e.g. 12:34:56,789
# and delete it
regex = r"(?<=\d\d:\d\d:\d\d\,\d\d\d --> \d\d:\d\d:\d\d\,\d\d\d).*"
lines = [re.sub(regex, "", i.rstrip()) for i in lines]

# Replace multiple blank lines with a single blank line
sbl = []
for i in range(len(lines[:-1])):
    if lines[i] == "" and lines[i+1] == "":
        continue
    else:
        sbl.append(lines[i])
if lines[-1] != "":
    sbl.append(lines[-1])

# Place a number before each time code (number empty lines)
enum = enumerate(sbl)
next(enum)
nel = [str(i) or "\n" + str(next(enum)[0]) for i in sbl]

# Write SRT file
with open(args.file + ".srt", "w") as f:
    f.write("\n".join(nel[3:]))

print("SRT file created:", args.file + ".srt")
