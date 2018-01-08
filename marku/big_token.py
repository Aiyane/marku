# coding: utf-8
__author__ = "Aiyane"
from types import GeneratorType
import big_token_deal_with as deal_wither
import little_token

__all__ = [
    'HeadToken', 'QuoteToken', 'BlockCodeToken', 'SeparatorToken', 'ListToken',
    'TableToken'
]


def deal_with(lines, root=None):

    return deal_wither.deal_with(lines, _token_types, ParagraphToken, root)


class BaseBigToken(object):
    """
    基础Token
    """

    def __init__(self, lines, deal_func):
        self._kids = deal_func(lines)

    @property
    def kids(self):
        if isinstance(self.kids, GeneratorType):
            self._kids = tuple(self._kids)
        return self._kids


class DocumentToken(BaseBigToken):
    """这是基础文档类"""

    def __init__(self, lines):

        BaseBigToken.__init__(self)

        self._kids = tuple(deal_with(lines, root=self))


class HeadToken(BaseBigToken):
    """这是标题Token"""

    def __init__(self, lines):
        """标题构造函数

        :lines: TODO

        """

        self._lines = lines
        if len(lines) == 1:
            hashes, content = lines[0].split('# ', 1)
            content = content.split(' #', 1)[0].strip()
            self.level = len(hashes) + 1
        else:
            if lines[-1][0] == '=':
                self.level = 2
            elif lines[-1][0] == '-':
                self.level = 1
            content = ' '.join([line.strip() for line in lines[:1]])

        super().__init__(content, little_token.deal_with_line)

    @staticmethod
    def match(lines):
        """匹配函数

        :lines: TODO
        :returns: TODO

        """
        if (len(lines) == 1 and lines[0].startswith('#')
                and lines[0].find('# ') != -1):
            return True
        return len(line) > 1 and (liens[-1].startswith('---')
                                  or lines[-1].startswith('==='))


class QuoteToken(BaseBigToken):
    """引用Token"""

    def __init__(self, lines):
        """引用Token的构造函数

        :lines: TODO

        """
        self._lines = lines
        content = []
        for line in lines:
            if line.startswith('> '):
                content.append(line[2:])
            else:
                content.append(line)
        super().__init__(content, deal_with)

    @staticmethod
    def match(lines):
        return lines[0].startswith('> ')


class ParagraphToken(BaseBigToken):
    """段落Token, 一种基本的Token, 由于是默认的块Token, 所以不需要match函数"""

    def __init__(self, lines):
        """段落Token的构造函数

        :lines: TODO

        """
        content = ''.join(lines).replace('\n', ' ').strip()
        self._lines = lines


class BlockCodeToken(BaseBigToken):
    """多行代码Token"""

    def __init__(self, liens):
        """多行代码Token的构造函数
        """

        self._liens = liens
        if lines[0].startswith('```'):
            content = ''.join(lines[1:-1])
            self.language = lines[0], strip()[3:]
        else:
            content = ''.join([line[4:] for line in lines])
            self.language = ''
        self._kids = (little_token.RawTextToken(content), )

    @staticmethod
    def match(lines):
        if line[0].startswith('```') and lines[-1] == '```\n':
            return True
        for line in lines:
            if not line.startswith(' ' * 4):
                return False
        return True


class SeparatorToken(BaseBigToken):
    """这是分隔符Token"""

    accept_params = frozenset(('---\n', '===\n', '***\n', '* * *\n'))

    def __init__(self, lines):
        self.lines = lines

    @staticmethod
    def macth(lines):
        return len(lines) == 1 and lines[0] in SeparatorToken.accept_params


