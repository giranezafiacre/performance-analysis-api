import pandas as pd
# calculate the Pearson's correlation between two variables
# from numpy.random import randn
# from numpy.random import seed
from scipy.stats import pearsonr
# seed random number generator
# seed(1)
# # prepare data
# data1 = 20 * randn(1000) + 100
# data2 = data1 + (10 * randn(1000) + 50)
# # calculate Pearson's correlation
# corr, _ = pearsonr(data1, data2)
# print('Pearsons correlation: %.3f' % corr)

def correlationRest():
    # dataset = pd.read_csv(filePath)
    # x=pd.Series([1,2,3,4,5,6])
    # y1=pd.Series([2,4,6,8,10,12])
    # y2=pd.Series([-1,-2,-3,-4,-5,-6])
    df1=pd.DataFrame({
        "A":[1,2,3,4,5,6], 
        "B":[2,4,6,8,10,12],
        "C":[-1,-2,-3,-4,-5,-6]
    })
    features=list(["A","B","C"])
    return df1[features].corr()
print(correlationRest())