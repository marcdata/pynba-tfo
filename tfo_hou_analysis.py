

""" Quick analysis of what's going on with Houston shooting. What's driving the difference 
between baseline shooting efficiency and epoch 3 shooting efficiency.

Focusing on splits between Harden vs Everybody Else.
Mostly all shot eFG% and 3pt shot eFG, and shot counts. 
Looked at changes in shooting distance towards the end, but not much changed.

Not really programmatic, just a script to run interactively. 

Output: tables, etc, printed out at the prompt.

"""

# -------------------------------------------------------------------------

# Pre: bigdf dataset loaded already. 

# -------------------------------------------------------------------------

# set up filters for Harden, non-Harden splits. Harden is one player for Houston.

filter_hou = bigdf['Tm'] == 'HOU'

subset_hou = bigdf[filter_hou]

filter_harden = subset_hou['shooter'] == 'J.Harden'
filter_notharden = subset_hou['shooter'] != 'J.Harden'

filter_3pt_attempts = subset_hou['shottype'] == 3


# ok, filters set 

# groupby epoch, do simple calcs. 

# how shooters besides Harden do, in epochs
grp = subset_hou[filter_notharden & filter_3pt_attempts].groupby('epoch')

# Print out a mini-report

print "\n Houston, non-Harden,3-pt,  mean points by epoch:"
print grp['points'].mean()
print "\n non-Harden, 3-pt, shot counts by epoch:"
print grp['points'].count()
print "\n non-Harden all shots, mean points per shot, by epoch: "
print subset_hou[filter_notharden].groupby('epoch')['points'].mean()
print "\n non-Harden all shots, shot counts by epoch: "
print subset_hou[filter_notharden].groupby('epoch')['points'].count()
print "\n"

# how Harden compares, by epochs

print "\n Harden, 3-pt, mean points by epoch:"
print subset_hou[filter_harden & filter_3pt_attempts].groupby('epoch')['points'].mean()
print "\n Harden, 3-pt shot counts by epoch:"
print subset_hou[filter_harden & filter_3pt_attempts].groupby('epoch')['points'].count()
print "\n Harden all shots, mean points per shot, by epoch: "
print subset_hou[filter_harden].groupby('epoch')['points'].mean()
print "\n Harden, all shot counts by epoch:"
print subset_hou[filter_harden].groupby('epoch')['points'].count()
print "\n"

# 3 pt shots specifically is most of the differnece.
# That's basically the story. 
# Harden 3pt shooting:
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


# subset_hou[filter_notharden & filter_3pt_attempts & (subset_hou['epoch'] == 3)]['shooter'].unique()

# array(['T.Ariza', 'J.Terry', 'T.Daniels', 'F.Garcia', 'N.Johnson',
#       'P.Beverley', 'D.Motiejunas', 'C.Brewer', 'J.Smith'], dtype=object)



