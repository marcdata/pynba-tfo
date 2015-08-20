

# TFO Story Figures 
# 
# Go ahead and collect subset of figures, for displaying main points of results, analysis. 

# This has some more annotation and formatting to it. So it's meant to be run 
# after all the data has been cycled thru, calculations made, etc. Offsets, etc
# will be dependent on the values. 

# Imports, Load in bigdf dataset.

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

fn_team_table = 'team_report_table.pik'
fn_player_table = 'player_report_table.pik'

# Issue with pickle compatibility? // Reading in using alt method, below. 
# team_report = pickle.load(open(fn_team_table, 'rb'))
# player_report = pickle.load(open(fn_player_table, 'rb'))

team_report = pd.read_pickle(fn_team_table)
player_report = pd.read_pickle(fn_player_table)

# -----------------------------------------------------------------------------

# Read in optional other tables ? 

# prepped team_report, plyr_report ???







# -----------------------------------------------------------------------------



# Figure 11: Basic shot distribution histogram. And SAS as example team. 

# Plot histogram of all shots, all teams, last 1 min

fig = plt.figure(11)
fig.clf()
axtop = fig.add_subplot(211)

bigdf["Time2"].hist(bins = 180, range=[0, 180], ax = axtop)

# Labels and xlimits
axtop.set_ylabel('Number of Shot Attempts')     #('Count of FGA')
axtop.set_xlabel('Time Remaining in Quarter (s)')
axtop.set_title('Distribution of Field Goal Attempts At End of Quarters \n All Teams ')

#fig.suptitle('Distribution of Field Goal Attempts At End of Quarters \n All Teams ')
#axtop.set_title('All Teams')

axtop.set_xlim([-0.5, 58.5])

# Annotate some explanatory text.
axtop.annotate('Increase in shots taken', xy=(33, 410), xytext=(38, 900),
            arrowprops=dict(facecolor='black', width = 1, shrink=0.05))

# Do similar, only using SAS as example team. Place in lower subplot.

axbot = fig.add_subplot(212)

bigdf[bigdf['Tm'] == 'SAS']['Time2'].hist(bins = 180, range=[0, 180], ax = axbot)

# Labels and xlimits
axbot.set_ylabel('Number of Shot Attempts')     #('Count of FGA')
axbot.set_xlabel('Time Remaining in Quarter (s)')
# axbot.set_title('Team: San Antonion Spurs ')

# axbot.legend(['Team: San Antonio Spurs'])
axbot.text(35, 45, 'Example Case: San Antonio Spurs')

axbot.set_xlim([-0.5, 58.5])

# Annotate some explanatory text.
# axbot.annotate('Use to establish lower cutoff in time', xy=(28, 21), xytext=(15, 35),
#            arrowprops=dict(facecolor='black', width = 1, shrink=0.05))

axbot.annotate('Sharper limits near t = 28, t = 36', xy=(28, 21), xytext=(15, 35),
    arrowprops=dict(facecolor='black', width = 1, shrink=0.05))

plt.show()

# Save figure

fig.savefig('out_figures/figure11.jpg')

# -------------------------------------------------

# Figure 12: Example Case: Houston. 
# 
# Plot both shot distribution in time, and eFG by epoch

fig = plt.figure(12)
fig.clf()
axtop = fig.add_subplot(211)

bigdf[bigdf['Tm'] == 'HOU']['Time2'].hist(bins = 180, range=[0, 180], ax = axtop)

# Labels and xlimits
axtop.set_ylabel('Number of Shot Attempts') 
axtop.set_xlabel('Time Remaining in Quarter (s)')
axtop.set_title('Example Case: Houston Rockets')

axtop.set_xlim([-0.5, 58.5])
axtop.grid(b=False)

# Annotate figure -- why are we showing this example?

axtop.annotate('Increased # of shots... \n but decreased shooting efficiency', xy=(31, 21), xytext=(33, 37),
    arrowprops=dict(facecolor='black', width = 1, shrink=0.05))
# Bottom plot: eFG by time (in epochs).

axbot = fig.add_subplot(212)

