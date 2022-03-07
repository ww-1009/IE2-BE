#!/usr/bin/env python
# -*- coding:utf-8 -*-

f = open(r"news_top.txt", "r", encoding="utf-8")
for i in range(10):
    data = f.readline()
    data=data.split(";")
    print(data[0])
f.close()