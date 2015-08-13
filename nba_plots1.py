
# script to import and plot out various nba data, for testing, learning



import pandas
import matplotlib.pyplot as plt

from pandas import read_csv
from urllib import urlopen
# page = urlopen("http://econpy.pythonanywhere.com/ex/NFL_1979.csv")
# page = urlopen("file:c:")

filepath = r'c://Users/Marc/Documents/nbadata/teamstats1-hoopdata2.csv'
df = read_csv(filepath)

df.plot(x='OffEff', y='DefEff', marker='.',  kind='scatter')
plt.show()


labels = df.Name.values
xvals = df.OffEff.values
yvals = df.DefEff.values

#

# plt.annotate('test2', xy=(105,105))

offset = 0.2;

for label, x, y in zip(labels, xvals, yvals):
    plt.annotate(
        label, 
        xy = (x, y),
        xytext=(x+offset, y+offset))
        
        

#############

#df = read_csv(page)
#print df
#print df['Line']





