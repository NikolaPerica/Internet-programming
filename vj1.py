# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 18:35:31 2022

@author: Student
"""

import socket, time, re

def connect(ip, port, retry = 10):
    s = socket.socket()
    try:
        s.connect((ip, port))
    except Exception as e:
        print (e)
        if retry > 0:
            time.sleep(1)
            retry -=1
            connect(ip, port, retry)       
    
    return s

def get_source(s, ip, page):

    CRLF = '\r\n'
    get = 'GET /' + page + ' HTTP/1.1' + CRLF
    get += 'Host: '
    get += ip
    get += CRLF
    get += CRLF

    s.send(get.encode('utf-8'))
    response = s.recv(10000000).decode('latin-1')
   # print (response)
    return response

def get_links(response):
    link_list = []
    beg = 0
    while True:
        beg_str = response.find('href="', beg)   
        if beg_str == -1:
            return link_list  
        end_str = response.find('"', beg_str + 6)      
        link = response[beg_str + 6:end_str]
        if link not in link_list:
            link_list.append(link)
        beg = end_str + 1
        
    return link_list

        
    

ip = 'www.watchthatpage.com'
port = 80
page = 'reportProblem.jsp'
s = connect(ip, port)
print (s)
response = get_source(s, ip, page)

list_links=get_links(response)
#print (list_links)

print('\n\n\n')
j=1
while True:
    response = get_source(s, ip, list_links[j])
    list_links.extend(get_links(response))
    j=j+1
    if(j>50):break
    
print (list_links)