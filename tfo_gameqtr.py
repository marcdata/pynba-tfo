
# Look at how and whether teams end up with the last shot of the quarter. 
# 
# Reconstruct mini-game log, of shots. 
# Reshape data to support game-quarter type of analysis. 

# ------------------------------------------------------------------------------


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

#fn_team_table = 'team_report_table.pik'
#fn_player_table = 'player_report_table.pik'

# Issue with pickle compatibility? // Reading in using alt method, below. 
# team_report = pickle.load(open(fn_team_table, 'rb'))
# player_report = pickle.load(open(fn_player_table, 'rb'))

#team_report = pd.read_pickle(fn_team_table)
#player_report = pd.read_pickle(fn_player_table)

# -----------------------------------------------------------------------------

# Find unique game-quarters, also find and construct unique game id's. 

# --------

# ok so need fields, game, Date, Tm, Opp, Qtr, Time2 (and other shot data)

# But Date, Tm, and Opp basically constitute a unique game identifier.
# So reconstruct gameid key from that. 




# ok - so groupby 4-way id. 

temp = bigdf.groupby(['Date', 'Tm', 'Opp', 'Qtr'])

temp['points'].count()

# can use temp.indices to pull the right events. 
# or temp.indices.keys() // ('2015-02-23', 'MIN', 'HOU', '1st'),


# Example output: 
#
# ('2015-04-15',
#  'WAS',
#  'CLE',
#  '1st'): array([40358, 40359, 40360, 40361, 40362, 40363, 40364, 40365, 40366], dtype=int64),
# ('2015-04-15',
#  'WAS',
#  'CLE',
#  '2nd'): array([40367, 40368, 40369, 40370, 40371, 40372], dtype=int64),
# ('2015-04-15',
#  'WAS',
#  'CLE',
#  '3rd'): array([40373, 40374, 40375, 40376, 40377, 40378], dtype=int64)}


# Note: values in groupby.indices, e.g. 40375 .. indexes shot events in bigdf. 

gamekey =  ('2015-04-12', 'LAL', 'DAL', '1st')

# can get a gamekey with: temp.indices.keys()[0]

# will be a indexable list []
shotids_for_game = temp.indices[gamekey]

#Example usage: bigdf.iloc[2]

bigdf.iloc[19070]

# This: bigdf.iloc[shotids_for_game]

bigdf.iloc[shotids_for_game]

# returns a subset of the bigdf (for that game only). 

subset[subset['Time2'] < 60]

# But this is only grabbing shots for one team. // need to bring in both. 

# Grab partially re-ordered key, to access shotevents for the opposing team. 
altkey = gamekey[0], gamekey[2], gamekey[1], gamekey[3]

# Grab a different subset of shots. Combine both keys
subset = bigdf.iloc[temp.indices[gamekey]]
subset2 = bigdf.iloc[temp.indices[altkey]]

# need to concatenate the keys. 
subsetx = pd.concat([subset, subset2])

subset_lastmin = subsetx[subsetx['Time2'] < 60].sort(columns = 'Time2', ascending = False)

subset_last3eps = subsetx[subsetx['epoch'] < 4].sort(columns = 'Time2', ascending = False)

# ok, so now have the set of shots in the last minute for a game-qtr combo. 


# Can use something like this: 
subset_lastmin[subset_lastmin['Tm'] == 'LAL']['epoch'].value_counts()

subset_last3eps[subset_last3eps['Tm'] == 'LAL']['epoch'].value_counts()


# .. to get counts by epoch
# Then do frequency incidences, .. ie, if a team gets shot in epoch 3, are they
# more likely to get the last shot in epoch 1?

# --- also: right now, have twice as many keys as game-qtrs, bc keyed from
# perspective of each team. Need to account for it during loop, iteration.


# ------------------------------

# What data to pull from the game-qtr shot log:
# 1) Who got the laset shot? (Team A?, B?, home team? away?
# 2) Who got the shot in the TFO window, A, B, Both ?
# 3) If got shot in TFO window, did they end up with more shots overall?
# 4) Overall count of shots in last minute? (don't account for ORebs, for now)


# --- 

# Just set Team A, B, as whoever got the first shot in the last minute. Tm, or Opp field.

team_a = subset_last3eps.iloc[0]['Tm']
team_b = subset_last3eps.iloc[0]['Opp']

