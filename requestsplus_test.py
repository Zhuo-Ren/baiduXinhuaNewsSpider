import requests
import requestsplus


url = 'http://www.chinanews.com/ty/2018/07-02/8553100.shtml'  # 这个网页是apparent_encoding会猜错的
url = 'http://toutiao.hebtv.com/shehui/bftt711164.html'  # 这个网页是内嵌js跳转的
url = 'http://news.carnoc.com/list/456/456513.html'  # 这个网页是需要meta跳转的

url = 'https://www.cnbeta.com/articles/tech/744107.htm'
# 使用fiddler吗
fiddler = None  #"./DO_NOT_TRUST_FiddlerRoot.crt"

# 发送一个http请求并接收结果
headers = {
    'Host': 'cn.bing.com',
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
r = requests.getPlus(url, headers=headers, verify=fiddler)
pass
