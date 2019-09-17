"""
解析每个省份用什么参数代表
例如 gd 广东
"""

import requests
import time
import re
from lxml import etree
import pickle as pk
from collections import OrderedDict

url = "https://www.tianyancha.com/search#delfilter"


def parse_page(url):
    province_dict = OrderedDict()
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
            'CooKie': 'aliyungf_tc=AQAAAD70vCzHpwUATep4ysFjmHDxZ+Fh; ssuid=3118312293; bannerFlag=true; csrfToken=pb8vO6ruUw2A-xmrxamEq9ud; TYCID=e48f0700d7b211e985baefd6bd263e3b; undefined=e48f0700d7b211e985baefd6bd263e3b; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1568549895,1568550973,1568630314; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1568708130; _ga=GA1.2.1655942331.1568549898; _gid=GA1.2.173652123.1568549898; RTYCID=7742e80e4c9e4f5c938f979b126bfbce; CT_TYCID=a686335a6b6449a68d6f037840fe8dff; cloud_token=dcb88edb51af4e7da27389f53c1196d5; token=a2224012e5934de1973a80f502234c97; _utm=69a8fb9e23104fb39ae850ae9d6407dd; _gat_gtag_UA_123487620_1=1; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25225%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522surday%2522%253A%2522365%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522onum%2522%253A%25226%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTIxNjY4MDY4MiIsImlhdCI6MTU2ODcwODE2NywiZXhwIjoxNjAwMjQ0MTY3fQ.rzrabc-InrpuBf4e5IWkljxWG_evFSSJDRwFY_ySEjnqt4uvK-2Z_DMPHH98ngIaHA-7-IwYMOnX2JjH8CYGHw%2522%252C%2522vipToTime%2522%253A%25221600166485966%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E6%259D%25B0%25E6%258B%2589%25E5%25B0%2594%25E5%25BE%25B7%25C2%25B7%25E8%258E%25AB%25E5%25B0%2594%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522isExpired%2522%253A%25220%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%252220%2522%252C%2522mobile%2522%253A%252215216680682%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTIxNjY4MDY4MiIsImlhdCI6MTU2ODcwODE2NywiZXhwIjoxNjAwMjQ0MTY3fQ.rzrabc-InrpuBf4e5IWkljxWG_evFSSJDRwFY_ySEjnqt4uvK-2Z_DMPHH98ngIaHA-7-IwYMOnX2JjH8CYGHw'
        }
        html = requests.get(url, headers=headers).text
        print(html)
        selector = etree.HTML(html)
        print(selector)
        province_urls = selector.xpath('.//div[@class="folder-body"]/div[2]/div[1]/a/@href')
        province_name = selector.xpath('.//div[@class="folder-body"]/div[2]/div[1]/a/text()')
        for i, j in zip(province_urls, province_name):
            province_dict[re.split(r'=', i)[1]] = j
        province_dict.pop("hk")
        province_dict.pop("mo")
        province_dict.pop("tw")
        for k, v in province_dict.items():
            print(k, v)
        pk.dump(province_dict, file=open('./data/province_dict.pkl', 'wb'))

        province_city_dict = {}
        for province, v in province_dict.items():
            url = "https://www.tianyancha.com/search?base=" + province
            html = requests.get(url, headers=headers).text
            selector = etree.HTML(html)

            city_name = selector.xpath('.//div[@class="folder-body"]/div[2]/div[1]/a/text()')
            if v not in ["香港特别行政区", "澳门特别行政区", "台湾省"]:
                province_city_dict[v] = city_name
                print(v, city_name)
        pk.dump(province_city_dict, file=open('./data/province_city_dict.pkl', 'wb'))

    except Exception as e:
        print(e)


if __name__ == '__main__':
    parse_page(url)
