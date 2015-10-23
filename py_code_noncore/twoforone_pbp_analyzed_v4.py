# nba two-for-one shot analysis, version 2 / run multiple teams at once / do report

# v4 -- do import only
# run base stats separately

# separate out per-team calculations
# run - per-minute efg calcs

# ------------------------------------------------------------------------

import os.path

import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv
from urllib import urlopen

import pandas as pd
import pickle

# ------------------------------------------------------------------------

# New folder: pynba-tfo

filepath = r'c://Users/Marc/Documents/pynba-tfo/Hou_pbp_fga_x1.csv'
#filepath = r'c://Users/Marc/Documents/pynba-tfo/PHI_pbp_fga_x1.csv'
#filepath = r'c://Users/Marc/Documents/pynba-tfo/LAC_pbp_fga_x1.csv'
#filepath = r'c://Users/Marc/Documents/pynba-tfo/MIA_pbp_fga_x1.csv'
#filepath = r'c://Users/Marc/Documents/pynba-tfo/ATL_pbp_fga_x1.csv'
#filepath = r'c://Users/Marc/Documents/pynba-tfo/GSW_pbp_fga_x1.csv'
#filepath = r'c://Users/Marc/Documents/pynba-tfo/MEM_pbp_fga_x1.csv'
#filepath = r'c://Users/Marc/Documents/pynba-tfo/SAS_pbp_fga_x1.csv'
#filepath = r'c://Users/Marc/Documents/pynba-tfo/CLE_pbp_fga_x1.csv'
#filepath = r'c://Users/Marc/Documents/pynba-tfo/LAL_pbp_fga_x1.csv'
filepath = r'c://Users/Marc/Documents/pynba-tfo/NYK_pbp_fga_x1.csv'
filepath = r'c://Users/Marc/Documents/pynba-tfo/CHI_pbp_fga_x1.csv'

# filename handling, for running on multiple teams at once
filepre = "c://Users/Marc/Documents/pynba-tfo/data_in/"
filepost = "_pbp_fga_x1.csv"
teamnames = ['HOU', 'PHI', 'LAC', 'MIA', 'ATL', 'GSW', 'MEM', 'SAS', 'CLE', 'LAL', 'NYK', 'CHI']

#drop LAL and NYK bc do they really play basketball?
teamnames = ['HOU', 'PHI', 'LAC', 'MIA', 'ATL', 'GSW', 'MEM', 'SAS', 'CLE', 'CHI']

#playoff teams
teamnames = ['ATL', 'BOS', 'CHI', 'CLE',  'DET', 'GSW', 'HOU', 'IND', 'LAC', 'MEM', 'MIL',
     'NOP', 'POR', 'SAS', 'TOR', 'WAS']  

# All 30 teams
teamnames = ['ATL', 'BOS', 'BRK', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL',
    'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']   
    
# note: for some reason CHA named CHO in orig data

for tn in teamnames:
    print os.path.normpath(filepre + tn + filepost)
    

df = read_csv(filepath)



#get sec assumes only minutes and seconds passed in / no hours
def getSec(s):
    """ Converts min:sec Time into Total Seconds.
    ie, '1:23:45' into something like 83 seconds. Returns numeric."""
    l = s.split(':')
    return float(int(l[0]) * 60 + float(l[1]))

print getSec('1:23:45')
print getSec('0:04:15.2')
print getSec('0:00:25.5')

# parse out make/miss result from pbp log  

def parseMake(s):
    """ Parses out shot description information from the descriptive text in dataset.
    Identifies Made Shots and Missed Shots."""
    isMake = s.find("makes")
    isMiss = s.find("misses")
    result = -1
    if isMake > 0: result = 1
    if isMiss > 0: result = 0
    return result

# eg... 25 ft shot... 2pt, 3pters
def parseShotTypeDistance(s):
    """ Parses out shot description information from the descriptive text in dataset."""
    
    fgatype = -1
    distance = -1
    a = s.split("from")
    # if it's blocked at rim, handle differently
    if len(a) == 1:
        a = s.split("shot")
        distance = 0 # at rim
        fgatype = int(a[0].split()[-1].split("-")[0])
    else:
        distance = int(a[1].split()[0])
        fgatype = int(a[0].split()[-2].split("-")[0])
    
    return fgatype, distance

