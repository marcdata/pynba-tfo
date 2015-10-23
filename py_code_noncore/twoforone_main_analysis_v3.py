
# Script for doing main, team-level analysis
# do per-minute analysis
# 
# Version 2: Cutting out individual team plots. 
# Streamlining some of the global calculations. 
#
# Version3: splitting out 2s from 3s, in Figure 8 (per-minute analysis). 



# -----------------------------------------------------------------------------

import os.path

import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import pickle

from scipy.stats.stats import pearsonr   
from scipy.stats.stats import spearmanr   


# -----------------------------------------------------------------------------

def movingaverage (values, windowsize):
    weights = np.repeat(1.0, windowsize)/windowsize
    smoothed = np.convolve(values, weights, 'same')
    return smoothed

def movingaverage2 (values, windowsize):
    weights = np.repeat(1.0, windowsize)/windowsize
    smoothed = np.convolve(values, weights, 'same')
    return smoothed
    
# -----------------------------------------------------------------------------

# Some prepatory basics

# All 30 teams
teamnames = ['ATL', 'BOS', 'BRK', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL',
    'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']   

# read in pickle file data from prev
outfilename = 'shots_allteams.pik'
bigdf = pickle.load(open(outfilename, 'rb'))

# -----------------------------------------------------------------------------


# ---------------------------------------------

# Leftover from prev per-team analysis. 

## Summary charts
#
#fig_team_scat = plt.figure(2)
#fig_team_scat.clf()
#ax_scat = fig_team_scat.add_subplot(111)
#
#ax_scat.scatter(tfo_gooses, efg_deltas)
#
#ax_scat.set_ylabel('Change in eFG%')     
#ax_scat.set_xlabel('Change in Shooting Rate')
#
## add labels for each x,y point. Identify with team name (short name triple)
#for label, x, y in zip(teams_out, tfo_gooses, efg_deltas):
#    plt.annotate(
#        label, 
#        xy = (x, y), xytext = (5, 5), textcoords = 'offset points')
#
#plt.show()
#
#from scipy.stats.stats import pearsonr   
#
#print pearsonr(tfo_gooses,efg_deltas)

# (-0.28226186560180239, 0.14559286204854066)
# (-0.30600024812464699, 0.1000656721856395)
# (-0.26979766638641567, 0.14934558828826472)
# various correlation results, varying epoch 3 bin cutoffs slightly

# --------------------------------------------

    

# ------------------------------------------------------------------------------

# Per-second analysis

# ------------------------------------------------------------------------------

# Data cleaning issue, spike in shot counts at ~ 60 seconds.

g2 = bigdf.groupby('Time2')

pts = g2["points"].sum()
fga = g2["points"].count()
efg = 0.5*pts/fga
nshots = g2['points'].count()

fig_time = plt.figure(3)
fig_time.clf()
ax_persec = fig_time.add_subplot(211)
ax_persec.bar(nshots.index, nshots.values, width = 1)

# Add annotation (arrow), show data blip.

ax_persec.annotate('Spike in # shots', xy=(70, 600), xytext=(100, 800),
    arrowprops=dict(color = 'black', facecolor='black', width = 1, shrink=0.05))
    
    
# ---------------

# Create a filter to drop out spike in data. // Different from epoch'ing method.

filter_noblip1 = bigdf['Time2'] < 60
filter_noblip2 = bigdf['Time2'] > 60
filter_noblip = filter_noblip1 | filter_noblip2

# ---------------

ax_persec2 = fig_time.add_subplot(212)
# g3 = bigdf[filter_threes_only & filter_noblip].groupby('Time2')
g3 = bigdf[filter_noblip].groupby('Time2')
pts = g3["points"].sum()
fga = g3["points"].count()
fg_perc = g3['MakeMiss'].mean()
efg = 0.5*pts/fga
nshots2 = g3['points'].count()

ax_persec2.bar(nshots2.index, nshots2.values, width = 1)

ax_persec2.set_xlabel('Seconds Remaining in Quarter')
ax_persec2.set_ylabel('# Shots')
ax_persec.set_ylabel('# Shots')

# -----------------------------------------------------------------

fig_persec_efg = plt.figure(4)
ax_efgsec = fig_persec_efg.add_subplot(111)
ax_efgsec.plot(nshots2.index, fg_perc)

# -----------------------------------------------------------------


# Split out between twos and threes / by ShotType

