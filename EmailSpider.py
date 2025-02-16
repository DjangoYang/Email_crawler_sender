# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 11:23:57 2020

"""
from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
import re

# a queue of urls to be crawled
new_urls = deque(['https://www.hyit.edu.cn/'])

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

    # Update the regular expression pattern to capture email addresses excluding image file extensions
    new_emails = set(re.findall(r"[a-z0-9.\-+_]+@[a-z0-9.\-+_]+\.(?!png|jpg|jpeg|gif)[a-z]+", response.text, re.I))

    # Add an additional filter step to exclude email addresses ending with image file extensions
    filtered_emails = set()
    for email in new_emails:
        if not any(email.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif']):
            # Fix emails ending with a single character after the dot
            domain_parts = email.split('.')
            if len(domain_parts[-1]) == 1:
                email = email + 'n'  # You can modify this logic as needed for other cases
            filtered_emails.add(email)

    emails.update(filtered_emails)

    # create a beautiful soup for the html document
    soup = BeautifulSoup(response.text, "html.parser")

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
