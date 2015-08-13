

# get dataset of top 100 shooters for further TFO analysis / 

import os.path

import numpy as np
from scipy.stats.stats import pearsonr   

import matplotlib.pyplot as plt
from pandas import read_csv
from urllib import urlopen

import pandas as pd
import pickle

import math


# -----------------------------------------------------------------------------

# Some prepatory basics

# All 30 teams
teamnames = ['ATL', 'BOS', 'BRK', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL',
    'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']   

# read in pickle file data from prev
outfilename = 'shots_allteams.pik'
bigdf = pickle.load(open(outfilename, 'rb'))

# -----------------------------------------------------------------------------


# pre:: bigdf exists / df of all shots / 
# post: limited to top 100 players, still per shot data

# Make pivot table, group by player (shooter), to get an idea of what's going on at epochs.
pivoted = bigdf.pivot_table(rows=['shooter'], cols=['epoch'], values='MakeMiss', fill_value=0)


print pivoted.head()
#bc this gets the columsn apparently.. problems bc not strings
pivoted['diff'] = pivoted[3]-pivoted[5]

print pivoted.head()

# pivoted data types not really used, was simpler to use diff data manipulations (for reconstruction, merging back together series, etc)

# ------------


# print histogram of all shots, all teams, last 3 min

plt.figure(1)
#ax = bigdf["Time2"].hist(bins = 62, range=[0, 61])
ax = bigdf["Time2"].hist(bins = 180, range=[0, 180])

ax.set_ylabel('Number of Shot Attempts')     #('Count of FGA')
ax.set_xlabel('Time Remaining in Quarter (s)')

ax.set_title('Distribution of Field Goal Attempts At End of Quarters \n All Teams ')
#ax.set_title('When Shots Happen At End of Quarters')    

ax.set_xlim([-0.5, 60.5])        
ax.set_xlim([-0.5, 58.5])

# ax.set_xlim([-0.5, 179]) 

plt.show()

#weird blip in data at ~ 59 seconds, 60 seconds


# -----------------------------------------------------------------

# filter down bigdf to only include top100 shooters... because don't care about plyrs who don't shoot
# grab keys,index from activeshooters or something

# Set filters, for Regions of Interest (epochs 3 and 5)
filter_epoch3 = bigdf["epoch"]==3
filter_epoch5 = bigdf["epoch"]==5

g3 = bigdf[filter_epoch3].groupby("shooter")

# get most active shooters ....  in TFO window (epoch 3)
# TFO = 2-for-1

activeshooters = g3["MakeMiss"].size().order(ascending=False)[:50]

# Active shooters is a list of players & the number of shots they took in epoch 3. Cutoff at top 50 players. 

x = bigdf["shooter"] == "J.Harden"

# Grow a list of players for Active Shooters List (top 50)
asfilt = []
for s in bigdf["shooter"]: 
    inlist = s in activeshooters.keys()
    print inlist
    asfilt.append(inlist)
    
# asfilt is Series of boolean values. Can be used to index/select rows in bigdf of the Active Shooters.

# print asfilt

# print out top active shooters
# print unique(bigdf[asfilt]["shooter"])

# so post: asfilt is the filter you can use from now on to select top 50 shooters, 
# or top 100 shooters. (reset # as needed for different cut size.)

# ------------------------------------------
 
# Save activeshooters list & filter to pickle file
shooters_out_fn = 'activeshooters.pik'
pickle.dump((activeshooters, asfilt), open(shooters_out_fn, 'wb'))

# Note, saved together in one object, need to read back in same order.

# ------------------------------------------




# this one: 
# set of ___ dataframe of all shot events for the top active shooters
bigdf[asfilt].groupby("shooter").size().order(ascending=False)
# active shooters , only in epoch 3 // to get a sense of 
bigdf[asfilt & filter_epoch3].groupby("shooter").size().order(ascending=False)

g4 = bigdf[asfilt].groupby(["shooter", "epoch"])

# probably discard g4 ? (is it needed? can delete for cleanup?)
    
print g4.agg( 'count')
    