filter_threes_only = bigdf['shottype'] == 3
filter_twos_only = bigdf['shottype'] == 2

grouped_shots_3s_only = bigdf[filter_threes_only & filter_noblip].groupby('Time2')
grouped_shots_2s_only = bigdf[filter_twos_only & filter_noblip].groupby('Time2')

# only need counts and mean of points

fga_twos = grouped_shots_2s_only["points"].count()
fga_threes = grouped_shots_3s_only["points"].count()

efg_twos = grouped_shots_2s_only["points"].mean()/2
efg_threes = grouped_shots_3s_only["points"].mean()/2

nshots_threes = grouped_shots_3s_only['points'].count()
nshots_twos = grouped_shots_2s_only['points'].count()

# ---

# Plot the eFG's by shottype, per minute. Add smoothing. 

figure8 = plt.figure(208)
figure8.clf()
ax = figure8.add_subplot(111)

seconds_index = nshots_twos.index

# Could use the same index (x-axis, minute counts), but later cleanup. 

# Plot smoothed versions, in color
# Window size 9 or 11 probably the best overall balance between smoothing and 
# temporal resolution. 

window_size = 11

ax.plot(seconds_index, 100 * movingaverage(efg_threes, window_size), 'r')
ax.plot(seconds_index, 100 * movingaverage(efg_twos, window_size), 'b')
# Add third, plot, smoother version of threes (better baseline comparison). Taken out for now. 
# ax.plot(seconds_index, movingaverage(efg_threes, 21), 'b:')

# Plot unsmoothed version, in grayscale
ax.plot(nshots_threes.index, 100* efg_threes, ':', color = '0.7')
ax.plot(nshots_twos.index, 100 * efg_twos, color = '0.8')

# set lims. Note: xlims need to account for smoothing. Low-end of 
# x-axis bitten off by box-smoothing, not accurate below x=windowsize/2.
ax.set_xlim([window_size/2, 80])
# ax.set_ylim([0.3, 0.75])
ax.set_ylim([30, 75])

# Add legend. Make sure matches plotting order.

ax.legend(['3s smoothed', '2s smoothed', '3s raw', '2s raw'], loc = 'lower right')

# Title, label axes, etc
ax.set_title('Shot Efficiency At End of Quarters, by Shot Type (2pt or 3pt)')
ax.set_xlabel('Seconds Remaining in Quarter')
ax.set_ylabel('eFG %')

# Add annotation (arrow), emphasizing drop in 3pt %

ax.annotate('Drop in 3pt efficiency', xy=(27, 60), xytext=(41, 70),
    arrowprops=dict(color = 'red', facecolor='red', width = 1, shrink=0.05))

plt.show()


# --------------------------------------------------------------

# Shot counts by type? 

fig99 = plt.figure(209)
ax_counts = fig99.add_subplot(111)

ax_counts.plot(nshots_threes.index, nshots_threes, 'r')
ax_counts.plot(nshots_twos.index, nshots_twos, 'b')
ax_counts.legend(['3 pt', '2 pt'])
plt.show()

# ----------------------------------------










# -----------------------------------------


# similar as 208, but with 2 drop arrows, vertical. 

# Plot the eFG's by shottype, per minute. Add smoothing. 

# Alternate version of Figure 208 -- with bar timeperiod highlight 
# vs the red arrow 

figure210 = plt.figure(210)
figure210.clf()
ax = figure210.add_subplot(111)

seconds_index = nshots_twos.index

# Could use the same index (x-axis, minute counts), but later cleanup. 

# Plot smoothed versions, in color
# Window size 9 or 11 probably the best overall balance between smoothing and 
# teporal resolution. 

window_size = 11

ax.plot(seconds_index, 100 * movingaverage(efg_threes, window_size), 'r', linewidth=2.0)
ax.plot(seconds_index, 100 * movingaverage(efg_twos, window_size), 'b', linewidth=2.0)
# Add third, plot, smoother version of threes (better baseline comparison). Taken out for now. 
# ax.plot(seconds_index, movingaverage(efg_threes, 21), 'b:')

# Plot unsmoothed version, in grayscale
ax.plot(nshots_threes.index, 100* efg_threes, ':', color = '0.6')
ax.plot(nshots_twos.index, 100 * efg_twos, color = '0.6')

# set lims. Note: xlims need to account for smoothing. Low-end of 
# x-axis bitten off by box-smoothing, not accurate below x=windowsize/2.
ax.set_xlim([window_size/2, 80])
# ax.set_ylim([0.3, 0.75])
ax.set_ylim([30, 75])

