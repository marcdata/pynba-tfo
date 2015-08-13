

# ----------------------------

import pandas as pd
import numpy as np
import pickle

# ----------------------------

# read in pickle file data from prev
outfilename = 'shots_allteams.pik'
bigdf = pickle.load(open(outfilename, 'rb'))

active_players_fn = 'activeshooters.pik'
activeshooters, asfilt = pickle.load(open(active_players_fn, 'rb'))


# ----------------------------


# Per player level summary report. 2-pts vs 3-pts, and shot distance
# 1 set a filter for the player
# 2 apply similar logic as prev to generate stats
# 3 print out


# in param df_shots == bigdf from prev (a dataframe full of pershot data

def tfo_player_report(plyr_name, df_shots):
    plyrdf = df_shots[df_shots['shooter']==plyr_name]

    print plyr_name
    print len(plyrdf)
        
    filter_epoch3 = plyrdf["epoch"]==3
    filter_epoch5 = plyrdf["epoch"]==5
    filter_shottype2 = plyrdf["shottype"]==2
    filter_shottype3 = plyrdf["shottype"]==3
    
    shotcounts_byType_e3 = plyrdf[filter_epoch3].groupby("shottype").size()
    shotcounts_byType_e5 = plyrdf[filter_epoch5].groupby("shottype").size()
    
    # Count of shots in epoch 3 (two-for-one situation)
    fga_e3_n = plyrdf[filter_epoch3]['shottype'].count()
               
    # If shotcounts_byType_e3 not populated, return NaN
    # Some types of players won't have enough observations to support this calculation.        
    try:
        proportion3s_e3 = shotcounts_byType_e3[3]/float(shotcounts_byType_e3[2]+shotcounts_byType_e3[3])
        proportion3s_e5 = shotcounts_byType_e5[3]/float(shotcounts_byType_e5[2]+shotcounts_byType_e5[3])
        proportion3s_diff = proportion3s_e3 - proportion3s_e5
    
    except:
        proportion3s_e3 = np.nan
        proportion3s_e5 = np.nan
        proportion3s_diff = np.nan

    plyr_efg_e3 = plyrdf[filter_epoch3]["points"].sum()*0.5/plyrdf[filter_epoch3]["points"].count()
    plyr_efg_e5 = plyrdf[filter_epoch5]["points"].sum()*0.5/plyrdf[filter_epoch5]["points"].count()
    plyr_efg_diff = plyr_efg_e3 - plyr_efg_e5

    shotdist_e3 = plyrdf[filter_epoch3 & filter_shottype2]["distance"].mean()
    shotdist_e5 = plyrdf[filter_epoch5 & filter_shottype2]["distance"].mean()
    
    # calc change in 3 pt shooting percentage
    
    
    # print out mini-report
    
    print 'shot distance, epoch 3: ', shotdist_e3
    print 'shot distance, epoch 5: ', shotdist_e5

    print "Proportion of 3s in epoch 3: ", proportion3s_e3
    print "Proportion of 3s in epoch 5: ", proportion3s_e5
    
    print "eFG in epoch 3: ", plyr_efg_e3
    print "eFG in epoch 5: ", plyr_efg_e5    
    
    # Again, for some players, 3pt calculations aren't going to work.
    try:
        three_pt_perc = plyrdf[plyrdf['shottype'] == 3].groupby('epoch')['MakeMiss'].mean()
        three_pt_n = plyrdf[plyrdf['shottype'] == 3].groupby('epoch')['MakeMiss'].count()
        threeperc_e3 = three_pt_perc[3]
        threeperc_e5 = three_pt_perc[5]
        threeperc_diff = threeperc_e3 - threeperc_e5 
    except:
        three_pt_n = [np.nan, np.nan, np.nan, np.nan, np.nan]
        threeperc_diff = np.nan
        threeperc_e3 = np.nan
        threeperc_e5 = np.nan
        
    #ok, kind of busy with all the variables, but we're reporting out each one, so it's ok
    
    print "3pt %, epoch 3: ", "%.2f" % threeperc_e3
    print "3pt %, epoch 5: ", "%.2f" % threeperc_e5
    print "3pt %, diff: ", "%.2f" % threeperc_diff
    print "3pt (n), epoch 3: ", "%.2f" % three_pt_n[3]
    
    # print crosstab(plyrdf['distance'], plyrdf['epoch'])
    
    
    
    
    
    
    
    
    
    # Calc differences in shot rate 
    
    # fga counts. We're just getting a count here, so counting on "points" column, but could count on most any.
    plyr_grouped = plyrdf.groupby("epoch")
    fga = plyr_grouped["points"].count()
    
    # Final shot rate bin sizes
    shot_rate = fga/[5, 22, 9, 29, 115]
    
    # calc shooting rate, shots/min (over all the season)
    base_shotrate = shot_rate[5]
    
    # shot rate diff, proportional based on epoch5 (in base_shotrate)
    shotrate_diff = (shot_rate[3]-base_shotrate)/base_shotrate
    
    d = {'fga_e3_n': fga_e3_n, 'threeperc_e3': threeperc_e3, 'threeperc_e5': threeperc_e5, 'threeperc_diff': threeperc_diff, 'three_pt_n': three_pt_n[3], 
        'prop_threes_e3': proportion3s_e3, 'prop_threes_e5': proportion3s_e5, 'prop_threes_diff': proportion3s_diff,
        'plyr_efg_e3': plyr_efg_e3 , 'plyr_efg_e5': plyr_efg_e5, 'plyr_efg_diff': plyr_efg_diff,
        'shotrate_base': base_shotrate , 'shotrate_diff': shotrate_diff}
    plyr_out_df = pd.DataFrame(data = d, index = pd.Series(plyr_name))
    
    return plyr_out_df
    

