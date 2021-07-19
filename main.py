import urllib.request, urllib.error
from bs4 import BeautifulSoup
import re
import xlwt

def main():
    baseUrl = "https://movie.douban.com/top250?start="

    # 爬取网页
    dataList = getData(baseUrl)
    # 保存数据
    savePath = "豆瓣top250.xls"
    saveData(savePath, dataList)

    # saveDataToDb(dataList)

def getData(baseurl):
    datalist =[]
    for i in range(0,10):
        url =baseurl + str(i*25)
        html = askURL(url)

        #解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all("div", class_="item"):
            data = []  # 存放一部电影的所有信息
            item = str(item)
            link = re.findall(r'<a href="(.*)">', item)[0]  # 链接
            data.append(link)
            image = re.findall(r'<img.*src="(.*)" .*/>', item)[0]  # 图片
            data.append(image)
            findtitles = re.compile(r'<span class="title">(.*)</span>')
            titles = re.findall(findtitles,item)   # 片名
            data.append(titles[0])  # 添加中文名
            if len(titles) == 2:  # 添加外国名
                data.append(titles[1].replace("/", "")[6:])
            else:
                data.append(" ")    #留空
            rate = re.findall(r'<span class="rating_num".*>(.*)</span>', item)[0]  # 评分
            data.append(rate)
            judge = re.findall(r'<span>(\d*)人评价</span>', item)[0]  # 评级人数
            data.append(judge)
            inq = re.findall(r'<span class="inq">(.*)</span>', item, re.S)  # 简述
            if len(inq) != 0:
                inq = inq[0].replace("。", "")
                data.append(inq)
            else:
                data.append("")
            bd = re.findall(r'<p class="">(.*?)</p>', item, re.S)[0]  # 其他信息
            bd = re.sub('<br/>', " ", bd)
            bd = re.sub("/", " ", bd)
            bd = re.sub("\\n", " ", bd)
            bd = re.sub(r"\xa0", " ", bd)
            data.append(bd.strip())
            datalist.append(data)
    # for item in datalist:
    #     print(item)

        #进行解析




    return datalist



def askURL(url):
    head = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 91.0.4472.124Safari / 537.36Edg / 91.0.864.70'
    }

    req = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(req)
        html = response.read().decode('utf-8')

    except urllib.error.URLError as a:
        if hasattr(a, 'code'):
            print(a.code)
        if hasattr(a, 'reason'):
            print(a.reason)
    return html

def saveData(savePath, dataList):
    workbook = xlwt.Workbook(encoding="utf-8", style_compression=0)
    worksheet = workbook.add_sheet("豆瓣top250", cell_overwrite_ok=True)
    col = ("电影详情链接", "图片链接", "影片中文名", "影片英文名", "评分", "评价数", "概况", "相关信息")
    for i in range(0, 8):
        worksheet.write(0, i, col[i])
    for i in range(0, 250):
        data = dataList[i]
        for j in range(0, 8):
            worksheet.write(i+1, j, data[j])
    workbook.save(savePath)

if __name__ == '__main__':
    main()