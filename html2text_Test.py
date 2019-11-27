# -*- coding: UTF-8 -*-
from html2text import html2text

contentWithTags = '''
<html>
    <body>
        <div>
            <div id="Content" class="article">
            <p><strong>“安享和平是人民之福，保卫和平是人民军队之责。”</strong></p> 
            <p><strong>——习近平</strong></p>
            <p align="center">
                <img id="img-5bebe863a3101a87b1daaf47" alt=" " src="//img3.chinadaily.com.cn/images/201811/14/5bebe863a3101a87b1daaf47.jpeg" align="middle"/>
            </p>
            <p>2018年1月3日，中共中央总书记、国家主席、中央军委主席习近平视察中部战区陆军某师。这是习近平同该师侦察英雄杨子荣生前所在连官兵亲切交谈。</p> <p align="center"><img id="img-5bebe863a3101a87b1daaf49" alt=" " src="//img3.chinadaily.com.cn/images/201811/14/5bebe863a3101a87b1daaf49.jpeg" align="middle"/></p> <p>2018年6月11日，中共中央总书记、国家主席、中央军委主席习近平视察北部战区海军，离开潜艇前，勉励官兵们坚定理想信念，建设坚强集体，把打赢本领搞过硬。</p> 
            <p><span/></p> <p><strong>我是谁</strong></p> <p>我是<strong>母亲倚在门口牵不到的那只手</strong></p> 
            <p align="center"><img id="img-5bebe863a3101a87b1daaf4c" alt="" src="//img3.chinadaily.com.cn/images/201811/14/5bebe863a3101a87b1daaf4c.png" align="middle"/></p> <p>我是<strong>妻子舍不得挂掉的电话</strong></p> <p align="center"><img id="img-5bebe863a3101a87b1daaf4e" alt="" src="//img3.chinadaily.com.cn/images/201811/14/5bebe863a3101a87b1daaf4e.png" align="middle"/></p> <p>我是<strong>儿子眼里不敢靠近的陌生人</strong></p> <p align="center"><img id="img-5bebe863a3101a87b1daaf50" alt="" src="//img3.chinadaily.com.cn/images/201811/14/5bebe863a3101a87b1daaf50.png" align="middle"/></p> <p>我是<strong>亲人的牵挂与骄傲</strong></p> <p align="center"><img id="img-5bebe863a3101a87b1daaf52" alt="" src="//img3.chinadaily.com.cn/images/201811/14/5bebe863a3101a87b1daaf52.png" align="middle"/></p> <p><strong>我身后是和平，我面前是战争</strong></p> <p><strong>拿起钢枪，就要放下儿女情长</strong></p> <p><strong>穿上军装，就要舍弃舒适安逸</strong></p> <p align="center"><img id="img-5bebe863a3101a87b1daaf54" alt="" src="//img3.chinadaily.com.cn/images/201811/14/5bebe863a3101a87b1daaf54.png" align="middle"/></p> <p><strong>征战疆场，男儿本色</strong></p> <p><strong>从军报国，此生无悔</strong></p> <p align="center"><img id="img-5bebe863a3101a87b1daaf56" alt="" src="//img3.chinadaily.com.cn/images/201811/14/5bebe863a3101a87b1daaf56.png" align="middle"/></p> <p><strong>我是中国军人</strong></p> 
            <p><strong>我是人民子弟兵</strong></p> <p><strong>我是美好生活的守护者</strong></p> <p align="center"><img id="img-5bebe863a3101a87b1daaf59" alt="" src="//img3.chinadaily.com.cn/images/201811/14/5bebe863a3101a87b1daaf59.png" align="middle"/></p> <p>今天，央视网与众多网络媒体</p> <p>共同发起“<strong>我和军队的不解之缘</strong>”网络互动活动</p> <p align="center"><img id="img-5bebe863a3101a87b1daaf5c" alt="" src="//img3.chinadaily.com.cn/images/201811/14/5bebe863a3101a87b1daaf5c.png" align="middle"/></p> <p><strong>“您和部队是怎样结下不解之缘的？”</strong></p> <p><strong>“在部队里您最难忘的一件事是什么？”</strong></p> <p><strong>“从警或入伍期间执行的最危险的任务是什么？”</strong></p> 
            <p><strong>“有个军人爸爸是一种怎样的体验？”</strong></p> <p><strong>“有个军人丈夫是一种怎样的体验？”</strong></p> <p><strong>......</strong></p> <strong> <p align="center">让我们一起聊聊我与军队的「不解之缘」</p> <p align="center">欢迎大家上传照片、视频、或撰写文字故事</p> <p align="center">分享您或家人与军队的故事</p> <p class="content5_xq17896_180426 red" align="center"><strong>您可以通过央视网新媒体参与活动</strong></p> <p class="content5_xq17896_180426 red" align="center">　　1、将自己或家人与军队的故事讲述给我们，您可以上传照片、视频到征集平台</p> <p class="content5_xq17896_180426 red" align="center">识别二维码进入征集平台</p> <p class="content5_xq17896_180426 red" align="center"><img alt="" src="//img3.chinadaily.com.cn/images/201811/14/5bebe863a3101a87b1daaf5e.png" id="img-5bebe863a3101a87b1daaf5e"/></p> <p class="content5_xq17896_180426 red" align="center">　　2、通过新浪微博平台，上传发布照片、视频或撰写文字故事，加话题#我和军队的不解之缘#并@央视网</p> <p class="content5_xq17896_180426 red" align="center">　　3、通过微信平台，给央视网公众号留言，上传照片、短视频或文字分享故事</p> <p align="center"><strong><span>我们会选择优秀的故事</span></strong></p> <p align="center"><strong><span>在全网多平台进行展播</span></strong></p> <p align="center"><strong><span>您的精彩故事将会分享给更多网友</span></strong></p> </strong> 
            </div>        
        </div>
    </body>
</html>
'''
print(html2text(contentWithTags))
