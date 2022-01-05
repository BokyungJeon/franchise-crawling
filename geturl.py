import requests
from bs4 import BeautifulSoup
from html_table_parser import parser_functions as parser # beautifulsoup 4.4.1버전 (konlpy 0.5.2는 beautifulsoup4 4.6.0필요)
import pandas as pd
import re
import csv


tags_list = []
url_list = []
for i in range(41):
    url = f'https://franchise.ftc.go.kr/mnu/00013/program/userRqst/list.do?searchCondition=&searchKeyword=&column=brd&selUpjong=21&selIndus=&pageUnit=300&pageIndex={i}'
    result = requests.get(url)
    # print(result.text)
    soup = BeautifulSoup(result.text, "html.parser")
    result_a = soup.find_all("a", {"class": "authCtrl"})
    # print(len(result_a)) # 600개. 2개씩 중복됨. 😑
    for a in result_a:
        tag = a['onclick']
        result_tag = re.sub(r'[a-zA-Z\/\.\?\=\(\)\'\_\;]', repl='', string=tag)
        result_tag = result_tag[5:]
        if result_tag not in tags_list:
            tags_list.append(result_tag)
            url_list.append(f'https://franchise.ftc.go.kr/mnu/00013/program/userRqst/view.do?firMstSn={result_tag}')
    print(len(tags_list))

df = pd.DataFrame(zip(tags_list, url_list), columns=['tag', 'url'])
print(df)

df.to_csv(f'url_{len(df)}_220105.csv')