# raw fg %    
print g4["MakeMiss"].agg('sum') / g4["MakeMiss"].agg('count')

# efg %    
print g4["points"].agg('sum') / (g4["points"].agg('count')*2)

# g4 ends up being similar to pivoted table generated earlier. 

# ------------------------------------------------------------

# shot proportion 
# number of two's per epoch (3,5)
# number of three's per epoch (3, 5)

shotcounts_byType_e3 = bigdf[asfilt & filter_epoch3].groupby("shottype").size()
shotcounts_byType_e5 = bigdf[asfilt & filter_epoch5].groupby("shottype").size()

proportion3s_e3 = shotcounts_byType_e3[3]/float(shotcounts_byType_e3[2]+shotcounts_byType_e3[3])
proportion3s_e5 = shotcounts_byType_e5[3]/float(shotcounts_byType_e5[2]+shotcounts_byType_e5[3])

print proportion3s_e3
print proportion3s_e5

# results = 2: 740, 3: 369

# // z test (offline) The Z-Score is 5.8312. The p-value is 0. The result is significant at p <0.05.

# -----------------------------------

# shot distance 
# avg distance of 2s, by epoch (3,5)
# avg distance of 3s, by epoch (3,5)

dists_e3 = bigdf[asfilt & filter_epoch3].groupby("shottype").mean()
dists_e3['distance']

dists_e5 = bigdf[asfilt & filter_epoch5].groupby("shottype").mean()
dists_e5['distance']

# wrong ... shotdistances = [ dists_e3['distance'][2] , dists_e5['distance']]
# -----------------------------------

# plot 2s vs 3s 

fig = plt.figure(101)
ax = fig.add_subplot(111)

width = 0.5

# confidence intervals for yvals
yerrterms = [np.sqrt(proportion3s_e3*(1-proportion3s_e3)/sum(shotcounts_byType_e3)), np.sqrt(proportion3s_e5*(1-proportion3s_e5)/sum(shotcounts_byType_e5))]

ax.bar([1,2], [proportion3s_e3, proportion3s_e5], width, yerr = yerrterms , 
    error_kw=dict(ecolor='gray', lw=2, capsize=5, capthick=2))

ax.set_ylabel('Proportion of 3s')     #('Count of FGA')
ax.set_xlabel('Seconds Remaining in Quarter')
ax.set_title('Shot Choice in Two-for-One')

#ax.set_title('When Shots Happen At End of Quarters')
xTickMarks = ['27-35', '61-180']
ax.set_xticks(np.arange(2)+1+(width/2))
xtickNames = ax.set_xticklabels(xTickMarks)
plt.setp(xtickNames, fontsize=10)

ax.set_xlim([0.5, 3])
ax.set_ylim([0, 0.4])
plt.show()
    
# -------------------------------

# plot shot distance by time remaining 
 
fig = plt.figure(102)
ax = fig.add_subplot(111)

width = 0.35

ax.bar([1,2, 1+width, 2+width], [dists_e3['distance'][2], dists_e5['distance'][2], dists_e3['distance'][3], dists_e5['distance'][3]] , width, color = ['r', 'r', 'b', 'b'] )

ax.set_ylabel('Distance of Shot')     #('Count of FGA')
ax.set_xlabel('Seconds Remaining in Quarter')
ax.set_title('Shot Distance in Two-for-One')

#ax.set_title('When Shots Happen At End of Quarters')
xTickMarks = ['27-35', '61-180']
ax.set_xticks(np.arange(2)+1+(width/2))
xtickNames = ax.set_xticklabels(xTickMarks)
plt.setp(xtickNames, fontsize=10)

ax.set_xlim([0.5, 3])
ax.legend(['2s', '1s', '3s', '3s'])

plt.show()



# ---------------------------
# Calc individual drop-off between epoch5 and epoch3, at individual level
# Heart of the analysis for individuals. 
# Will be similar to prev calculations at team-level

g2 = bigdf[asfilt].groupby(["shooter"])

# split 1
g_e3 = bigdf[asfilt & filter_epoch3].groupby(['shooter'])
plyr_fga_e3 = g_e3['points'].count()
plyr_efg_e3 = g_e3["points"].sum()*0.5/plyr_fga_e3

