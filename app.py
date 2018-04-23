#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Marku的简单使用
为渲染的html标签添加class属性值
扩展文件my_token中的语法
"""
# import my_token
from marku import Marku, Mark
# import os
# import webbrowser  # 打开浏览器
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
# from html.parser import HTMLParser


# html_parser = HTMLParser()
app = Flask(__name__)

# 获得当前路径
# loc = os.getcwd()

# 扩展html标签的class属性值
# tokenClass = {
#     "strongClass":      "strong",
#     "emClass":          "em",
#     "codeClass":        "code",
#     "delClass":         "del",
#     "imgClass":         "img",
#     "aClass":           "a",
#     "hClass":           "h",
#     "blockquoteClass":  "quote",
#     "preClass":         "pre",
#     "tableClass":       "table",
#     "pClass":           "p"
# }


@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        text = request.form.get('text')
        mk = Mark().deal_lines(text)
        md = Marku(text).render()
        # 增加class属性值
        # md.addClass(tokenClass)
        # 增加自定义语法
        # md.add_extra(my_token)
        # 浏览器打开
        # webbrowser.open(loc + "/out.html")

        # 渲染输出
        return jsonify({'markdown': md, 'mk': mk})
    return render_template('index.html', md='')


if __name__ == '__main__':
    app.run()
