

import json
import requests
requests.packages.urllib3.disable_warnings()
from lxml import etree
from datetime import datetime, timedelta
from threading import Thread
import csv
from math import ceil
import os
import re 
from time import sleep
from random import randint

headers = {
            "Cookie": "_T_WM=50116707496; Hm_lvt_eaa57ca47dacb4ad4f5a257001a3457c=1643878787,1643886820,1643889148; SCF=Am2rYpDFDwdVLW6K20J9kESyETHv9-9ovWecPggEfuUwm-4lFGOIykaoJnU8sJfdyQLX4ur57hDdiQWrxbr1biU.; SUB=_2A25M_5PpDeRhGeNI7FoV9irEwj6IHXVsAz2hrDV6PUNbktCOLRH3kW1NSDrv_nFGBHYhFdiXAdRvNgn8Y6McdoKc; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWJGJBKjv59nMSO1YwICkih5JpX5KzhUgL.Fo-cS0nXSoBR1Kz2dJLoIEBLxK.LB-BL1h-LxK-L122L1-zLxK-LB.-L1K5LxK-LBKML1K5t; SSOLoginState=1643897785; ALF=1646489785; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803; Hm_lpvt_eaa57ca47dacb4ad4f5a257001a3457c=1643897826 referer: https://weibo.cn/cctvxinwen",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
        }

headers_1 = {
            "Cookie": "SUB=_2A25M_-auDeRhGeNI7FoV9irEwj6IHXVsA4rmrDV6PUJbkdAKLUHCkW1NSDrv_iUN8lNZYU5SbeI1Qm5UA_1U5nWI; _T_WM=50116707496; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803; Hm_lvt_eaa57ca47dacb4ad4f5a257001a3457c=1643878787; Hm_lpvt_eaa57ca47dacb4ad4f5a257001a3457c=1643880220",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
        }


def find_w():
        topics=[]
        urls=[]
        res = requests.get('https://weibo.cn/cctvxinwen',headers=headers)
        commentNum = re.findall("【.*?】",res.text)
        print(len(commentNum))
        commentNum_1 = str(commentNum)[1:-1].split(',')
        tmp=2
        for i in range(len(commentNum)):
          commentNum = commentNum_1[i][tmp:-2]
          commentNum = commentNum.split('#')
          if tmp==2:tmp=tmp+1
          print(commentNum[1])
          topics.append(commentNum[1])
        
        url_c = re.findall(">转发\[.*?>评论",res.text)
        print(len(url_c))
        url_c_1 = str(url_c)[1:-1].split(',')
        tmp=2
        for i in range(len(url_c)):
          url_c = url_c_1[i][tmp:-2]
          url_c = url_c.split('\"')
          if tmp==2:tmp=tmp+1
          print(url_c[1])
          urls.append(url_c[1])
        print(topics)
        key_input = input("请输入关键字:")
        input_n=0
        for i in range(len(topics)):
             if (topics[i].find(key_input))>=0:
                 print(i)
                 input_n=i
                 break
        r_url=urls[input_n].split('?')[0]
        r_url=r_url.split('/')[-1]
        print(r_url)
        return r_url

   # 保存文件
def save(filename, content):
    with open(filename, 'w', encoding="utf-8") as f:
        if filename.endswith('.json') and isinstance(content, dict):
            json.dump(content, f, ensure_ascii=False, indent=2)
        else:
            f.write(content)

