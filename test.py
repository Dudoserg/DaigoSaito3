#!/usr/bin/env python
import json
def foobar(json1):
    msg = json.loads(json1)
    return msg

kek = foobar('{"arr":[],"input":"1234"}')
print(kek['input'])