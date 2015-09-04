
""" 
Look at per-second 3 pt percentage, within the two-for-one window. 
Correlate and see if there's a drop-off in time. 
"""
    
    
    
# pre: data exists, loaded into memory. 

# -------------

# ----------


grp_time = bigdf.groupby('Time2')

# set filter, within 25-40 seconds

filter_window = (bigdf['Time2'] < 41) & (bigdf['Time2'] > 26)

filter_threes_only = bigdf['shottype'] == 3



# check filter for window time constraints. 

bigdf[filter_window]['Time2'].describe()

# Calculate per-second 3pt % (or mean points, efg, which is just mean of 'points')
bigdf[filter_window & filter_threes_only].groupby('Time2')['points'].mean()

y = bigdf[filter_window & filter_threes_only].groupby('Time2')['points'].mean()
x = y.index

tfo_extra.plot_scatter_with_reg_overlay(x, y.values/2, figurenum = 1051, overlay = True)

pearsonr(x,y)

# r, pval = (0.33536333291710885, 0.22172500228048758)
# so... not that correlated with decreasing efficiency in time, during TFO window. 
# time window 26-40

# alt calc: (0.39257413965252602, 0.16500560251097346)
# Still no, time window = 27-40.


# --------

# alt metrics:

# Calculate per-second shot distance
bigdf[filter_window & filter_threes_only].groupby('Time2')['distance'].mean()
## Basically flat: 
#27    25.061538
#28    25.138298
#29    25.080460
#30    25.066667
#31    25.230769
#32    25.267327
#33    25.019802
#34    25.069767
#35    25.174419
#36    24.815385
#37    24.716216
#38    25.119403
#39    24.946429
#40    24.901639

# ---
# Per second shot distance - for two's.
bigdf[filter_window & (filter_threes_only * -1)+1].groupby('Time2')['distance'].mean()
# Still flat, beteen 7 and 8.5 ft usually.


