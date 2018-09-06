import os

import pandas as pd
import requests
import time
import re
import pymysql

if __name__ == "__main__":

    #df = pd.read_table('kukudm_test' + time.strftime("%Y-%m-%d", time.localtime()) + '.txt', header=None, names=['content'], encoding='utf-8')
    # df = pd.read_table('kukudm_test2018-06-28.txt', header=None,
    #                    names=['content'], encoding='utf-8')
    db = pymysql.connect("localhost","root","","myspyder",use_unicode=True, charset="utf8")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM kukumanhuarecord WHERE recordStatus=0")

    record_list = cursor.fetchall()

    if len(record_list) == 0 :
        print("没有要更新的漫画")
    cwd = os.getcwd()
    for row in record_list:
        sql = "UPDATE kukumanhuarecord SET recordStatus=1 WHERE recordUrl='%s'" % (row[1])
        cursor.execute(sql)
        print(sql)
        comicdir = "\\" + row[0] + "\\" + re.search('\d+', row[2]).group()
        try:
            os.makedirs(cwd + comicdir)
        except Exception as err:
            print(err)
            continue
        os.chdir(cwd + comicdir)

        now_page_url = row[1]
        print(now_page_url)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'}
        res = requests.get(now_page_url, headers=headers)

        pattern = re.compile(r'/\d+\.htm')
        t = pattern.search(now_page_url).span()[0]
        print(t)
        print(now_page_url[t])

        i = 0
        while True:
            i += 1

            tt = list(now_page_url)
            if i > 10:
                tt[t+2] = ''
                tt[t+1] = str(i)
            else:
                tt[t+1] = str(i)
            now_page_url = ''.join(tt)
            print(now_page_url)

            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
            res = requests.get(now_page_url, headers=headers)
            if res.status_code == 404:
                print(res.status_code)
                break
            if i == 48:
                print(i)
                break
            print(res)
            html = res.content.decode('gbk', 'ignore').encode('utf-8').decode()
            # print(html)
            match_url = re.search('newkuku(\S)+jpg',html)
            print(match_url.group())
            # html = etree.HTML(html)
            # html_data = html.xpath('//img')
            # print(html_data[0])
            # print(html_data[0].get('src'))
            # img_link = html_data[0].get('src')

            img_link = 'http://n5.1whour.com/' + match_url.group()
            path = '~/comic/'+'.jpg'
            imgpage = requests.get(img_link, headers=headers)

            #获取图片的名字方便命名

            file_name = str(i)+'.jpg'

            #图片不是文本文件，以二进制格式写入，所以是html.content
            f = open(file_name,'wb')
            f.write(imgpage.content)
            f.close()
        
        db.commit()
        db.close()