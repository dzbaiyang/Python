import datetime
import os
import zipfile
import pandas as pd
import sqlite3
import pymysql
from openpyxl.packaging.manifest import mimetypes
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# 获取时间变量#
localtime = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d")  # 多加（减）一天
# 获取路径变量
# 测试
# pathname = 'D:\Stock\{}_库存明细数据.xlsx'.format(localtime)
# pathname1 = 'D:\Stock\库存{}分析报告.xlsx'.format(localtime)
# zipfilepath = 'D:\Stock\{}_库存明细及库存分析报告.zip'.format(localtime)
# 服务器
pathname = '/data/mail_data/sales_monitor/{}_贸易额平台账户监测.xlsx'.format(localtime)
# pathname = r'D:\works\贸易额平台账户监测_{}.xlsx'.format(localtime)
# pathname1 = '/data/mail_data/stock/库存{}分析报告.xlsx'.format(localtime)
# zipfilepath = '/data/mail_data/stock/{}_库存明细及库存分析报告.zip'.format(localtime)

# 获取文件变量
filename = '贸易额平台账户监测'

# 连接mysql数据库
conn = pymysql.connect(
    host='offline-tech.ikunchi.com',
    user="bi_pro",
    passwd='EpKgKepLOFdVeClk',
    port=43005,
    db='dw',
    charset='utf8'
)
#####################################################################################################################################
print("执行SQL时间：", datetime.datetime.now())
stockdetail = pd.read_sql("""
    select a.*  from dw.dm_spider_username_monitor_sales a 
    """, con=conn)
#####################################################################################################################################
# stockanalytics = pd.read_sql("""
# select * from ads.ads_t08_01_stock_daily_analytics
# """,con=conn)
#####################################################################################################################################
# 输出文件内容
page = pathname
# page1 = pathname1
stockdetail.to_excel(page, index=False)
# stockanalytics.to_excel(page1,index = False)
print("执行SQL结束时间：", datetime.datetime.now())
#####################################################################################################################################
# 邮件附件内容
From = "bi-report@ilarge.cn"
# To = "baiyang@ilarge.cn;wangzizi@ilarge.cn;xuyang@ilarge.cn"
To = "baiyang@ilarge.cn;xuyang@ilarge.cn"
file_name = page  # 附件名

server = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
server.login("bi-report@ilarge.cn", "wxbTUH56vXctckW5")  # 仅smtp服务器需要验证时

# 构造MIMEMultipart对象做为根容器
main_msg = MIMEMultipart()

# 构造MIMEText对象做为邮件显示内容并附加到根容器
text_msg = MIMEText(
    "Dear all：\n \n  附件为截止{} [京东VC] & [唯品VIS] 贸易额平台账号爬虫数据监控，请查收!\n \n  获取数据异常的账户还请及时维护，谢谢！".format(localtime))  # 邮件正文内容
main_msg.attach(text_msg)

# 构造MIMEBase对象做为文件附件内容并附加到根容器
ctype, encoding = mimetypes.guess_type(file_name)
if ctype is None or encoding is not None:
    ctype = 'application/octet-stream'
maintype, subtype = ctype.split('/', 1)
file_msg = MIMEImage(open(file_name, 'rb').read(), subtype)
print(ctype, encoding)
## 设置附件头
basename = os.path.basename(file_name)
file_msg.add_header('Content-Disposition', 'attachment', filename=basename)  # 修改邮件头
main_msg.attach(file_msg)

# 设置根容器属性
main_msg['From'] = From
main_msg['To'] = To
main_msg['Subject'] = filename

# 得到格式化后的完整文本
fullText = main_msg.as_string()

# 用smtp发送邮件
try:
    server.sendmail(From, To.split(','), fullText)
finally:
    server.quit()
print("邮件发送成功！")
