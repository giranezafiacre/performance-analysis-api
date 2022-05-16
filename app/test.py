

import pandas as pd

x = pd.Series([1, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10])
y = pd.Series([15.62, 16.0, 13.0, 11.0, 15.0, 15.2, 14.2, 13.6, 14.2, 17.5, 13.0])
print(x.corr(y))