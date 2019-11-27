# -*- coding: utf-8 -*-
from dbsql_sqlite import DbSql


class SysDb(DbSql):
    表结构 = {
        'websiteTabel': {
            '搜索引擎': {'类型': '文本', '初始值': None, '主键否': '非主键'},
            '搜索日期年': {'类型': '整型', '初始值': None, '主键否': '非主键'},
            '搜索日期月': {'类型': '整型', '初始值': None, '主键否': '非主键'},
            '搜索日期日': {'类型': '整型', '初始值': None, '主键否': '非主键'},
            '搜索网址': {'类型': '整型', '初始值': None, '主键否': '非主键'},
            '搜索html': {'类型': '整型', '初始值': None, '主键否': '非主键'},
            '新闻序号': {'类型': '整型', '初始值': None, '主键否': '非主键'},  # 新闻在bing页面中的序号
            '新闻ID': {'类型': '文本', '初始值': None, '主键否': '主键'},
            '新闻网址原': {'类型': '文本', '初始值': None, '主键否': '非主键'},  # 新闻在bing页面中的url
            '新闻网址真': {'类型': '文本', '初始值': None, '主键否': '非主键'},  # 经历自动跳转后新闻页面的真实url
            '新闻html': {'类型': '文本', '初始值': None, '主键否': '非主键'},
            '新闻标题': {'类型': '文本', '初始值': None, '主键否': '非主键'},
            '新闻作者': {'类型': '文本', '初始值': None, '主键否': '非主键'},
            '新闻机构': {'类型': '文本', '初始值': None, '主键否': '非主键'},
            '新闻日期年': {'类型': '整型', '初始值': None, '主键否': '非主键'},
            '新闻日期月': {'类型': '整型', '初始值': None, '主键否': '非主键'},
            '新闻日期日': {'类型': '整型', '初始值': None, '主键否': '非主键'},
            '新闻正文': {'类型': '文本', '初始值': None, '主键否': '非主键'}
        }
    }
    # 各"通用类型"在表示“此字段不存在”时的值
    typeNotExist = {
        '整型': ['NULL', None],
        '浮点型': ['NULL', None],
        '文本': ['NULL', None]
    }
    # 各"通用类型"在表示“此字段存在但值未知”时的值
    typeEmpty = {
        '整型': ['NULL', None],
        '浮点型': ['NULL', None],
        '文本': ['NULL', None]
    } 
    @staticmethod
    def initAllSysTables(updateStrategy='rewrite'):
        """
        :function 初始化所有系统表
        
        :param updateStrategy='rewrite'or'continue'。如果要建立的表已经存在，是删除旧表建新表，还是放弃建表操作。
        """
        for key in SysDb.表结构:
            SysDb.ensureTable(tableName=key, tableStructureInDict=SysDb.表结构[key], updateStrategy=updateStrategy)