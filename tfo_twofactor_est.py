
# Two-variable regression, of shot rate diff, and efg baseline (team_efg_e5). 
# Y = team_efg_diff -- ie, how much difference in shooting efficiency in 2-for-1 
# window. 

import pandas as pd
import numpy as np
import statsmodels.api as sm

# pre: team_report data structure exists in namespace. (see tfo_team_report.py)

# set X and Y as columns from team_report

X = team_report[['team_efg_e5', 'shotrate_diff']]

y = team_report[['team_efg_diff']]

## fit a OLS model with intercept on team_efg_e5 and shotrate_diff
X = sm.add_constant(X)
est = sm.OLS(y, X).fit()

est.summary()

# Output summary to file

fn = 'two_var_reg_out.txt'
f = open(fn, 'w')
f.write(est.summary().as_text())
f.close()

# Done







