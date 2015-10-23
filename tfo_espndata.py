
# Import espn spreadsheet of 2014-2015 team stats




import pandas as pd
import os.path
import pickle
import tfo_extra

import matplotlib.pyplot as plt

from scipy.stats.stats import pearsonr   

# -----------------------------------

filepre = "c://Users/Marc/Documents/nbadata/"
filename = "espn_nba_offense_20142015.csv"

df_espn = pd.read_csv(filepre + filename)

df_espn.set_index(['team_short'], inplace=True)


# ----------------------
# Read in main dataset

outfilename = 'shots_allteams.pik'
bigdf = pickle.load(open(outfilename, 'rb'))

fn_team_table = 'team_report_table.pik'

# Issue with pickle compatibility? // Reading in using alt method, below. 
# team_report = pickle.load(open(fn_team_table, 'rb'))

team_report = pd.read_pickle(fn_team_table)

# ----------- a test
# test to make sure what AFG is. 

test_afg = (df_espn['FGM'] + df_espn['3PM'].div(2)).div(df_espn['FGA'])
test_afg - df_espn['AFG%']


# so their AFG% is what we're calling eFG / same, point-weighted version of FG%

# -----------

# Compare ESPN's season-long eFG to what we calculated in epoch 5 

print df_espn['AFG%'].sort_index()
print team_report['team_efg_e5'].sort_index()

x = team_report['team_efg_e5'].sort_index() - df_espn['AFG%'].sort_index()

print "mean diff between whole season stats and epoch 5: ", x.mean()

# mean at 0.0100486358233. So basically, epoch 5 stats are the same as entire season. Valid baseline. 


# -----------------------

# epoch 5 vs espn season stats

tfo_extra.plot_scatter_with_reg_overlay(df_espn['AFG%'].sort_index(), team_report['team_efg_e5'].sort_index(), figurenum = 1002, overlay = True)

plt.xlabel('regular season eFG%')
plt.ylabel('eFG% in epoch 5')

print pearsonr(df_espn['AFG%'].sort_index(), team_report['team_efg_e5'].sort_index())
# results: (0.81549272252163574, 4.0378399944744899e-08)

# ------------


# Ok -- do some code // team_efg_e4 defined in alternate file (tfo_team_report)

print "season avg vs epoch 5: "
print pearsonr(df_espn['AFG%'].sort_index(), team_report['team_efg_e5'].sort_index())

print "season avg vs epoch 4: "
print pearsonr(df_espn['AFG%'].sort_index(), team_efg_e4)
# results: (0.42785093451288075, 0.018346954168638345)

print "season avg vs epoch 3: "
print pearsonr(df_espn['AFG%'].sort_index(), team_efg_e3)
# results: (0.13073341070140868, 0.49107855614736429)

print "season avg vs epoch 2: "
print pearsonr(df_espn['AFG%'].sort_index(), team_efg_e2)
# results: (0.37861269977355372, 0.039098513528723983)

print "season avg vs epoch 1: "
print pearsonr(df_espn['AFG%'].sort_index(), team_efg_e1)
# results: (0.46303466707202551, 0.0099741143348143855)

# n's for epochs / 

bigdf.groupby(['epoch'])['points'].count()
#Out[47]: 
#epoch
#1     3659
#2     3329
#3     2626
#4     6618
#5    24147
#Name: points, dtype: int64



# ------------------------

# epoch 3 vs espn season stats
tfo_extra.plot_scatter_with_reg_overlay(df_espn['AFG%'].sort_index(), team_report['team_efg_e3'].sort_index(), figurenum = 1003, overlay = True)

plt.xlabel('regular season eFG%')
plt.ylabel('eFG% in epoch 3')

# ------------------------

# espn season stats vs e5-e3 diff
tfo_extra.plot_scatter_with_reg_overlay(df_espn['AFG%'].sort_index(), team_report['team_efg_diff'].sort_index(), figurenum = 1004, overlay = True)

plt.xlabel('regular season eFG%')
plt.ylabel('epoch 3-5 diff, eFG%')

# ------------------------

# additional comparisons

# espn season stats vs diff (e3 - espn)
tfo_extra.plot_scatter_with_reg_overlay(df_espn['AFG%'].sort_index(), team_report['team_efg_e3']- df_espn['AFG%'], figurenum = 1025, overlay = True)

plt.xlabel('regular season eFG%')
plt.ylabel('efg e3 - reg season efg  efg%')

pearsonr(df_espn['AFG%'], team_report['team_efg_e3'] - df_espn['AFG%'] )


