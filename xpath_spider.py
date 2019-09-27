"""
人数过滤参数：

500999 500-999

4999  1000-4999

9999 5000-9999

10000 10000+

"""

import requests
import time
import re
import random
import os
from lxml import etree
import pickle as pk
from csv import DictWriter
import time

url = "https://www.qichacha.com/firm_576c21e3468a6b178bbf291e4820e896.html"
ulist = []

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
user_agent = random.choice(USER_AGENTS)


def write2csv(info_dict, province):
    try:
        fieldnames = ['com_name', 'province', 'city', 'credit_no', 'legal_person', 'com_type', 'com_cate',
                      'data_eastablish', 'capital', 'num_emp', 'locate', 'email', 'bussiness_scope', 'com_url', 'phone',
                      'more_phone']
        if os.path.exists('./data/' + province + '.csv'):
            flag = 1
        else:
            flag = 0
        with open('./data/' + province + '.csv', 'a', newline='', encoding='UTF-8') as f:
            f_csv = DictWriter(f, fieldnames=fieldnames)
            if flag == 0:
                f_csv.writeheader()
            else:
                pass
            f_csv.writerow(info_dict)
    except Exception as e:
        print(e)


def parse_page(url, province):
    """
    解析最终公司信息页面
    """
    info_dict = {}
    time.sleep(5)
    print(url)
    headers = {
        'User-Agent': user_agent,
        'CooKie': 'aliyungf_tc=AQAAAD70vCzHpwUATep4ysFjmHDxZ+Fh; ssuid=3118312293; bannerFlag=true; csrfToken=pb8vO6ruUw2A-xmrxamEq9ud; TYCID=e48f0700d7b211e985baefd6bd263e3b; undefined=e48f0700d7b211e985baefd6bd263e3b; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1568549895,1568550973,1568630314; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1568708130; _ga=GA1.2.1655942331.1568549898; _gid=GA1.2.173652123.1568549898; RTYCID=7742e80e4c9e4f5c938f979b126bfbce; CT_TYCID=a686335a6b6449a68d6f037840fe8dff; cloud_token=dcb88edb51af4e7da27389f53c1196d5; token=a2224012e5934de1973a80f502234c97; _utm=69a8fb9e23104fb39ae850ae9d6407dd; _gat_gtag_UA_123487620_1=1; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25225%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522surday%2522%253A%2522365%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522onum%2522%253A%25226%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTIxNjY4MDY4MiIsImlhdCI6MTU2ODcwODE2NywiZXhwIjoxNjAwMjQ0MTY3fQ.rzrabc-InrpuBf4e5IWkljxWG_evFSSJDRwFY_ySEjnqt4uvK-2Z_DMPHH98ngIaHA-7-IwYMOnX2JjH8CYGHw%2522%252C%2522vipToTime%2522%253A%25221600166485966%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E6%259D%25B0%25E6%258B%2589%25E5%25B0%2594%25E5%25BE%25B7%25C2%25B7%25E8%258E%25AB%25E5%25B0%2594%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522isExpired%2522%253A%25220%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%252220%2522%252C%2522mobile%2522%253A%252215216680682%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTIxNjY4MDY4MiIsImlhdCI6MTU2ODcwODE2NywiZXhwIjoxNjAwMjQ0MTY3fQ.rzrabc-InrpuBf4e5IWkljxWG_evFSSJDRwFY_ySEjnqt4uvK-2Z_DMPHH98ngIaHA-7-IwYMOnX2JjH8CYGHw'
    }
    html = requests.get(url, headers=headers).text
    selector = etree.HTML(html)

    table = selector.xpath('.//div[@id="_container_baseInfo"]/table[2]')[0]

    # 公司名称
    com_name = selector.xpath('.//div[@class="content"]/div/h1/text()')[0]
    print(com_name)

    # 省份
    province_2_CN = pk.load(file=open('./data/province_dict.pkl', 'rb'))
    province = province_2_CN[province]
    print(province)

    # 城市
    province_2_city = pk.load(file=open('./data/province_city_dict.pkl', 'rb'))
    city_list = province_2_city[province]
    locate = table.xpath('//tr[10]//td[2]/text()')[0].strip()
    city = "-"
    for i in city_list:
        if i in locate or i[:-1] in locate:
            city = i
    print(city)

    # 信用代码
    credit_no = table.xpath('//tr[3]/td[2]/text()')[0].strip()
    print(credit_no)

    #  法定代表人
    legal_person = selector.xpath('//div[@class="name"]/a/text()')[0]
    print(legal_person)

    #  企业类型
    com_type = table.xpath('//tr[5]/td[2]/text()')[0].strip()
    print(com_type)

    # 所属行业
    com_cate = table.xpath('//tr[5]/td[4]/text()')[0].strip()
    print(com_cate)

    # 成立日期
    data_eastablish = table.xpath('//tr[2]/td[2]/div/text()')[0].strip()
    print(data_eastablish)

    # 注册资本
    # capital = table.xpath('//tr[1]/td[1]/text()')[0].strip()
    capital = selector.xpath('.//div[@id="_container_baseInfo"]/table[2]//tr[1]/td[4]/text()')[0].strip()
    print(capital)

    # 企业人数
    num_emp = table.xpath('//tr[8]//td[4]/text()')[0].strip()
    print(num_emp)

    # 公司位置
    print(locate)

    # 邮箱
    email = selector.xpath('.//div[@class="detail "]/div[1]/div[2]/span[2]/text()')[0]
    print(email)

    # 经营范围
    bussiness_scope = table.xpath('//tr[11]//span/text()')[0].strip()
    print(bussiness_scope)

    # 网址
    com_url = '-'
    if selector.xpath('.//div[@class="detail "]/div[2]/div[1]/a/text()'):
        com_url = selector.xpath('.//div[@class="detail "]/div[2]/div[1]/a/text()')[0]
    print(com_url)

    # 电话号码
    phone = selector.xpath('.//div[@class="detail "]/div[1]/div[1]/span[2]/text()')[0]
    print(phone)

    # 更多号码
    more_phone = '-'
    if selector.xpath('.//div[@class="detail "]/div[1]/div[1]/span[3]/span[1]/text()'):
        more_phone = selector.xpath('.//div[@class="detail "]/div[1]/div[1]/span[3]/span[1]/text()')[0]
    print(more_phone)

    info_dict['com_name'] = com_name
    info_dict['province'] = province
    info_dict['city'] = city
    info_dict['credit_no'] = credit_no
    info_dict['legal_person'] = legal_person
    info_dict['com_type'] = com_type
    info_dict['com_cate'] = com_cate
    info_dict['data_eastablish'] = data_eastablish
    info_dict['capital'] = capital
    info_dict['num_emp'] = num_emp
    info_dict['locate'] = locate
    info_dict['email'] = email
    info_dict['bussiness_scope'] = bussiness_scope
    info_dict['com_url'] = com_url
    info_dict['phone'] = phone
    info_dict['more_phone'] = more_phone

    """
    如果公司人数大于500，写入CSV
    """
    # if re.search(r'[\d]+', info_dict['num_emp']):
    #     num_emp = int(re.search(r'[\d]+', info_dict['num_emp']).group())
    #     if num_emp >= 500:
    print("公司的人数有:", info_dict['num_emp'], "写入数据")
    write2csv(info_dict, province)
    print("====================================================================")
    print("")


