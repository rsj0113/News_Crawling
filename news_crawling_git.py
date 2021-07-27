# %%
pip install feedparser
# %%
pip install konlpy
# %%
import pandas as pd
import numpy as np
import feedparser
from bs4 import BeautifulSoup as bs
import urllib
import urllib.request as req
import requests
from konlpy.tag import Kkma, Okt, Komoran
okt = Okt()
from konlpy.utils import pprint
import warnings
warnings.filterwarnings("ignore")

def Crawling(keyword, date, date2):
  keyword = '+'.join(keyword.split(' '))

  last = False
  page_num = 1

  ds = date
  de = date2

  href_list = []   # 기사 주소가 들어갈 리스트
  TitDesc_list = []   # 제목 + 요약 내용 리스트
  title_list = []   # 제목 리스트

  while last == False:
      url = "https://search.naver.com/search.naver?&where=news&query={0}&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=3&ds={1}&de={2}&docid=&nso=so:r,p:,a:all&mynews=1&cluster_rank=238&start={3}&refresh_start=0".format(keyword,ds,de,str(page_num))
      # print(url)
      raw = requests.get(url)
      html = raw.content
      soup = bs(html, 'html.parser')

      tit_list = soup.find_all('a', {'class':'news_tit'})

      for tit in tit_list:
          try:
              title_list.append(tit['title'])
              # print(tit['title'])
          except AttributeError:
              pass

      # 마지막 페이지 주소 확인 (다음페이지 버튼이 없으면 종료페이지로 간주)
      if soup.find('a',  {'class':'btn_next'})['aria-disabled'] == 'false' and page_num < 100:
        page_num += 10
      else : 
        print(page_num)
        last = True
      
  title_df = pd.DataFrame(title_list)
  title_df['회사'] = keyword
  title_df.columns = [['뉴스','회사']]

  nm = "/Users/seonjin/ColabProjects/live_2018_4/new_title_{0}_{1}_{2}.csv".format(keyword, date, date2)
  print(nm)
  title_df.to_csv(nm, encoding='utf-8-sig')

  # return title_df

# %%
# company 파일 반입
import pandas as pd
comp_live = pd.read_excel("data_company_2018.xlsx", engine = 'openpyxl')
# %%
comp_list = comp_live[['회사명']][1775:]
comp_list.reset_index(inplace = True)
comp_list
# %%
for i in range(len(comp_list)):
  Crawling(comp_list['회사명'][i], '2018.07.01','2018.12.31')
