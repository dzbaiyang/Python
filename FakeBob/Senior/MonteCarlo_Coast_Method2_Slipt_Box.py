import numpy as np
import xlwt
import pandas as pd
# 创建一个workbook 设置编码
workbook = xlwt.Workbook(encoding = 'utf-8')
# 创建一个worksheet
worksheet = workbook.add_sheet('CashHand')
# 写入excel
# 参数对应 行, 列, 值


mean = np.array([1322,292])
list_df = []
var_x = 2772833
var_y = 285351
cov_xy = 45870
cov = [[var_x,cov_xy],[cov_xy,var_y]]
sample_num = 90
monthly_debt = 7000
roll_num = 20000


for j in range(1,roll_num+1):
    df = pd.DataFrame()
    s_xy = np.random.multivariate_normal(mean,cov,sample_num)
    for i in [29,59,89]:
        s_xy[i][1] += monthly_debt

    s_Gap = [0]*sample_num
    s_accGap = [0]*sample_num

    for i in range(sample_num):
        s_Gap[i] = s_xy[i][1] - s_xy[i][0]

    for i in range(sample_num):
        s_accGap[i] = s_Gap[i] + s_accGap[i - 1]

    CashInHand = np.array(s_accGap)
    for num in range(len(CashInHand)):
        df=df.assign(roll_num=[j],
                     time_step=[num],
                     CashInHand=CashInHand[num])
        list_df.append(df)
df_result = pd.concat(list_df)
# print(df_result)
df_result.to_csv('pre_test_method.csv',index=False)



df_test = pd.concat(list_df).sort_values('CashInHand',ascending=True)

step = 1000
min_value = -7000
max_value = 70000

list_value = [group_value for group_value in np.arange(min_value,max_value,step)]
data_bin = pd.cut(df_test['CashInHand'],list_value)
pd.value_counts(data_bin).to_csv('acc_bin.csv')