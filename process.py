from sysdb import SysDb  # 数据库
import re
from baidusearcher import baidusearcher  # 百度爬虫
import traceback  # 用于获取异常的详细信息
from lxml import etree
import datetime3 as datetime  # 用于获取当前日期作为默认日期


def searchPageProcess():
    # 生成保存路径
    filePath = "./corpora"
    filePath += ("/" + baidusearcher.searchEngine)
    filePath += ('-' + baidusearcher.searchKeyword + "/")
    if baidusearcher.searchSourceWebsite is not None:
        filePath += baidusearcher.searchSourceWebsite
    filePath += str(baidusearcher.searchStartTime.date())
    filePath += '-'
    filePath += str(baidusearcher.searchEndTime.date())
    filePath += '.html'
    # 保存搜索页
    file = open(filePath, "wb")
    file.write(baidusearcher.searchHtml.encode('utf-8'))
    file.close()


def resultPageProcess():
    try:
        # 在新标签页访问result页，driver句柄切换到新标签页
        '''有bug，模拟按键方法无效：
        baidusearcher.driver.find_element_by_xpath('//body').send_keys(Keys.CONTROL, 't')
        baidusearcher.driver.switch_to.window(baidusearcher.driver.window_handles[1])
        baidusearcher.driver.get(baidusearcher.resultUrlInput)
        '''
        baidusearcher.driver.execute_script("window.open('"+baidusearcher.resultUrlInput+"','_blank');") 
        baidusearcher.driver.switch_to.window(baidusearcher.driver.window_handles[1])
        # 获取resultUrlOutput
        baidusearcher.resultUrlOutput = baidusearcher.driver.current_url
        if re.search('www.xinhuanet.com/world', baidusearcher.resultUrlOutput) is None:
            # 只处理新华网http://www.xinhuanet.com/world分支下的新闻
            return(False, '不是world分支下的新闻')
        # 获取resultHtml
        baidusearcher.resultHtml = baidusearcher.driver.page_source
        # 获取resultRoot
        baidusearcher.resultRoot = etree.HTML(baidusearcher.resultHtml)
        # 获取resultTitle
        resultTitle = baidusearcher.resultRoot.xpath('/html/body/div[2]/div[3]/div/div[1]')[0].text
        resultTitle = re.sub(r'^\s*', "", resultTitle)
        resultTitle = re.sub(r'\s*$', "", resultTitle)
        baidusearcher.resultTitle = resultTitle
        # 获取resultText
        pList = baidusearcher.resultRoot.xpath('//*[@id="p-detail"]/p')
        textList = []
        for p in pList:
            if p.text is not None:
                textList.append(p.text)
        textList = [re.sub(r'^\s*', "", x) for x in textList]
        textList = [re.sub(r'\s*$', "", x) for x in textList]
        baidusearcher.resultText = '\n'.join(textList)
        # 获取resultTime
        resultTime = baidusearcher.resultRoot.xpath('/html/body/div[2]/div[3]/div/div[2]/span[1]')[0].text
        resultTimeY = int(re.search(r'(?<= )\d+(?=-)', resultTime).group())
        resultTimeM = int(re.search(r'(?<=-)\d+(?=-)', resultTime).group())
        resultTimeD = int(re.search(r'(?<=-)\d+(?= )', resultTime).group())
        baidusearcher.resultTime = datetime.date(resultTimeY, resultTimeM, resultTimeD)
        # 存到数据库
        resultSaveToDb()
        # 如果顺利执行，则isSaved置True
        return(True, 0)
    # 如果有任何问题，则跳过这次循环
    except Exception:
        return(False, traceback.format_exc())
    # 如果新标签页建立成功，最后要关闭新标签页，切回搜索页
    finally:
        if len(baidusearcher.driver.window_handles) == 2:
            baidusearcher.driver.switch_to.window(baidusearcher.driver.window_handles[1])
            baidusearcher.driver.close()
            baidusearcher.driver.switch_to.window(baidusearcher.driver.window_handles[0])


def resultSaveToDb():
    SysDb.insertRow(
        'websiteTabel',
        {
            '搜索引擎': baidusearcher.searchEngine,
            '搜索关键字': baidusearcher.searchKeyword,
            '搜索日期年': baidusearcher.searchStartTime.year,
            '搜索日期月': baidusearcher.searchStartTime.month,
            '搜索日期日': baidusearcher.searchStartTime.day,
            '搜索网址': baidusearcher.searchUrlInput,
            '搜索html': baidusearcher.searchHtml,
            '新闻序号': baidusearcher.resultSaved,
            '新闻ID': '%s-%s@%d/%d/%d-%d' % (
                baidusearcher.searchEngine,
                baidusearcher.searchKeyword,
                baidusearcher.searchStartTime.year,
                baidusearcher.searchStartTime.month,
                baidusearcher.searchStartTime.day,
                baidusearcher.resultIndex
            ),
            '新闻网址原': baidusearcher.resultUrlInput,
            '新闻网址真': baidusearcher.resultUrlOutput,
            '新闻html': baidusearcher.resultText,
            '新闻标题': baidusearcher.resultTitle,
            # '新闻作者': {'类型': '文本', '初始值': None, '主键否': '非主键'},
            # '新闻机构': {'类型': '文本', '初始值': None, '主键否': '非主键'},
            '新闻日期年': baidusearcher.resultTime.year,
            '新闻日期月': baidusearcher.resultTime.month,
            '新闻日期日': baidusearcher.resultTime.day,
            '新闻正文': baidusearcher.resultText
        }
    )
