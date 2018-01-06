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


class BaesBigToken(object):
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


class DocumentToken(BaesBigToken):
    """这是基础文档类"""

    def __init__(self, lines):

        BaesBigToken.__init__(self)

        self._kids = tuple(deal_with(lines, root=self))


class HeadToken(BaesBigToken):
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


class QuoteToken(BaesBigToken):
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


class ParagraphToken(BaesBigToken):
    """段落Token, 一种基本的Token, 由于是默认的块Token, 所以不需要match函数"""

    def __init__(self, lines):
        """段落Token的构造函数

        :lines: TODO

        """
        content = ''.join(lines).replace('\n', ' ').strip()
        self._lines = lines


class BlockCodeToken(BaesBigToken):
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

    @property
    def match(lines):
        if line[0].startswith('```') and lines[-1] == '```\n':
            return True
        for line in lines:
            if not line.startswith(' ' * 4):
                return False
        return True


class SeparatorToken(BaesBigTokens):
    """这是分隔符Token"""

    accept_params = frozenset(('---\n', '===\n', '***\n', '* * *\n'))

    def __init__(self, lines):
        self.lines = lines

    @property
    def macth(lines):
        return len(lines) == 1 and lines[0] in SeparatorToken.accept_params


class ListToken(BaesBigToken):

    """这是一个列表Token"""

    def __init__(self, lines):
        """列表Token的构造函数

        :lines: TODO

        """
        self._lines = lines
        self._kids = list(List.build_list(lines))
        leader = lines[0].split(' ', 1)[0]
        if leader[:-1].isdigit():
            self.start = int(leader[:-1])
        else:
            self.start = None


    @property
    def build_list(lines):
        pass

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
