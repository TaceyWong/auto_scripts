# coding:utf-8
import hashlib
import requests
import base64
import re
import urllib
import rsa
import json
import binascii
from bs4 import BeautifulSoup
import pickle
import time


class Utils(object):
    @classmethod
    def get_md5(cls, text):
        md5 = hashlib.md5()
        md5.update(text)
        return md5.hexdigest()

    @classmethod
    def get_sp(cls, pubkey, servertime, nonce, password):
        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey, 65537)
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
        sp = binascii.b2a_hex(rsa.encrypt(message, key))
        return sp

    @classmethod
    def get_base64(cls, ori):
        url_quote = urllib.quote(ori)
        bs64 = base64.b64encode(url_quote)
        return bs64

    @classmethod
    def gen_postdata(cls, su, servertime, nonce, sp, rsakv):
        postdata = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'userticket': '1',
            'ssosimplelogin': '1',
            'vsnf': '1',
            'vsnval': '',
            'su': su,
            'service': 'miniblog',
            'servertime': servertime,
            'nonce': nonce,
            'pwencode': 'rsa2',
            'sp': sp,
            'encoding': 'UTF-8',
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META',
            'rsakv': rsakv,
        }
        return postdata


class Weibo:
    url_prelogin = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.5)&_=1364875106625'
    url_login = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.5)'
    url_index = "http://weibo.com/u/{}"
    post_text_url = "http://weibo.com/p/aj/v6/mblog/add?ajwvr=6&domain=100505&__rnd={}"
    session = requests.Session()
    headers = {}
    username = None
    password = None

    def login(self, username, password):
        # 获取服务器端信息
        self.username = username
        self.password = password
        resp = self.session.get(self.url_prelogin)
        json_data = re.search('\((.*)\)', resp.content).group(1)
        data = json.loads(json_data)
        servertime = data['servertime']
        nonce = data['nonce']
        pubkey = data['pubkey']
        rsakv = data['rsakv']
        su = Utils.get_base64(username)
        sp = Utils.get_sp(pubkey, servertime, nonce, password)
        # 构造登陆请求
        postdata = Utils.gen_postdata(su, servertime, nonce, sp, rsakv)
        resp = self.session.post(self.url_login, data=postdata)
        login_url = re.findall('replace\(\'(.*)\'\)', resp.content)
        respo = self.session.get(login_url[0])
        uid = re.findall('"uniqueid":"(\d+)",', respo.content)[0]
        url = self.url_index.format(uid)
        self.session.get(url)
        self.headers['set-cookie'] = resp.headers['set-cookie']
        self.headers['Referer'] = 'http://weibo.com/comment/inbox?leftnav=1&wvr=5'
        self.headers["User-Agent"] ="Mozilla/5.0(Macintosh;Intel Mac OS X 10_11_4) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 56.0.2924.87Safari/537.36"
        flag = self._check_login()
        if not flag:
            print self.username, "登录失败"
            return False
        # user = {"session": self.session, "headers": self.headers}
        # name = Utils.get_md5(self.username) + ".pkl"
        # pkl_file = file(name, 'wb')
        # pickle.dump(user, pkl_file, True)
        # pkl_file.close()
        print self.username, "登陆成功"

    def _check_login(self):
        resp = self.session.get("http://www.weibo.com")
        content = resp.content
        soup = BeautifulSoup(content, "lxml")
        result = u"我的首页 微博-随时随地发现新鲜事" == soup.title.text
        return result


    def post_text(self, text):
        post_url = self.post_text_url.format(time.time()*100)
        playground = {
            "title": "有什么新鲜事想告诉大家?",
            "location": "page_100505_home",
            "text": text,
            "appkey": None,
            "style_type": 1,
            "pic_id": None,
            "rank": 0,
            "rankid": None,
            "pub_source": "page_2",
            "longtext": "1",
            "topic_id": "1022:",
            "pub_type": "dialog",
            "_t": 0,
        }
        r = self.session.post(url,data=playground,headers=self.headers)
        print r.content

    def post_text_pic(self, text, fileobj):
        title:有什么新鲜事想告诉大家?
        location:page_100505_home
        text:这是测试
        appkey:
        style_type:1
        pic_id:67
        aa34a5ly1fd9tzeoj76j20g40g475x
        pdetail:1005051739207845
        gif_ids:
        rank:0
        rankid:
        pub_source:page_2
        longtext:1
        topic_id:1022:
        pub_type:dialog
        _t:0

    def _upload_pic(self,fileobj):
        Referer:http: // js.t.sinajs.cn / t6 / home / static / swf / MultiFilesUpload.swf?version = 6785
        aab081e102e3
        User - Agent:Mozilla / 5.0(Macintosh;
        Intel
        Mac
        OS
        X
        10
        _11_4) AppleWebKit / 537.36(KHTML, like
        Gecko) Chrome / 56.0
        .2924
        .87
        Safari / 537.36
        X - Requested - With:ShockwaveFlash / 24.0
        .0
        .221
        http: // picupload.service.weibo.com / interface / pic_upload.php?app = miniblog & data = 1 & url = weibo.com / iTacey & markpos = 1 & logo = 1 & nick = % 40
        TaceyWong & marks = 1 & mime = image / jpeg & ct = 0.9979112613946199


if __name__ == "__main__":

    w = Weibo()
    w.login("dnapro@sina.cn","WANGXINYONG123")
    w.post_text("zheshiceshi ")