hou_efg = bigdf[bigdf['Tm'] == 'HOU'].groupby('epoch')['points'].mean()/2

width = 0.5
axbot.bar([1,2,3,4,5], hou_efg, width)

axbot.set_ylabel('eFG%')
axbot.set_xlabel('Seconds Remaining in Quarter')

# Label tick marks for time periods.

xTickMarks = ['0-4', '5-26', '27-35', '36-65', '66-180']
axbot.set_xticks(np.arange(5)+1+(width/2))
xtickNames = axbot.set_xticklabels(xTickMarks)
plt.setp(xtickNames, fontsize=10)

axbot.set_xlim([0.5, 6])
# axbot.set_ylim([0, 0.8])

plt.show()

# Save figure

fig.savefig('out_figures/figure12_HOU.jpg')

# -------------------------------------------------

# Figure 15

# Team shotrate, efg, efg_diff comparisons. 

fig = plt.figure(15)
fig.clf()
axleft = fig.add_subplot(1,2,1)

# first plot: shotrate_diff vs efg_diff

axleft.plot(team_report['shotrate_diff'], team_report['team_efg_diff'], '.')
# add regression overlay
# in this case - no regression overlay bc r is too low (marginal)
# tfo_extra.add_reg_to_axis(team_report['shotrate_diff'], team_report['team_efg_diff'], axleft)

print pearsonr(team_report['shotrate_diff'], team_report['team_efg_diff'])

# Add labels, etc

axleft.set_xlabel('Change in Shot Rate (shots/min), proportional')
axleft.set_ylabel('Change in eFG %')
fig.suptitle('What Drives Team-Level Shooting Changes')

# second plot: # efg_e5 vs efg_diff

axright = fig.add_subplot(1,2,2)

axright.plot(team_report['team_efg_e5'], team_report['team_efg_diff'], '.')

# add regression overlay
tfo_extra.add_reg_to_axis(team_report['team_efg_e5'], team_report['team_efg_diff'], axright)
r_val, p_val = pearsonr(team_report['team_efg_e5'], team_report['team_efg_diff'])
axright.text(0.55, 0.1, 'r = '+ "{:.2f}".format(round(r_val, 2))) 

# add labels, titles, etc
# Changeto: percentage point

axright.set_xlabel('Baseline eFG %')
axright.set_ylabel('Change in eFG %')


# Set y-axis limits equal to each other, for comparison. 
matching_ylims = [-0.20, 0.15]
axright.set_ylim(matching_ylims)
axleft.set_ylim(matching_ylims)
plt.show()

# Highlight a couple specific teams? (HOU, SAS, MIA, CLE, GSW ?)

some_teams = ['HOU', 'SAS', 'CLE', 'GSW', 'MIA']
some_offsets = [(10, 10), (10, -10), (10, 10), (-10, 10), (10, 10)]

offset_dict = {'HOU':(10, 10), 'SAS':(10, -10), 'CLE':(10, 10), 'GSW':(-15, 10), 'MIA':(10, 10)}
offsets_left = {'HOU':(10, 10), 'SAS':(10, 10), 'CLE':(-30, 0), 'GSW':(-30, -15), 'MIA':(10, 10)}

for t in some_teams:
    # print "doing somthing for team: ", t
    # Get x,y values from the dataframe (and the plot)
    x,y = team_report[team_report.index==t]['team_efg_e5'][0], team_report[team_report.index==t]['team_efg_diff'][0]

    # print "x,y values: ", x, y
    # Plot and annotate.
    axright.scatter(x,y, s=80, marker='o', facecolors='none')
    axright.annotate(t, xy = (x,y), xytext=offset_dict[t], textcoords='offset points')
    
    # Annotate left axis also
    
    xleft,yleft = team_report[team_report.index==t]['shotrate_diff'][0], team_report[team_report.index==t]['team_efg_diff'][0]
    axleft.scatter(xleft,yleft, s=80, marker='o', facecolors='none')
    # Annotate using tag p (for player code, and the corresponding offset coords in the offset dict/mapping. 
    axleft.annotate(t, xy = (xleft,yleft), xytext=offsets_left[t], textcoords='offset points')

