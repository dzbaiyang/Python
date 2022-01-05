import numpy as np
import pandas as pd
list_df = []
mean = np.array([1762,1588])
var_x = 4766997
var_y = 5718500
cov_xy = 3012173
cov = [[var_x,cov_xy],[cov_xy,var_y]]
sample_num = 90
roll_num = 10
roll_num = 10
for j in range(1,roll_num+1):
    df = pd.DataFrame()
    s_xy = np.random.multivariate_normal(mean,cov,sample_num)
    s_Gap = [0]*sample_num
    s_accGap = [0]*sample_num
    for i in range(sample_num):
        s_xy[i][0] = max(0, s_xy[i][0])
        s_xy[i][1] = max(0, s_xy[i][1])
        s_Gap[i] = s_xy[i][1] - s_xy[i][0]
        s_accGap[i] = s_Gap[i] + s_accGap[i - 1]
    CashInHand = s_accGap
    for num in range(len(CashInHand)):
        df=df.assign(roll_num=[j],
                     time_step=[num],
                     CashInHand=CashInHand[num])
        list_df.append(df)
df_result = pd.concat(list_df)
print(df_result)
df_result.to_csv('pre_test.csv',index=False)