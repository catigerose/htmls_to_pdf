#!/usr/bin/env python
# coding: utf-8

'''
下载并导出vw3schools官网文档为pdf
'''

#  导入包

from feed_funcs import get_soup
import pdfkit
import os
from PyPDF2 import PdfMerger
path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)


#  侧边栏列表


theme = "nodejs"


path = "./{}".format(theme)
# 判断结果
if not os.path.exists(path):
    os.makedirs(path)
domain = "https://www.w3schools.com/{}/".format(theme)


try:
    soup = get_soup(domain+"default.asp")
    a_list = soup.find("div", id="leftmenuinnerinner").find_all("a")
except:
    soup = get_soup(domain+"index.php")
    a_list = soup.find("div", id="leftmenuinnerinner").find_all("a")
asp_list = [(a["href"], a.get_text()) for a in a_list]
asp_list2 = []
for i in range(len(asp_list)-1):
    if asp_list[i][0] != asp_list[i+1][0]:
        asp_list2.append(asp_list[i])
len(asp_list2)


# # 导出pdf


for i in range(0, len(asp_list2)):
    relative_url = asp_list2[i][0]
    if relative_url.startswith('/'):
        url = "https://www.w3schools.com{}".format(relative_url)
    else:
        url = domain + relative_url

    name = asp_list2[i][-1].replace('/', '-')
    name = name.replace("?", "")

    if os.access("./{0}/{1}.pdf".format(theme, name), os.F_OK):
        # print("跳过：",i,name)
        pass

    else:

        try:
            soup = get_soup(url)

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

            new_tag = soup.new_tag(
                "base", href="https://www.w3schools.com/", target="_blank")
            if soup.head:
                soup.head.title.insert_after(new_tag)
            soup.body.style.append(
                "h1{color: red;background-color: lightblue;}")

            dels = []
            dels.append(soup.find("div", id="leftmenuinner"))
            dels.append(soup.find("div", id="pagetop"))
            dels.append(soup.find("div", id="topnav"))
            dels.append(soup.find("div", id="right"))
            dels.append(soup.find("div", id="footer"))
            dels.append(soup.find("form", id="w3-exerciseform"))
            dels.append(soup.find("div", id="mainLeaderboard"))
            dels.append(soup.find("div", id="sidenav"))
            dels.append(soup.find("div", class_="w3-clear nextprev"))
            if soup.find_all("div", class_="w3-clear nextprev"):
                dels.append(soup.find_all(
                    "div", class_="w3-clear nextprev")[-1])
            for tag in dels:
                try:
                    tag.decompose()
                except:
                    continue
            print("处理中：", i, name)
            pdfkit.from_string(
                str(soup), r"./{0}/{1}.pdf".format(theme, name), configuration=config)

        except:
            print("异常：", i)

            continue


file_merger = PdfMerger()
for i in range(0, len(asp_list2)):
    url = domain+asp_list2[i][0]
    name = asp_list2[i][-1].replace('/', '-')
    name = name.replace("?", "")

    try:
        file_merger.append("./{0}/{1}.pdf".format(theme, name))
        # pdfkit.from_file(name +".html",name +".pdf", configuration=config)
    except:
        print("异常：", i, name)

        continue
file_merger.write("{0}.pdf".format(theme))
file_merger.close()
