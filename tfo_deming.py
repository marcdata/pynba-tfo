
# Experiment with Deming regression / orthogonal distiance



import scipy.odr as deming


# -- 
def f(B, x):
    '''Linear function y = m*x + b'''
    # B is a vector of the parameters.
    # x is an array of the current x values.
    # x is in the same format as the x passed to Data or RealData.
    #
    # Return an array in the same format as y passed to Data or RealData.
    return B[0]*x + B[1]
# -- 

linear = deming.Model(f)


# Create data instance. 

mydata = deming.RealData(team_report['team_efg_e5'], team_report['team_efg_e3'])


# 

myodr = deming.ODR(mydata, linear, beta0=[1., 2.])

# Run the fit.:

myoutput = myodr.run()

# Examine output.:

myoutput.pprint()
