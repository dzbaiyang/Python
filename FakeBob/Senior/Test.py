import datetime
import os
import zipfile
import pandas as pd
import pymysql

#连接mysql数据库
conn = pymysql.connect(
    host='offline-kz.ikunchi.com',
    user = "bi_read",
    passwd = 'OEEDdf1endDNYMsx',
    port = 3513,
    db = 'kc_wms',
    charset='utf8'
)
#####################################################################################################################################
print("执行SQL时间：",datetime.datetime.now())
test = pd.read_sql("""
select * from adjustment_type a
""",con=conn)
print(test)