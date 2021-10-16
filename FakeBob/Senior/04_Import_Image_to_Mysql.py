# CREATE TABLE double_11.b2c_dim_platform_imag (
#     id int(11) NOT NULL auto_increment,
#                         platform varchar(45) NOT NULL default '',
#                                                               img longblob NOT NULL,
#                                                                                PRIMARY KEY (id)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

import MySQLdb
conn=MySQLdb.connect\
    (host = 'rm-bp1ewtt415rb50614ko.mysql.rds.aliyuncs.com',
                     port = 3306,
                     user = 'wdt',
                     passwd = 'bU6jPopzhcPfSUvR',
                     database = 'double_11',
                     charset = 'utf8')

print('successfully connect')

cursor = conn.cursor()
fin = open("./img/*.png",'rb')   #'rb'加上才能将图片读取为二进制
img = fin.read()                 #将二进制数据读取到img中
fin.close()

sql = "INSERT INTO b2c_dim_platform_imag values  (%s,%s,%s);"   #将数据插入到mysql数据库中，指令
args = ('','拼多多',img)                              #对应表格的数据

cursor.execute(sql,args)                      #执行相关操作
conn.commit()                                 #更新数据库

print('image import successfully')
#print(2)
cursor.close()
conn.close()