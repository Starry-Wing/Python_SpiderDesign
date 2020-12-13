#学号:5120186290

import requests
#爬虫框架
import os
#文件的读写，用于保存爬取的图片
import urllib
#网页操作
import re
#正则表达式解析html文本


# 爬取百度图片页面的html文本（爬虫A）
def getText(page_url):
    headers = {
        'Referer': 'https://image.baidu.com/search/index?tn=baiduimage',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }#该字典设置爬虫A的爬取网页（百度图片网站）和马甲系统及浏览器
    try:
        r = requests.get(page_url, headers=headers)
        #创建爬虫A导入上述的字典作为爬虫A的参数
        if r.status_code == 200:
            r.encoding = r.apparent_encoding
            return r.text
            #返回整个页面的html文本
        else:
            print('错误')
    except Exception as e:
        print(e)


# 从爬取的html文本中提取出图片的url
def getPicurl(text):
    pic_url = re.findall('"thumbURL":"(.*?)",', text)
    #应用正则表达式解析出图片的url
    return pic_url


# 爬取图片的二进制信息
def getImage(pic_url):
    headers = {
        'Referer': pic_url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }#该字典设置爬虫B的爬取网页（搜索出来的图片地址）和马甲系统及浏览器
    try:
        r = requests.get(pic_url, headers=headers)
         #创建爬虫B导入上述的字典作为爬虫B的参数
        if r.status_code == 200:
            r.encoding = r.apparent_encoding
            return r.content
            #返回该图片的二进制信息
        else:
            print('错误')
    except Exception as e:
        print(e)


# 将图片的二进制信息写入文件并保存在本地
def save_pic(pic_url, content,pic_name,num):
    root_path = 'D://爬取图片//'+pic_name+'//'
    #爬取图片的目录（自定义）
    pic_path = root_path + pic_name+str(num)+".jpg"
    #每张图片文件保存的本地地址
    if not os.path.exists(root_path):
        os.mkdir(root_path)
    if not os.path.exists(pic_path):
        with open(pic_path, 'wb') as f:
            f.write(content)
            print('图片{}保存成功，地址在{}'.format(pic_url, pic_path))
            #将爬取的图片有序地保存在本地，如没有该关键字的目录则创建
    else:
        pass


#用户输入信息的字典
def names():
    namedict={};
    numstr=input("一共要查询多少个关键字？")
    nums=int(numstr)
    for i in range(nums):
        pic_name = input('输入关键字: ')
        depth = int(input("输入爬取'{}'的图片的页数(每页30张图): ".format(pic_name)))
        namedict.update({pic_name:depth})
    return namedict


# 主函数
def main():
    namedict=names()
    #创建用户输入信息的字典
    for pic_name in namedict:
        pic_name_trans = urllib.parse.quote(pic_name)
        #将信息转化为url
        depth=namedict[pic_name]
        j=0
        for i in range(depth):
            url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord+=&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&word={}&z=&ic=0&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&step_word={}&pn={}&rn=30&gsm=1e&1541136876386='.format(
                pic_name_trans, pic_name_trans, i*30)
            html = getText(url)
            pic_urls = getPicurl(html)
            #遍历图片url
            j=j+1
            for pic_url in pic_urls:
                j=j+1
                content = getImage(pic_url)
                save_pic(pic_url, content,pic_name,j)
                #爬取图片并保存成本地文件

                
main()