plt.show()

# Save Figure

fig.savefig('out_figures/figure15_team_correlations.jpg')

# --------------------------------------------------------


# Individual level: shotrate, efg, efg_diff comparisons. 
# Similar to above, but diff level. 

fig = plt.figure(16)
fig.clf()
axleft = fig.add_subplot(1,2,1)

# first plot: shotrate_diff vs efg_diff

axleft.plot(player_report['shotrate_diff'], player_report['plyr_efg_diff'], '.')
# add regression overlay
# in this case - no regression overlay bc r is too low (marginal)
# tfo_extra.add_reg_to_axis(team_report['shotrate_diff'], team_report['team_efg_diff'], axleft)

print pearsonr(player_report['shotrate_diff'], player_report['plyr_efg_diff'])

# Add labels, etc

axleft.set_xlabel('Change in Shot Rate (shots/min), proportional')
axleft.set_ylabel('Change in eFG %')
fig.suptitle('What Drives Player-Level Shooting Changes')

# second plot: # efg_e5 vs efg_diff

axright = fig.add_subplot(1,2,2)

axright.plot(player_report['plyr_efg_e5'], player_report['plyr_efg_diff'], '.')

# add regression overlay
tfo_extra.add_reg_to_axis(player_report['plyr_efg_e5'], player_report['plyr_efg_diff'], axright)
r_val, p_val = pearsonr(player_report['plyr_efg_e5'], player_report['plyr_efg_diff'])
# xy positioning of text here depends on the actual results: tweak for formatting, prettiness.
axright.text(0.61, 0.4, 'r = '+ "{:.2f}".format(round(r_val, 2))) 

# add labels, titles, etc
axright.set_xlabel('Baseline eFG %')
axright.set_ylabel('Change in eFG %')

# Set y-axis limits & set to match right and left axes.
# This matching_ylis value seems decent for both left and right plots. 

matching_ylims = [-0.4, 0.5]
axright.set_ylim(matching_ylims)
axleft.set_ylim(matching_ylims)
plt.show()

# Highlight a few specific players. (L.James, J.Harden, S.Curry, S.Blake ?)

highlight_players = ['L.James', 'J.Harden', 'S.Curry', 'S.Blake']
# player_offsets = [(10, 10), (10, -10), (10, 10), (-10, 10), (10, 10)]

player_offset_dict = {'L.James':(-20, 10), 'J.Harden':(10, 10), 'S.Curry':(-10, 10), 'S.Blake':(-30, 10)}
player_offsets_left = {'L.James':(10, 10), 'J.Harden':(10, 10), 'S.Curry':(-50, 5), 'S.Blake':(-30, 10)}

for p in highlight_players:
    # print "doing somthing for player: ", p
    # Get x,y values from the dataframe (and the plot)
    x,y = player_report[player_report.index==p]['plyr_efg_e5'][0], player_report[player_report.index==p]['plyr_efg_diff'][0]

    # print "x,y values: ", x, y
    # Plot and annotate.
    axright.scatter(x,y, s=80, marker='o', facecolors='none')
    # Annotate using tag p (for player code, and the corresponding offset coords in the offset dict/mapping. 
    axright.annotate(p, xy = (x,y), xytext=player_offset_dict[p], textcoords='offset points')
    
    # Annotate left axis also
    
    xleft,yleft = player_report[player_report.index==p]['shotrate_diff'][0], player_report[player_report.index==p]['plyr_efg_diff'][0]
    axleft.scatter(xleft,yleft, s=80, marker='o', facecolors='none')
    # Annotate using tag p (for player code, and the corresponding offset coords in the offset dict/mapping. 
    axleft.annotate(p, xy = (xleft,yleft), xytext=player_offsets_left[p], textcoords='offset points')
    

plt.show()

# Save Figure

fig.savefig('out_figures/figure16_indivlevel.jpg')

# --------------------------------------------------------









# Some numbers, numerical results, not displayed graphically.

# For the top (x) shooters by # shots in Epoch 3, eFG drops 0.04 percentage points. 

player_report['plyr_efg_diff'].mean()
# Out[211]: -0.043870995358532783