def parse_columns(province="gd", num=500999):
    """
    解析地区的选择翻页界面
    """

    # 解析查询结果的页数
    url_base = "https://www.tianyancha.com/search/oss" + str(num) + "?base=" + province
    print(url_base)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
        'CooKie': 'aliyungf_tc=AQAAAD70vCzHpwUATep4ysFjmHDxZ+Fh; ssuid=3118312293; bannerFlag=true; csrfToken=pb8vO6ruUw2A-xmrxamEq9ud; TYCID=e48f0700d7b211e985baefd6bd263e3b; undefined=e48f0700d7b211e985baefd6bd263e3b; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1568549895,1568550973,1568630314; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1568708130; _ga=GA1.2.1655942331.1568549898; _gid=GA1.2.173652123.1568549898; RTYCID=7742e80e4c9e4f5c938f979b126bfbce; CT_TYCID=a686335a6b6449a68d6f037840fe8dff; cloud_token=dcb88edb51af4e7da27389f53c1196d5; token=a2224012e5934de1973a80f502234c97; _utm=69a8fb9e23104fb39ae850ae9d6407dd; _gat_gtag_UA_123487620_1=1; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25225%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522surday%2522%253A%2522365%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25220%2522%252C%2522onum%2522%253A%25226%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTIxNjY4MDY4MiIsImlhdCI6MTU2ODcwODE2NywiZXhwIjoxNjAwMjQ0MTY3fQ.rzrabc-InrpuBf4e5IWkljxWG_evFSSJDRwFY_ySEjnqt4uvK-2Z_DMPHH98ngIaHA-7-IwYMOnX2JjH8CYGHw%2522%252C%2522vipToTime%2522%253A%25221600166485966%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E6%259D%25B0%25E6%258B%2589%25E5%25B0%2594%25E5%25BE%25B7%25C2%25B7%25E8%258E%25AB%25E5%25B0%2594%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522isExpired%2522%253A%25220%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%252220%2522%252C%2522mobile%2522%253A%252215216680682%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTIxNjY4MDY4MiIsImlhdCI6MTU2ODcwODE2NywiZXhwIjoxNjAwMjQ0MTY3fQ.rzrabc-InrpuBf4e5IWkljxWG_evFSSJDRwFY_ySEjnqt4uvK-2Z_DMPHH98ngIaHA-7-IwYMOnX2JjH8CYGHw'
    }
    html = requests.get(url_base, headers=headers).text
    selector = etree.HTML(html)
    table = selector.xpath('.//ul[@class="pagination"]/li/a/text()')
    page_num = int(table[-2].strip('.'))
    print(page_num)

    for i in range(1, page_num + 1):
        time.sleep(2)
        print("下面爬取第%d页内容" % i)
        print("*********************")
        url = 'https://www.tianyancha.com/search/oss' + str(num) + '/p' + str(i) + '?base=' + province
        print(url)

        html = requests.get(url, headers=headers).text
        selector = etree.HTML(html)

        table = selector.xpath('.//div[@class="result-list sv-search-container"]//div[@class="header"]/a/@href')
        for url_ in table:
            parse_page(url_, province)


if __name__ == '__main__':
    # parse_columns("gd", 500999)
    parse_columns()