class WeiboCommentScrapy(Thread):

    def __init__(self,wid):
        global headers
        Thread.__init__(self)
        self.headers = headers
        self.result_headers = [
            '评论者主页',
            '评论者昵称',
            '评论者性别',
            '评论者所在地',
            '评论者微博数',
            '评论者关注数',
            '评论者粉丝数',
            '评论内容',
            '评论获赞数',
            '评论发布时间',
        ]
        if not os.path.exists('comment'):
            os.mkdir('comment')
        
        self.wid = wid
        self.start()

 

    def parse_time(self,publish_time):
        publish_time = publish_time.split('来自')[0]
        if '刚刚' in publish_time:
            publish_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        elif '分钟' in publish_time:
            minute = publish_time[:publish_time.find('分钟')]
            minute = timedelta(minutes=int(minute))
            publish_time = (datetime.now() -
                            minute).strftime('%Y-%m-%d %H:%M')
        elif '今天' in publish_time:
            today = datetime.now().strftime('%Y-%m-%d')
            time = publish_time[3:]
            publish_time = today + ' ' + time
        elif '月' in publish_time:
            year = datetime.now().strftime('%Y')
            month = publish_time[0:2]
            day = publish_time[3:5]
            time = publish_time[7:12]
            publish_time = year + '-' + month + '-' + day + ' ' + time
        else:
            publish_time = publish_time[:16]
        return publish_time

    def getPublisherInfo(self,url):
        res = requests.get(url=url,headers=self.headers,verify=False)
        html = etree.HTML(res.text.encode('utf-8'))
        
        head = html.xpath("//div[@class='ut']/span[1]")[0]
        head = head.xpath('string(.)')[:-3].strip()
        keyIndex = head.index("/")
        nickName = head[0:keyIndex-2]
        sex = head[keyIndex-1:keyIndex]
        location = head[keyIndex+1:]

        footer = html.xpath("//div[@class='tip2']")[0]
        weiboNum = footer.xpath("./span[1]/text()")[0]
        weiboNum = weiboNum[3:-1]
        followingNum = footer.xpath("./a[1]/text()")[0]
        followingNum = followingNum[3:-1]
        followsNum = footer.xpath("./a[2]/text()")[0]
        followsNum = followsNum[3:-1]
        print(nickName,sex,location,weiboNum,followingNum,followsNum)
        return nickName,sex,location,weiboNum,followingNum,followsNum

    def get_one_comment_struct(self,comment):
        # xpath 中下标从 1 开始
        userURL = "https://weibo.cn/{}".format(comment.xpath(".//a[1]/@href")[0])

        content = comment.xpath(".//span[@class='ctt']/text()")
        # '回复' 或者只 @ 人
        if '回复' in content or len(content)==0:
            test = comment.xpath(".//span[@class='ctt']")
            content = test[0].xpath('string(.)').strip()

            # 以表情包开头造成的 content == 0,文字没有被子标签包裹
            if len(content)==0:
                content = comment.xpath('string(.)').strip()
                content = content[content.index(':')+1:]
        else:
            content = content[0]

        praisedNum = comment.xpath(".//span[@class='cc'][1]/a/text()")[0]
        praisedNum = praisedNum[2:praisedNum.rindex(']')]

        publish_time = comment.xpath(".//span[@class='ct']/text()")[0]

        publish_time = self.parse_time(publish_time)
        nickName,sex,location,weiboNum,followingNum,followsNum = self.getPublisherInfo(url=userURL)

        return [userURL,nickName,sex,location,weiboNum,followingNum,followsNum,content,praisedNum,publish_time]

    def write_to_csv(self,result,isHeader=False):
        with open('comment/' + self.wid + '.csv', 'a', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            if isHeader == True:
                writer.writerows([self.result_headers])
            writer.writerows(result)
        print('已成功将{}条评论写入{}中'.format(len(result),'comment/' + self.wid + '.csv'))
        #archive_filepath = f'comment/' + self.wid
        """line = '1. [{title}]({url}) {hot}'
        lines = [line.format(title=k, hot=v['hot'], url=v['url']) for k, v in news.items()]
        lines = '\n'.join(lines)
        # lines = f'## {today_str}热门搜索 \r\n最后更新时间 {datetime.now()} \r\n![{today_str}]({today_str}.png) \r\n' + lines + '\r\n'
        lines = f'## {today_str}热门搜索 \r\n最后更新时间 {datetime.now()} \r\n' + lines + '\r\n'"""
        #save(f'{archive_filepath}.md', str(result))

    def run(self):
        res = requests.get('https://weibo.cn/comment/{}'.format(self.wid),headers=self.headers,verify=False)
       
        commentNum = re.findall("评论\[.*?\]",res.text)[0]
        commentNum = int(commentNum[3:len(commentNum)-1])
        print(commentNum)
        pageNum = ceil(commentNum/10)
        print(pageNum)
        for page in range(pageNum):
            result = []
            res = requests.get('https://weibo.cn/comment/{}?page={}'.format(self.wid,page+1), headers=self.headers,verify=False)
            html = etree.HTML(res.text.encode('utf-8'))
            comments = html.xpath("/html/body/div[starts-with(@id,'C')]")
            print('第{}/{}页'.format(page+1,pageNum))
            for i in range(len(comments)):
                result.append(self.get_one_comment_struct(comments[i]))
            if page==0:
                self.write_to_csv(result,isHeader=True)
            else:
                self.write_to_csv(result,isHeader=False)

            sleep(randint(1,5))

if __name__ =="__main__":
    wid=find_w()
    WeiboCommentScrapy(wid)

