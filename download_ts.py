import aiohttp
import logging
import asyncio
import re
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

Basic_url = input('请输入要爬取的m3u8文件的链接:')

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) APPlewebKit/537.36 (KHTML, likeGecko) \
    Chrome/52.0.2743.116 safari/   537.36'
}

session = None
semaphore = asyncio.Semaphore(5)


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


async def save_ts(content):
    for n in range(len(results)):
        with open('C:\\Users\\吴晨宇\\PycharmProjects\\Scrape_lib\\project4\\m3u8_lst\\{}.ts'.format(n), 'wb') as file:
            file.write(content)


async def scrape_ts_in_m3u8(url):  # 爬取ts文件
    return await scrape_ts(url)


async def save_m3u8(html):
    with open('C:\\Users\\吴晨宇\\PycharmProjects\\Scrape_lib\\project4\\m3u8_lst\\index.m3u8', 'w') as file:
        file.write(html)


async def main():
    global session
    session = aiohttp.ClientSession(headers=headers)

    scrape_m3u8_task = await scrape_m3u8(Basic_url)
    save = await save_m3u8(scrape_m3u8_task)

    global results
    results = re.findall('[a-zA-z]+://[^\s]*', scrape_m3u8_task)
    '''logging.info('获得results %s', results)'''

    scrape_ts_tasks = [asyncio.ensure_future(scrape_ts_in_m3u8(url)) for url in results]
    ts_results = await asyncio.gather(*scrape_ts_tasks)

    save_data = [asyncio.ensure_future(save_ts(data)) for data in ts_results]
    await asyncio.wait(save_data)

    await session.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())