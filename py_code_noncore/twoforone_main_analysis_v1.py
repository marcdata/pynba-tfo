
# Script for doing main, team-level analysis
# do per-minute analysis
# 

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

# -----------------------------------------------------------------------------

# Some prepatory basics

# All 30 teams
teamnames = ['ATL', 'BOS', 'BRK', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL',
    'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']   

# read in pickle file data from prev
outfilename = 'shots_allteams.pik'
bigdf = pickle.load(open(outfilename, 'rb'))

# -----------------------------------------------------------------------------

# per-team analysis 

# Do loop, and crank out some per-team calcs: efg, shot_rate_diffs, etc
# plot per team figs

# pre: bigdf exists, loaded

tfo_gooses = []
fg_deltas = []
efg_deltas = []
teams_out = []
filter_team = []

efgs_e3 = []
efgs_e5 = []
efgs_e3_threes = []
efgs_e5_threes = []

i=0
for tn in teamnames:   

    # filter by team // column = bigdf['Tm']
    filter_team = bigdf['Tm']==tn
    teamdf = bigdf[filter_team]
    
    # divide and analyze by 3pt shot type too
    
    filter3s = teamdf["shottype"]==3
    
    # use all shots
    grouped = teamdf.groupby("epoch")
    grouped_threesonly = teamdf[filter3s].groupby("epoch")
    
    # filter to look at 3pt FGA only
    # grouped = df2[filter3s].groupby("epoch")
    
    grouped["MakeMiss"].sum()
    grouped["MakeMiss"].count()
    
    fg_perc = grouped["MakeMiss"].sum()  / grouped["MakeMiss"].count()
    
    pts = grouped["points"].sum()
    fga = grouped["points"].count()
    
    efg = 0.5*pts/fga
    
    # same but for 3pt shots only

    fg_perc = grouped_threesonly["MakeMiss"].sum()  / grouped_threesonly["MakeMiss"].count()
    pts_3s = grouped_threesonly["points"].sum()
    fga_3s = grouped_threesonly["points"].count()
    efg_3s = 0.5*pts_3s/fga_3s

    print "Team: ", tn
    print "fg % and eFG% by epoch \n", "fg% \n", fg_perc, '\n', "efg \n", efg
    
    # shot rate
    # "shots a second" in the fga, aka // sum of freq counts of the bins in a hist of time2
    # proxy for how often a team goes for a 2for1 situation
    shot_rate = fga/[5, 23, 7, 25, 120]
    shot_rate = fga/[5, 22, 9, 24, 120]
    
    shot_rate = fga/[5, 22, 9, 24, 120]
    
    # shot rate division for alt epoch bins
    shot_rate = fga/[5, 22, 9, 29, 115]
    
    # Final shot rate bin sizes
    shot_rate = fga/[5, 22, 9, 29, 115]
    
    print "shot rate", '\n', shot_rate
    
    # calc summary stats for xy plot later
    # old method: base_shotrate = (shot_rate[4]+shot_rate[5])/2
    base_shotrate = shot_rate[5]
    
#    tfo_goose = (shot_rate[3]-shot_rate[4]+)/shot_rate[4]
    tfo_goose = (shot_rate[3]-base_shotrate)/base_shotrate
    tfo_efgdrop = (efg[3]-efg[5])
    tfo_fgpdrop = (fg_perc[3]-fg_perc[5])
    
    print "Team: ", tn, " TFO_Goose", tfo_goose, " EFG Change: ", tfo_efgdrop, " FGP Change: ", tfo_fgpdrop
    
    teams_out.append(tn)
    tfo_gooses.append(tfo_goose)
    efg_deltas.append(tfo_efgdrop)
    fg_deltas.append(tfo_fgpdrop)
    
    
    # Plot figure for eFG for team, by epoch (time remaining in qtr)
    fig = plt.figure(20+i)
    ax = fig.add_subplot(111)
    
    width = 0.5
    ax.bar([1,2,3,4,5], efg, width)

    ax.set_ylabel('eFG%')     #('Count of FGA')
    ax.set_xlabel('Seconds Remaining in Quarter')
    ax.set_title(tn)
    #ax.set_title('When Shots Happen At End of Quarters')
    xTickMarks = ['0-4', '5-26', '27-35', '36-60', '61-180']
    ax.set_xticks(np.arange(5)+1+(width/2))
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, fontsize=10)

    ax.set_xlim([0.5, 6])
    plt.show()
    
    # ending loop, increment manual counter (bc figure are broken)
    i = i+1
    
