#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

@author: MZZheng
"""
import pandas as pd
import vk

inwords = 'keyword1, keyword2,...'       # input keywords
low_inwords = inwords.lower()
session = vk.AuthSession(app_id='6709861', user_login='Your user ID', user_password='Your password')
api = vk.API(session)
qwords = low_inwords.split(",")
communities = []

for keywords in qwords:    
    data = api.groups.search(q=keywords ,version = 5.92, count = 1000)
    n_comu = data[0] - 1
    del data[0]
    print ('%d communities are found for keywords %s' %(n_comu, keywords))
    communities.extend(data)
    
df = pd.DataFrame(communities)
df.drop_duplicates(subset=['gid'], keep='first', inplace = True)    

print( 'Total %d unique communities are found' % len(df))
g_list = list(df['gid'])
dataframe = pd.DataFrame({'gid':g_list})
dataframe.to_csv('communities_list.csv')

