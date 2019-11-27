# -*- coding: utf-8 -*-

import re
from lxml import etree


def html2text(htmlText):
    # 利用lxml包处理content中的html标签，得到纯文本的content
    plainText = ''
    root = etree.HTML(htmlText)
    for element in root.iter():
        # 对于p，先换行
        if element.tag == 'p':
            plainText += '\n'
            # print('\n', end='')
        # 再考虑文本
        #   对于<html><header>等不包含文本的标签，直接跳过
        if element.text is None:
            pass
        #   对只包含不可见文本的标签，直接跳过
        elif re.search('^\s*$', element.text):
            pass
        # 对包含可见文本的标签
        else:
            plainText += element.text.strip()  # strip()用于取出字符串首尾空格
            # print(element.text.strip(), end='')
        # 最后考虑尾巴文本
        if element.tail is None:
            pass
        #   对只包含不可见文本的标签，直接跳过
        elif re.search('^\s*$', element.tail):
            pass
        # 对包含可见文本的标签
        else:
            plainText += element.tail.strip()
            # print(element.tail.strip(), end='')
    # 取出多余空行
    plainText = plainText.replace('\n\n', '\n')
    plainText = re.sub(r'^\n+', "", plainText)
    #
    return plainText
