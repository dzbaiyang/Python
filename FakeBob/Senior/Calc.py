from array import array

import numpy as np

x = 4766997
y = 5718500
Cover = [x,y]
# 求均值
arr_mean = np.mean(Cover)
# 求方差
arr_var = np.var(Cover)
# 求总体标准差
arr_std_1 = np.std(Cover)
# 求样本标准差
arr_std_2 = np.std(Cover, ddof=1)

var3 = np.sqrt(x)

print(var3)

print(arr_mean)
print(arr_var)
print(arr_std_1)
print(arr_std_2)