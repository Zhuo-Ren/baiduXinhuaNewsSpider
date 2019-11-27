# -*- coding: utf-8 -*-
import requests
import re
from lxml import etree

def getPlus(url, params=None, **kwarg):
    """
        :function requests.get函数的升级版本。之后会添加到requests.getPlus()。\n
        1.原版get实现了304自动跳转；
        本升级版本增加了对meta自动跳转的实现。\n
        2.原版get中如果不提供headers参数，则会在header中声明自己是程序；
        本升级版本增加了默认header，声明自己是浏览器。

        :param url: URL for the new Request object.

        :param params: (optional) Dictionary or bytes to be sent in the query string for the Request.

        :param **kwargs: Optional arguments that request takes.

        :return: Response <Response> object

        :example 1 \n
                requests.getPlus('http://news.carnoc.com/list/456/456513.html')
    """
    ifNeedGet = True
    curUrl = url
    while ifNeedGet:
        # 更新参数（主要是更新header）
        '''
        此处更新参数有两个功能。
        1.提供默认的header。如果getPlus的参数中没有header，那么使用默认header
        2.如果需要跳转，为跳转访问提供header
        '''
        host = re.search('(?<=://)\S+?(?=/)', curUrl).group()
        if 'headers' not in kwarg.keys():
            kwarg['headers'] = {
                'Host': host,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Accept-Encoding': 'gzip, deflate',  # , br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cookie': 'SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=E97E2854C8B940839A4C0B7EDDDDA6E3&dmnchg=1; SRCHUSR=DOB=20191117&T=1573969605000; _SS=SID=3F775F87A79A66621E315190A6B46703&HV=1573970707; _EDGE_S=F=1&SID=3F775F87A79A66621E315190A6B46703; _EDGE_V=1; MUID=1482B60FE8C9631F3087B818E9E76213; MUIDB=1482B60FE8C9631F3087B818E9E76213; SRCHHPGUSR=CW=1600&CH=774&DPR=1&UTC=480&WTS=63709566405; ipv6=hit=1573973206991&t=6'
                # 'cache-control': 'no-cache,no-store',  # 'max-age=0',  # '  #'max-age=0'  # 'no-cache'
                # 'Pragma': 'no-cache'
                # 'TE': 'Trailers'
            }
        else:
            kwarg['headers']['Host'] = host
        print('    发起访问请求')
        r = requests.get(curUrl, params, **kwarg)
        # 判断是否正常返回
        if 400 <= r.status_code < 600:
            print('    error: 状态码为4**或5**  <-------------------------------------------')
        # 判断是否304跳转
            pass
        # 判断是否meta跳转
        ''' r.encoding = "utf-8" '''
        '先假设返回的是html文件（不是也没关系，因为判定失败不会执行）'
        html = r.text
        root = etree.HTML(html)
        '''meta中的跳转一般长这样:
           <meta http-equiv="Refresh" content="3;url=http://www.haishui.NET">
           其中3是3秒后跳转，url是跳到哪里
        '''
        '尝试取出content的值'
        # 这里有bug，处于<no-script>标签中的内容不应被识别
        content = root.xpath('//meta[@http-equiv="refresh" and @content]/@content')
        if content == []:
            # 没匹配到content就是返回的不是html文件，或者是html文件但无需meta跳转
            pass
        else:  # content不空就是需要meta跳转
            print('    需要meta跳转')
            content = content[0]
            nextUrl = re.search(r"(?<=url=) *\S+", content)
            if nextUrl is None:
                print('    error:跳转url提取失败 <-------------------------------------------')
                return r
            else:
                nextUrl = nextUrl.group()
                nextUrl = nextUrl.replace(' ', '')
                print('    跳转到：', nextUrl)
            curUrl = nextUrl
            continue
        # 判断是否js跳转
        "<script language='javascript'\r\ntype='text/javascript'>window.location.href='http://www.bfttiao.com/shehui/bftt711164.html'</script>"
        if False:  # 太麻烦，没实现
            print('    需要js跳转')
            nextUrl = '巴拉巴拉'
            curUrl = nextUrl
            continue
        # 无任何跳转
        ifNeedGet = False
        # 确定编码
        try:
            # <meta charset="gbk">
            # <meta http-equiv="Content-Type" content="text/html; charset=gb2312">
            trueEncoding = re.search(r"<meta [^<>]*charset[^<>]*>", r.text, re.I).group()
            trueEncoding = re.search(r"(?<=charset=)[\'\" ]*[^ \'\"]+(?=[ \'\">])", trueEncoding, re.I).group()
            trueEncoding = trueEncoding.replace('\'', '')
            trueEncoding = trueEncoding.replace('\"', '')
            r.encoding = trueEncoding
        except Exception:
            print('    error: 找不到真实编码格式，只能用猜的了  <-------------------------------------------')
            r.encoding = r.apparent_encoding
    return r


requests.getPlus = getPlus
