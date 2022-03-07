from lxml.html import etree
import requests

def getEntityNews(entity):
    url = 'https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&ie=utf-8&word={}'.format(entity)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/86.0.4240.75 Safari/537.36'}


    response = requests.get(url=url, headers=headers)
    page_text = response.text
    tree = etree.HTML(page_text)

    newsListELement = tree.xpath('//div[@id="content_left"]/div[contains(@class, "result-op")]')
    newsUrlList = newsListELement[0].xpath('//h3[@class="news-title_1YtI1 "]/a/@href')
    titleList = newsListELement[0].xpath('//h3[@class="news-title_1YtI1 "]/a/@aria-label')
    # abstractList = newsListELement[0].xpath('//span[contains(@class, "c-color-text")]/@aria-label')
    # timeLineList = newsListELement[0].xpath('//span[contains(@class, "c-gap-right-xsmall")]/@aria-label')
    # imgList = newsListELement[0].xpath('//div[@class="c-img c-img-radius-large  c-img3 compatible_rxApe"]/img/@src')
    # print(imgList)
    newsList = []
    for i in range(0, 10):
        temp=[]
        temp.append(titleList[i].replace("标题：", "").replace('}', ""))
        temp.append(newsUrlList[i])
        # newsDict = {
        #     'newsUrl':newsUrlList[i],
        #     'newsTitle':titleList[i].replace("标题：", "").replace('}', ""),
        #     # 'newsAbstract':abstractList[i].replace("摘要 ", ""),
        #     # 'newsTime':timeLineList[i].replace("发布于：",""),
        # }
        #
        # print(newsDict)
        newsList.append(temp)
    print(newsList)
# if __name__ == '__main__':
#     getEntityNews("Elon Musk")

