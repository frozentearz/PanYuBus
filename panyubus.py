# -*- coding: utf-8 -*-

import requests
import json
import ast
import sys

reload(sys)
sys.setdefaultencoding('UTF-8')

pan68_url = u"http://h5.thecampus.cc/api/v1/line?line_number=3150&direction=1"
dict=ast.literal_eval(requests.get(pan68_url).encode('utf-8').content.decode('utf-8'))


print(dict)