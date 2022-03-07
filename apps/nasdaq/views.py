import re

from django.shortcuts import render
from apps.nasdaq.models import NasdaqGraph
from elasticsearch import Elasticsearch
# 引入JsonResponse模块
from django.http import JsonResponse
# 导入json模块
import json
from lxml.html import etree
import requests
# 导入Q查询
from django.db.models import Q

# Create your views here.

client = Elasticsearch(hosts=["127.0.0.1"])

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
    newsList = []
    for i in range(0, 10):
        temp=[]
        temp.append(titleList[i].replace("标题：", "").replace('}', ""))
        temp.append(newsUrlList[i])
        newsList.append(temp)
    # print(newsList)
    return newsList

def node_depth(depth, nodes):
    entityNode = []
    depth=int(depth)
    depth += 1
    deep = 0
    num=0
    idmap=[]
    while depth:
        S = "level" + str(deep)
        level = nodes[S]
        for row in level:
            idmap.append(row[0])
            # print(row[1])
            temp = {"name": row[1], "category": deep, "id": num}
            entityNode.append(temp)
            num += 1
        deep += 1
        depth -= 1
    # print(entityNode)
    return entityNode,idmap


def link_depth(depth, nodes,idmap,key_word):
    entityLink = []
    porpertyNode = []
    temp = {"name": str(key_word), "category": 0, "id": 0}
    porpertyNode.append(temp)
    helpList=[]
    depth=int(depth)
    deep = 1
    num = 1
    while depth:
        S = "level" + str(deep)
        level = nodes[S]
        for row in level:
            source=idmap.index(row[0])
            target = idmap.index(row[2])
            temp = {"source": source, "target": target, "category": 0, "value": row[1], "symbolSize": 10}
            entityLink.append(temp)
            if row[1] not in helpList:
                temp2 = {"name": row[1], "category": 1, "id": num}
                num += 1
                helpList.append(row[1])
                porpertyNode.append(temp2)
        deep += 1
        depth -= 1
    return entityLink, porpertyNode


def Type_tool(nodes,link,map):
    typeNode = []
    Links=[]
    id_help={}
    typemap={}
    # temp = {"name": str(key_word), "category": 0, "id": 0}
    # typeNode.append(temp)
    for row in nodes:
        if re.findall('Wikicat', row[1]) == [] and re.findall('Yago', row[1]) == []:
            new_crazy = filter(str.isalpha, row[1])
            temp = {"name": ''.join(list(new_crazy)), "category": 1, "id": row[0]}
            typeNode.append(temp)
            id_help[row[1]]=row[0]
        else:
            break
    for i in link:
        temp = {"source":i[0], "target": i[1], "category": 0, "symbolSize": 10}
        Links.append(temp)
    for i in map:
        s=""
        for j in i:
            if j!=i[0]:
                s=s+j+"<br>"

        typemap[id_help[i[0]]]=s
    return typeNode,Links,typemap

def NodeToLink(nodes,s):
    num=len(nodes)
    Links=[]
    for i in range(num):
        temp = {"source":0, "target": i+1, "category": 0, "value": s, "symbolSize": 10}
        Links.append(temp)
    return Links

def explore_graph(oldNodes,oldLinks,newNodes,newLinks,key_word_id):
    entityNodes=[]
    entityLines=[]
    level0=[]
    idmap=[]
    for node in oldNodes:
        if node["category"]==0:
            entityNodes.append(node)
            level0.append(node["name"])
        else:
            break
    baseNum=len(level0)
    for i in range(baseNum-1):
        entityLines.append(oldLinks[i])

    for link in oldLinks:
        if link["source"]==baseNum-1 and link["target"]==key_word_id:
            link["target"]=baseNum
            entityLines.append(link)
            break

    for node in newNodes:
        # print(node)
        if node["name"] in level0:
            node_id=node["id"]
            newNodes.pop(node_id)
            for index,link in enumerate(newLinks):
                if link["source"]==node_id or link["target"]==node_id:
                    newLinks.pop(index)

    num=0
    for node in newNodes:
        # print(node)
        idmap.append(node["id"])

        node["id"]=baseNum+num
        num+=1
        entityNodes.append(node)

    for link in newLinks:
        # print(link)
        link["source"]=baseNum+idmap.index(link["source"])
        link["target"]=baseNum+idmap.index(link["target"])
        entityLines.append(link)
    return entityNodes,entityLines



