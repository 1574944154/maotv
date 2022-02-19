from urllib.parse import urljoin
import requests
from lxml import etree

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
    html = etree.HTML(res.content)
    m3u8_links = html.xpath("//div[@id='play_2']//a/@href")
    vodBox = get_first(html.xpath("//div[@class='vodBox']"))
    img = get_first(vodBox.xpath("div[@class='vodImg']/img/@src"))
    name = get_first(vodBox.xpath("div[@class='vodInfo']/div[@class='vodh']/h2/text()"))
    kvs = vodBox.xpath("div[@class='vodInfo']/div[@class='vodinfobox']/ul/li")
    print(name, img, m3u8_links)
    for kv in kvs:
        k = get_first(kv.xpath("text()"), "")
        v = get_first(kv.xpath("span/text()"), "") or get_first(kv.xpath("span/font/text()"), "")
        print(k, v)


def parse_list(url):
    res = requests.get(url, headers=headers)
    html = etree.HTML(res.content)
    lis = html.xpath("//div[@class='xing_vb']/ul/li")[1:]
    for li in lis:
        link = get_first(li.xpath("span/a/@href"))
        print(link)
        parse_detail(urljoin(index_page, link))
    next_page = get_first(html.xpath("//div[@class='page_info']/a[@title='下一页']/@href"))
    print("nextpage: ", next_page)
    if(next_page!=None):
        parse_list(urljoin(index_page, next_page))

def main():
    res = requests.get(index_page, headers=headers)
    html = etree.HTML(res.content)
    categories = html.xpath('//*[@id="sddm"]/li')
    for category in categories:
        link = get_first(category.xpath("a/@href"))
        name = get_first(category.xpath("a/text()"))
        print(link, name)
        url = urljoin(index_page, link)
        parse_list(url)

if __name__ == "__main__":
    main()