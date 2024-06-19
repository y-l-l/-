import json
from lxml import etree
import requests
import pymysql
import time
import random

headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'Referer':
        'https://so.toutiao.com/search?dvpf=pc&source=search_subtab_switch&keyword=%E6%A0%B8%E5%BA%9F%E6%B0%B4&pd=information'
        '&action_type=search_subtab_switch&page_num=0&search_id=&from=news&cur_tab_title=news',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cookie': 'tt_webid=7300771276162729472; _ga=GA1.1.1896388257.1699843291; '
              'passport_csrf_token=3a499478d75939e898c0d199d140ef55; '
              'passport_csrf_token_default=3a499478d75939e898c0d199d140ef55; '
              'n_mh=6_XU3Ug6LdyjPOH9VF8yvXNTODJr9FWk_5L738GWdLs; sso_uid_tt=5713b61772742745fbc403c269ff48eb; '
              'sso_uid_tt_ss=5713b61772742745fbc403c269ff48eb; toutiao_sso_user=fbeef197d5b6f14b63433736cd6bbc9d; '
              'toutiao_sso_user_ss=fbeef197d5b6f14b63433736cd6bbc9d; '
              'sid_ucp_sso_v1=1.0.0'
              '-KDhjYzFmM2NhYzMxYTY3YmI4ZGM0M2Y3OTdmMmFjYjNmNDYxOGM5OTYKHwiP8tDz34y3BxDzmsaqBhjPCSAMML3R_5oGOAZA9AcaAmhsIiBmYmVlZjE5N2Q1YjZmMTRiNjM0MzM3MzZjZDZiYmM5ZA; ssid_ucp_sso_v1=1.0.0-KDhjYzFmM2NhYzMxYTY3YmI4ZGM0M2Y3OTdmMmFjYjNmNDYxOGM5OTYKHwiP8tDz34y3BxDzmsaqBhjPCSAMML3R_5oGOAZA9AcaAmhsIiBmYmVlZjE5N2Q1YjZmMTRiNjM0MzM3MzZjZDZiYmM5ZA; passport_auth_status=cfa0a69c19594030940eebb514dfb716%2C; passport_auth_status_ss=cfa0a69c19594030940eebb514dfb716%2C; sid_guard=61bbb88bd79834c6983cbf1e6812b022%7C1699843444%7C5184001%7CFri%2C+12-Jan-2024+02%3A44%3A05+GMT; uid_tt=850cdb498f887c780b16b8d1b14a145e; uid_tt_ss=850cdb498f887c780b16b8d1b14a145e; sid_tt=61bbb88bd79834c6983cbf1e6812b022; sessionid=61bbb88bd79834c6983cbf1e6812b022; sessionid_ss=61bbb88bd79834c6983cbf1e6812b022; sid_ucp_v1=1.0.0-KGQ1YjY2YTVkNjMzNGI4NDVkNmJhY2MzZmQ2MTE5N2MzZDg0YjVjYTAKGQiP8tDz34y3BxD0msaqBhjPCSAMOAZA9AcaAmxxIiA2MWJiYjg4YmQ3OTgzNGM2OTgzY2JmMWU2ODEyYjAyMg; ssid_ucp_v1=1.0.0-KGQ1YjY2YTVkNjMzNGI4NDVkNmJhY2MzZmQ2MTE5N2MzZDg0YjVjYTAKGQiP8tDz34y3BxD0msaqBhjPCSAMOAZA9AcaAmxxIiA2MWJiYjg4YmQ3OTgzNGM2OTgzY2JmMWU2ODEyYjAyMg; store-region=cn-hn; store-region-src=uid; odin_tt=7a8beb989a1b2cebc2063cc20eee35b25ccd6a70f4493c774cbbd6b0aad1635fab569b3cdc574a1be58ef8dda402e2e2; msToken=AYqmSWXsv_yeBrKu3DfQA8ZSh03EfO5irb9de4dhvJ63-xx3KUV1QCuGjby_hRMuBIgwFUTLqORG5r_TW8Ino22aFbxrfk2Fv6USOfJYa20ElB-g4XpPXp4LNha-JA==; ttwid=1%7CBeGD7rZihOMSpl_bLJl5cJBZZv3M7B4LmpAprCHzGzM%7C1700313453%7C8f22335966605ed26f192fede381632b5fb37fc4677f764e4b9616ac06606d30; _ga_QEHZPBE5HH=GS1.1.1700313454.2.0.1700313454.0.0.0; __ac_nonce=06558b97400c7a6ac76f0; __ac_signature=_02B4Z6wo00f01StmOMgAAIDCfuSzVHYcJmkrRjxAAC-Ec2; __ac_referer=https://www.toutiao.com/; _tea_utm_cache_4916=undefined; _S_IPAD=0; s_v_web_id=verify_lp42qims_2DDhkkax_3sIB_4UDU_Aqi8_0cB6NJnqH9ru; _S_WIN_WH=1055_753; _S_DPR=2.0000000596046448'
}
headers1 = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cookie': 'tt_webid=7300771276162729472; _ga=GA1.1.1896388257.1699843291; '
              'passport_csrf_token=3a499478d75939e898c0d199d140ef55; '
              'passport_csrf_token_default=3a499478d75939e898c0d199d140ef55; '
              'n_mh=6_XU3Ug6LdyjPOH9VF8yvXNTODJr9FWk_5L738GWdLs; sso_uid_tt=5713b61772742745fbc403c269ff48eb; '
              'sso_uid_tt_ss=5713b61772742745fbc403c269ff48eb; toutiao_sso_user=fbeef197d5b6f14b63433736cd6bbc9d; '
              'toutiao_sso_user_ss=fbeef197d5b6f14b63433736cd6bbc9d; '
              'sid_ucp_sso_v1=1.0.0'
              '-KDhjYzFmM2NhYzMxYTY3YmI4ZGM0M2Y3OTdmMmFjYjNmNDYxOGM5OTYKHwiP8tDz34y3BxDzmsaqBhjPCSAMML3R_5oGOAZA9AcaAmhsIiBmYmVlZjE5N2Q1YjZmMTRiNjM0MzM3MzZjZDZiYmM5ZA; ssid_ucp_sso_v1=1.0.0-KDhjYzFmM2NhYzMxYTY3YmI4ZGM0M2Y3OTdmMmFjYjNmNDYxOGM5OTYKHwiP8tDz34y3BxDzmsaqBhjPCSAMML3R_5oGOAZA9AcaAmhsIiBmYmVlZjE5N2Q1YjZmMTRiNjM0MzM3MzZjZDZiYmM5ZA; passport_auth_status=cfa0a69c19594030940eebb514dfb716%2C; passport_auth_status_ss=cfa0a69c19594030940eebb514dfb716%2C; sid_guard=61bbb88bd79834c6983cbf1e6812b022%7C1699843444%7C5184001%7CFri%2C+12-Jan-2024+02%3A44%3A05+GMT; uid_tt=850cdb498f887c780b16b8d1b14a145e; uid_tt_ss=850cdb498f887c780b16b8d1b14a145e; sid_tt=61bbb88bd79834c6983cbf1e6812b022; sessionid=61bbb88bd79834c6983cbf1e6812b022; sessionid_ss=61bbb88bd79834c6983cbf1e6812b022; sid_ucp_v1=1.0.0-KGQ1YjY2YTVkNjMzNGI4NDVkNmJhY2MzZmQ2MTE5N2MzZDg0YjVjYTAKGQiP8tDz34y3BxD0msaqBhjPCSAMOAZA9AcaAmxxIiA2MWJiYjg4YmQ3OTgzNGM2OTgzY2JmMWU2ODEyYjAyMg; ssid_ucp_v1=1.0.0-KGQ1YjY2YTVkNjMzNGI4NDVkNmJhY2MzZmQ2MTE5N2MzZDg0YjVjYTAKGQiP8tDz34y3BxD0msaqBhjPCSAMOAZA9AcaAmxxIiA2MWJiYjg4YmQ3OTgzNGM2OTgzY2JmMWU2ODEyYjAyMg; store-region=cn-hn; store-region-src=uid; odin_tt=7a8beb989a1b2cebc2063cc20eee35b25ccd6a70f4493c774cbbd6b0aad1635fab569b3cdc574a1be58ef8dda402e2e2; msToken=AYqmSWXsv_yeBrKu3DfQA8ZSh03EfO5irb9de4dhvJ63-xx3KUV1QCuGjby_hRMuBIgwFUTLqORG5r_TW8Ino22aFbxrfk2Fv6USOfJYa20ElB-g4XpPXp4LNha-JA==; ttwid=1%7CBeGD7rZihOMSpl_bLJl5cJBZZv3M7B4LmpAprCHzGzM%7C1700313453%7C8f22335966605ed26f192fede381632b5fb37fc4677f764e4b9616ac06606d30; _ga_QEHZPBE5HH=GS1.1.1700313454.2.0.1700313454.0.0.0; __ac_nonce=06558b97400c7a6ac76f0; __ac_signature=_02B4Z6wo00f01StmOMgAAIDCfuSzVHYcJmkrRjxAAC-Ec2; __ac_referer=https://www.toutiao.com/; _tea_utm_cache_4916=undefined; _S_IPAD=0; s_v_web_id=verify_lp42qims_2DDhkkax_3sIB_4UDU_Aqi8_0cB6NJnqH9ru; _S_WIN_WH=1055_753; _S_DPR=2.0000000596046448'
}
# 配置自己的数据库
db = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='',
    charset='utf8'
)