def query_name(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        key_words = data['inputstr']
        print(data['inputstr'])
        data = []
        if key_words:
            s = NasdaqGraph.search(index="suggestion")
            s = s.suggest('my_suggest', key_words,
                completion={
                "field": "namesuggest", "fuzzy": {
                    "fuzziness": 2
                },
                "size": 8
            })
            suggestions = s.execute_suggest()
            id = 1
            for match in suggestions.my_suggest[0].options:
                temp = {}
                source = match._source
                temp["id"] = id
                temp['value'] = source["name"]
                id = id + 1
                data.append(temp)
                # 返回
        return JsonResponse({'code': 1, 'data': data})
    except Exception as e:
        # 如果出现异常，返回
        return JsonResponse({'code': 0, 'msg': "查询学生信息出现异常，具体错误：" + str(e)})


def get_Graph(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        old_key_words=""
        key_words = data['inputstr']
        depth = data['depth']
        oldNodes=data['oldNodes']
        oldLinks = data['oldLinks']
        key_word_id = data['keywordid']
        explore =data['explore']
        data = []
        if key_words:
            response = client.search(
                index="reindex",
                doc_type="GraphType",
                body={
                    "query": {
                        "match": {
                            "name": key_words
                        }
                    },
                    "size": 1,
                    "_source": ["name", "imgUrl", "abstract", "node", "link","typeNode","typemap","typeLink"]
                }
            )
            hit = response["hits"]["hits"][0]["_source"]
            name = hit["name"]
            imgUrl = hit["imgUrl"]
            abstract = hit["abstract"]
            nodes = hit["node"]
            links = hit["link"]
            typeNodes = hit["typeNode"]
            typeLinks = hit["typeLink"]
            typemaps = hit["typemap"]
            entityNodes,idmap = node_depth(depth, nodes)
            entityLink, porpertyNode = link_depth(depth, links,idmap,key_words)
            porpertyLink=NodeToLink(porpertyNode,"porperty")
            typeNode,typeLink,typemap = Type_tool(typeNodes,typeLinks,typemaps)
            if explore:
                entityNodes, entityLink = explore_graph(oldNodes, oldLinks, entityNodes, entityLink, key_word_id)
            if old_key_words!=key_words:
                entityNews=getEntityNews(key_words)
                old_key_words = key_words

            data.append(name)
            data.append(imgUrl)
            data.append(abstract)
            data.append(entityNodes)
            data.append(entityLink)
            data.append(porpertyNode)
            data.append(porpertyLink)
            data.append(typeNode)
            data.append(typeLink)
            data.append(typemap)
            data.append(entityNews)

            return JsonResponse({'code': 1, 'data': data})
    except Exception as e:
        # 如果出现异常，返回
        print(str(e))
        return JsonResponse({'code': 0, 'msg': "查询信息出现异常，具体错误：" + str(e)})


def getnewstop(request):
    try:
        datas = []
        tops = []
        img = []
        f = open(r"/home/vv/ww/project/python/IE2-BE/apps/nasdaq/news_top.txt", "r", encoding="utf-8")
        for i in range(12):
            new = f.readline()
            new = new.split(";")
            tops.append(new)
        for i in range(3):
            img.append(f.readline())
        f.close()
        datas.append(tops)
        print(tops)
        datas.append(img)
        return JsonResponse({'code': 1, 'data': datas})
    except Exception as e:
        # 如果出现异常，返回
        print(str(e))
        return JsonResponse({'code': 0, 'msg': "top出现异常，具体错误：" + str(e)})
