# Marku

这是一个`Markdown`解释器, 一个自己练手的小项目, 打算解析出`Markdown`文件的抽象语法树, 再利用抽象语法树解析成`HTML`格式

## 测试



目前已完成一部分功能, 下载源码后, 在终端 `cd` 到 主目录下, 即 `marku-master` 目录. 这是的文件目录结构如下

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

