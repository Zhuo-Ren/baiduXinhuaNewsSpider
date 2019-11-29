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
    if baidusearcher.searchStartTime is None and baidusearcher.searchEndTime is None:
        pass
    elif baidusearcher.searchStartTime is not None and baidusearcher.searchEndTime is None:
        pass  # 不可能出现这种情况，以为这时endTime会被设为当前时间
    elif baidusearcher.searchStartTime is None and baidusearcher.searchEndTime is not None:
        filePath += '0'
        filePath += '-'
        filePath += str(baidusearcher.searchEndTime.date())
    elif baidusearcher.searchStartTime is not None and baidusearcher.searchEndTime is not None:
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


def resultPageProcessWangyi():
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
        # 获取resultHtml
        baidusearcher.resultHtml = baidusearcher.driver.page_source
        # 获取resultRoot
        baidusearcher.resultRoot = etree.HTML(baidusearcher.resultHtml)
        # 获取resultTitle
        resultTitle = baidusearcher.resultRoot.xpath('/html/body/div[4]/div[2]/h1')[0].text
        resultTitle = re.sub(r'^\s*', "", resultTitle)
        resultTitle = re.sub(r'\s*$', "", resultTitle)
        baidusearcher.resultTitle = resultTitle
        # 获取resultText
        div = baidusearcher.resultRoot.xpath('//*[@id="endText"]')[0]
        baidusearcher.resultText = html2textWangyi(etree.tostring(div).decode('utf-8'))
        # 获取resultTime
        resultTime = baidusearcher.resultRoot.xpath('/html/body/div[4]/div[2]/div[1]')[0].text
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


def html2textWangyi(htmlText):
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
            if element.tag == 'img':
                plainText += '\n【图】\n'
            else:
                pass
        #   对<!--  -->，直接跳过
        elif re.search(r'^<cyfunction Comment at', str(element.tag)):
            pass
        #   对只包含不可见文本的标签，直接跳过
        elif re.search('^\s*$', element.text):
            pass
        #   对包含可见文本的标签
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


def resultSaveToDb():
    now = datetime.datetime.now()
    sY = baidusearcher.searchStartTime.year if baidusearcher.searchStartTime is not None else 0
    sM = baidusearcher.searchStartTime.month if baidusearcher.searchStartTime is not None else 0
    sD = baidusearcher.searchStartTime.day if baidusearcher.searchStartTime is not None else 0
    eY = baidusearcher.searchEndTime.year if baidusearcher.searchStartTime is not None else now.year
    eM = baidusearcher.searchEndTime.month if baidusearcher.searchStartTime is not None else now.month
    eD = baidusearcher.searchEndTime.day if baidusearcher.searchStartTime is not None else now.day
    SysDb.insertRow(
        'websiteTabel',
        {
            '搜索引擎': baidusearcher.searchEngine,
            '搜索关键字': baidusearcher.searchKeyword,
            '搜索起始日期年': sY,
            '搜索起始日期月': sM,
            '搜索起始日期日': sD,
            '搜索终止日期年': eY,
            '搜索终止日期月': eM,
            '搜索终止日期日': eD,
            '搜索网址': baidusearcher.searchUrlInput,
            '搜索html': baidusearcher.searchHtml,
            '新闻序号': baidusearcher.resultSaved,
            '新闻ID': '%s-%s@%d/%d/%d-%d/%d/%d-%d' % (
                baidusearcher.searchEngine,
                baidusearcher.searchKeyword,
                sY, sM, sD, eY, eM, eD,
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