# split 2
g_e5 = bigdf[asfilt & filter_epoch5].groupby(['shooter'])
plyr_efg_e5 = g_e5["points"].sum()*0.5/g_e5["points"].count()

# combine (aka, e3-e5). Now have the difference between e5 and e3 efg%. Negative values indicate dropoff from epoch 5 to epoch 3. 

plyr_efg_diff = plyr_efg_e3-plyr_efg_e5
plyr_efg_diff.sort(ascending=True)

print plyr_efg_diff

# --------------------------------------------------------------------------
# Calc change in shot rate between epoch5 and epoch3, at individual level
# Heart of the analysis for individuals (part 2)
# Will be similar to prev calculations at team-level
# Baseline shotrate = shotrate in e5


plyr_shotrate_e3 = g_e3["points"].size()/float(9)
# because 9 seconds in bin of e3

plyr_shotrate_e5 = g_e5["points"].size()/float(115)
# because 115 seconds in bin of e3 (from 65-180 seconds time, left in quarter)

plyr_shotrate_diff = (plyr_shotrate_e3-plyr_shotrate_e5)/plyr_shotrate_e5
# negative values indicate less shooting, positive values indicate taking more shots 
plyr_shotrate_diff.sort(ascending=True)
print plyr_shotrate_diff

print 'Correlation beteen shot rate and change in eFG, player level: '
print pearsonr(plyr_shotrate_diff.sort_index(ascending=True),plyr_efg_diff.sort_index(ascending=True))


# --- 
# alt per player check, correlation between 'avg efg' and 'change in efg'
plyr_efg_corr = pearsonr(plyr_efg_e5.sort_index(ascending=True), plyr_efg_diff.sort_index(ascending=True))

print 'Correlation beteen regular eFG and change in eFG, player level: '
print plyr_efg_corr

fig = plt.figure(103)
fig.clf()
ax_scat2 = fig.add_subplot(1,2,2)
ax_scat2.clear()
ax_scat2.scatter(plyr_efg_e5.sort_index(ascending=True),plyr_efg_diff.sort_index(ascending=True))

ax_scat2.set_ylabel('Change in eFG%') 
ax_scat2.set_xlabel('Player\'s regular eFG%')
ax_scat2.set_title('Effect of 2-for-1 Shooting on player eFG%')

plt.show()

# label players of interest
player_list = ['L.James', 'J.Harden', 'S.Curry', 'S.Blake']

# annotate labels of certain playersj
for p in player_list:
    ax_scat2.scatter(plyr_efg_e5[p], plyr_efg_diff[p], s=80, marker=u'o', facecolors='none')
    ax_scat2.annotate(p,
                (plyr_efg_e5[p], plyr_efg_diff[p]),
                xytext=(-20, 10), 
                textcoords='offset points')
                
# add overlay regression line
# calc reg line

mask = plyr_efg_e5.index.isin(['S.Mack'])

# wrong ... 


from scipy import stats
# old code:
slope, intercept, r_val, p_val, std_err = stats.linregress(plyr_efg_e5.sort_index(), plyr_efg_diff.sort_index())

# plot reg line
xvals = plyr_efg_e5
yvals = xvals*slope+intercept
#
#ax_scat2.plot(xvals, yvals, 'r-')



# do simple linear fit
# Gotta make sure series are sorted right, first. (otherwise you get bad p-values, because the data aren't paired up.)
p = np.polyfit(plyr_efg_e5.sort_index(), plyr_efg_diff.sort_index(), 1)

rval, pval = pearsonr(plyr_efg_e5.sort_index(), plyr_efg_diff.sort_index())
print 'correlation, plyr_efg_e5 vs plyr_efg_diff: ', rval, pval

xfit = plyr_efg_e5
yfit = p[0]*xfit+p[1]

# plot overlay of 
plt.plot(xfit, yfit, 'r')


# alt xytext=(5,5)

# -----------------
# plot x,y scatter of shot rate diff vs efg diff (player level)


