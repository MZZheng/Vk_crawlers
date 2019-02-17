#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

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
users_dir = output_dir + "Users_Data/"


if not os.path.exists(d_year):
    os.mkdir(d_year)
    
if not os.path.exists(d_month):
    os.mkdir(d_month)
    
if not os.path.exists(d_day):
    os.mkdir(d_day)
    
if not os.path.exists(users_dir):
    os.mkdir(users_dir)

###################################starts here#################################
def getuserinfo(user_id):
    try:
        time.sleep(randint(7,10) + random.uniform(0,1))
        user_info = api.users.get(user_ids = user_id, version = 5.92, fields = 'verified,sex,bdate,city,country,education,followers_count,counters,occupation,personal,activities,interests,music,movies,tv,book,games,quotes')
        return user_info
    except VkAPIError as error:
        if str(error).startswith('6'):
            print ("SLEEPING FOR 5 MINUTES TO RESET NETWORK CONNECTION")
            sleep(5*60)
            return getuserinfo(user_id)
        else:
            user_info = [{}]
            return user_info
    except:
        print ("SLEEPING FOR 5 MINUTES TO RESET NETWORK CONNECTION")
        sleep(5*60)
        return getuserinfo(user_id)
		
def getfriend(userid):
    try:
        time.sleep(randint(7,10) + random.uniform(0,1))
        friend = api.friends.get(user_id = userid, version = 5.92)
        return friend
    except VkAPIError as error:
        if str(error).startswith('6'):
            print ("SLEEPING FOR 5 MINUTES TO RESET NETWORK CONNECTION")
            sleep(5*60)
            return getfriend(userid)
        else:
            friend = []
            return friend
    except:
        print ("SLEEPING FOR 5 MINUTES TO RESET NETWORK CONNECTION")
        sleep(5*60)
        return getfriend(userid)
        
def getfollower(userid):
    try:
        time.sleep(randint(7,10) + random.uniform(0,1))
        followers = api.users.getFollowers(user_id = userid, version = 5.92,count = 1000)
        items = followers['items']
        count = followers['count']
        return items, count
    except VkAPIError as error:
        if str(error).startswith('6'):
            print ("SLEEPING FOR 5 MINUTES TO RESET NETWORK CONNECTION")
            sleep(5*60)
            return getfollower(userid)
        else:
            items = ''
            count = 0
            return items, count
    except:
        print ("SLEEPING FOR 5 MINUTES TO RESET NETWORK CONNECTION")
        sleep(5*60)
        return getfollower(userid)
        
def getpost(userid):
    try:
        time.sleep(randint(7,10) + random.uniform(0,1))
        post = api.wall.get(owner_id = userid, version = 5.92,count = 100)
        return post
    except VkAPIError as error:
        if str(error).startswith('6'):
            print ("SLEEPING FOR 5 MINUTES TO RESET NETWORK CONNECTION")
            sleep(5*60)
            return getpost(userid)
        else:
            post = [0]
            return post
    except:
        print ("SLEEPING FOR 5 MINUTES TO RESET NETWORK CONNECTION")
        sleep(5*60)
        return getpost(userid)
###############################################################################
    
data = pd.read_csv("users_list.csv")
user_IDs = list(data['users'])
users_data = []
#user_IDs = user_IDs[0:4] #for test only
#print(user_IDs)
for i in user_IDs:
    print('collecting user id %d information' %i)
    user_info = getuserinfo(i)
        
    friends = getfriend(i)
    user_info[0]['friends_list'] = friends
    user_info[0]['firends_count'] = len(friends)
    
    item,count = getfollower(i)
    user_info[0]['followers_list'] = item
    user_info[0]['followers_count'] = count
    
        
    post = getpost(i)
    user_info[0]['num_posts'] = post[0]
    
    if len(post) > 1:
        post_df = pd.DataFrame(post[1:])
        post_filename = users_dir + str(i) + '_post.xlsx'
        post_df.to_excel(post_filename)
    
    users_data.append(user_info[0])
    
df = pd.DataFrame(users_data)
df.drop_duplicates(subset=['uid'], keep='first', inplace=True)
excel_file = output_dir + 'users.xlsx'
df.to_excel(excel_file)

print (start_time)
print (str(datetime.datetime.now()))
    