class ListToken(BaseBigToken):
    """这是一个列表Token"""

    def __init__(self, lines):
        """列表Token的构造函数
        """
        self._lines = lines
        self._kids = list(List.build_list(lines))
        leader = lines[0].split(' ', 1)[0]
        if leader[:-1].isdigit():
            self.start = int(leader[:-1])
        else:
            self.start = None

    @staticmethod
    def build_list(lines):
        """
        这里逻辑稍微复杂, 所以我解释一下
        判断每一行,
        - 问: 这一行的列表标志在开头吗?
            *是的, 这是一个普通行
                - 问: 是否它的前许多行是嵌套的?
                    + 是的, 所以将list_buffer用ListToken包裹起来, 再用ListItem包裹这一行
                    + 不是, 所以就是一个普通的列表行, 用ListItem包裹起来
            * 不是, 不在开头, 不是一个普通的列表
                - 问: 去掉四个空格这一行的标志在开头吗?
                    + 是的, 这是一个嵌套的列表, 所以放到list_buffer中
                    + 不是, 不是一个嵌套的列表, 但还是当作嵌套列表表示, 放到list_buffer中
        """
        list_buffer = []  # 这里存嵌套行的内容
        for line in lines:

            if ListToken.has_leader(line):

                if list_buffer:
                    yield ListToken(list_buffer)
                    list_buffer.clear()
                yield ListItem(line)  # 把这一行yield出去

            elif line.startswith(' ' * 4):
                line = line[4:]
                list_buffer.append(line)

            else:
                list_buffer.append(line)  # 自动算作子行

        if list_buffer:
            yield ListToken(list_buffer)
            list_buffer.clear()

    @staticmethod
    def has_leader(line):
        return line.startswith(
            ('- ', '* ', '+ ')) or line.split(' ', 1)[0][:-1].isdigit()

    @staticmethod
    def match(lines):
        return ListToken.has_leader(lines[0].strip())


class ListItem(BaseBigToken):
    """这是一个一行的ListItem"""

    def __init__(self, line):
        """ListItem的构造函数

        :line: TODO

        """
        try:
            content = line.split(' ', 1)[1].strip()
        except Exception:
            content = ''
        super.__init__(content, little_token.deal_with_line)


class TableToken(BaseBigToken):
    """这是一个表格Token"""

    def __init__(self, lines):
        """表格Token的构造函数

        :lines: TODO

        """
        self._lines = lines
        if lines[1].find('---') != -1:
            self.aligns = self.aligns_deal_with(lines[1])
            self._kids = tuple(
                TableRow(line, self.aligns) for line in lines.pop(1))
            _kids[0].header = True
        else:
            self.aligns = [0]
            self._kids = tuple(TableRow(line, self.aligns) for line in lines)

    @staticmethod
    def aligns_deal_with(line):
        aligns = line[1:-2].split('|').strip()
        res = []
        for align in aligns:
            if align[:4] == ':---' and align[-4:] == '---:':
                res.append(1)
            elif align[-4:] == '---:':
                res.append(2)
            else:
                res.append(0)
        return res

    @staticmethod
    def match(lines):
        return lines[0][0] == '|' and lines[0][-2] == '|' and lines[-1][0] == '|' and lines[-1][-2] == '|'


class TableRow(BaseBigToken):
    """Table一行的Token"""

    def __init__(self, line, aligns=[0], header=False):
        """一行的Table的构造函数

        :line: TODO
        :aligns: TODO

        """
        self.header = header
        self._line = line[1:-2].split('|').strip()
        self._aligns = aligns
        self._kid = tuple(
            TableCell(line, align)
            for line, align in zip(self._line, self._aligns))


class TableCell(BaseBigToken):
    """一行中一个元素的Token"""

    def __init__(self, content, align=0):
        """构造函数

        :line: TODO
        :align: TODO

        """
        self.align = align
        super().__init__(content, little_token.deal_with_line)


_token_types = [
    'HeadToken', 'QuoteToken', 'BlockToken', 'SeparatorToken', 'ListToken',
    'TableToken'
]

from ipdb import set_trace
if __name__ == "__main__":
    lines = ['## 标题2']
    test = HeadToken(lines)
    set_trace()
    print(test)
