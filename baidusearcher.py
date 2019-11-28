# -*- coding: utf-8 -*-

import datetime3 as datetime  # 用于获取当前日期作为默认日期
import time  # 用于获取unix时间作为url中的参数，用于睡觉
from lxml import etree
from indentation import indent  # 字符串缩进
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class baidusearcher():
    # 根本参数
    driver = None  # webdriver.Chrome()

    # 搜索参数
    searchKeyword = None
    searchBaseUrl = 'https://www.baidu.com/s' +\
        '?ie=utf-8' +\
        '&tn=monline_4_dg' +\
        '&ct=2097152' +\
        '&rqlang=cn'
    searchEngine = 'baidu.com'
    searchSourceWebsite = None  # 限定来源网站
    searchHowManyResultsOnePage = 10  # 设置每页显示多少结果
    searchStartTime = None  # None表示没设置时间限制
    searchEndTime = None  # None表示没设置时间限制
    resultWanted = None
    searchPageProcess = None
    resultPageProcess = None

    # 运行参数
    searchUrlInput = None  # 生成的searchUrl
    searchUrlOutput = None  # 访问searchUrlInput并经过自动跳转后的真实searchUrl
    searchIndex = -1  # 一次搜索返回多个搜索页(search)，这是搜索页索引,从0开始。
    searchHtml = None
    searchRoot = None
    searchTitle = None
    resultIndex = -1  # 一次搜索返回多条返回结果(result)，这是结果的总(跨页)索引，从0开始。
    resultIndexInPage = None  # 一个搜索页中有多条返回结果(result)，这是结果的页内索引，从0开始。
    resultXPathPattern = lambda x: '//*[@id=\"' + str(x + 1) + '\"]'  # 生成resultXPath的模板
    resultXPath = None  # 从searchRoot到页内第x个resultElement的xpath
    resultElement = None  # result块
    resultAXPath = 'h3/a'  # 从resultElement到searchUrlInput的xpath
    resultUrlInput = None
    resultUrlOutput = None
    resultTitle = None
    resultText = None
    resultTime = None
    resultSaved = 0  # 不是每个结果都符合要求，这是已经处理了的符合要求的reasult的个数。

    @staticmethod
    def initDriver():
        # 创建options
        options = Options()
        # options添加启动参数
        options.add_argument('--headless')  # 无头模式(不展示界面)
        options.add_argument('log-level=3')  # INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
        # options添加试验选项
        prefs = {
            "profile.managed_default_content_settings.images": 2,  # 禁用图片
            'profile.default_content_setting_values': {'notifications': 2}  # 禁用弹窗
        }
        options.add_experimental_option("prefs", prefs)
        # 创建driver
        baidusearcher.driver = webdriver.Chrome(
            options=options,
            executable_path='D:/ProgramFiles/chromedriver/chromedriver.exe'
        )

    @staticmethod
    def closeDriver():
        # baidusearcher.driver.close()  # 关闭当前窗口，如果是当前打开的最后一个窗口，则退出浏览器（driver）
        baidusearcher.driver.quit()  # 关闭所有相关的窗口，退出浏览器（driver）

    @staticmethod
    def initSearcher(
        keyword,
        startY=None, startM=None, startD=None, startH=None, startMi=None, startS=None,
        endY=None, endM=None, endD=None, endH=None, endMi=None, endS=None,
        howManyResultWanted=5,
        sourceWebsite=None,
        fiddler=None,
        searchPageProcess = None,
        resultPageProcess = None
    ):
        # 传参：要多少result
        baidusearcher.resultWanted = howManyResultWanted
        # 传参：关键字
        baidusearcher.searchKeyword = keyword
        # 传参：限制来源网页
        if sourceWebsite is not None:
            baidusearcher.searchSourceWebsite = sourceWebsite
        # 传参：限制开始时间
        now = datetime.datetime.now()
        ifStartTimeSeted = (startY or startM or startD or startH or startMi or startS) is not None
        ifEndTimeSeted = (endY or endM or endD or endH or endMi or endS) is not None
        if ifStartTimeSeted is True:
            startY = startY if startY is not None else now.year
            startM = startM if startY is not None else now.month
            startD = startD if startY is not None else now.day
            'startH = startH if startY is not None else today.day'
            'startMi = startMi if startY is not None else today.day'
            'startS = startS if startY is not None else today.day'
            baidusearcher.searchStartTime = datetime.datetime(startY, startM, startD, 0, 0, 0)
        # 传参：限制结束时间
        if ifEndTimeSeted is True:
            endY = endY if endY is not None else now.year
            endM = endM if endY is not None else now.month
            endD = endD if endY is not None else now.day
            'endH = endH if endY is not None else today.day'
            'endMi = endMi if endY is not None else today.day'
            'endS = endS if endY is not None else today.day'
            baidusearcher.searchEndTime = datetime.datetime(endY, endM, endD, 23, 59, 59)
        else:
            if ifStartTimeSeted is True:
                # 当开始时间设置了，即使结束时间没设置，也要默认设为当前时间
                baidusearcher.searchEndTime = now
            else:
                pass
        # 传参：搜索网址
        baidusearcher.searchUrlInput = baidusearcher.searchBaseUrl
        '''添加关键词'''
        baidusearcher.searchUrlInput += ('&wd=' + baidusearcher.searchKeyword)
        '''添加来源网站'''
        if baidusearcher.searchSourceWebsite is not None:
            baidusearcher.searchUrlInput += ('&si=' + baidusearcher.searchSourceWebsite)
        '''添加开始时间'''
        if baidusearcher.searchStartTime is not None:
            startTimeUnix = time.mktime(baidusearcher.searchStartTime.timetuple())
            startTimeUnix = str(int(startTimeUnix))
            baidusearcher.searchUrlInput += ('&gpc=stf=' + startTimeUnix)
        elif baidusearcher.searchEndTime is not None:
            baidusearcher.searchUrlInput += ('gpc=stf=' + '0')
        '''添加结束时间'''
        if baidusearcher.searchEndTime is not None:
            endTimeUnix = time.mktime(baidusearcher.searchEndTime.timetuple())
            endTimeUnix = str(int(endTimeUnix))
            baidusearcher.searchUrlInput += (',' + endTimeUnix)
            baidusearcher.searchUrlInput += '%7Cstftype%3D2&tfflag=1'
        '''添加每页结果数'''
        baidusearcher.searchUrlInput += ('&rn=' + str(baidusearcher.searchHowManyResultsOnePage))
        # 传参：处理函数
        baidusearcher.searchPageProcess = searchPageProcess
        baidusearcher.resultPageProcess = resultPageProcess

    @staticmethod
    def search():
        # 类变量名字太长，固定不变的类变量起个简短的别名
        rn = baidusearcher.searchHowManyResultsOnePage
        # 运行参数归零
        baidusearcher.searchIndex = -1
        baidusearcher.resultIndex = -1
        baidusearcher.resultIndexInPage = None
        baidusearcher.resultSaved = 0
        # 遍历每个返回结果
        while baidusearcher.resultSaved <= baidusearcher.resultWanted:
            # 遍历下一个result
            baidusearcher.resultIndex += 1
            # 确认页数
            ifNextPage = baidusearcher.searchIndex != (baidusearcher.resultIndex // rn)
            baidusearcher.searchIndex = baidusearcher.resultIndex // rn
            baidusearcher.resultIndexInPage = baidusearcher.resultIndex % rn
            # 是否翻页
            if ifNextPage:
                baidusearcher.searchUrlInput += ('&pn=' + str(baidusearcher.searchIndex*rn))
                print(
                    indent(
                        '第'+str(baidusearcher.searchIndex)+'页'+baidusearcher.searchUrlInput,
                        length=100, fIndent=2, lIndent=2
                    )
                )
                # 访问
                baidusearcher.driver.get(baidusearcher.searchUrlInput)
                # 获取信息
                baidusearcher.searchHtml = baidusearcher.driver.page_source
                baidusearcher.searchTitle = baidusearcher.driver.title
                baidusearcher.searchUrlOutput = baidusearcher.driver.current_url
                baidusearcher.searchRoot = etree.HTML(baidusearcher.searchHtml)
                # 处理搜索页
                baidusearcher.searchPageProcess()
            # 定位result
            baidusearcher.resultXPath = baidusearcher.resultXPathPattern(baidusearcher.resultIndexInPage)
            baidusearcher.resultElement = baidusearcher.searchRoot.xpath('.'+baidusearcher.resultXPath)
            # 如果result定位失败,则跳过此次循环
            if baidusearcher.resultElement == []:
                print('  没有更多的结果了')
                return 0
            else:
                baidusearcher.resultElement = baidusearcher.resultElement[0]
            # 定位resultUrl
            baidusearcher.resultUrlInput = baidusearcher.resultElement.xpath('./'+baidusearcher.resultAXPath+'/@href')
            # 如果结果url定位失败则跳过此次循环
            if baidusearcher.resultUrlInput == []:
                print(
                    indent(
                        '第%d(%dp%d)个结果,因如下原因落选:%s' % (
                            baidusearcher.resultIndex,
                            baidusearcher.searchIndex,
                            baidusearcher.resultIndexInPage,
                            '未找到网址'
                        ),
                        length=100, fIndent=4, lIndent=4
                    )
                )
                continue
            else:
                baidusearcher.resultUrlInput = baidusearcher.resultUrlInput[0]
            # 处理resultPage
            resultProcessReturn = baidusearcher.resultPageProcess()
            # 判断结果是否合格
            if resultProcessReturn[0]:
                baidusearcher.resultSaved += 1
                print(
                    indent(
                        '第%d(%dp%d)个结果入选为第%d个正确结果: ' % (
                            baidusearcher.resultIndex,
                            baidusearcher.searchIndex,
                            baidusearcher.resultIndexInPage,
                            baidusearcher.resultSaved
                        ),
                        length=100, fIndent=4, lIndent=4
                    )
                )
            else:
                print(
                    indent(
                        '第%d(%dp%d)个结果,因如下原因落选:%s' % (
                            baidusearcher.resultIndex,
                            baidusearcher.searchIndex,
                            baidusearcher.resultIndexInPage,
                            resultProcessReturn[1]
                        ),
                        length=100, fIndent=4, lIndent=4
                    )
                )
