import numpy as np
import xlwt
# 创建一个workbook 设置编码
workbook = xlwt.Workbook(encoding = 'utf-8')
# 创建一个worksheet
worksheet = workbook.add_sheet('CashHand')
# 写入excel
# 参数对应 行, 列, 值


mean = np.array([1762,1588])
var_x = 4766997
var_y = 5718500
cov_xy = 3012173
cov = [[var_x,cov_xy],[cov_xy,var_y]]
sample_num = 90

for j in range(0,20000):

    s_xy = np.random.multivariate_normal(mean,cov,sample_num)

    for i in range(sample_num):
        s_xy[i][0] = max(0, s_xy[i][0])
        s_xy[i][1] = max(0, s_xy[i][1])

    s_Gap = [0]*sample_num
    s_accGap = [0]*sample_num

    for i in range(sample_num):
        s_Gap[i] = s_xy[i][1] - s_xy[i][0]

    for i in range(sample_num):
        s_accGap[i] = s_Gap[i] + s_accGap[i - 1]

    CashInHand = np.array(s_accGap)
    print(CashInHand)
    # worksheet.write(j,0, label = CashInHand)

# workbook.save('Excel_test.xls')