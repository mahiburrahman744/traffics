import asyncio
import random
import lxml.html
import tldextract
import httpx
from fake_useragent import UserAgent
import os
import requests

class Header:
    screen_resolution = [
        '800×600', '1024×768', '1152×864', '1280×1024', '1440×900', '1680×1050', '1920×1080'
    ]

    def generate_header_list(self, num_headers):
        headers = []
        ua = UserAgent()
        for _ in range(num_headers):
            headers.append({
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'accept-encoding': 'gzip, deflate, br',
                'cache-control': 'max-age=0',
                'connection': 'keep-alive',
                'upgrade-insecure-requests': '1',
                'user-agent': ua.random
            })
        return headers

class GetProxy:
    def get_proxy(self, http='proxies.txt'):
        if os.path.exists(http):
            with open(http, 'r') as file:
                proxies = file.read().splitlines()
            return proxies
        else:
            response = requests.get('https://www.proxy-list.download/api/v1/get?type=http')
            proxies = response.text.splitlines()
            with open(http, 'w') as file:
                file.write("\n".join(proxies))
            return proxies

class RateUp(Header, GetProxy):

    def __init__(self):
        self.min_time = 62
        self.max_time = 146
        self.good = 0
        self.bad = 0

    async def go_to_url(self, proxy, header, url_list, resolution, semaphore):
        site_url = random.choice(url_list)
        links_from_site = []
        ext = tldextract.extract(site_url)
        async with semaphore:
            try:
                status = await self.validation_proxy(proxy, header)
                if status['status']:
                    self.good += 1
                    async with httpx.AsyncClient(proxies={"http": proxy, "https": proxy}, headers=header, timeout=10) as client:
                        domain = site_url
                        for i in range(0, random.choice([2, 3, 4, 5, 6])):
                            if ext.subdomain:
                                header['host'] = f'{ext.subdomain}.{ext.domain}.{ext.suffix}'
                            else:
                                header['host'] = f'{ext.domain}.{ext.suffix}'
                            try:
                                response = await client.get(domain)
                                content = response.text
                                print(f'{resolution} | {status["country"]} | {domain} | {proxy} | {header}')
                                header['referer'] = domain
                                html = lxml.html.fromstring(content)
                                all_urls = html.xpath('//a/@href')
                                await asyncio.sleep(random.uniform(self.min_time, self.max_time))
                                for u in all_urls:
                                    if f'{ext.domain}.{ext.suffix}' in u:
                                        links_from_site.append(u)
                                if domain in links_from_site:
                                    links_from_site.remove(domain)
                                domain = random.choice(links_from_site)
                            except:
                                domain = random.choice(url_list)
            except:
                self.bad += 1

    async def validation_proxy(self, proxy, header):
        try:
            async with httpx.AsyncClient(proxies={"http": proxy, "https": proxy}, headers=header, timeout=10) as client:
                response = await client.get('http://www.google.com')
                if response.status_code == 200:
                    return {"status": True, "country": response.headers.get('X-Geo-Country', 'Unknown')}
        except:
            return {"status": False}
        return {"status": False}

    async def main(self, proxy_list_for_site, header_list, url_list):
        semaphore = asyncio.Semaphore(20)
        queue = asyncio.Queue()
        task_list = []

        for proxy in proxy_list_for_site:
            resolution = random.choice(Header.screen_resolution)
            header = random.choice(header_list)
            task = asyncio.create_task(self.go_to_url(proxy, header, url_list, resolution, semaphore))
            task_list.append(task)
            await asyncio.sleep(0.5)

        await queue.join()
        await asyncio.gather(*task_list, return_exceptions=True)
        print(f'Good visits: {self.good}')
        print(f'Bad visits: {self.bad}')

    def start(self, proxies, header_list, site_url):
        asyncio.run(self.main(proxies, header_list, site_url))

if __name__ == "__main__":
    proxies = GetProxy().get_proxy(http='proxies.txt')
    headers = Header().generate_header_list(10)
    urls = ['https://www.highrevenuenetwork.com/iaqgtx69y1?key=14a1e46999747270c942f2634ef5306a']
    rateup = RateUp()
    rateup.start(proxies, headers, urls)
