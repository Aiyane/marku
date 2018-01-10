# Marku

这是一个`Markdown`解释器, 一个自己练手的小项目, 打算解析出`Markdown`文件的抽象语法树, 再利用抽象语法树解析成`HTML`格式

## 测试

目前已完成一部分功能, 下载源码后, 用 IDE 打开源码文件夹到主目录下, 即 `marku-master` 目录. 这是的文件目录结构如下

- marku-master
    - marku
        - HTML_render.py
        - big_token.py
        - big_token_deal_with.py
        - little_token.py
        - little_token_deal_with.py
        - render.py
        - run.py
        - test.md
    - test
        - test.py
        - test.md
    - .gitignore
    - README.md

在IDE中直接运行 `test/test.py` 文件, 默认会解析 `test` 文件夹中的 `test.md` 文件, 这时你会看到 `test` 文件夹中多出一个 `output.html` 文件, 可以直接打开查看测试结果.

或者你直接打开终端, 利用 `cd` 命令到 `test` 文件夹, 运行 `python test.py` 也是同样效果, 当然你也可以运行 `python test.py test2.md output.html` 这样是将 `test` 文件夹中 `test2.md` 文件转化成 `output.html`.

## 运行

暂时在 `marku`文件夹中, 运行 `python input.md output.html` 即可, 这里的 `input.md` 是你需要转换的md文件, 请放到 `marku` 文件夹中, 这里的 `output.html` 是任意html输出名字

