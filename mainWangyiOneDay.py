# -*- coding: utf-8 -*-
'''
功能：查询一次（指定关键字和来源网站)
'''

from sysdb import SysDb  # 数据库
from baidusearcher import baidusearcher  # 百度爬虫
from process import searchPageProcess
from process import resultPageProcessWangyi as resultPageProcess

# 关键字
kw = r'737max空难'
# 来源网站限制
sourceWebsite = 'news.163.com'
# 每天搜几个新闻
howManyNewsOneDay = 8
# 使用fiddler吗
certFile = None  # "./DO_NOT_TRUST_FiddlerRoot.crt"  # None

# 参数合理性检查
pass

# 主逻辑
try:
    # 连接数据库
    SysDb.connectDataBase('./main.sqlite')

    # 初始化所有系统表
    SysDb.initAllSysTables(updateStrategy='rewrite')

    # 初始化浏览器driver
    baidusearcher.initDriver()

    # 初始化爬虫
    baidusearcher.initSearcher(
        keyword=kw,
        sourceWebsite=sourceWebsite,
        howManyResultWanted=howManyNewsOneDay,
        fiddler=certFile,
        searchPageProcess=searchPageProcess,
        resultPageProcess=resultPageProcess
    )
    # 爬取一下
    baidusearcher.search()

finally:
    # 释放数据库
    SysDb.disconnectDataBase()
    # 释放浏览器driver
    baidusearcher.closeDriver()
