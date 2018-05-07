from bs4 import BeautifulSoup
import requests
import re
import pymongo
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client.genconf
talks = db.talks
page_link = 'https://www.lds.org/general-conference/2017/10/the-plan-and-the-proclamation?lang=eng'
page_response = requests.get(page_link, timeout=5)
page_content = BeautifulSoup(page_response.content, "html.parser")


talkObj = {
    'title': "",
    'author': "",
    'date': "",
    'text': [],
    'references': [],
}

title = page_content.find(
    'span', attrs={"class": "sticky-banner__current"}).text.encode('utf-8')
date = page_content.find('a', attrs={"class": "sticky-banner__link"}).text.encode('utf-8')
author = page_content.find(
    'a', attrs={"class": "article-author__name"}).text.encode('utf-8')

print title
print date
print author
talkObj["title"] = title
talkObj["date"] = date
talkObj["author"] = author

textP = []
for x in page_content.find_all('p', id=lambda x: x and x.startswith('p')):
    paragraphs = x.text.encode('utf-8')
    print paragraphs
    talkObj['text'].append(paragraphs)
scrRef = []
for x in page_content.findAll('a', attrs={"class": "scripture-ref"}):
    ref = x.text
    talkObj['references'].append(ref)

print talkObj
talkObj_id = talks.insert_one(talkObj).inserted_id
