# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from datetime import datetime, date
from soushi.managedata import formatProName
from soushi.notifyJava import notifyJava
from soushi.program import Program
from soushi.pipelines import SoushiPipeline


class MoiveSpider(CrawlSpider):

    name="soushi"
    allowed_domains=["www.tvsou.com"]
    dayOfWeek = '%d' % (datetime.now().weekday() + 1)   #今天星期几，构成搜视网电视台 url
    url_pre = "http://www.tvsou.com"
    start_urls=[url_pre + "/programys/TV_1/Channel_1/W" +dayOfWeek+ ".htm", url_pre + "/programws/TV_24/Channel_46/W" +dayOfWeek+ ".htm"]
    #stations字典存放我们关注的电视频道信息，不在该字典中的频道是我们不关心的电视频道，那么不访问此电视频道页面
    stations = {'CCTV-1（综合） | 综合频道':('cctv1','cctv1'), 'CCTV-2（财经） | 经济频道':('cctv2','cctv2') , 'CCTV-3（综艺） | 综艺频道':('cctv3','cctv3') , 'CCTV-4中文国际（美）':('cctv4','cctv4') , 'CCTV-5（体育） | CCTV-5体育频道':('cctv5','cctv5') , 'CCTV-6（电影） | CCTV-6':('cctv6','cctv6') , 'CCTV-7（军事 农业） | 军事·农业频道':('cctv7','cctv7') , 'CCTV-8（电视剧） | 电视剧频道':('cctv8','cctv8') , 'CCTV-9（纪录） | CCTV-9（纪录频道）':('cctv9','cctv9') , 'CCTV-10（科教） | 科教频道':('cctv10','cctv10') , 'CCTV-11（戏曲） | 戏曲频道':('cctv11','cctv11') , 'CCTV-12（社会与法） | 法制频道':('cctv12','cctv12') , 'CCTV-13（新闻） | CCTV新闻频道':('cctv13','cctv13') , 'CCTV-14（少儿） | CCTV少儿频道':('cctvchild','cctvchild') , 'CCTV-15（音乐） | CCTV音乐频道':('cctv15','cctv15') , '湖北卫视':('湖北卫视','hubei') , '湖南卫视':('湖南卫视','hunan') , '吉林卫视':('吉林卫视','jilin') , '江苏卫视':('江苏卫视','jiangsu') , '江西卫视 | JXTV—1':('江西卫视','jiangxi') , '辽宁卫视':('辽宁卫视','liaoning') , '内蒙古卫视':('内蒙古卫视','neimenggu') , '宁夏卫视':('宁夏卫视','ningxia') , '青海卫视':('青海卫视','qinghai') , '山东卫视':('山东卫视','shandong') , '深圳卫视 | 卫星频道':('深圳卫视','shenzhen') , '陕西卫视':('陕西卫视','shan3xi') , '山西卫视':('山西卫视','shan1xi') , '四川卫视':('四川卫视','sichuan') , '天津卫视':('天津卫视','tianjin') , '西藏卫视 | 西藏一套（汉语）':('西藏卫视','xizang') , '厦门卫视':('厦门卫视','xiamen') , '新疆卫视':('新疆卫视','xinjiang') , '云南卫视':('云南卫视','yunnan') , '浙江卫视':('浙江卫视','zhejiang') , '安徽卫视':('安徽卫视','anhui') , 'BTV北京卫视 | BTV-1':('北京卫视','btv1') , '重庆卫视':('重庆卫视','chongqing') , '东方卫视':('东方卫视','dongfang') , '东南卫视':('东南卫视','dongnan') , '广东卫视':('广东卫视','guangdong') , '广西卫视':('广西卫视','guangxi') , '甘肃卫视':('甘肃卫视','gansu') , '贵州卫视':('贵州卫视','guizhou') , '河北卫视':('河北卫视','hebei') , '河南卫视':('河南卫视','henan') , '黑龙江卫视':('黑龙江卫视','heilongjiang') }
    pipe = SoushiPipeline()#负责操作数据库的一个对象
    
    #parse_channel_page 方法  处理每一个电视频道的当天电视节目数据
    def parse_channel_page(self, response):
        sel = Selector(response)
        #爬取电视频道名字
        program_li = sel.xpath('//div[@class="tvgenre clear"]/li')
        channelList = sel.xpath('//div[@id="TvChannelDIV"]/a/b/text()').extract()
        if len(channelList) > 0:
            channelName = channelList[0]
        else:
            channelName = 'null'
        channelName = channelName.strip().encode('utf8')
        #如果当前页面的频道名字不在字典中，那么不再处理本页面。
        if channelName not in self.stations:
            return
        #print channelName
        _channelName = self.stations[channelName][0]
        channelCid = self.stations[channelName][1]
        #定义一个列表用来存放电视节目单--->主要目的是用来得出电视节目的结束时间。我们把下一个节目的开始时间当做上一个节目的结束时间
        l = []
        #爬取电视节目单信息
        for i in range(len(program_li)):
            timeList = program_li[i].xpath("./span/text()").extract()
            proNameList = program_li[i].xpath("./a/text()").extract()
            if len(timeList) == 0:
                continue
            else:
                time = timeList[0]
                if len(proNameList) == 0:
                    proNameTemp = program_li[i].xpath('./text()').extract()
                    if len(proNameTemp) > 0:
                        proName = proNameTemp[0]
                    else:
                        proName = 'null'
                else:
                    proName = proNameList[0]
            
            time = time.strip()
            proName = proName.strip()
            #对电视节目的名字进行处理
            endProName = formatProName(proName).encode('utf8').strip()
            if len(endProName) <= 0:
                endProName = '_null_'
            else:
                pass
            #print time, endProName
            l.append((time, endProName))
        menus = []#当前页面的经过各种处理的最终电视节目列表
        i = 0
        while i < len(l) - 1:
            #根据构造方法，生成Program对象
            program = Program(l[i][0],l[i][1], channelCid, _channelName)
            program.end = l[i + 1][0]
            i = i + 1
            menus.append(program)
        #处理每一个电视频道页面中最后一个节目
        program = Program(l[i][0],l[i][1], channelCid, _channelName)
        menus.append(program)
        #将数据存入数据库
        self.pipe.savePro(menus)
        print '$$$$$$   ' + channelCid + '   $$$$$$'


    #parse 方法   爬虫默认处理 start_urls，在这里方法抓取目标页面中的电视台的 url
    def parse(self, response):
        #首先，提取当前页面的电视节目单数据
        self.parse_channel_page(response)
        #提取当前页面中符合条件的电视频道url
        sel = Selector(response)
        channel_infos = sel.xpath('//div[@class="listmenu2"][1]/div/a')
        #print "提取的电视频道总数：", len(channel_infos)
        for i in range(len(channel_infos)):
            channel_names = channel_infos[i].xpath("./text()").extract()
            channel_urls = channel_infos[i].xpath("./@href").extract()
            if len(channel_names) == 0 or len(channel_urls) == 0:
                continue
            else:
                channel_name = channel_names[0].encode('utf8')
                channel_url = self.url_pre + channel_urls[0]
                #print channel_name, channel_url
                #通过url访问对应的电视频道页面，提取页面的电视节目单数据
                yield Request(channel_url, callback = self.parse_channel_page)


    #closed 方法  判断爬虫结束方式，若完成爬取正常结束，则通知相关建立索引进程数据已经更新，重新建立索引
    def closed(self, reason):
        if reason == "finished":
            print 'scrapy completed crawling, closed. Notify java process to create index_file.'
            notifyJava()
        else:
            print 'scrapy was closed in other ways'
            
