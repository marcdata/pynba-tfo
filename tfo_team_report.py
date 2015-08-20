

# pre: // pass in bigdf basically, dataframe of per shot data
# post: returns back a dataframe of stats, calculated for a team
# example usage mydataframe = tfo_team_report('HOU', bigdf)

# calculate efg, differnetials, by shot type, mostly between epoch 3 and epoch 5

# -----------------------------------------------------------------------------

import os.path

import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import pickle

from scipy.stats.stats import pearsonr   
from scipy.stats.stats import spearmanr   

# Using plot function from tfo_extra.py
import tfo_extra

# -----------------------------------------------------------------------------

# All 30 teams
teamnames = ['ATL', 'BOS', 'BRK', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL',
    'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']   
    
# -----------------------------------------------------------------------------

# read in pickle file data from prev
outfilename = 'shots_allteams.pik'
bigdf = pickle.load(open(outfilename, 'rb'))

# -----------------------------------------------------------------------------

def tfo_team_report(team_name, df_shots):
    """Calculates some per-team 2-for-1 stats, returns a small dataframe of those summary stats."""
        
    teamdf = df_shots[df_shots['Tm']==team_name]

    print team_name
    print len(teamdf)
        
    # set up filters to make later analysis easier
    filter_epoch3 = teamdf["epoch"]==3
    filter_epoch5 = teamdf["epoch"]==5
    filter_shottype2 = teamdf["shottype"]==2
    filter_shottype3 = teamdf["shottype"]==3
    
    shotcounts_byType_e3 = teamdf[filter_epoch3].groupby("shottype").size()
    shotcounts_byType_e5 = teamdf[filter_epoch5].groupby("shottype").size()
    
    proportion3s_e3 = shotcounts_byType_e3[3]/float(shotcounts_byType_e3[2]+shotcounts_byType_e3[3])
    proportion3s_e5 = shotcounts_byType_e5[3]/float(shotcounts_byType_e5[2]+shotcounts_byType_e5[3])
    proportion3s_diff = proportion3s_e3 - proportion3s_e5

    team_efg_e3 = teamdf[filter_epoch3]["points"].sum()*0.5/teamdf[filter_epoch3]["points"].count()
    team_efg_e5 = teamdf[filter_epoch5]["points"].sum()*0.5/teamdf[filter_epoch5]["points"].count()
    team_efg_diff = team_efg_e3 - team_efg_e5
    
    shotdist_e3 = teamdf[filter_epoch3 & filter_shottype2]["distance"].mean()
    shotdist_e5 = teamdf[filter_epoch5 & filter_shottype2]["distance"].mean()
    
    # calc change in 3 pt shooting percentage
    
    
    # print out mini-report
    
    print 'shot distance, epoch 3: ', shotdist_e3
    print 'shot distance, epoch 5: ', shotdist_e5

    print "Proportion of 3s in epoch 3: ", proportion3s_e3
    print "Proportion of 3s in epoch 5: ", proportion3s_e5
    
    print "eFG in epoch 3: ", team_efg_e3
    print "eFG in epoch 5: ", team_efg_e5    
    
    three_pt_perc = teamdf[teamdf['shottype'] == 3].groupby('epoch')['MakeMiss'].mean()
    three_pt_n = teamdf[teamdf['shottype'] == 3].groupby('epoch')['MakeMiss'].count()
    threeperc_e3 = three_pt_perc[3]
    threeperc_e5 = three_pt_perc[5]
    threeperc_diff = threeperc_e3 - threeperc_e5 
    
    #ok, kind of busy with all the variables, but we're reporting out each one, so it's ok
    
    print "3pt %, epoch 3: ", "%.2f" % threeperc_e3
    print "3pt %, epoch 5: ", "%.2f" % threeperc_e5
    print "3pt %, diff: ", "%.2f" % threeperc_diff
    print "3pt (n), epoch 3: ", "%.2f" % three_pt_n[3]
    
    # Add in Change in Shot Rate 
    
    # fga counts. We're just getting a count here, so counting on "points" column, but could count on most any.
    team_grouped = teamdf.groupby("epoch")
    fga = team_grouped["points"].count()
    
    # Final shot rate bin sizes
    shot_rate = fga/[5, 22, 9, 29, 115]
    
    # calc summary stats for xy plot later
    # old method: base_shotrate = (shot_rate[4]+shot_rate[5])/2
    base_shotrate = shot_rate[5]
    