# --- Main here 

player_report = pd.DataFrame()

shortlist = ['J.Harden', 'R.Westbrook', 'G.Hayward', 'L.Williams', 'J.Wall', 'J.Smith', 'L.James']

for p in shortlist:
    print p
    if p == 'J.Harden':
        print 'found it'
        
# throwing errors when players dont have enough 3 pt shot attempts, for some. Skipping for now. 
#if p != 'L.Aldridge' and p != 'C.Kaman' and p != 'A.Horford' and p != 'H.Sims' and p != 'D.Waiters': < --- list of players w NaN's

for p in activeshooters.index:
    plyrdf = tfo_player_report(p, bigdf)
    player_report = pd.concat([player_report, plyrdf])


# Select only a few main columns here

player_report[['fga_e3_n', 'plyr_efg_e3', 'plyr_efg_e5', 'plyr_efg_diff', 'prop_threes_diff', 'threeperc_diff']]


# ------------------------------------------

# Save to file / pickled. 
 
# Save new team table to pickle file
outfilename = 'player_report_table.pik'
pickle.dump(player_report, open(outfilename, 'wb'))

# ------------------------------------------

# ------


# main

# Prior version fo data / table format function def. 
#
#plyrframe = tfo_player_report('L.James', bigdf)
#
#
#plyrframe[plyrframe['distance'] < 6].groupby('epoch').mean()
#
## part of it is that LBJ becomes average at the rim, forced shots ?
#
## not hitting anything from long range
#
#plyrframe[plyrframe['distance'] > 20].groupby('epoch')['points'].sum()
#
## this
#plyrframe[plyrframe['shottype'] == 3].groupby('epoch').mean()
#
## boil down to just 3 pt shooting percentage, change in 
#
#plyrframe[plyrframe['shottype'] == 3].groupby('epoch')['MakeMiss'].mean()

# 

#
#
#bigdf[bigdf['shottype'] == 3].groupby('epoch')['MakeMiss'].mean()
#Out[260]: 
#epoch
#1        0.219833
#2        0.359404
#3        0.335430
#4        0.377193
#5        0.376858
#Name: MakeMiss, dtype: float64
#
## on aggregate, epoch makes no diff to 3pt %
#


# -----------------


# shortlist = ['J.Harden', 'R.Westbrook', 'G.Hayward', 'L.Williams', 'J.Wall', 'J.Smith', 'L.James']


# -----------------

# Dig into Houston case

hou_players = bigdf[bigdf['Tm'] == 'HOU']['shooter'].value_counts()

hou_players = ['J.Harden', 'J.Smith', 'C.Brewer', 'J.Terry', 'T.Ariza', 'D.Motiejunas', 'P.Beverley', 'T.Jones', 'D.Howard']

hou_report = pd.DataFrame()

for p in hou_players:
    houdf = tfo_player_report(p, bigdf)
    hou_report = pd.concat([hou_report, houdf])


# Select only a few main columns here

hou_report[['fga_e3_n', 'plyr_efg_e3', 'plyr_efg_e5', 'plyr_efg_diff', 'prop_threes_diff', 'threeperc_e5', 'threeperc_e3', 'threeperc_diff', 'shotrate_base', 'shotrate_diff']]








