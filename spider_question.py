import requests
import time
import pandas as pd
import os 
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
import random
import openpyxl as op
import math
import xlwt
import numpy as np
import pandas as pd

def trans_date(v_timestamp):
    """10位时间戳转换为时间字符串"""
    timeArray = time.localtime(v_timestamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

def zhihuanswers(qid):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    params={
        'include':'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,attachment,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,is_labeled,paid_info,paid_info_content,reaction_instruction,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_recognized;data[*].mark_infos[*].url;data[*].author.follower_count,vip_info,badge[*].topics;data[*].settings.table_of_content.enabled',
        'limit':'5',
        'offset': '0',
        'order': 'default',
        'platform':'desktop',
    }
#     url0='https://www.zhihu.com/question/'+str(qid)
#     r0=requests.get(url0,headers=headers)
#     soup=BeautifulSoup(r0.content,'lxml').encode('utf-8').decode("unicode_escape")
#     pattern=re.compile('"next":"(https://www.zhihu.com/api/v4/questions/.*_id=\d+)"')
#     url=re.findall(pattern,soup)[0]#6开始
    
    #开头前5回答
    urlstart='https://www.zhihu.com/api/v4/questions/'+str(qid)+'/feeds?'
    datas=requests.get(urlstart, headers=headers,params=params).json()
    
    allinfo=[]
    #创建要写入的excel
    tableTitle = ['作者名', '性别', '作者简介', 'medal','认证', 'url','提问者是否正关注', '提问者是否关注过','followers', '问题id', 
                          '问题创建时间', '问题修改时间','回答id', '提问者是否谢过', '回答创建时间', '回答更新时间','点赞数', '评论数',
                          '感谢数', '内容','内容图片']

    df=pd.DataFrame(columns=tableTitle)
    for info in datas['data']:

        #作者信息
        name=info['target']['author']['name']
        gender=info['target']['author']['gender']
        biaoqian=info['target']['author']['headline']
        try:
            medal=info['target']['author']['exposed_medal']['description']
        except:
            medel=''
        badge=info['target']['author']['badge_v2']['title']
        url='zhihu.com/'+info['target']['author']['user_type']+'/'+info['target']['author']['url_token']
        isfollowing=info['target']['author']['is_following']
        isfollowed=info['target']['author']['is_followed']
        followers=info['target']['author']['follower_count']
        
        #问题信息
        questionid=info['target']['question']['id']
        question_created_time=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(info['target']['question']['created']))
        question_update_time=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(info['target']['question']['updated_time']))
        #回答信息
        answerid=info['target']['id']
        author_thanked=info['target']['relationship']['is_thanked']
        createdtime=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(info['target']['created_time']))
        updatetime=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(info['target']['updated_time']))
        dianzan=info['target']['voteup_count']
        comment=info['target'][ 'comment_count']
        thanka_count=info['target'][ 'thanks_count']
        content=BeautifulSoup(info['target']['content']).text
        try:
            image=[x['data-original'] for x in BeautifulSoup(info['target']['content']).find_all('img')]
        except:
            image=''
        #写入
        oneinfo = [name,gender,biaoqian,medal,badge,url,isfollowing,isfollowed,followers,questionid,question_created_time,question_update_time,
                  answerid,author_thanked,createdtime,updatetime,dianzan,comment,thanka_count,content,image]
        df.loc[len(df)+1]=oneinfo
        #allinfo.append(oneinfo)
    next_url = datas['paging']['next']
#     for t in allinfo:
#         ws.append(t)
    
    
    #time.sleep(random.uniform(1.1,2.2))
    
    for j in tqdm(range(2000)):
        datas=requests.get(next_url,headers=headers).json()
        for info in datas['data']:
            #作者信息
            name=info['target']['author']['name']
            gender=info['target']['author']['gender']
            biaoqian=info['target']['author']['headline']
            try:
                medal=info['target']['author']['exposed_medal']['description']
            except:
                medel=''
            badge=info['target']['author']['badge_v2']['title']
            url='zhihu.com/'+info['target']['author']['user_type']+'/'+info['target']['author']['url_token']
            isfollowing=info['target']['author']['is_following']
            isfollowed=info['target']['author']['is_followed']
            followers=info['target']['author']['follower_count']

            #问题信息
            questionid=info['target']['question']['id']
            question_created_time=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(info['target']['question']['created']))
            question_update_time=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(info['target']['question']['updated_time']))
            #回答信息
            answerid=info['target']['id']
            author_thanked=info['target']['relationship']['is_thanked']
            createdtime=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(info['target']['created_time']))
            updatetime=time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(info['target']['updated_time']))
            dianzan=info['target']['voteup_count']
            comment=info['target'][ 'comment_count']
            thanka_count=info['target'][ 'thanks_count']
            content=BeautifulSoup(info['target']['content']).text
            try:
                image=[x['data-original'] for x in BeautifulSoup(info['target']['content']).find_all('img')]
            except:
                image=''
            #写入
            oneinfo = [name,gender,biaoqian,medal,badge,url,isfollowing,isfollowed,followers,questionid,question_created_time,question_update_time,
                      answerid,author_thanked,createdtime,updatetime,dianzan,comment,thanka_count,content,image]
            df.loc[len(df)+1]=oneinfo
            #allinfo.append(oneinfo)
        next_url = datas['paging']['next']
#         for t in allinfo:
#             ws.append(t)
            
        time.sleep(random.uniform(1.1,2.2))
        
        if datas['paging']['is_end']:
            print('到底了')
            #wb.save(str(qid)+'.xlsx')
            df.to_csv(str(qid)+'.csv',index=0,encoding='utf_8_sig')
            return 
        
    print('1w回答了')
    #wb.save(str(qid)+'.xlsx')
    df.to_csv(str(qid)+'.csv',index=0,encoding='utf_8_sig')
    return 

if __name__ == '__main__':
    zhihuanswers(634072760)
