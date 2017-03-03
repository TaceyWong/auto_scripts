# coding:utf-8

from urlparse import urljoin
import re
import requests
from StringIO import StringIO
from datetime import datetime


header = {
    "User-Agent": "Mozilla/5.0(Macintosh;Intel Mac OS X 10_11_4) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 56.0.2924.87Safari/537.36"
}

class Weibo(object):
    TOKEN = ""

    @classmethod
    def post_text(cls, text):
        url_post_a_text = "https://api.weibo.com/2/statuses/update.json"
        playload = {
            "access_token": cls.TOKEN,
            "status": text
        }
        r = requests.post(url_post_a_text, data=playload)
        return r.content

    @classmethod
    def post_text_pic(cls, text, fileobj):
        url_post_pic = "https://upload.api.weibo.com/2/statuses/upload.json"
        playload = {
            "access_token": cls.TOKEN,
            "status": text
        }
        files = {"pic": fileobj}
        r = requests.post(url_post_pic, data=playload, files=files)
        return r.content


def get_pic_info():
    bing_url = "https://www.bing.com"

    pic_url_re = re.compile(r'url: \"(.*?)jpg')
    pic_title_re = re.compile(r'<a id="sh_cp" class="sc_light" title="(.*?)"')
    content = requests.get(bing_url, headers=header).content
    pic_url = pic_url_re.findall(content)[0]
    pic_title = pic_title_re.findall(content)[0]
    pic_url = urljoin("https://www.bing.com", pic_url) + "jpg"

    return pic_url, pic_title


def main():
    pic_url, pic_title = get_pic_info()
    print pic_title
    print pic_url
    pic_content = requests.get(pic_url,headers=header).content
    text = datetime.now().strftime("%Y-%m-%d")+":[BING]:"+pic_title
    result = Weibo.post_text_pic(text=text, fileobj=StringIO(pic_content))
    print result

if __name__ == "__main__":
    main()
