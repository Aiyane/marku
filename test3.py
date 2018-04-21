#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
# test3.py
from marku import Marku

res = """
> 引用
> > 引用
> 引用
"""

md = Marku(res)

result = md.render()

print(result)
