#!/usr/bin/python3

import base64
import json
import os
import sys

if len(sys.argv) < 2:
    print("Usage: python3 %s decoded/*.json")

# files = os.listdir()
# files = list(filter(lambda fn: fn.startswith("decoded.hex"), files))

files = sys.argv[1:]
for file in files:
    pdu = json.load(open(file, "r"))["pdu"]
    raw = base64.b64decode(pdu)
    print("File %s" %file)
    print("\tCallsigns FROM: %s" % bytes([_>>1 for _ in raw[0:6]]))
    print("\tCallsigns TO:   %s" % bytes([_>>1 for _ in raw[7:13]]))
    print("\tRaw data: %s" %raw)