# Add legend. Make sure matches plotting order.

ax.legend(['3s smoothed', '2s smoothed', '3s raw', '2s raw'], loc = 'lower right')

# Title, label axes, etc
ax.set_title('Shot Efficiency At End of Quarters, by Shot Type (2pt or 3pt)')
ax.set_xlabel('Seconds Remaining in Quarter')
ax.set_ylabel('eFG %')

# REM Add annotation (arrow), emphasizing drop in 3pt %

# REM ax.annotate('Drop in 3pt efficiency', xy=(27, 60), xytext=(41, 70),
# REM   arrowprops=dict(color = 'red', facecolor='red', width = 1, shrink=0.05))

# Add annotation, emphasize drop, but highlight start, end times. T = 27, 40.
# or two arrows? To start and end times?

ax.annotate('Drop in 3pt efficiency', xy=(41, 64), xytext=(41, 72),
    arrowprops=dict(color = 'red', facecolor='red', width = 1, shrink=0.05))
ax.annotate('', xy=(27, 55), xytext=(27, 72),
    arrowprops=dict(color = 'red', facecolor='red', width = 1, shrink=0.05))
    
    
tfo_extra.update_plot_properties(ax)

plt.show()


# ---------------------------------------


# ----------------------------------------

# overlay eFG shooting per second, with smoothed eFG (top plot)
# number of shots a second (bottom plot)
# league-wide figure; visual comparison of # shots vs shot efficiency

# ---- 
winsize = 9 
# or winsize nine also works decent, or 7

fig8 = plt.figure(8)
fig8.clf()
axtop = fig8.add_subplot(211)

# Plot efg (noisy) in greyscale, so it's less in forefront. 
axtop.plot(efg, color = '0.7') 
axtop.plot(movingaverage(efg, winsize))
# set lims
axtop.set_xlim([5, 75])
axtop.set_ylim([0.3, 0.7])

axbot = fig8.add_subplot(212)
axbot.plot(nshots2)
# set lims
axbot.set_xlim([5, 75])
axbot.set_ylim([0, 400])

# set labels
axtop.set_title('All Teams, End of Quarter Shots')
axbot.set_xlabel('Seconds Remaining in Quarter')
axbot.set_ylabel('Number of Shots Taken')

axtop.set_ylabel('Shooting Efficiency (eFG)')
axtop.legend(['eFG % raw', 'smoothed'], loc = 'lower right' )

# save fig
fig8.savefig('figure 8 -- allteams efg vs time.jpg')

# ---------------------------------------------------------------


# ---------------------------------------------------------------

# do MA moving average smoothed series for all teams .... 
# overlay all teams to single linechart, eFG vs Time of Shot

# setup filter for data cleaning, use same for all teams
filter_noblip1 = bigdf['Time2'] < 59
filter_noblip2 = bigdf['Time2'] > 61
filter_noblip = filter_noblip1 | filter_noblip2
    
teams2 = []
shots2 = []

for tn in teamnames:
    
    filter_team = (bigdf['Tm'] == tn) 
    
    g3 = bigdf[filter_team & filter_noblip].groupby('Time2')
    
    pts = g3["points"].sum()
    fga = g3["points"].count()
    fg_perc = g3['MakeMiss'].mean()
    efg = 0.5*pts/fga
    
    nshots2 = g3['points'].count()
    
    fig7 = plt.figure(7)
    axtop = fig7.add_subplot(211)
    axtop.plot(movingaverage(fg_perc, winsize))
    
    axbot = fig7.add_subplot(212)
    axbot.plot(nshots2)

    # also kick out number of shots between 28-38 seconds

    shotcount = nshots2[27:37].sum()
    
    print tn, "number of shots: ", shotcount
    teams2.append(tn)
    shots2.append(shotcount)

# end loop

# -------------------------------------------------

# categorize teams based on their shot rank (how often they're shooting in this window)
b = pd.Series(shots2, index=teams2)
b.sort(ascending = False)

# Generate mappings into thirds, top third, middle third, lower third, numbered 1,2,3 respectively. 
# Generate mappings into fourths, similarly, numbered 1,2,3,4. 
# Qs and Ts Maps Team-Name into Grouping. 