# eg... 25 ft shot... 2pt, 3pters
def parseShotTypeDistancePlayer(s):
    """ Parses out shot description information from the descriptive text in dataset.
    Includes Shottype (2pt, or 3pt), Distance (ft), Name of Shooter."""
    
    fgatype = -1
    distance = -1
    s2 = s.split()
    player = s2[0]+s2[1]
    
    a = s.split("from")
    # if it's blocked at rim, handle differently
    if len(a) == 1:
        a = s.split("shot")
        distance = 0 # at rim
        fgatype = int(a[0].split()[-1].split("-")[0])
    else:
        distance = int(a[1].split()[0])
        fgatype = int(a[0].split()[-2].split("-")[0])
    
    return fgatype, distance, player
    
def epochTime_orig(t):
    epoch = -1
    if 180 > t >= 60: epoch = 5
    if 60 > t >= 36: epoch = 4
    if 36 > t >= 27: epoch = 3
    if 27 > t >= 5: epoch = 2
    if 5 > t  >= 0: epoch = 1    
    return epoch
    
    
def epochTime(t):
    """ Partitions Time of Shot into different Regions of Interest (ie, chunks time)."""
    epoch = -1
    if 180 > t >= 65: epoch = 5
    if 65 > t >= 36: epoch = 4
    if 36 > t >= 27: epoch = 3
    if 27 > t >= 5: epoch = 2
    if 5 > t  >= 0: epoch = 1    
    return epoch
    
# use alt epochs to get a nicer shaped cloud in the scatter, clearer trend possibly.
def epochTime_alt(t):
    """ Partitions Time of Shot into different bins; uses alternate time cutoffs."""
    epoch = -1
    if 180 >= t >= 65: epoch = 5
    if 65 > t >= 37: epoch = 4
    if 37 > t >= 27: epoch = 3
    if 27 > t >= 5: epoch = 2
    if 5 > t  >= 0: epoch = 1    
    return epoch
    
def epochTime_wide(t):
    """ Partitions Time of Shot into different bins; uses alternate (wider) time cutoffs."""
    epoch = -1
    if 180 > t >= 90: epoch = 5
    if 90 > t >= 45: epoch = 4
    if 45 > t >= 25: epoch = 3
    if 25 > t >= 5: epoch = 2
    if 5 > t  >= 0: epoch = 1    
    return epoch
    
# ----------------------------------------------------------------

# for all teams in set / make a dataframe df and do pbp (play by play) analysis 

bigdf = pd.DataFrame()

for tn in teamnames:
    filepath = os.path.normpath(filepre + tn + filepost)
    print "reading... ", filepath

    df = read_csv(filepath)

    # Do work , convert string timestamps to float values
    
    array_out = [getSec(temp) for temp in df.Time]
    df['Time2'] = array_out
    
    #df["Time2"].hist(bins=100)
    
    df2 = df[df["Time2"] < 180]
    df2 = df2[df2["Qtr"] != "4th" ]
    df2 = df2[df2["Qtr"] != "OT" ]
    df2 = df2[df2["Qtr"] != "2OT"] 

    #qtrs_check = unique(df2.Qtr)
    #print qtrs_check

    df2["MakeMiss"] = [parseMake(temp) for temp in df2.Description]
    
    # pick which method to bin epochs with epochTime or epochTime_alt
    df2["epoch"] = [epochTime(s) for s in df2.Time2]

    shotTypeDists = [parseShotTypeDistancePlayer(s) for s in df2.Description]
    fgatypes = [s[0] for s in shotTypeDists]
    shotdistances = [s[1] for s in shotTypeDists]
    players = [s[2] for s in shotTypeDists]
    
    # add back in the new calculated variables as columns in the dataframe
    
    df2["shottype"] =  fgatypes
    df2["distance"] = shotdistances
    df2["shooter"] = players
    
    points = df2.MakeMiss * df2.shottype
    df2["points"] = points

    # filter out full court heaves
    
    df2 = df2[df2["distance"] < 40] # approx 2-3% of a dataset
    
    # done with basic shot analysis
    
    # collect per-team datasets into one big dataset (bigdf) of all teams
    
    bigdf = bigdf.append(df2)
    
    print "length of big df: ", len(bigdf)
    
 
# ------------------------------------------
 
# Save all teams dataset to pickle file
outfilename = 'shots_allteams.pik'
pickle.dump(bigdf, open(outfilename, 'wb'))

# ------------------------------------------

# basic quality check: 
# Print out # records
# Print out number of teams read in

print 'Number of records read in: ', len(bigdf)
print 'Number of teams: ', len(pd.unique(bigdf['Tm']))

# ------------------------------------------





    