#    tfo_goose = (shot_rate[3]-shot_rate[4]+)/shot_rate[4]
    shotrate_diff = (shot_rate[3]-base_shotrate)/base_shotrate
    
    
    # print crosstab(teamdf['distance'], teamdf['epoch'])
    
    # create output dataframe of computed stats
    #    >>> d = {'col1': ts1, 'col2': ts2}
    #>>> df = DataFrame(data=d, index=index)

    d = {'threeperc_e3': threeperc_e3, 'threeperc_e5': threeperc_e5, 'threeperc_diff': threeperc_diff, 'three_pt_n': three_pt_n[3], 
        'prop_threes_e3': proportion3s_e3, 'prop_threes_e5': proportion3s_e5, 'prop_threes_diff': proportion3s_diff,
        'team_efg_e3': team_efg_e3 , 'team_efg_e5': team_efg_e5, 'team_efg_diff': team_efg_diff,
        'shotrate_base': base_shotrate, 'shotrate_diff': shotrate_diff
        }
    team_out_df = pd.DataFrame(data = d, index = pd.Series(team_name))
    
    return team_out_df
    
    
# ----------------

# Collect all team-tables (dataframes) into one big new dataframe.

team_report = pd.DataFrame()

for tn in teamnames:
    tmdf = tfo_team_report(tn, bigdf)
    team_report = pd.concat([team_report, tmdf])

# ----------------

# Re order columns for better display. Overwrite team_report with new version.

team_report = team_report.reindex_axis(['team_efg_e3' , 'team_efg_e5', 'team_efg_diff',
    'threeperc_e3', 'threeperc_e5', 'threeperc_diff', 'three_pt_n', 
    'prop_threes_e3', 'prop_threes_e5', 'prop_threes_diff',     
    'shotrate_base', 'shotrate_diff'],
    axis = 1)
   

# ------------------------------------------
 
# Save new team table to pickle file
outfilename = 'team_report_table.pik'
pickle.dump(team_report, open(outfilename, 'wb'))

# ------------------------------------------



# ----------------

aa = team_report['threeperc_diff']
aa = aa.order()
    


# teams shooting more threes in epoch 3 / 

team_report['prop_threes_diff'].order()

a = team_report['prop_threes_diff']
b = team_report['threeperc_diff']

# 
# pearsonr(a, b)
# Out[421]: (-0.30965900753032488, 0.095868846310719527)


# plot quick scatter 
plt.figure(5)
plt.plot(a, b, '.')

pearsonr(a, b)

# rank order comparison: 

[r_val, p_val] = spearmanr(a, b)


plt.figure(1000)
plt.plot(team_report['threeperc_e5'], team_report['threeperc_diff'], '.')
plt.xlabel('3 pt % baseline')
plt.ylabel('Change in 3 pt %')
    
pearsonr(team_report['threeperc_e5'], team_report['threeperc_diff'])

# similar for per player

# check if 3pt % influences how often teams shoot threes?

rval, pval = pearsonr(team_report['threeperc_e5'], team_report['prop_threes_e5'])

# quick plot reg efg diff vs efg diff 
plt.figure(1001)
plt.plot(team_report['team_efg_e5'], team_report['team_efg_diff'], '.')
plt.xlabel('eFG % baseline')
plt.ylabel('change in eFG %')

p = np.polyfit(team_report['team_efg_e5'], team_report['team_efg_diff'], 1)

xfit = team_report['team_efg_e5']
yfit = p[0]*xfit+p[1]

# plot overlay of 
plt.plot(xfit, yfit, 'r')


# quick correlation
pearsonr(team_report['team_efg_e5'], team_report['team_efg_diff'])
# GSW shows little/no drop off, maintain high eFG

# quick plot reg efg e5 vs efg e3 
plt.figure(1002)
plt.plot(team_report['team_efg_e5'], team_report['team_efg_e3'], '.')
plt.xlabel('eFG % baseline')
plt.ylabel('eFG % 2-for-1 Window')


# quick correlation
pearsonr(team_report['team_efg_e5'], team_report['team_efg_e3'])
# (-0.05933702066021676, 0.75544567941622742)
# regular eFG little/no relation to epoch 3 efg 

# redo above / highlight HOU and GSW  ... diff strats potentially for the two teams





# ----------------------

# make new control epoch... for control group type test
# similar to epoch 4, but without some of the data problems near time=60 seconds

filter_newepoch = (bigdf['Time2'] > 45) & (bigdf['Time2'] < 56)

bigdf[filter_newepoch].groupby('Tm')["points"].sum()*0.5/bigdf[filter_newepoch].groupby('Tm')["points"].count()

# calc per-team efg for the selected time period
team_efg_econtrol = bigdf[filter_newepoch].groupby('Tm')["points"].sum()*0.5/bigdf[filter_newepoch].groupby('Tm')["points"].count()

# generate second comparison point. To compare with team_efg_diff
team_efg_diff2 = team_efg_econtrol - team_report['team_efg_e5'] 

# mini table of the two diffs
x = pd.DataFrame(data = {'team_efg_diff': team_report['team_efg_diff'], 'team_efg_diff2': team_efg_diff2})
x.mean()




