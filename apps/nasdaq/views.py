from django.shortcuts import render
from apps.nasdaq.models import NasdaqIndex7
from apps.nasdaq.models import NasdaqSpo3
from apps.nasdaq.models import NasdaqDepth
# 引入JsonResponse模块
from django.http import JsonResponse
# 导入json模块
import json
# 导入Q查询
from django.db.models import Q
# Create your views here.

def query_index_7(request):
    '''查询学生信息'''
    # 接受传递过来的查询条件---axios默认的是json格式---字典类型（‘inputstr’）---data['inputstr']
    data = json.loads(request.body.decode('utf-8'))
    try:
        print(data['inputstr'])
        # 使用ORM获取满足条件的信息 并把对象转为字典格式
        obj_index_7 = NasdaqIndex7.objects.filter(Q(index__contains=data['inputstr'])).values()
        # 把结果转为List
        index_7s =list(obj_index_7)
        if index_7s!=[]:
            for raw in index_7s:
                del raw['index']
                raw['value']=raw['prompt']
                del raw['prompt']
        # 返回
        return JsonResponse({'code':1,'data':index_7s})
    except Exception as e:
        # 如果出现异常，返回
        return JsonResponse({'code': 0, 'msg': "查询学生信息出现异常，具体错误："+str(e)})


def getentityData(request):
    # 接受传递过来的查询条件---axios默认的是json格式---字典类型（‘inputstr’）---data['inputstr']
    data = json.loads(request.body.decode('utf-8'))
    try:
        # 使用ORM获取满足条件的信息 并把对象转为字典格式
        obj_nodes = NasdaqDepth.objects.filter(Q(target__exact=data['inputstr'])&Q(depth__lte=data['depth'])).values()
        # 把结果转为List
        obj_nodes = list(obj_nodes)
        nodes_id=[]
        links=[]
        nodes=[]
        if obj_nodes != []:
            num=0
            for node in obj_nodes:
                del node['target']
                del node['id']
                n=node['depth']
                node['category'] = int(n)
                del node['depth']
                node['id'] = num
                num=num+1
                if node['name'] not in nodes_id:
                    nodes_id.append(node['name'])
                nodes.append(node)
                # print(node)
        # print(nodes_id)
        # print()
        for s in nodes_id:
            obj_links = NasdaqSpo3.objects.filter(Q(s__exact=s)).values()
            obj_links = list(obj_links)
            if obj_links != []:
                for link in obj_links:
                    if link['o'] in nodes_id:
                        del link['id']
                        link['source']=nodes_id.index(s)
                        link['target'] = nodes_id.index(link['o'])
                        link['category']=0
                        link['value']=link['p']
                        del link['p']
                        del link['s']
                        del link['o']
                        link['symbolSize']=10
                        links.append(link)
                        # print(link)
        datas=[]
        datas.append(nodes)
        datas.append(links)
        # 返回
        return JsonResponse({'code': 1, 'data': datas})

    except Exception as e:
        # 如果出现异常，返回
        print(str(e))
        return JsonResponse({'code': 0, 'msg': "查询信息出现异常，具体错误：" + str(e)})

def getporpertyData(request):
    # 接受传递过来的查询条件---axios默认的是json格式---字典类型（‘inputstr’）---data['inputstr']
    data = json.loads(request.body.decode('utf-8'))
    try:
        # 使用ORM获取满足条件的信息 并把对象转为字典格式
        obj_nodes = NasdaqSpo3.objects.filter(Q(s__exact=data['inputstr'])).values()
        # 把结果转为List
        obj_nodes = list(obj_nodes)
        node_data = []
        Tree_data = []
        if obj_nodes != []:
            num=0
            count=0
            p=[]
            child_list = []
            Treedic = {}
            p_temp=''
            for node in obj_nodes:
                if node['p']!=p_temp:
                    if p_temp!='':
                        Treedic['children']=child_list
                        Tree_data.append(Treedic)
                    Treedic = {}
                    count = count + 1
                    p_temp=node['p']
                    Treedic['id']=count
                    Treedic['label']=p_temp
                    child_list = []
                child_dic={}
                count = count + 1
                child_dic['id']=count
                child_dic['label']=node['o']
                child_list.append(child_dic)

                temp={}
                if node['p'] not in p:
                    p.append(node['p'])
                    temp['id']=num
                    num=num+1
                    temp['category']=1
                    temp['name']=node['p']
                    node_data.append(temp)
            Treedic['children'] = child_list
            Tree_data.append(Treedic)
        # print(Tree_data)
        data=[]
        data.append(node_data)
        data.append(Tree_data)
        return JsonResponse({'code': 1, 'data': data})
    except Exception as e:
    # 如果出现异常，返回
        print(str(e))
        return JsonResponse({'code': 0, 'msg': "查询信息出现异常，具体错误：" + str(e)})

def getnewstop(request):
    try:
        datas=[]
        tops=[]
        img=[]
        f = open(r"F:\项目\web\Nasdaq_Be\apps\nasdaq\news_top.txt", "r", encoding="utf-8")
        for i in range(10):
            new = f.readline()
            new = new.split(";")
            tops.append(new)
        img.append(f.readline())
        f.close()
        datas.append(tops)
        datas.append(img)
        return JsonResponse({'code': 1, 'data': datas})
    except Exception as e:
        # 如果出现异常，返回
        print(str(e))
        return JsonResponse({'code': 0, 'msg': "top出现异常，具体错误：" + str(e)})
