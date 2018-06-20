#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 13:46:34 2018

@author: bigley
"""

import pandas as pd
import time


url_main = 'https://www.basketball-reference.com/play-index/draft_finder.cgi?request=1&year_min=1992&college_id=0&pos_is_g=Y&pos_is_gf=Y&pos_is_f=Y&pos_is_fg=Y&pos_is_fc=Y&pos_is_c=Y&pos_is_cf=Y&order_by=ws&offset='
offsets = range(0,1500, 100)
all_data =  []#initalize url and offsets
start_time = time.clock()
counter = 0
for offset in offsets:  #loop to create all of the needed URLS
       loop_start_time = time.clock()
       url = url_main+str(offset) 
       df_l = pd.read_html(url, header=1)
       if counter%10 == 0:
           print('read time =' +str(time.clock() - loop_start_time))#read URL
       df = df_l[0] #transoform from list to dataframe
       drop = [] #create place to store rows to remove
       PLAYER = df['Player']
       LG = df['Lg']
       start = time.clock()
       for i in range(len(df)):
           if PLAYER[i] == 'Player' or PLAYER[i] == 'Totals' or PLAYER[i] == 'Per Game' or PLAYER[i] == 'Shooting' or PLAYER[i] == 'Advanced' or LG[i] == 'Per Game':
              drop.append(i) #store rows with extra header info             #drop extra rows 
       all_data.append(df.drop(drop)) #add data to list
       time.sleep(.10)
       if counter%10 == 0:
           print('I have scraped up to offset =' + str(offset))
       counter = counter+1
all_data_f = pd.concat(all_data) #take all data frames from list and combine into one dataframe
all_data_f.to_csv('draft_data.csv')
print('Total ex time:' + str(time.clock()-start_time)) 
    
    
           
           
       
