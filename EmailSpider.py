# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 11:23:57 2020

@author: yangyj
"""

'''import requests, re
 
# regex = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
# regex = r"([a-zA-Z0-9_.+-]+@[a-pr-zA-PRZ0-9-]+\.[a-zA-Z0-9-.]+)"  # 这个正则表达式过滤掉了qq邮箱
 
regex = r"([a-zA-Z0-9_.+-]+@[a-fh-pr-zA-FH-PRZ0-9-]+\.[a-zA-Z0-9-.]+)"  # 这个正则表达式过滤掉了谷歌邮箱和QQ邮箱
 
url = 'http://www.ccdi.gov.cn/special/zyxszt/dshierlxs_zyxs/agls_xs12_zyxs/201709/t20170901_106360.html'
html = requests.get(url).text
 
emails = re.findall(regex, html)
i = 0
for email in emails:
    i += 1
    if i < 16 :
        print("{},".format(email))'''
        
from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
import re

# a queue of urls to be crawled
new_urls = deque(['https://www.zhipin.com/i100020-c101270100/'])

# a set of urls that we have already crawled
processed_urls = set()

# a set of crawled emails
emails = set()

# process urls one by one until we exhaust the queue
while len(new_urls):

    # move next url from the queue to the set of processed urls
    url = new_urls.popleft()
    processed_urls.add(url)

    # extract base url to resolve relative links
    parts = urlsplit(url)
    base_url = "{0.scheme}://{0.netloc}".format(parts)
    path = url[:url.rfind('/')+1] if '/' in parts.path else url

    # get url's content
    print("Processing %s" % url)
    try:
        response = requests.get(url)
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        # ignore pages with errors
        continue

    # extract all email addresses and add them into the resulting set
    new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
    emails.update(new_emails)

    # create a beutiful soup for the html document
    soup = BeautifulSoup(response.text)

    # find and process all the anchors in the document
    for anchor in soup.find_all("a"):
        # extract link url from the anchor
        link = anchor.attrs["href"] if "href" in anchor.attrs else ''
        # resolve relative links
        if link.startswith('/'):
            link = base_url + link
        elif not link.startswith('http'):
            link = path + link
        # add the new url to the queue if it was not enqueued nor processed yet
        if not link in new_urls and not link in processed_urls:
            new_urls.append(link)
    print(', '.join(emails))
    #print(str(emails).strip("'"))