# -- plot comparisons
# Using plot function from tfo_extra.py

tfo_extra.plot_scatter_with_reg_overlay(team_report['team_efg_e5'], team_report['team_efg_diff'], figurenum = 1010, overlay = True)
plt.xlabel('Team efg e5')
plt.ylabel('Diff efg e3, e5')

tfo_extra.plot_scatter_with_reg_overlay(team_report['team_efg_e5'], team_efg_diff2, figurenum = 1011, overlay = True)#
plt.xlabel('Team efg e5')
plt.ylabel('Diff efg e3, econtrol')


# crank out r values //

# one correlates, one doenst. Seems valid. 

# Last check: use econtrol in place of e5 

tfo_extra.plot_scatter_with_reg_overlay(team_efg_econtrol, team_report['team_efg_e3']-team_efg_econtrol, figurenum = 1012, overlay = True)
plt.xlabel('Team efg econtrol')
plt.ylabel('Diff efg e3, econtrol')

# still see regressing to the mean type of effect. 
# So, in epoch 3, teams shoot more like "average NBA shot" than how that team normally shoots. 
# High performers become mediocre performers. 

# Check efg control vs efg e5. Correlates, mean diff = 0.006, correlates, but noisy.
tfo_extra.plot_scatter_with_reg_overlay(team_report['team_efg_e5'], team_efg_econtrol, figurenum = 1013, overlay = True)
plt.xlabel('Team efg epoch 5')
plt.ylabel('Team efg econtrol')

# Make sure plots display.
plt.show()

# ---------------------

# Diff between e3 and e5 efg. 
# x = team_report['team_efg_e5'] - team_report['team_efg_e3']
# x.mean()
# Out[58]: 0.020222287576907551



# ---------------------


# A couple more scatter comparisons. 

# shot_rate vs efg (again)

tfo_extra.plot_scatter_with_reg_overlay(team_report['shotrate_diff'], team_report['team_efg_diff'], figurenum = 1020, overlay = True)
plt.xlabel('Shot Rate Diff')
plt.ylabel('team_efg_diff')

pearsonr(team_report['shotrate_diff'], team_report['team_efg_diff'])
# (-0.30600024812464699, 0.1000656721856395)
# Marginal correlation. // Could be diff with Demming Error method?

# shotrate_diff vs proportion of 3s

tfo_extra.plot_scatter_with_reg_overlay(team_report['shotrate_diff'], team_report['prop_threes_diff'], figurenum = 1021, overlay = True)
plt.xlabel('shotrate_diff')
plt.ylabel('prop_threes_diff')

pearsonr(team_report['shotrate_diff'], team_report['prop_threes_diff'])
# (0.48164911393624316, 0.0070403594139744228)
# Higher TFO Shotrate -> Higher Proportion of 3s Attempted. 

# **

# Change in Proportion of 3s vs eFG conversion of 3 pt attempts

tfo_extra.plot_scatter_with_reg_overlay(team_report['prop_threes_diff'], team_report['threeperc_diff'], figurenum = 1022, overlay = True)
plt.xlabel('prop_threes_diff')
plt.ylabel('threeperc_diff')

pearsonr(team_report['prop_threes_diff'], team_report['threeperc_diff'])
# (-0.30965900753032488, 0.095868846310719527)
# Marginal


# Change in eFG for three divisions of teams (tripiles) (aka 3-way quartiles). 

# Based on prev two, check change in shotrate vs change in 3pt efg

tfo_extra.plot_scatter_with_reg_overlay(team_report['shotrate_diff'], team_report['threeperc_diff'], figurenum = 1023, overlay = True)
plt.xlabel('shotrate_diff')
plt.ylabel('threeperc_diff')

pearsonr(team_report['shotrate_diff'], team_report['threeperc_diff'])
# ... 
# Neglibile:
# (-0.14635949429813827, 0.44026210425654566)





# -----------------------------------------------------------------

# Double check Assumption: how many offensive rebounds affecting Epoch 3? 

# Sort unique by Team, Game, Quarter. 
# *Should* be only 1 shot in that 9 second span the majority of the time. 

filter_e3_qa = bigdf['epoch'] == 3

bigdf[filter_e3_qa].groupby(['Tm', 'Date', 'Qtr'])[['Tm', 'Date', 'Qtr', 'epoch']].head()
bigdf[filter_e3_qa].groupby(['Tm', 'Date', 'Qtr'])['epoch'].head()

qa_e3_counts = bigdf[filter_e3_qa].groupby(['Tm', 'Date', 'Qtr'])['epoch'].value_counts()

qa_e3_counts.value_counts()

#Out[34]: 
#1    2263
#2     174
#3       5
#dtype: int64

# float(179)/sum([2263, 174, 5])
# Out[58]: 0.0733005733005733