quartiles = np.concatenate((np.repeat(1,8), np.repeat(2,7), np.repeat(3,7), np.repeat(4,8)))
tripiles = np.concatenate((np.repeat(1,10), np.repeat(2,10), np.repeat(3,10)))
qs = pd.Series(quartiles, index=b.index)
ts = pd.Series(tripiles, index=b.index)
# qs = Team:Quartile pairing, e.g. MIA:4, ATL:1, etc
# basically split entire league into four groups

# remap into series of quartile groupings
qs2 = qs[bigdf['Tm']]
ts2 = ts[bigdf['Tm']]
# qs2 is same size as bigdf now. Can now add as column to df
bigdf['quartile'] = pd.Series(qs2.values, index=bigdf.index)
bigdf['tripile'] = pd.Series(ts2.values, index=bigdf.index)

# # check with: pd.crosstab(bigdf['Tm'], bigdf['quartile'])
# checks out, mapping was good

# ------

# display efg vs time, grouped by tripile (3-way quartiles)

# for qrank in [1, 2, 3, 4]:
# nix: for hrank in [1, 3]:  

fig6 = plt.figure(6)
fig6.clf()
    
for trirank in [1, 2, 3]:
    

    filter_tripile = (bigdf['tripile'] == trirank)
    # alt code for quartiles, half-tiles
    # filter_quartile = (bigdf['quartile'] == qrank)
    # filter_quartile = (bigdf['quartile'] == hrank) | (bigdf['quartile'] == (hrank+1))
    
    g4 = bigdf[filter_tripile & filter_noblip].groupby('Time2')
    
    pts = g4["points"].sum()
    fga = g4["points"].count()
    fg_perc = g4['MakeMiss'].mean()
    efg = 0.5*pts/fga
    
    nshots2 = g4['points'].count()

    axtop = fig6.add_subplot(211)
    axtop.plot(movingaverage(efg, winsize))
    
    axbot = fig6.add_subplot(212)
    axbot.plot(nshots2)

# annotate fig
axtop.set_title('All Teams, Grouped by # Shots')
axtop.legend(['Upper Third', 'Middle Third', 'Lower Third'], loc = 'lower right')

axbot.set_xlabel('Seconds Remaining in Quarter')
axbot.set_ylabel('Number of Shots')
axtop.set_ylabel('Shooting Efficiency (eFG)')

# set limits
axtop.set_xlim([5, 75])
axtop.set_ylim([0.25, 0.6])

axbot.set_xlim([5, 75])
axbot.set_ylim([0, 200])

# save figure
fig6.savefig('figure 6 -- tripiles - efg vs time.jpg')


# Show all plots if not up already. 
plt.show()




# -----------------------------------------------

# Basic eFG group by tripile (TFO agressiveness grouping) and epoch

g = bigdf.groupby(['tripile', 'epoch'])

g['points'].mean()/2

# eFG by epoch and tripile

#tripile  epoch
#1        1        0.358215
#         2        0.485294
#         3        0.470952
#         4        0.515409
#         5        0.518905
#2        1        0.335871
#         2        0.469820
#         3        0.490555
#         4        0.506726
#         5        0.498823
#3        1        0.361014
#         2        0.483374
#         3        0.495199
#         4        0.509937
#         5        0.500125


# FG% diffs, by epoch

#g['MakeMiss'].mean()
#Out[154]: 
#tripile  epoch
#1        1        0.309077
#         2        0.427992
#         3        0.410476
#         4        0.462741
#         5        0.465340
#2        1        0.298646
#         2        0.431532
#         3        0.442739
#         4        0.464574
#         5        0.458431
#3        1        0.318182
#         2        0.433901
#         3        0.443073
#         4        0.460705
#         5        0.452086
#Name: MakeMiss, dtype: float64

# #         3        0.470952
#         5        0.518905
# diff about 0.05 ~~ or about .1 Point Per Shot. A small dip, but not much.
# Value of last possession (0-5 seconds at shot time) about 0.35 eFG, or about 0.7 PPS.


# -----------
# Overall - not much change in eFG by epoch
#bigdf.groupby("epoch")['points'].mean()/2
#Out[157]: 
#epoch
#1        0.351872
#2        0.479423
#3        0.484006
#4        0.510653
#5        0.505984
#Name: points, dtype: float64


# -----------------------------------------------------------------------------

# Some basic comparisons, similar to teaml-level, and player-level calcs.

