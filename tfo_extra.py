
# plot an x-y scatter plot, with linear regression overlay (if desired)
# optional print out to a specified figure number (default = 1)
# a, b are iterables, list-likes, a = x, b = y of resulting scatter plot

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# ----------------------------------------

def plot_scatter_with_reg_overlay(a, b, figurenum = 1, overlay = False):
    """Creates and displays a scatter-plot figure, optionally with regression overlay."""

    from scipy.stats import pearsonr
    
    rval, pval = pearsonr(a, b)
    
    # quick plot 
    plt.figure(figurenum)
    plt.plot(a, b, '.')
    
    p = np.polyfit(a, b, 1)
    
    print p
    
    xfit = np.array(a)
    yfit = p[0]*xfit+p[1]
    
    print xfit
    print yfit
    
    # plot overlay of 
    # print "overlay is: ", overlay
    
    if overlay is True :
        plt.plot(xfit, yfit, 'r')
        
    # auto-adjust limits on figure, so extreme points don't hang off the end.
    xpadding = (max(a)-min(a)) * .05
    ypadding = (max(b)-min(b)) * .05
    plt.xlim([min(a)-xpadding, max(a)+xpadding])
    plt.ylim([min(b)-ypadding, max(b)+ypadding])
    

    # plt.legend(['', rval])

    return    
    
def add_reg_to_axis(a, b, ax):
    """Adds regression overlay to an axis."""
    
    p = np.polyfit(a, b, 1)
    
    # print p
    
    xfit = np.array(a)
    yfit = p[0]*xfit+p[1]
    
    # print xfit
    # print yfit
    
    ax.plot(xfit, yfit, 'r')
        
    # auto-adjust limits on figure, so extreme points don't hang off the end.
    xpadding = (max(a)-min(a)) * .05
    ypadding = (max(b)-min(b)) * .05
    ax.set_xlim([min(a)-xpadding, max(a)+xpadding])
    ax.set_ylim([min(b)-ypadding, max(b)+ypadding])
    

    # plt.legend(['', rval])

    return    
