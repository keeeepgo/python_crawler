import urllib.request
from lxml import etree
import time
import pymysql



if __name__ == '__main__':

    today = time.strftime("%Y-%m-%d", time.localtime())
    print(today)

    db = pymysql.connect("localhost","root","","myspyder",use_unicode=True, charset="utf8")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM kukumanhualist")
    comic_list = cursor.fetchall()
    for row in comic_list:
        print(row)
        comicname = row[0]
        comicname = comicname.encode('utf-8').decode()
        print(comicname)
        comicurl = row[1]

        res = urllib.request.urlopen(comicurl)
        html = res.read().decode('gbk', 'ignore').encode('utf-8').decode()
        # print(html)
        html = etree.HTML(html)
        
        dd_s = html.xpath('//*[@id="comiclistn"]/dd')
        
        for i in range(len(dd_s)-1,0,-1) :
            a_s = dd_s[i].findall('a')
            print(a_s[0].tag, a_s[0].attrib)
            
            nowurl = "http://comic3.kukudm.com" + a_s[0].get('href')
            nowtitle = a_s[0].text.replace(' ','')
            nowurl = nowurl.encode('utf-8').decode()
            nowtitle = nowtitle.encode('utf-8').decode()
            print(nowurl)
            print(nowtitle)
            try:
                if cursor.execute("SELECT * FROM kukumanhuarecord WHERE comicName='%s' AND recordUrl='%s'" % (comicname,nowurl)) == 1 :
                    print("有该漫画记录")
                    break
                else:
                    print("没有该漫画记录")
                    try:
                        insertsql = "INSERT INTO kukumanhuarecord VALUES ('%s','%s','%s','%s',%d)" % (
                        comicname, nowurl, nowtitle, today, 0)
                        print(insertsql)
                        cursor.execute(insertsql)
                        db.commit()
                        print("插入成功")
                    except Exception as err:
                        print(err)
                        db.rollback()
                        print("插入失败")
            except Exception as err:
                print(err)
                print("查询记录失败")
    
    
            # with open('kukudm_test' + time.strftime("%Y-%m-%d", time.localtime()) + '.txt', "wb+") as fo:
            #     if len(comic_url) == 0:
            #         print("fail")
            #     else:
            #         fo.write(comic_url.encode('UTF-8'))
            #         fo.write(('\n').encode('UTF-8'))
            # fo.close()
    
            