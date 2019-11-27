# -*- coding: utf-8 -*-

import datetime3 as datetime  # 用于获取当前日期作为默认日期
import time  # 用于获取unix时间作为url中的参数，用于睡觉
from lxml import etree
import re
# from readability import Document
# from html2text import html2text
from indentation import indent  # 字符串缩进
# from sysdb import SysDb  # 数据库
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class baidusearcher():
    driver = None  # webdriver.Chrome()

    @staticmethod
    def initDriver():
        # 创建options
        options = Options()
        # options添加启动参数
        # options.add_argument('--headless')  # 无头模式(不展示界面)
        options.add_argument('log-level=3')#INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
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
    def search(
        keyword,
        startY=None, startM=None, startD=None, startH=None, startMi=None, startS=None,
        endY=None, endM=None, endD=None, endH=None, endMi=None, endS=None,
        howManyResultWanted=5,
        sourceWebsite=None,
        fiddler=None,
        # searchProcessFunc=None,  # 处理搜索页面的函数
        # responseProcessFunc=None  # 处理每个搜索结果的函数
    ):
        # url
        searchBaseUrl = 'https://www.baidu.com/s' +\
            '?ie=utf-8' +\
            '&tn=monline_4_dg' +\
            '&ct=2097152' +\
            '&rqlang=cn'
        # '&f=8'
        # '&rsv_bp=1'
        # '&rsv_enter=1' +\
        # '&rsv_dl=tb'
        # 搜索引擎
        searchEngine = 'baidu.com'
        # 关键字
        searchBaseUrl = searchBaseUrl + '&wd=' + keyword
        # 限定网站
        if sourceWebsite is not None:
            searchBaseUrl = searchBaseUrl + '&si=' + sourceWebsite
        # 限定时间
        today = datetime.datetime.now()
        ifStartTimeSeted = not (startY == startM == startD == startH == startMi == startS == None)
        ifEndTimeSeted = not (endY == endM == endD == endH == endMi == endS == None)
        if ifStartTimeSeted is False and ifEndTimeSeted is False:
            pass
        else:
            # 开始时间，设置
            if ifStartTimeSeted is True:
                startY = startY if startY is not None else today.year
                startM = startM if startY is not None else today.month
                startD = startD if startY is not None else today.day
                'startH = startH if startY is not None else today.day'
                'startMi = startMi if startY is not None else today.day'
                'startS = startS if startY is not None else today.day'
                startTime = datetime.datetime(startY, startM, startD, 0, 0, 0)
                startTimeUnix = time.mktime(startTime.timetuple())
                searchBaseUrl = searchBaseUrl + '&gpc=stf=' + str(int(startTimeUnix))
            # 开始时间，不设置则为0
            else:
                searchBaseUrl = searchBaseUrl + 'gpc=stf=' + '0'
            # 结束时间，设置
            if ifStartTimeSeted is True:
                endY = endY if endY is not None else today.year
                endM = endM if endY is not None else today.month
                endD = endD if endY is not None else today.day
                'endH = endH if endY is not None else today.day'
                'endMi = endMi if endY is not None else today.day'
                'endS = endS if endY is not None else today.day'
                endTime = datetime.datetime(endY, endM, endD, 23, 59, 59)
                endTimeUnix = time.mktime(endTime.timetuple())
                searchBaseUrl = searchBaseUrl + ',' + str(int(endTimeUnix))
            # 结束时间，不设置则为当前时间
            else:
                searchBaseUrl = searchBaseUrl + ',' + time.mktime(today.timetuple())
            # 时间的其他相关设置
            searchBaseUrl = searchBaseUrl + '%7Cstftype%3D2&tfflag=1'
        # 设置每页显示多少结果
        rn = 10
        searchBaseUrl = searchBaseUrl + '&rn=' + str(rn)  # 每页十个结果

        # 遍历每个返回结果
        howManyResultSaved = 0
        curResultIndex = -1  # 从0开始
        curPage = -1  # 从0开始
        curResultIndexInPage = None  # 从0开始
        while howManyResultSaved <= howManyResultWanted:
            curResultIndex += 1
            # 确认页数
            ifNextPage = curPage != curResultIndex // rn
            curPage = curResultIndex // rn
            curResultIndexInPage = curResultIndex % rn
            # 是否翻页
            if ifNextPage:
                curSearchUrlInput = searchBaseUrl + '&pn=' + str(curPage*rn)
                print(indent('第'+str(curPage)+'页'+curSearchUrlInput, fIndent=2, length=200))
                # 访问
                baidusearcher.driver.get(curSearchUrlInput)
                # 获取信息
                curSearchHtml = baidusearcher.driver.page_source
                curSearchTitle = baidusearcher.driver.title
                curSearchUrlOutput = baidusearcher.driver.current_url
                curSearchRoot = etree.HTML(curSearchHtml)
                # ###########处理搜索页面(开始)#################################################
                # 保存搜索页
                filePath = "./corpora/"+ searchEngine + "/"
                if sourceWebsite is not None:
                    filePath += sourceWebsite
                filePath += str(startTime.date())
                filePath += '-'
                filePath += str(endTime.date())
                filePath += '.html'
                file = open(filePath, "wb")
                file.write(curSearchHtml.encode('utf-8'))
                file.close()
                # ###########处理搜索页面(结束)#################################################
            # 定位搜索结果
            curResultXPath = '//*[@id=\"' + str(curResultIndexInPage + 1) + '\"]'
            curResultElement = curSearchRoot.xpath(curResultXPath)
            if curResultElement == []:
                # 没有更多的结果了
                return 0
            else:
                curResultElement = curResultElement[0]
            curResultUrlInput = curResultElement.xpath('./h3/a/@href')
            if curResultUrlInput == []:
                print(indent('第'+str(curResultIndex)+'个结果,因未找到网址而落选: '))
                continue
            else:
                curResultUrlInput = curResultUrlInput[0]
            # ###########处理结果页面(开始)#################################################
            isSaved = False
            baidusearcher.driver.find_element_by_xpath(curResultXPath+'/h3/a').click()
            baidusearcher.driver.switch_to.window(baidusearcher.driver.window_handles[1])
            curResultUrlOutput = baidusearcher.driver.current_url
            curResultHtml = baidusearcher.driver.page_source
            baidusearcher.driver.close()
            time.sleep(2)

            
            # ###########处理结果页面(结束)#################################################
            if isSaved:
                howManyResultSaved += 1
                print(indent('第'+str(curResultIndex)+'个结果入选为第' + str(howManyResultSaved) + '个正确结果：'))
            else:
                print(indent('第'+str(curResultIndex)+'个结果,被结果处理函数判定为落选: '))



    '''
    # 结束时间
    pass
    # 输出进度
    print('搜索Url：', url)

    # 发送一个http请求并接收结果
    r = requests.getPlus(url, verify=fiddler)
    # 判断http请求是否正确返回
    if r.status_code != 200:
        print('error：搜索页状态码异常')
        return 0
    # 获取返回html文本
    'r.encoding = "utf-8"  # 因为是针对bing，我们知道编码肯定是utf-8'
    searchHtml = r.text
    # 判断返回中是否有查询结果，判断是否被ban
    t = re.findall(r'条结果', searchHtml, re.I)
    if t == []:
        print('error：被ban了')
        return 0
    else:
        t = re.findall(r'\d+(?= 条结果)', searchHtml, re.I)
        t = t[0]
        print('搜索结果共几条：', t)
    # 解析searchHtml
    tree = etree.HTML(searchHtml)
    # 真正有效的新闻有几条（不算视频集和图片集）
    newsList = tree.xpath('/html/body[1]/div[1]/main[1]/ol[1]/li[@class="b_algo"]')
    newsNum = len(newsList)
    print('真正有效的新闻共几条：', newsNum)
    # 保存搜索页
    file = open("./corpora/" + searchEngine + '_' + str(curDate) + '.html', "wb")
    file.write(searchHtml.encode('utf-8'))
    file.close()

    # 循环(howManyNewsOneDay)条真正有效的新闻
    newsIndex = 0  # 注意是从1开始的,因为以上来就+=1(历史原因，懒得改了)
    howManyNewsSaved = 0
    while howManyNewsSaved < maxWebsitesNum:
        newsIndex += 1
        # 如果总共都不够那么多条，那及时退出
        if newsIndex > newsNum:
            break
        print('  第%d个新闻' % newsIndex)
        # 取出当前新闻的相关信息
        news = newsList[newsIndex-1]
        titleElement = news.xpath('./h2/a')
        # 判断是否网页新闻(有可能是ppt,pdf)
        if titleElement == []:
            print('    新闻可能是文件形式，不算数')
            continue
        titleElement = titleElement[0]
        newsUrl = titleElement.attrib['href']
        print('    网址：', newsUrl)
        newsTitle = titleElement.text
        print('    标题：', newsTitle)
        introduction = news.xpath('string(./div[1]/p[1])')
        print('    简介：', end='')
        print(indent(introduction, length=40, fIndent=0, lIndent=10))
        newsTime = re.findall(r'^\d+-\d+-\d+', introduction, re.I)[0]
        newsTimeYear = int(re.findall(r'^\d+(?=-)', newsTime, re.I)[0])
        newsTimeMonth = int(re.findall(r'(?<=-)\d+(?=-)', newsTime, re.I)[0])
        newsTimeDay = int(re.findall(r'(?<=-)\d+$', newsTime, re.I)[0])
        print('    发布时间：', newsTime)
        newsId = searchEngine + '_' + str(curDate) + '_' + str(newsIndex)
        print('    Id：', newsId)

        # 判断是否文字新闻，是否合格
        host = re.search('(?<=://)\S+?(?=/)', newsUrl).group()
        if host in ['www.yunjuu.com', 'v.qq.com', 'www.bilibili.com', 'v.youku.com', 'haokan.baidu.com', ]:
            print('    新闻不合格，这个不算数')
            continue

        # 访问新闻网页
        try:
            r = requests.getPlus(newsUrl, verify=fiddler)
        except Exception as e:
            print('    这个新闻网站跪了，不算数：', e)
            continue
        # 是否返回成功
        if r.status_code != 200:
            print('    error: 状态码非200,不算数')
            continue
        # 获取返回html文本
        'r.encoding = "utf-8"'
        newsHtml = r.text
        # 去掉html中的回车和多余空格
        newsHtml = newsHtml.replace('\n', '')
        newsHtml = newsHtml.replace('  ', '')
        # 用readability抽取主要信息
        newsdoc = Document(newsHtml)
        newsTitle = newsdoc.title()
        print('    标题：', newsTitle)
        newsContentWithTags = newsdoc.summary()  # readability包的处理结果是带着html标签的
        # 去掉html标签，得到纯文本
        newsContent = html2text(newsContentWithTags)
        # 输出content
        print('    正文：', end='')
        print(indent(newsContent, length=40, fIndent=0, lIndent=10))

        # 判断是否文字新闻，是否合格
        if len(newsContent) < 270:
            print('    新闻不合格，这个不算数')
            continue

        # 插入数据库
        SysDb.insertRow(
            'websiteTabel',
            {
                '搜索引擎': searchEngine,
                '搜索日期年': curDate.year,
                '搜索日期月': curDate.month,
                '搜索日期日': curDate.day,
                '搜索网址': searchUrl,
                '搜索html': searchHtml,
                '新闻序号': newsIndex,
                '新闻ID': newsId,
                '新闻网址原': newsUrl,
                '新闻网址真': r.url,
                '新闻html': newsHtml,
                '新闻标题': newsTitle,
                # '新闻作者': {'类型': '文本', '初始值': None, '主键否': '非主键'},
                # '新闻机构': {'类型': '文本', '初始值': None, '主键否': '非主键'},
                '新闻日期年': newsTimeYear,
                '新闻日期月': newsTimeMonth,
                '新闻日期日': newsTimeDay,
                '新闻正文': newsContent
            }
        )
        # 保存了一个，计数加一
        howManyNewsSaved += 1
        '''