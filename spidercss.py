from urllib.parse import urljoin
import requests
from lxml import etree
from bs4 import BeautifulSoup as bs

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.50"
}

index_page = "https://www.hongniuzy.com/"

result = {}

def get_first(list, default=None):
    try:
        ret = list[0]
    except:
        ret = default
    finally:
        return ret

def parse_detail(url):
    res = requests.get(url, headers=headers)
    # html = etree.HTML(res.content)
    soup = bs(res.content, "lxml")
    # m3u8_links = html.xpath("//div[@id='play_2']//a/@href")
    m3u8_links = [a.get("href") for a in soup.select("div#play_2 a")]
    # vodBox = get_first(html.xpath("//div[@class='vodBox']"))
    vodBox = soup.select_one("div.vodBox")
    # img = get_first(vodBox.xpath("div[@class='vodImg']/img/@src"))
    img = vodBox.select_one("div.vodImg > img").get("src")
    # name = get_first(vodBox.xpath("div[@class='vodInfo']/div[@class='vodh']/h2/text()"))
    name = vodBox.select_one("div.vodInfo > div.vodh > h2").get_text()
    # kvs = vodBox.xpath("div[@class='vodInfo']/div[@class='vodinfobox']/ul/li")
    kvs = vodBox.select("div.vodInfo > div.vodinfobox > ul > li")
    print(name, img, m3u8_links)
    for kv in kvs:
        # k = get_first(kv.xpath("text()"), "")
        k, v = kv.get_text().split("：")
        # v = get_first(kv.xpath("span/text()"), "") or get_first(kv.xpath("span/font/text()"), "")
        # v = kv.select_one("span").get_text()
        print(k, v)


def parse_list(url):
    res = requests.get(url, headers=headers)
    # html = etree.HTML(res.content)
    soup = bs(res.content, "lxml")
    # lis = html.xpath("//div[@class='xing_vb']/ul/li")[1:]
    lis = soup.select("div.xing_vb > ul > li > span > a")
    for li in lis:
        # link = get_first(li.xpath("span/a/@href"))
        link = li.get("href")
        print(link)
        parse_detail(urljoin(index_page, link))
    # next_page = get_first(html.xpath("//div[@class='page_info']/a[@title='下一页']/@href"))
    next_page = soup.select_one("div.page_info > a[title='下一页']").get("href")
    print("nextpage: ", next_page)
    if(next_page!=None):
        parse_list(urljoin(index_page, next_page))

def main():
    res = requests.get(index_page, headers=headers)
    # html = etree.HTML(res.content)
    soup = bs(res.content, 'lxml')
    # categories = html.xpath('//*[@id="sddm"]/li')
    categories = soup.select("#sddm > li > a")
    for category in categories:
        link = category.get("href")
        name = category.get_text()
        print(link, name)
        url = urljoin(index_page, link)
        parse_list(url)

if __name__ == "__main__":
    main()