# Example to just do simple linear regression. 

# get a simple set of x,y type data

a = [1, 2, 3, 4, 5, 6, 7]
b = [2, 1.7, 2.5, 4.3, 5.1, 4, 7.5]

fig = plt.figure(1)
fig.clf()

plt.plot(a, b, 'o')

# do simple linear fit
p = numpy.polyfit(a, b, 1)

# In [41]: p
# Out[41]: array([ 0.84642857,  0.48571429])

xfit = arange(1,8)
yfit = p[0]*xfit+p[1]

# plot overlay of 
plt.plot(xfit, yfit, 'r')

plt.axes().set_xlim([0, 9])
plt.axes().set_ylim([0, 9])


# save fig as image file
plt.savefig("example_corr.jpg")


# calculate pearsonr for comparison

rval, pval = pearsonr(a, b)
print 'rval, pval:', rval, pval


# --------------------------

# Make sure the diff version of the code match. 

#
#slope, intercept, r_val, p_val, std_err = stats.linregress(plyr_efg_e5.sort_index(), plyr_efg_diff.sort_index())
#
#
#slope
#Out[109]: -1.6326266657195507
#
#intercept
#Out[110]: 0.80650575726657425
#
#p = np.polyfit(plyr_efg_e5.sort_index(), plyr_efg_diff.sort_index(), 1)
#
#p
#Out[112]: array([-1.63262667,  0.80650576])
#
# So: params from polyfit agree with the params from the stats.linregress. good. 
# So, looks like either way, it works. 

# --------------------------