# end loop

# ------------------------------------------

# close some plots 
for fnum in np.arange(20, 50):
    plt.close(fnum)



# -----------------------------------------

# first cut calculations

# --------------------------------------------

# Generate table of team comparison points, efg_differnetial, etc

# Want: efg_diff, efg_diff_3ptshots_only
d = {'efg_diff': efg_deltas}
teamstats_df = pd.DataFrame(data = d, index = teams_out)
teamstats_df['Tm'] = teams_out
teamstats_df['efg_diff'] = efg_deltas





# ---------------------------------------------

# Summary charts

fig_team_scat = plt.figure(2)
fig_team_scat.clf()
ax_scat = fig_team_scat.add_subplot(111)

ax_scat.scatter(tfo_gooses, efg_deltas)

ax_scat.set_ylabel('Change in eFG%')     
ax_scat.set_xlabel('Change in Shooting Rate')

# add labels for each x,y point. Identify with team name (short name triple)
for label, x, y in zip(teams_out, tfo_gooses, efg_deltas):
    plt.annotate(
        label, 
        xy = (x, y), xytext = (5, 5), textcoords = 'offset points')

plt.show()

from scipy.stats.stats import pearsonr   

print pearsonr(tfo_gooses,efg_deltas)

# (-0.28226186560180239, 0.14559286204854066)
# (-0.30600024812464699, 0.1000656721856395)
# (-0.26979766638641567, 0.14934558828826472)
# various correlation results, varying epoch 3 bin limits slightly

# --------------------------------------------

# Generate table of team comparison points, efg_differnetial, etc
    










# ----------------------------------------------------------------------------------------

# per-minute analysis


g2 = bigdf.groupby('Time2')

pts = g2["points"].sum()
fga = g2["points"].count()
efg = 0.5*pts/fga
nshots = g2['points'].count()

fig_time = plt.figure(3)
ax_persec = fig_time.add_subplot(211)
ax_persec.bar(nshots.index, nshots.values, width = 1)

# filter_team = (bigdf['Tm'] == 'CLE') | (bigdf['Tm'] == 'HOU') | (bigdf['Tm'] == 'SAS') 

filter_threes_only = bigdf['shottype'] == 3
# ---

filter_noblip1 = bigdf['Time2'] < 60
filter_noblip2 = bigdf['Time2'] > 60
filter_noblip = filter_noblip1 | filter_noblip2

ax_persec2 = fig_time.add_subplot(212)
g3 = bigdf[filter_threes_only & filter_noblip].groupby('Time2')

pts = g3["points"].sum()
fga = g3["points"].count()
fg_perc = g3['MakeMiss'].mean()
efg = 0.5*pts/fga

nshots2 = g3['points'].count()

ax_persec2.bar(nshots2.index, nshots2.values, width = 1)

fig_persec_efg = plt.figure(4)
ax_efgsec = fig_persec_efg.add_subplot(111)
ax_efgsec.plot(nshots2.index, fg_perc)


    


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


# -------------------------------------------------------

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

print proportion3s_e3
print proportion3s_e5

# Need this in a figure 



# --------------------

# Change in efg for 3s, league-wide

three_pt_perc = bigdf[bigdf['shottype'] == 3].groupby('epoch')['MakeMiss'].mean()
three_pt_n = bigdf[bigdf['shottype'] == 3].groupby('epoch')['MakeMiss'].count()
threeperc_e3 = three_pt_perc[3]
threeperc_e5 = three_pt_perc[5]
threeperc_diff = threeperc_e3 - threeperc_e5 


# ------------------

# Change in league wide eFG, by epoch 

team_efg_e3 = bigdf[filter_epoch3]["points"].sum()*0.5/bigdf[filter_epoch3]["points"].count()
team_efg_e5 = bigdf[filter_epoch5]["points"].sum()*0.5/bigdf[filter_epoch5]["points"].count()
team_efg_diff = team_efg_e3 - team_efg_e5



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




# ------------------------

# Distance of shot by shot type. Distance of shot as indicator of shot quality.

bigdf.groupby(['shottype', 'epoch'])['distance'].mean()

#
#Out[13]: 
#shottype  epoch
#2         1         8.972719
#          2         8.026171
#          3         7.851894
#          4         8.013458
#          5         8.019370
#3         1        26.536856
#          2        25.055208
#          3        25.127188
#          4        24.834889
#          5        24.854966
#Name: distance, dtype: float64








