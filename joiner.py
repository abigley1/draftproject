# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import math

draft = pd.read_csv('/home/bigley/Desktop/springboard/Basketball_Project/draft_data.csv')
advanced = pd.read_csv('/home/bigley/Desktop/springboard/Basketball_Project/advanced_stats.csv')
totals = pd.read_csv('/home/bigley/Desktop/springboard/Basketball_Project/stat_totals.csv')
per_game = pd.read_csv('/home/bigley/Desktop/springboard/Basketball_Project/per_game_data.csv')
final = pd.read_csv('/home/bigley/Desktop/springboard/Basketball_Project/final.csv')
anthro = pd.read_csv('/home/bigley/Desktop/springboard/Basketball_Project/anthro.csv')
dups = pd.read_csv('/home/bigley/Desktop/springboard/Basketball_Project/dups.csv')


#premerge processing of 'University' coloumn
school_dict ={}
for idx in dups.index:
    college = dups['College'][idx]
    school = dups['School'][idx]
    school_dict[school] = college
final = final.replace(school_dict)

dft_final = pd.merge(draft, final, how = 'inner', left_on = ['Player', 'College'], right_on =['Player', 'School'])
dft_anth_final = pd.merge(dft_final, anthro, how='outer', left_on='Player', right_on = 'PLAYER_NAME')
dft_anth_final = dft_anth_final.set_index('Player') #merge dataframes and set index



to_drop = ['Unnamed: 0_x', 'Rk_x', 'Lg', 'Unnamed: 0_y', 'Rk_y', 'Unnamed: 0.1',
                    'Unnamed: 0', 'TEMP_PLAYER_ID', 'PLAYER_ID' , 'FIRST_NAME', 
                    'LAST_NAME', 'PLAYER_NAME', 'HAND_LENGTH', 'HAND_WIDTH', 
                    'BODY_FAT_PCT', 'POSITION', 'Pos_x', 'Pos_y', 'Born',
                    'eFG%', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%',
                    'TOV%', 'USG%', 'PProd', 'ORtg', 'DRtg',  'OWS', 'DWS',
                    'WS_y', 'OBPM', 'DBPM', 'BPM']
dft_anthro_final = dft_anth_final.drop(to_drop, axis = 1) #dropping useless columns 


year_filter = dft_anthro_final['Year'] > 2000 #eliminate players from before 2000 because that's the range of my height weight data
daf_year = dft_anthro_final[year_filter]


college_filter = daf_year['College'].notnull() 
daf_college = daf_year[college_filter] #eliminate players who didn't attend  college



#filter players who were drafted in 2001 but played in the 90se = d
filter_ = daf_college['ORB_x'].notnull()
daf_college = daf_college[filter_]


 #find players who have different schools listed from thier college stats and draft data (incorrectly merged)



daf_college.groupby(['Player', 'Season'])
daf_college.to_csv('dft_anthro_final.csv')

fgm = daf_college['FG_y']
ftm = daf_college['FT_y']
fga = daf_college['FGA_y']
fta = daf_college['FTA_y']
tttpm = daf_college['3P_y'] #three pointers made
tttpa = daf_college['3PA_y']
tpm = daf_college['2P_y']
tpa = daf_college['2PA_y']
orb = daf_college['ORB_y']
drb = daf_college['DRB_y']
trb = daf_college['TRB_y']
ast = daf_college['AST_y']
stl =daf_college['STL_y']
blk = daf_college['BLK_y']
tov = daf_college['TOV_y']
pf = daf_college['PF_y']
pts = daf_college['PTS_y']
mp = daf_college['MP_y']
rookie_year = daf_college['From']
last_year = daf_college['To']






#multiply per game stats by games played for missing totals
columns_to_replace = daf_college.columns.values[47:64]
for player in daf_college.index:
    #print(len(daf_college.loc[player]))
    if len(daf_college.loc[player]) == 73:
        print(math.isnan(daf_college.loc[player]['AST_y']))
        if math.isnan(daf_college.loc[player]['AST_y']) == True:
              print(daf_college.loc[player]['AST_y'])
              for column in columns_to_replace:   
                  oppo_col = str(column.strip('_y') + '_x')
                  print(daf_college[column].loc[player])
                  daf_college[column].loc[player] = round(daf_college[oppo_col].loc[player]*daf_college['G_y'].loc[player])
                  print(daf_college[column].loc[player])
        else:
            pass

            
      

    if len(daf_college.loc[player]) != 73:
        for i in range(len(daf_college.loc[player])):
            if math.isnan(daf_college.loc[player]['AST_y'].iloc[i]) == True:
                 for column in columns_to_replace:   
                     oppo_col = str(column.strip('_y') + '_x')
                     daf_college[column].loc[player] = round(daf_college[oppo_col].loc[player].iloc[i]*daf_college['G_y'].loc[player])
            else:
                pass
            
daf_college.groupby(['Player', 'Season'])
daf_college.to_csv('dft_anthro_final1.csv')      
            


#time to fill in some missing columns

#effective shooting %  (FG + 0.5 * 3P) / FGA

efg = (fgm + (0.5* tttpm))/fga

#trueshooting  PTS / (2 * TSA)    TSA =  FGA + 0.44 * FTA

tsa = fga + (0.44 * fta)
ts = pts/(2*tsa)

# big vs wing
 
 
 # 2 and three point shot frequency
 
two_point_frequency = tpa / fga
three_point_frequency = tttpa / fga
 
 #assist to turnover ratio
 
ast_to_tov = ast/tov
 
 #free throw to fga ratio
 
fta_to_fga = fta/fga
 
 # years in the nba
 
experience = last_year - rookie_year
 
 #power 5 confrence?
 
confs = ['PAC-12', 'Pac-10', 'ACC', 'Big 12', 'SEC', 'Big Ten']
is_power_five = {}
for conf in daf_college['Conf']:
     if conf in confs:
         is_power_five[str(conf.index)] = 'Yes'
     else:
         is_power_five[str(conf.index)] = 'No'
         
 #offensive defensive rebound split
 
orb_split = orb/trb
drb_split = drb/trb
 
 #fouls per min

fouls_per_min = pf/mp
 
 #blocks per min
 
blocks_per_min = blk/mp
 
 #steals per min
 
steals_per_min = stl/mp
 
 #years in college
 
college_years={}
for player in daf_college.index:
    if len(daf_college.loc[player]) == 95:
        college_years[player] = 1
    else:
        college_years[player] = len(daf_college.loc[player])



 #catagroicals
 
lis= [efg, ts, two_point_frequency, three_point_frequency,ast_to_tov, fta_to_fga,
       experience, orb_split, drb_split, fouls_per_min, blocks_per_min, steals_per_min]
labels = ['Effective FG%', 'True Shooting%', 'Two Point Frequency', 'Three point frequency',
          'ast-to-tov', 'fta to fga', 'NBA Experience', 'Offensive reb split', 'Defensive reb split',
          'fouls per min', 'blocks per min', 'steals per min']
df = pd.concat(lis, axis = 1)
df.columns = labels
daf_college_w_stats = pd.concat([daf_college, df], axis = 1)
daf_college_w_stats.to_csv('cleaned_data.csv')








