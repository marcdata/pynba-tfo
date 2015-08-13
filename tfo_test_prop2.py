
# Some combination code / results file. 
# Basically intput / output from interactive Canopy session. 

# Looking at diff in shooting effiency (eFG) at tripile level (ie, teams in thirds)

g = bigdf.groupby(['tripile', 'epoch'])

g
Out[145]: <pandas.core.groupby.DataFrameGroupBy object at 0x0000000026AAADA0>

g['points'].mean()
Out[146]: 
tripile  epoch
1        1        0.716429
         2        0.970588
         3        0.941905
         4        1.030819
         5        1.037810
2        1        0.671743
         2        0.939640
         3        0.981110
         4        1.013453
         5        0.997646
3        1        0.722028
         2        0.966748
         3        0.990398
         4        1.019874
         5        1.000251
Name: points, dtype: float64

g['points'].mean()/2
Out[147]: 
tripile  epoch
1        1        0.358215
         2        0.485294
         3        0.470952
         4        0.515409
         5        0.518905
2        1        0.335871
         2        0.469820
         3        0.490555
         4        0.506726
         5        0.498823
3        1        0.361014
         2        0.483374
         3        0.495199
         4        0.509937
         5        0.500125
Name: points, dtype: float64







bigdf[bigdf['tripile'] == 1]][['MakeMiss'].groupby(['epoch']).mean()
  File "<ipython-input-148-28031306d114>", line 1
    bigdf[bigdf['tripile'] == 1]][['MakeMiss'].groupby(['epoch']).mean()
                                ^
SyntaxError: invalid syntax
 

bigdf[bigdf['tripile'] == 1].groupby(['epoch'])['MakeMiss'].mean()
Out[149]: 
epoch
1        0.309077
2        0.427992
3        0.410476
4        0.462741
5        0.465340
Name: MakeMiss, dtype: float64

bigdf[bigdf['tripile'] == 1].groupby(['epoch'])['MakeMiss'].sum()

Out[150]: 
epoch
1         412
2         422
3         431
4        1006
5        3766
Name: MakeMiss, dtype: int64

bigdf[bigdf['tripile'] == 1].groupby(['epoch'])['MakeMiss'].count()
Out[151]: 
epoch
1        1333
2         986
3        1050
4        2174
5        8093
Name: MakeMiss, dtype: int64


# ------------

bigdf[bigdf['tripile'] == 1].groupby(['epoch'])['MakeMiss'].sum()

bigdf[bigdf['tripile'] == 1].groupby(['epoch'])['MakeMiss'].count()

# hard create frequency matrix 

shotsmat = np.array([[431, 3766], [1050, 8093 ]])

stats.chi2_contingency(shotsmat)

# Chi2_contingency returned: 
# chi = 4.1800827919127945,
# pval = 0.040901702609794199,

# So yes, p at .05 then is sigdiff in ratio of makes/total.

# calculating as raw FG percent, because chi2 is defined for ratio counts (not weighted means). 









# --------------

# Another QA item // re the data bump -- make sure it's not a coding translation error 

a = bigdf[bigdf['Time2'] == 60][['Time', 'Time2']]

#unique(a['Time'])
#Out[146]: 
#array(['1:00.0'], 
#      dtype='|S6')

# All Time2 == 60 items look like they were originally coded at 1:00... so looks like it's from the input. 

# ---------------------



