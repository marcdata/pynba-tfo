from scipy import stats

import numpy as np

# shotsmat = np.array([[369, 2323], [740, 7003]])
shotsmat = np.array([[369, 740], [2323, 7003]])


# test line shotsmat = np.array([[12, 24], [25, 48]])

stats.chi2_contingency(shotsmat)

       
       
       
       