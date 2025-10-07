import requests
from lxml import etree
import csv
import re
import time
import random

def header_x():
    # 随机获取一个headers
    user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
                   'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0'
                   ]

    headers = {
        "User-Agent": random.choice(user_agents)
    }
    return headers

# 要爬取的 豆瓣读书中的 分类名称
kinds = ["经济学"]


for book_kind in kinds:

    # 为每个分类创建一个csv文件
    csvFile = open("{}.csv".format(book_kind), mode="w+", encoding="utf-8")

    for i in range(1, 51):
        print('{name}   开始爬取第 {index} 页'.format(name=book_kind,index=i))

        # 拼接url
        url = 'https://book.douban.com/tag/{name}?start={num}&type=T'.format(name=book_kind,num=i*20-20)

        headers = header_x()

        resp = requests.get(url, headers=headers)
        html = etree.HTML(resp.text)

        lis = html.xpath("//div[@id='subject_list']/ul/li")

        for li in lis:
            try:
                name = li.xpath("./div[@class='info']/h2/a/@title")   # 书名
                author = li.xpath("./div[@class='info']/div[@class='pub']/text()")[0].strip().split('/')[0]  # 作者
                publisher = li.xpath("./div[@class='info']/div[@class='pub']/text()")[0].strip().split('/')[-3]  # 出版社
                publish_time = li.xpath("./div[@class='info']/div[@class='pub']/text()")[0].strip().split('/')[-2]  # 出版年
                # 判断出版社，出版年份是否在指定位置 如果不在 则跳过
                if(publish_time.find('-')==-1):
                    continue
                grade = li.xpath(".//span[@class='pl']/text()")[0].strip()   # 评价数

                # 处理grade 提取数字
                grade_num = []
                grade_num = re.findall("\d+\.?\d*", grade)

                intro_1 = li.xpath("./div[@class='info']/p/text()")[0].strip()   # 小简介

                # 子链接
                son_url = li.xpath("./div[@class='info']/h2/a/@href")[0]   #子链接


                resp_son = requests.get(son_url, headers=headers)
                html_son = etree.HTML(resp_son.text)

                # 评分
                score = html_son.xpath("//strong[@class='ll rating_num ']/text()")[0].strip()
            except IndexError:
                continue

            # 把字符串转换成列表
            author = list(author.split('&&'))
            publisher = list(publisher.split('&&'))
            publish_time = list(publish_time.split('&&'))
            intro_1 = list(intro_1.split('&&'))

            score = list(score.split('&&'))

            # 把数据放入列表
            result = []
            result.extend(name)
            result.extend(author)
            result.extend(publisher)
            result.extend(publish_time)
            result.extend(grade_num)
            result.extend(intro_1)

            result.extend(score)

            # 将列表写入 csv文件
            write = csv.writer(csvFile)
            write.writerow(result)

            # 设置每条数据的时间间隔
            time.sleep(random.randint(5, 8))


        print("{name}    第 {index} 页爬取完成！！！".format(name=book_kind,index=i))

        # 设置换页的时间等待时间
        time.sleep(random.randint(3, 5))


