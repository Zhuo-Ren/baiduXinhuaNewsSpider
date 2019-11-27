# -*- coding: utf-8 -*-
# 教程 https://www.cnblogs.com/awakenedy/articles/9182036.html
# 教程 https://docs.python.org/3/library/datetime.html#module-datetime

from sysdb import SysDb  # 数据库
from baidusearcher import baidusearcher  # 百度爬虫
import datetime3  # 用于循环日期
from time import sleep

# 起止日期限制(2018, 10, 29)
startDay = (2018, 10, 30)  # 从此日期开始(包括此日期)
endDay = (2018, 10, 31)  # 到此日期结束(不包括此日期)
# 来源网站限制
sourceWebsite = 'xinhuanet.com'
# 每天搜几个新闻
howManyNewsOneDay = 5
# 使用fiddler吗
certFile = None  # "./DO_NOT_TRUST_FiddlerRoot.crt"  # None
# 关键字
kw = r'737max空难'

try:
    # 连接数据库
    SysDb.connectDataBase('./main.sqlite')

    # 初始化所有系统表
    SysDb.initAllSysTables(updateStrategy='continue')

    # 初始化浏览器driver
    baidusearcher.initDriver()

    # 起止日期（截止日期当天不搜）
    startDate = datetime3.date(startDay[0], startDay[1], startDay[2])
    endDate = datetime3.date(endDay[0], endDay[1], endDay[2])
    # 参数合理性检查
    pass
    # 循环中的当前日期
    curDate = startDate
    # 循环日期
    while curDate != endDate:
        print('搜素日期：', curDate)
        # 爬取当日新闻
        baidusearcher.search(
            keyword=kw,
            startY=curDate.year, startM=curDate.month, startD=curDate.day,
            endY=curDate.year, endM=curDate.month, endD=curDate.day,
            sourceWebsite=sourceWebsite,
            howManyResultWanted=howManyNewsOneDay,
            fiddler=certFile,
        )
        # curDate++
        curDate = curDate + datetime3.timedelta(1)
        # 睡一会
        print('zzz')
        sleep(2)

finally:
    # 释放数据库
    SysDb.disconnectDataBase()
    # 释放浏览器driver
    baidusearcher.closeDriver()
