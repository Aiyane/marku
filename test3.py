#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
# test3.py
from marku import Marku

res = """
# 标题
## 标题
"""

md = Marku(res)

result = md.render()

print(result)
