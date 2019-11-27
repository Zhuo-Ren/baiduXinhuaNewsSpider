# -*- coding: utf-8 -*-


def indent(text, length=40, fIndent=2, lIndent=2):
    """
        :function 把正常文本变成自动换行并且添加缩进的文本。
        
        :param length=INT。一行多长(再长就自动换行)。

        :param fIndent=INT。首行缩进几个空格。

        :param lIndent=INT。左缩进几个空格。
    """
    # re是最后要返回的文本
    re = ''
    # 首行缩进
    for i in range(0, fIndent):
        re += ' '
    count = 0
    for charIndex in range(0, len(text)):
        curChar = text[charIndex]
        if count == length or curChar == '\n':
            re += '\n'
            for i in range(0, lIndent):
                re += ' '
            count = 0
        if curChar != '\n':
            re += curChar
            count += 1
    return re
