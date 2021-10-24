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


#获取时间变量#
localtime = (datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y%m%d") #多加（减）一天
#获取路径变量
#测试
# pathname = 'D:\Stock\{}_库存明细数据.xlsx'.format(localtime)
# pathname1 = 'D:\Stock\库存{}分析报告.xlsx'.format(localtime)
# zipfilepath = 'D:\Stock\{}_库存明细及库存分析报告.zip'.format(localtime)
#服务器
pathname = '/data/mail_data/stock/{}_库存明细数据.xlsx'.format(localtime)
pathname1 = '/data/mail_data/stock/库存{}分析报告.xlsx'.format(localtime)
zipfilepath = '/data/mail_data/stock/{}_库存明细及库存分析报告.zip'.format(localtime)

# 获取文件变量
filename = '{}_库存明细数据'.format(localtime)


#连接mysql数据库
conn = pymysql.connect(
    host='offline-tech.ikunchi.com',
    user = "bi_pro",
    passwd = 'EpKgKepLOFdVeClk',
    port = 43005,
    db = 'ads',
    charset='utf8'
)
#####################################################################################################################################
print("执行SQL时间：",datetime.datetime.now())
stockdetail = pd.read_sql("""
select ds as 库存时间,
warehouse_type as 仓库属性,
warehouse_is_proxy as 是否代销,
org_code as 库存组织,
org_name as 库存组织名称, 
core_business_name as OBC仓库映射事业部,
business_unit_code_map as "核心对照表+手工事业部",
warehouse_code as 仓库编码,
warehouse_name as 仓库名称,
channel_code as 渠道编码,
cus_channel_name as 渠道名称,
is_cooperation as 是否合作品牌,
prod_line as 产品线编码,
prod_line_name as 产品线名称,
good_or_bad as 商品属性,
goods_code as 商品编码,
goods_name as 商品名称,
first_stock_in_time as 首次入库时间,
invalid_date as 过期时间,
available_stock as 数量,
final_price as "单价（未税）",
final_amount as  "金额（未税）" ,
batch_no as 批次号,
batch_description as 批次注释,
source_order_no as 源单号,
quality_type as 效期类型,
goods_type as 好坏,
import_type as "国产/进口",
prod_type_name as 商品类型,
diff_age as "库龄（天）",
stock_age as 库龄分布,
with_amount as 计提金额,
diff_invalid_age as 剩余效期,
effective_type as 效期类型 from dm.dm_t08_01_stock_final a 
where ds = date_format(DATE_SUB(NOW(),INTERVAL 1 day),'%Y%m%d')
limit 100
""",con=conn)
#####################################################################################################################################
stockanalytics = pd.read_sql("""
select * from ads.ads_t08_01_stock_daily_analytics
""",con=conn)
#####################################################################################################################################
#输出文件内容
page = pathname
page1 = pathname1
stockdetail.to_excel(page,index = False)
stockanalytics.to_excel(page1,index = False)
print("执行SQL结束时间：",datetime.datetime.now())
#####################################################################################################################################
# 压缩目录下面的文件
def compress_attaches(files, out_name):
    f = zipfile.ZipFile(out_name, 'w', zipfile.ZIP_DEFLATED)
    for file in files:
        f.write(file)
    f.close()
files = [page, page1]
compress_attaches(files, zipfilepath)

# zip_file = zipfile.ZipFile(zipfilepath, 'w',zipfile.ZIP_DEFLATED)
# zip_file.write(page)
# zip_file.close()
#####################################################################################################################################
#邮件附件内容
From = "bi-report@ilarge.cn"
To = "baiyang@ilarge.cn"
file_name = zipfilepath  #附件名

server = smtplib.SMTP_SSL("smtp.exmail.qq.com",465)
server.login("bi-report@ilarge.cn","f4ND674F9jGnGLhC") #仅smtp服务器需要验证时

# 构造MIMEMultipart对象做为根容器
main_msg = MIMEMultipart()

# 构造MIMEText对象做为邮件显示内容并附加到根容器
text_msg = MIMEText("Dear all：\n \n  附件为截止{}库存明细数据及库存分析报告,请查收!\n \n  另事业部缺失信息，已在KATA系统中更新，还请及时维护，谢谢！\n \n  维护地址：https://bi.ikunchi.com/decision".format(localtime)) #邮件正文内容
main_msg.attach(text_msg)

# 构造MIMEBase对象做为文件附件内容并附加到根容器
ctype,encoding = mimetypes.guess_type(file_name)
if ctype is None or encoding is not None:
    ctype='application/octet-stream'
maintype,subtype = ctype.split('/',1)
file_msg=MIMEImage(open(file_name,'rb').read(),subtype)
print(ctype,encoding)
## 设置附件头
basename = os.path.basename(file_name)
file_msg.add_header('Content-Disposition','attachment', filename = basename)#修改邮件头
main_msg.attach(file_msg)

# 设置根容器属性
main_msg['From'] = From
main_msg['To'] = To
main_msg['Subject'] = filename

# 得到格式化后的完整文本
fullText = main_msg.as_string( )

# 用smtp发送邮件
try:
    server.sendmail(From, To, fullText)
finally:
    server.quit()