filter_tfo = subset_last3eps['epoch'] == 3
filter_epoch1 = subset_last3eps['epoch'] == 1

filter_team_a = subset_last3eps['Tm'] == team_a
filter_team_b = subset_last3eps['Tm'] == team_b

team_a_total_shots = subset_last3eps[filter_team_a & (subset_lastmin['epoch'] < 4)]['points'].count()
team_b_total_shots = subset_last3eps[filter_team_b & (subset_lastmin['epoch'] < 4)]['points'].count()

team_a_tfo_shots = subset_last3eps[filter_tfo & filter_team_a]['points'].count()
team_b_tfo_shots = subset_last3eps[filter_tfo & filter_team_b]['points'].count()

tfo_winner = ''
# Assign a winner status to tfo window, team a, b, neither, both. 
if team_a_tfo_shots > team_b_tfo_shots:
    tfo_winner = 'A'
elif team_b_tfo_shots > team_a_tfo_shots:
    tfo_winner = 'B'
elif team_b_tfo_shots == 0 and team_a_tfo_shots == 0:
    tfo_winner = 'N' # n for neither
elif team_a_tfo_shots > 0 and team_b_tfo_shots > 0:
    tfo_winner = 'both'

# Tally total points in the last minute.
# Free throws???



team_a_total_points = subset_last3eps[filter_team_a]['points'].sum()
team_b_total_points = subset_last3eps[filter_team_b]['points'].sum()

# Who got the last shot.
tm_last_shot = subset_last3eps.iloc[len(subset_last3eps)-1]['Tm']
if tm_last_shot == team_a:
    tm_last_shot = 'A'
else:
    tm_last_shot = 'B'


# Print out all of those variables we just calculated:

print 'team A total points: ', team_a_total_points
print 'team B total points: ', team_b_total_points

print 'TFO winner: ', tfo_winner
print 'Team with last shot: ', tm_last_shot





# ----------------------------

# Also, build a visualization of shots (by opposing teams) at end of qtr. 










def analyze_lastmin_shots(subset_df):
    #Pre: passing in shots in the last minute, in a dataframe subset
    # Post: passing back selected analysis points, TFO winner, last minute winner,
    # who got the last shot, etc. 
        
    team_a = subset_df.iloc[0]['Tm']
    team_b = subset_df.iloc[0]['Opp']
    
    filter_tfo = subset_df['epoch'] == 3
    filter_epoch1 = subset_df['epoch'] == 1
    
    filter_team_a = subset_df['Tm'] == team_a
    filter_team_b = subset_df['Tm'] == team_b
    
    team_a_total_shots = subset_df[filter_team_a]['points'].count()
    team_b_total_shots = subset_df[filter_team_b]['points'].count()
    
    team_a_tfo_shots = subset_df[filter_tfo & filter_team_a]['points'].count()
    team_b_tfo_shots = subset_df[filter_tfo & filter_team_b]['points'].count()
    
    tfo_winner = ''
    # Assign a winner status to tfo window, team a, b, neither, both. 
    if team_a_tfo_shots > team_b_tfo_shots:
        tfo_winner = 'A'
    elif team_b_tfo_shots > team_a_tfo_shots:
        tfo_winner = 'B'
    elif team_b_tfo_shots == 0 and team_a_tfo_shots == 0:
        tfo_winner = 'N' # n for neither
    elif team_a_tfo_shots > 0 and team_b_tfo_shots > 0:
        tfo_winner = 'both'
    
    # Tally total points in the last minute.
    # Free throws???
    
    # Just tally total points under last 40 seconds, last 3 epochs. Since TFO.
    team_a_total_points = subset_df[filter_team_a]['points'].sum()
    team_b_total_points = subset_df[filter_team_b]['points'].sum()
    
    # Who got the last shot.
    tm_last_shot = subset_df.iloc[len(subset_df)-1]['Tm']
    if tm_last_shot == team_a:
        tm_last_shot = 'A'
    else:
        tm_last_shot = 'B'
        
        
    # return multiple values as in a list
    # Return values: tfo winner, team with last shot, team a total points, team b total points, team a shot count, team b shot count
    return [tfo_winner , tm_last_shot, team_a_total_shots, team_b_total_shots, team_a_total_points, team_b_total_points  ]



