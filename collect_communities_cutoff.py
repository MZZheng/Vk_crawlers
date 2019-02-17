#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Free access
@author: MZZheng
"""

import pandas as pd
import vk
from vk.exceptions import VkAPIError
import random
from random import randint
import os
import datetime
import time
from time import sleep

start_time = str(datetime.datetime.now())

session = vk.AuthSession(app_id='6709861', user_login='Your user ID', user_password='Your password')
api = vk.API(session)

current_time = time.strftime("%H_%M_%S")
current_day = time.strftime("%d")
current_month = time.strftime("%m")
current_year = '20' + time.strftime("%y")
current_date = time.strftime("%D")



home_dir = './'

	
d_year = home_dir + current_year
d_month = home_dir + current_year + "/" + current_month
d_day = home_dir + current_year + "/" + current_month + "/" + current_day
output_dir = home_dir + current_year + "/" + current_month + "/" + current_day + '/'
groups_dir = output_dir + "Communities_Data/"


if not os.path.exists(d_year):
    os.mkdir(d_year)
    
if not os.path.exists(d_month):
    os.mkdir(d_month)
    
if not os.path.exists(d_day):
    os.mkdir(d_day)
    
if not os.path.exists(groups_dir):
    os.mkdir(groups_dir)


############################start from here####################################

def getgroupinfo(group_id):
    try:
        time.sleep(randint(7,10) + random.uniform(0,1))
        group_info = api.groups.getById(group_ids = group_id, version = 5.92, fields = 'contacts,counters,description,links,members_count')
        return group_info
    except VkAPIError as error:
        if str(error).startswith('6'):
            print ("SLEEPING FOR 5 MINUTES TO RESET NETWORK CONNECTION")
            sleep(5*60)
            return getgroupinfo(group_id)
        else:
            group_info = [{}]
            return group_info
    except:
        print ("SLEEPING FOR 5 MINUTES TO RESET NETWORK CONNECTION")
        sleep(5*60)
        return getgroupinfo(group_id)

def getgroupid(group_id):
    try:
        time.sleep(randint(7,10) + random.uniform(0,1))
        group_info = api.groups.getById(group_ids = group_id, version = 5.92)
        g_id = group_info[0]['gid']
        return g_id
    except VkAPIError as error:
        if str(error).startswith('6'):
            print ("SLEEPING FOR 5 MINUTES TO RESET NETWORK CONNECTION")
            sleep(5*60)
            return getgroupid(group_id)
        else:
            g_id = ''
            return g_id
    except:
        print ("SLEEPING FOR 5 MINUTES TO RESET NETWORK CONNECTION")
        sleep(5*60)
        return getgroupid(group_id)
    
def getmember(groupid):
    try:
        time.sleep(randint(7,10) + random.uniform(0,1))
        mem = api.groups.getMembers(group_id = groupid, version = 5.92)
        return mem
    except VkAPIError as error:
        if str(error).startswith('6'):
            print ("SLEEPING FOR 5 MINUTES TO RESET NETWORK CONNECTION")
            sleep(5*60)
            return getmember(groupid)
        else:
            mem = []
            return mem
    except:
        print ("SLEEPING FOR 5 MINUTES TO RESET NETWORK CONNECTION")
        sleep(5*60)
        return getmember(groupid)
        
def getpost(groupid):
    try:
        time.sleep(randint(7,10) + random.uniform(0,1))
        post = api.wall.get(owner_id = -groupid, version = 5.92,count = 100)
        return post
    except VkAPIError as error:
        if str(error).startswith('6'):
            print ("SLEEPING FOR 5 MINUTES TO RESET NETWORK CONNECTION")
            sleep(5*60)
            return getpost(groupid)
        else:
            post = [0]
            return post
    except:
        print ("SLEEPING FOR 5 MINUTES TO RESET NETWORK CONNECTION")
        sleep(5*60)
        return getpost(groupid)
###############################################################################

data = pd.read_csv("communities_list.csv")
comu_IDs = list(data['gid'])
flag = 20 * len(comu_IDs)
communities_data = []
user_list = set()
#comu_IDs = comu_IDs [0:1] # for test only
print(comu_IDs)


for i in comu_IDs:
    
    print('collecting community id %d information' %i)
    
    group_info = getgroupinfo(i)    
    keys = list(group_info[0].keys())
    if 'links' in keys:
        link_groups = group_info[0]['links']
        g_links_gid = []
        for gps in link_groups:
            url_str = gps['url']
            if url_str.startswith('https://vk.com/'):
                s_name = url_str.split('/')[-1]
            else:
                s_name = ''
            
            if len(s_name) > 0:
                g_id = getgroupid(s_name)
            else:
                g_id = ''
            if (g_id not in comu_IDs) and (len(comu_IDs) <= flag):
                comu_IDs.append(g_id)
                
            g_links_gid.append(g_id)
    else:
        g_links_gid = ''
    group_info[0]['links_gid'] = g_links_gid
        
    mem = getmember(i)    
    group_info[0]['members_list'] = mem
    if len(mem) > 0:
        user_list = user_list.union (set (mem['users']))
    else:
        user_list = user_list
    
    post = getpost(i)
    group_info[0]['num_posts'] = post[0]
    if len(post) > 1:
        post_df = pd.DataFrame(post[1:])
        post_filename = groups_dir + str(i) + '_post.xlsx'
        post_df.to_excel(post_filename)

    communities_data.append(group_info[0])
        
df = pd.DataFrame(communities_data)
df.drop_duplicates(subset=['gid'], keep='first', inplace=True)
df = df.drop(['photo','photo_medium'],axis = 1)
excel_file = output_dir + 'communities.xlsx'
df.to_excel(excel_file)

g_list = list(df['gid'])
dataframe_g = pd.DataFrame({'gid':g_list})
dataframe_g = dataframe_g.dropna(subset=["gid"])
dataframe_g.to_csv('communities_list.csv')

u_list = list(user_list)
dataframe = pd.DataFrame({'users':u_list})
dataframe.to_csv('users_list.csv')       


print (start_time)
print (str(datetime.datetime.now()))

