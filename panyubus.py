# -*- coding: utf-8 -*-

import requests
import json
import ast

pan68_url = u"http://h5.thecampus.cc/api/v1/line?line_number=3150&direction=1"
dict = json.loads(requests.get(pan68_url).content.decode('utf-8'))
# dict=ast.literal_eval(requests.get(pan68_url).content.decode('utf-8'))
for kv in dict.items():
    print(kv)