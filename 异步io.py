import asyncio
import requests
from lxml import etree
import  time

url='http://quote.stockstar.com/stock/ranklist_a_3_1_1.html'
page=int(url.split('_')[-1].split('.')[0])
next_page=page
list_url=[]
list_url.append(url)
for i in range(115):
    next_page+=1
    next_url=url.replace('{}.html'.format(page),'{}.html'.format(next_page))
    list_url.append(next_url)

import aiohttp
async def get_url(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as html:
                res=await html.text()
                return res
                # print(res)

async def parse(url):
    r=await get_url(url)
    #x=await asyncio.sleep(0.001)
    root=etree.HTML(r)
    print(url)
    for res in root.xpath('//tbody/tr/td[2]/a/text()'):
        print(res)

# @asyncio.coroutine
# def hello(name):
#     print('hello %s'%name)
#     r=yield from asyncio.sleep(2)
#     print('hello again')
# list=['a','b','c']
start=time.time()
loop=asyncio.get_event_loop()
tasks=[parse(url) for url in list_url]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
print('Haoshi %s'%(time.time()-start))
