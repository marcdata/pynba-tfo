

# 


labels = df.Name.values
xvals = df.OffEff.values
yvals = df.DefEff.values

#

# plt.annotate('test2', xy=(105,105))

offset = 1

plt.annotate(labels[1], xy=(xvals[1], yvals[1]))
show()


offset = 0.3;

for label, x, y in zip(labels, xvals, yvals):
    plt.annotate(
        label, 
        xy = (x, y),
        xytext=(x+offset, y+offset))


plt.show()



