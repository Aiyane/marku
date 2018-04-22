#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
# test3.py
from marku import Marku

res = """
```py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Hello(object):
	def __init__(self, name):
    	self.name = name
    def say_hello(self):
    	print("Hello, " + self.name)

if __name__ == "__main__":
	hello = Hello('Aiyane')
    hello.say_hello()
```
"""

md = Marku(res)

result = md.render()

print(result)
