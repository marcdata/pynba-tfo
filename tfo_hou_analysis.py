



filter_hou = bigdf['Tm'] == 'HOU'

subset_hou = bigdf[filter_hou]

filter_harden = subset_hou['shooter'] == 'J.Harden'
filter_notharden = subset_hou['shooter'] != 'J.Harden'

filter_3pt_attempts = subset_hou['shottype'] == 3


# ok, filters set 

# groupby epoch, do simple calcs. 

# how shooters besides Harden do, in epochs
grp = subset_hou[filter_notharden & filter_3pt_attempts].groupby('epoch')

grp['points'].mean()
grp['points'].count()

# how Harden compares, by epochs

subset_hou[filter_harden & filter_3pt_attempts].groupby('epoch')['points'].mean()
subset_hou[filter_harden & filter_3pt_attempts].groupby('epoch')['points'].count()

# 3 pt shots specifically

# That's basically the story. 

# epoch
#1    1.200000
#2    1.285714
#3    1.000000
#4    0.882353
#5    1.034483
#Name: points, dtype: float64
#
# -- Non-Harden Shooters (drop to .46 efficiency)
#In [33]: grp['points'].mean()
#Out[33]: 
#epoch
#1    0.717391
#2    1.258065
#3    0.468750
#4    1.232143
#5    1.093220

# subset_hou[filter_harden & filter_3pt_attempts & (subset_hou['epoch'] == 3)]

# subset_hou[filter_harden & filter_3pt_attempts & (subset_hou['epoch'] == 3)].groupby('MakeMiss')['distance'].mean()
#Out[44]: 
#MakeMiss
#0    26.1
#1    25.0
#Name: distance, dtype: float64


# Harden, misses on threes were about 1 ft farther than for Makes. 

# For other-than-Harden
#MakeMiss
#0    24.592593
#1    25.400000
#Name: distance, dtype: float64


# Distance was a non-factor. Misses were actually closer than Makes.