# Set filters, for Regions of Interest (epochs 3 and 5)
filter_epoch3 = bigdf["epoch"]==3
filter_epoch5 = bigdf["epoch"]==5

# Proportion of 3s, by epoch 
# Change in shot type may indicate change in shot selection, strategy

# shot proportion 
# number of two's per epoch (3,5)
# number of three's per epoch (3, 5)

shotcounts_byType_e3 = bigdf[filter_epoch3].groupby("shottype").size()
shotcounts_byType_e5 = bigdf[filter_epoch5].groupby("shottype").size()

proportion3s_e3 = shotcounts_byType_e3[3]/float(shotcounts_byType_e3[2]+shotcounts_byType_e3[3])
proportion3s_e5 = shotcounts_byType_e5[3]/float(shotcounts_byType_e5[2]+shotcounts_byType_e5[3])

print '\n'
print 'Summary Results: '
print '\n'
print 'Proportion of shots that are 3pt attempts, epoch 3: ', '%.2f' % proportion3s_e3
print 'Proportion of shots that are 3pt attempts, epoch 5: ', '%.2f' % proportion3s_e5
print '\n'


# --------------------

# Change in efg for 3s, league-wide

three_pt_perc = bigdf[bigdf['shottype'] == 3].groupby('epoch')['MakeMiss'].mean()
three_pt_n = bigdf[bigdf['shottype'] == 3].groupby('epoch')['MakeMiss'].count()
threeperc_e3 = three_pt_perc[3]
threeperc_e5 = three_pt_perc[5]
threeperc_diff = threeperc_e3 - threeperc_e5 

print '3pt fg %, epoch 3: ', '%.2f' % threeperc_e3
print '3pt fg %, epoch 5: ', '%.2f' % threeperc_e5
print 'Change in 3pt fg %: ', '%.2f' % threeperc_diff
print '\n'


# ------------------

# Change in league wide eFG, by epoch 

team_efg_e3 = bigdf[filter_epoch3]["points"].sum()*0.5/bigdf[filter_epoch3]["points"].count()
team_efg_e5 = bigdf[filter_epoch5]["points"].sum()*0.5/bigdf[filter_epoch5]["points"].count()
team_efg_diff = team_efg_e3 - team_efg_e5

print 'Overall eFG %, epoch 3: ', '%.2f' % team_efg_e3
print 'Overall eFG %, epoch 5: ', '%.2f' % team_efg_e5
print 'Change in Overall eFG %: ', '%.2f' % team_efg_diff
print '\n'

#threeperc_diff
#Out[65]: -0.035369015858490949
#
#team_efg_diff
#Out[66]: -0.02197808731244405


# -------------------------------------------------------


# problem in the orig data / nshots[3]?
# see prev code re: "blip" ... looks like too many shots coded at Time2 = 60 seconds.
# Compared to neighbors.
#
#nshots[58]
#Out[100]: 182
#
#nshots[59]
#Out[101]: 189
#
#nshots[60]
#Out[102]: 442   <------------- data coded "unevenly"
#
#nshots[61]
#Out[103]: 180
#
#nshots[62]
#Out[104]: 198


# -- 

""" So ... given that efg may drop about 0.05 (or 0.1 points per shot (PPS)), expected value (EV) of the first possession drops from around 1.0
to around 0.9. 

The value of that second shot (the extra possession gained in a 2-for-1)... then is probably around 0.7 (shots from 0-5 seconds remaining yielded 0.35 efg). 

Most of the value comes from denying your opponent the chance to run a 2-for-1. That 0.5 point swing * 2 = 1. It's a 0.5 point loss from one team 
executing it, and the potential 0.5 pt gain if the opponent successfully executes it. 

So a 0.1 PPS drop seems worth the payoff of a potential 1.0 point swing on the scenario as a whole. 

Team shooting may be impacted slightly, in the league as a whole, but it's not enough to cause a team to abandon the 2-for-1 strategy. 

The value of the first shot may be compromised, but it's likely not dropping far enough to give up a shot at an additional 0.7 points if they can get a second shot. 


...

Where it's more interesting, is which teams may be paying more of a cost to as they go for a 2-for-1. 

Segue into diff teams, team baseline efg rates, etc. 



"""



# --------------------
bigdf[bigdf['Tm']=='HOU'].groupby('epoch')['points'].mean()/2


#1        0.414729
#2        0.509524
#3        0.400000
#4        0.504950
#5        0.552885
#Name: points, dtype: float64