# So approx 07 % of shots in Epoch 3 may be result of 2nd chance, offensive rebounds. 
# aka 2 or more records in Epoch 3 for a given Team-Game-Quarter 


# ------------------------------------------------------------------------------

# Some more, extra comparison

# Filter not GSW
filter_not_gsw = team_report.index != 'GSW'

teams_not_gsw = team_report[filter_not_gsw]

tfo_extra.plot_scatter_with_reg_overlay(teams_not_gsw['team_efg_e5'], teams_not_gsw['team_efg_e3'], figurenum = 1031, overlay = True)
plt.xlabel('team_efg_e5')
plt.ylabel('team_efg_e3')

pearsonr(teams_not_gsw['team_efg_e5'], teams_not_gsw['team_efg_e3'])

# so weakly neg correlated, if you take out GSW
# Pearson r: -0.22670861463354905, 0.23695328299743237



# -------------

tfo_extra.plot_scatter_with_reg_overlay(team_report['team_efg_e5'], team_report['team_efg_e3'], figurenum = 1033, overlay = True)
plt.xlabel('team_efg_e5')
plt.ylabel('team_efg_e3')

pearsonr(team_report['team_efg_e5'], team_report['team_efg_e3'])
# Variances

print "Variance in efg in e3: ", var(team_report['team_efg_e3'])

print "Variance in efg in e5: ", var(team_report['team_efg_e5'])

# Variance in efg in e3:  0.00287592554404
# Variance in efg in e5:  0.000748020287562

team_report['team_efg_e3'].describe()

team_report['team_efg_e5'].describe()


# Alt version, use season long espn AFG data

tfo_extra.plot_scatter_with_reg_overlay(df_espn['AFG%'].sort_index(), team_report['team_efg_diff'].sort_index(), figurenum = 1034, overlay = True)
plt.xlabel('AFG%')
plt.ylabel('team_efg_diff')

pearsonr(df_espn['AFG%'].sort_index(), team_report['team_efg_diff'].sort_index())

# (-0.24814652224854314, 0.18610368990953505) 

# Marginally neg regression.


# Shot rate vs three pt percentage difference

# filter out lowest two shotrate_diff's teams / no MIA, no GSW

filter_shotratediff_only = (team_report.index != 'GSW') & (team_report.index != 'MIA')

tfo_extra.plot_scatter_with_reg_overlay(team_report[filter_shotratediff_only]['shotrate_diff'].sort_index(), team_report[filter_shotratediff_only]['threeperc_diff'].sort_index(), figurenum = 1035, overlay = True)
plt.xlabel('shotrate_diff')
plt.ylabel('threeperc_diff')

pearsonr(team_report[filter_shotratediff_only]['shotrate_diff'].sort_index(), team_report[filter_shotratediff_only]['threeperc_diff'].sort_index())

#  (-0.41324150433709711, 0.028835574286124273)

# So, the more teams go for TFO, the lower 3pt efficiency gets. 
# Broadly, but it kind of looks like two diff populations, one strictly lower than 0,
# one that's slightly above zero diff. 


# 

# Compare efg e5, vs e3, keep out GSW

filter_no_gsw = (team_report.index != 'GSW') 

tfo_extra.plot_scatter_with_reg_overlay(team_report[filter_no_gsw]['team_efg_e5'].sort_index(), team_report[filter_no_gsw]['team_efg_e3'].sort_index(), figurenum = 1036, overlay = True)
plt.xlabel('team_efg_e5')
plt.ylabel('team_efg_e3')

pearsonr(team_report[filter_no_gsw]['team_efg_e5'].sort_index(), team_report[filter_no_gsw]['team_efg_e3'].sort_index())
# (-0.22670861463354905, 0.23695328299743237)


# ---------------------------------

# Compare e3 minus mean(e5) as alternate comparison; instead of pairwise differences.

filter_no_gsw = (team_report.index != 'GSW') 

y = team_report[filter_no_gsw]['team_efg_e3'] - team_report[filter_no_gsw]['team_efg_e5'].mean()
x = team_report[filter_no_gsw]['team_efg_e5']
tfo_extra.plot_scatter_with_reg_overlay(x, y, figurenum = 1037, overlay = True)
plt.xlabel('team_efg_e5')
plt.ylabel('team_efg_e3 minus e5 mean')

pearsonr(x, y)



# Compare e5 to econtrol, simply, no differencing. 

filter_no_gsw = (team_report.index != 'GSW') 

y = team_efg_econtrol
x = team_report['team_efg_e5']
tfo_extra.plot_scatter_with_reg_overlay(x, y, figurenum = 1038, overlay = True)
plt.xlabel('team_efg_e5')
plt.ylabel('econtrol')

pearsonr(x, y)


# p < .10 (0.31637600575723901, 0.088512439422266012)