try:
    cursor = db.cursor()
    sqlyujv = """
        CREATE TABLE 今日头条 (
        time  varchar(255) NOT NULL,
        title VARCHAR(255) NOT NULL,
        content TEXT NOT NULL
    );
    """
    cursor.execute(sqlyujv)
except:
    print("已经存在该数据库")


def newget(url):
    count = 0
    res = requests.get(url=url, headers=headers)
    time.sleep(3)
    respond = etree.HTML(res.text)
    items = respond.xpath('/html/body//div[@class="s-result-list"]/div')
    for i in items:
        count += 1
        xpath_lujing = './/div[@class="cs-view cs-view-block cs-card"]//@data-log-extra'
        url_0 = i.xpath(xpath_lujing)
        if url_0:
            url_1 = json.loads(url_0[0])
            content_url = 'https://www.toutiao.com/article/{}/?channel=&source=news'.format(url_1["value"])
            res_0 = requests.get(url=content_url, headers=headers1)
            time.sleep(random.randint(0, 5))
            html = etree.HTML(res_0.text)
            content_0 = html.xpath(
                './/article[@class="syl-article-base tt-article-content syl-page-article syl-device-pc"]//text()')
            content = "".join(content_0)
            article_time_1 = html.xpath('.//div[@class="article-meta"]/span[1]//text()')
            article_time_2 = html.xpath('.//div[@class="article-meta"]/span[2]//text()')
            if article_time_1[0] == '首发' or article_time_1[0] == '原创':
                article_time = article_time_2[0]
            else:
                article_time = article_time_1[0]
            title = html.xpath('.//div[@class="article-content"]/h1//text()')
            insert_statement = """
                    INSERT INTO 今日头条 (time,title, content)
                    VALUES (%s, %s, %s);
                    """
            insert_data = (article_time, title, content)
            cursor.execute(insert_statement, insert_data)
            db.commit()
            print(f"正在爬取第{count}条数据")


# 关键词设置
keyword = ""
#设置爬多少页
for page in range(0, 40):
    url = ('https://so.toutiao.com/search?dvpf=pc&source=input&keyword={}}&pd=information&action_type'
           '=search_subtab_switch&page_num={}&from=news&cur_tab_title=news').format(
        keyword, page)
    newget(url)
