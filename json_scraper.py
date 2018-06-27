#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 13:29:46 2018

@author: bigley
"""
import json
import csv
import sys
import requests
import pandas as pd

url = 'https://stats.nba.com/stats/draftcombineplayeranthro?LeagueID=00&SeasonYear='
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
years = ('2000-01', '2001-02', '2002-03', '2003-04', '2004-05', '2005-06', '2006-07', '2007-08', '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14','2014-15', '2015-16', '2016-17', '2017-18', '2018-19')
all_data = []
for year in years:
    response = requests.get(url+year, headers = headers)
    json_data = response.json()
    #print(json_data)
    data = response.text
    json_headers = json_data["resultSets"][0]["headers"] #these are the headers
    json_players = json_data["resultSets"][0]["rowSet"] #these are the cases
    df = pd.DataFrame(json_players, columns = json_headers)
    all_data.append(df)
all_data_f = pd.concat(all_data) #take all data frames from list and combine into one dataframe
all_data_f.to_csv('anthro.csv')