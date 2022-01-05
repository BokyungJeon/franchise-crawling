
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os


def check_file(file_name):
    print('check file')
    if os.path.isfile(file_name):
        _result_df = pd.read_excel(file_name)
        _start = len(_result_df)
        print(f'start: {_start}')
    else:
        columns = ['상호', '영업표지', '대표자', '업종', '법인설립등기일', '사업자등록일', '대표번호', '대표팩스번호', '등록번호', '최초등록일', '최종등록일',
                   '주소', '사업자유형', '법인등록번호', '사업자등록번호', '연도', '전체', '가맹점수', '직영점수']
        _result_df = pd.DataFrame(columns=columns)
        _start = 0
    return _result_df, _start


def crawling_body(result_df, start):
    df = pd.read_csv(f'url_9386_220105.csv')
    urls = df['url']
    count = 0
    end = 11739

    try:
        for url in urls[start:end]:
            body_result = requests.get(url)
            body_soup = BeautifulSoup(body_result.text, "html.parser")
            tables = body_soup.find_all("table")
            # print(tables[0])
            result_list = []

            # '상호', '영업표지', '대표자', '업종', '법인설립등기일', '사업자등록일', '대표번호', '대표팩스번호', '등록번호', '최초등록일', '최종등록일',
            tds = tables[0].find("tbody").find_all("td")
            # print(tds)
            for i in range(11):
                # print(tds[i].text.replace(" ", ""))
                text = tds[i].text
                text = re.sub(r'\s', '', text)
                if i == 0:
                    text = text.strip('상호')
                elif i == 1:
                    text = text.strip('영업표지')
                elif i == 2:
                    text = text.strip('대표자')
                # print(text)
                # print('------------_')
                result_list.append(text)

            # '주소', '사업자유형', '법인등록번호', '사업자등록번호',
            tds = tables[1].find("tbody").find_all("td")
            # print(tds)
            for i in range(4):
                text = tds[i].text
                text = re.sub(r'\s', '', text)
                # print(text)
                # print('-------------')
                result_list.append(text)

            # '연도'
            year = tables[6].find("th", {"class": "listOfCntShow"}).text
            year = re.sub(r'\s', '', year)
            result_list.append(year)
            # '전체', '가맹점수', '직영점수'
            tbody = tables[6].find("tbody")
            tds = tbody.find_all("td", {"class": "listOfCntShow"})
            for i in range(3):
                text = tds[i].text
                text = re.sub(r'\s', '', text)
                # print(text)
                result_list.append(text)

            result_df.loc[result_df.shape[0]] = result_list
            count += 1
            if count % 50 == 0:
                print(count)

    except Exception as e:
        print(e.args)
        raise

    except KeyboardInterrupt as e:
        print(e)

    finally:
        print(count)
        print('len', len(result_df))
        result_df.to_excel(f'result_220105.xlsx', index=False)
        # result_df.to_excel(f'result_{start}_{len(result_df)}_{count}_220105.xlsx')


if __name__ == '__main__':
    file_name = 'result_220105.xlsx'
    result_df, start = check_file(file_name)
    crawling_body(result_df, start)