bb = plyr_efg_diff.sort_index(ascending=True)
cc = plyr_shotrate_diff.sort_index(ascending=True)

print plyr_efg_diff
print plyr_shotrate_diff

# ax_scat = plt.scatter(plyr_shotrate_diff, plyr_efg_diff)

fig = plt.figure(103)
ax_scat = fig.add_subplot(1,2,1)
ax_scat.scatter(cc, bb)

ax_scat.set_ylabel('Change in eFG%') 
ax_scat.set_xlabel('Change in Shot Rate')
ax_scat.set_title('eFG% vs Shot Rate, by player')

# annotate labels of certain playersj
for p in player_list:
    ax_scat.scatter(cc[p], bb[p], s=80, marker=u'o', facecolors='none')
    ax_scat.annotate(p,
                (cc[p], bb[p]),
                xytext=(-15, 10), 
                textcoords='offset points')
                
plt.show()

plt.savefig('player_level_efg.png')

# keep as proportional-change (not percentage change, bc plotting gets weirdly compressed along x-axis

# ----------------------------





# ----------------------------

plyr_efg = g2["points"].sum()*0.5/g2["points"].count()

# calc base shot rate from epoch 5 only


#
#
#base_shotrate = (shot_rate[4]+shot_rate[5])/2
##    tfo_goose = (shot_rate[3]-shot_rate[4]+)/shot_rate[4]
#tfo_goose = (shot_rate[3]-base_shotrate)/base_shotrate
#tfo_efgdrop = (efg[3]-efg[4])
#tfo_fgpdrop = (fg_perc[3]-fg_perc[4])

# -- Notes: Alternate way to do "TFO Prevalency" would be to look at TFO shots vs Opponent TFO shots.
# ie, how well did one team control the TFO possesion exchange in comparison to other teams. 
# Could make diff for teams like GSW, where they have  fairly high pace, which may under-state
# their TFO Preference.


# -------------------------------------------
# print table: player, efg_e5, efg_e3, efg_diff, n (num_fga_e3)

from itertools import izip

#for line in izip(plyr_efg_e3.keys(), plyr_efg_e3, plyr_fga_e3):
#    print line

# -  Use alt method, zip iterator
for line in izip(plyr_efg_e3.keys(), plyr_efg_e3, plyr_fga_e3):
    print line[0], '\t', "%.2f" %  line[1], '\t', line[2]
# --- 
# print full table
# correx - need to ensure all lists are pre-sorted (by player name)
print 'Table of player stats for two-for-one shooting'
print 'player -- n(shots) -- efg_e3 -- efg_e5 -- efg_diff'
for line in izip(plyr_efg_e3.keys(), plyr_fga_e3.sort_index(), plyr_efg_e3.sort_index(), plyr_efg_e5.sort_index(), plyr_efg_diff.sort_index()):
    print line[0], '\t', line[1], '\t', "%.2f" %  line[2], '\t', "%.2f" % line[3], '\t', "%.2f" % line[4]

# -----
# print table as above, but concat them all into a new dataframe, preferably (so sort order stuff maintained)

# example code : pd.concat({'efg_e3': plyr_efg_e3, 'efg_e5': plyr_efg_e5}, axis=1)

plyrdf = pd.concat({'fga_e3':plyr_fga_e3, 'efg_e3': plyr_efg_e3, 'efg_e5': plyr_efg_e5,  'efg_diff': plyr_efg_diff}, axis=1)
# ok, but it gets the ordering of the columns wrong?
# unexpected sorting is a pandas issue (link https://github.com/pydata/pandas/issues/4588) / known bug
# so manually re-order columns
plyrdf = plyrdf.reindex_axis(['fga_e3', 'efg_e3', 'efg_e5', 'efg_diff'], axis=1)

# output either of these:
print plyrdf.sort(columns='fga_e3', ascending=False)

# print plyrdf.sort(columns='efg_diff')

# --------------------------------------





# -------------------------
# - extra queries basically 

# number of shots in epoch3 for each player
bigdf[asfilt & filter_epoch3].groupby(['shooter'])['points'].count()




