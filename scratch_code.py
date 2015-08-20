

# Scratch --- spare code -- removed code 


# Output HTML Table 

# Format to two decimal places

pd.options.display.float_format = '{:.2f}'.format

plyr_html_table = player_report.to_html()





# ------------------------------------------------------------------------------


# Nah - keep in tfo_allplayers. 

# Some basic comparisons, similar to teaml-level, and player-level calcs.

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

# ----

# should - "league wide" comparisons only be done for active shooters?

# pro: keep focus on ppl active in TFO
# con: muddles concept of "league wide" analysis.....



