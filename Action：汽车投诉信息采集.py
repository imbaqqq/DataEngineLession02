"""
投诉编号，投诉品牌，投诉车系，投诉车型，问题简述，典型问题，投诉时间，投诉状态
"""
import xlrd
from xlrd import xldate_as_tuple
import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame

# url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-1.shtml'

# 请求URL
def get_page_content(request_url):
    
   

   # 得到页面的内容
   headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
   html=requests.get(request_url,headers=headers,timeout=10)
   content = html.text
   # 通过content创建BeautifulSoup对象
   soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
   return soup

#分析当前页面的投诉
def analysis(soup):
    
    temp=soup.find('div',class_='tslb_b')
    #创建Dataframe
    df=pd.DataFrame(columns=['id','brand','car_model','type','desc','problem','datetime','status'])
    tr_list=temp.find_all('tr')
    for tr in tr_list:
        
        #提取汽车投诉信息
        temp={}
        td_list=tr.find_all('td')
        #第一个tr没有td,其余都有8个td
        if len(td_list)>0:
            
            
            id,brand,car_model,type,desc,problem,datetime,status=td_list[0].text,td_list[1].text,td_list[2].text,td_list[3].text,td_list[4].text,td_list[5].text,td_list[6].text,td_list[7].text
            #放到DateFrame中
            temp['id'],temp['brand'],temp['car_model'],temp['type'],temp['desc'],temp['problem'],temp['datetime'],temp['status']=id,brand,car_model,type,desc,problem,datetime,status
            df=df.append(temp,ignore_index=True)
    return df

#df=analysis(soup)
#print(df)

page_num=20
base_url='http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-0-0-0-0-0-'
result=pd.DataFrame(columns=['id','brand','car_model','type','desc','problem','datetime','status'])
for i in range(page_num):
    request_url=base_url+str(i+1)+'.shtml'
    soup=get_page_content(request_url)
    df=analysis(soup)
    print(df)
    result=result.append(df)
result.to_excel('汽车质量投诉 - 车质网1.xlsx')
    




