# Ok, we have a function, loop over all the game-qtrs and find what happened:

# List of game-qtrs in here: 

# re-define temp, the groupby game-qtr structure. // Let's call it game_qtrs.

game_qtrs = bigdf.groupby(['Date', 'Tm', 'Opp', 'Qtr'])

game_qtr_results = pd.DataFrame(columns=('tfo_winner', 'tm_last_shot', 'team_a_total_shots', 'team_b_total_shots', 'team_a_total_points', 'team_b_total_points'))

# For now, drop gamekey from the resulting df



for gamekey in game_qtrs.indices.keys():

    # construct alt-key, for opposing team shots:
    
    # Grab partially re-ordered key, to access shotevents for the opposing team. 
    altkey = gamekey[0], gamekey[2], gamekey[1], gamekey[3]

    # Grab a different subset of shots. Combine both keys
    # Pulling the shots from bigdf dataframe of all shots.
    subset = bigdf.iloc[game_qtrs.indices[gamekey]]
    subset2 = bigdf.iloc[game_qtrs.indices[altkey]]
    
    # need to concatenate the keys. 
    subsetx = pd.concat([subset, subset2])
    # re-order into game-log type of format, by shot time.
    # subset_lastmin = subsetx[subsetx['Time2'] < 60].sort(columns = 'Time2', ascending = False)
    
    subset_last3ps = subsetx[subsetx['epoch'] < 4].sort(columns = 'Time2', ascending = False)

    # if subset_last3eps is empty, return null results
    if len(subset_last3ps) == 0:
        continue
    
    # Run mini-analysis on the subset of shots, gamelog
    
    # for now, just print out results:
    
    # print gamekey, ' :: ', analyze_lastmin_shots(subset_lastmin)

    # ok, so it works. Now save each game-qtr output to a data structure. 

    game_res = analyze_lastmin_shots(subset_last3ps)
    game_qtr_results.loc[len(game_qtr_results)+1] = game_res
    
    
# End loop

# Save as pickle file 

outfilename_qtrs = 'game_qtrs.pik'
pickle.dump(game_qtr_results, open(outfilename_qtrs, 'wb'))


# -------------------------------------
    
    
    
# Adjust, so know / count whether TFO window gave advantage after that point. 

# -----------











# that's the main comparison question.

pd.crosstab(game_qtr_results['tfo_winner'], game_qtr_results['tm_last_shot'])

## Table:
#A 2780 1744
#B 2 6
#N 1165 1475

# So team that wins TFO, gets the last shot of the quarter approx 2:1 times. (2780 vs 1744) / 2 .
# Or 1390 times vs 872 times. // 1.6 to 1.  or 3:2. 

# When neither team wins tfo_window, then it's pretty 50/50 who gets the last shot, 600 vs 700.

#  ----------

    
    # pd.crosstab(game_qtr_results['tfo_winner'], game_qtr_results['team_a_total_points'] > game_qtr_results['team_b_total_points'])

pd.crosstab(game_qtr_results['tfo_winner'], game_qtr_results['team_a_total_points'] > game_qtr_results['team_b_total_points'])

# But ajust total points down to just sum of points in epohcs 1-3.

pd.crosstab(game_qtr_results['tfo_winner'], game_qtr_results['team_a_total_shots'] > game_qtr_results['team_b_total_shots'])

# So team that wins TFO, ends up with more shots in the rest of the quarter approx 2:1 times. 3040 vs 1484. 

# --- 


#game_qtr_results.groupby(['tfo_winner'])['team_a_total_points'].sum()
#Out[49]: 
#tfo_winner
#A       7490
#B          4
#N       3190
#both     318
#Name: team_a_total_points, dtype: float64
#
#game_qtr_results.groupby(['tfo_winner'])['team_b_total_points'].sum()
#Out[50]: 
#tfo_winner
#A       3806
#B         20
#N       1540
#both     250
#Name: team_b_total_points, dtype: float64


# ---

# Data check:
# Total games in season: 1230 <= (82 * 15 team-pairs).
# Total game qtr's, 7342 divided by 6 = 1223 (so 42 total quarters without shots in the last 36 seconds).
# Divided by six because 3 quarters (dropping 4th), and 2 teams.  
# But game totals pretty much match up, so not missing any data. 
# ----
