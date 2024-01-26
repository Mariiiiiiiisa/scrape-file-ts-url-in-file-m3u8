import aiohttp
import logging
import asyncio
import re
from Scrape_lib.project4.modify_m3u8 import modify_function
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')
''' 
这个程序是爬取链接不完整的,只有一部分链接
'''


m3u8_url = input('请输入要爬取的m3u8文件的链接:')
ts_url = input('请输入ts的URL，以补全')

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) APPlewebKit/537.36 (KHTML, likeGecko) \
    Chrome/52.0.2743.116 safari/   537.36'
}

session = None
semaphore = asyncio.Semaphore(5)
total_size = None


async def scrape_m3u8(url):
    async with semaphore:
        try:
            logging.info('开始爬取 URL %s', url)
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    logging.info('无法识别响应码%s，爬取URL %s过程中出现了异常', response.status, url)
        except aiohttp.ClientError:
            logging.info('爬取URL %s 过程中出现了一些异常', url)


async def scrape_ts(url):
    async with semaphore:
        try:
            logging.info('开始爬取 URL %s', url)
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.read()
                else:
                    logging.info('无法识别响应码%s，爬取URL %s过程中出现了异常', response.status, url)
        except aiohttp.ClientError:
            logging.info('爬取URL %s 过程中出现了一些异常', url)


def complement(m3u8):  # 更改sub就可以改变匹配的字符
    complement_after = re.sub('video', ts_url, m3u8)
    if not complement_after:
        return m3u8
    else:
        return complement_after


def save_ts(content):
    with open('F:\\Pycharm\\PycharmProjects\\Scrape_lib\\project4\\m3u8_lst\\{}.ts'.format(total_size), 'wb') as file:
        if content:
            file.write(content)


async def scrape_ts_in_m3u8(url):  # 爬取ts文件
    return await scrape_ts(url)


def save_m3u8(html):
    with open('F:\\Pycharm\\PycharmProjects\\Scrape_lib\\project4\\m3u8_lst\\index.m3u8', 'w') as file:
        file.write(html)


async def main():
    global session
    session = aiohttp.ClientSession(headers=headers)

    global total_size
    total_size = 0

    m3u8 = await scrape_m3u8(m3u8_url)
    complement_m3u8 = complement(m3u8)
    save_m3u8(complement_m3u8)

    results = re.findall('https://.*?\.ts', complement_m3u8)
    '''logging.info('获得results %s', results)'''

    scrape_ts_tasks = [asyncio.ensure_future(scrape_ts_in_m3u8(url)) for url in results]
    ts_results = await asyncio.gather(*scrape_ts_tasks)

    for ts_data in ts_results:
        if ts_data:
            save_ts(ts_data)
            total_size += 1
    logging.info('有效链接为：%s', total_size)

    await session.close()

    modify_function()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())