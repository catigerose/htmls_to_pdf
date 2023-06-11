#!/usr/bin/env python
# coding: utf-8

'''
下载并导出vue官网文档为pdf
'''

from feed_funcs import get_soup
from bs4 import BeautifulSoup
import pdfkit
import os
from PyPDF2 import PdfMerger
path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)


domain = "https://cn.vuejs.org"


theme = "vuejs"


path = "./{}".format(theme)
# 判断结果
if not os.path.exists(path):
    os.makedirs(path)


# # 侧边栏列表


url = "https://cn.vuejs.org/guide/introduction.html"
soup = get_soup(url)


href_list = []
names = []
div_list = soup.find("nav", id="VPSidebarNav").find_all("div", class_="group")
div_list[0].find_all("a")


for div in div_list:
    for a in div.find_all("a"):
        href_list.append(a["href"])
        names.append(a.get_text())


# # 导出pdf


for i in range(len(names)):
    name = names[i]

    if os.access("./{0}/{1}.pdf".format(theme, name), os.F_OK):
        # print("跳过：",i,name)
        pass

    else:

        try:

            url = "https://cn.vuejs.org"+href_list[i]

            soup = get_soup(url)
            content = soup.find("main").div

            imgs = soup.find_all("img")
            for img in imgs:
                if img.get('src'):
                    if not (img["src"].startswith('/') or img["src"].startswith('http')):
                        img["src"] = domain+img["src"]

            links = soup.find_all("a")
            for link in links:
                if link.get('href'):
                    if not (link["href"].startswith('/') or link["href"].startswith('http') or link["href"].startswith('javascript')):
                        link["href"] = domain+link["href"]

            new_tag = soup.new_tag("base", href=domain, target="_blank")
            if soup.head:
                soup.head.title.insert_after(new_tag)
            # soup.body.style.append("h1{color: red;background-color: lightblue;}")

            new_soup = BeautifulSoup(
                " <html>  <head> </head> <body> <div> </div/> </body></html>", 'html.parser')
            new_soup.head.replace_with(soup.head)
            new_soup.body.div.replace_with(content)

            print("处理中：", i, name, end="--")
            pdfkit.from_string(
                str(new_soup), r"./{0}/{1}.pdf".format(theme, name), configuration=config)
            print("已写入pdf：", i, name, end="-")

        except:
            print("-------------------------------------------------------异常：", i)

            continue


file_merger = PdfMerger()
for i in range(len(names)):
    name = names[i]

    try:
        file_merger.append("./{0}/{1}.pdf".format(theme, name))
        # pdfkit.from_file(name +".html",name +".pdf", configuration=config)
    except:
        print("异常：", i, name)

        continue
file_merger.write("{0}.pdf".format(theme))
file_merger.close()
