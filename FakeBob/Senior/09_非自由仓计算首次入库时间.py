# encoding: utf-8
"""
  > FileName: python1.py
  > Author: Jack
  > Mail: yeboyan@ilarge.com
  > CreatedTime: 2021-04-27 15:20
"""
import csv
from odps import ODPS
from datetime import datetime, timedelta

options.tunnel.use_instance_tunnel = True
options.tunnel.limit_instance_tunnel = False

class EXECUTE_SQL(object):
    def __init__(self):
        self.allsku=[]
        self.sku_records = []
        self.allrecords = {}
        self.results = []

    def parseResult(self,skus,recs):
        VL = ''
        for rec in self.splitStock(skus,recs):
            type_name = '1' # typename
            sku = str(rec[0])
            tnum = str(rec[1])
            ddate = str(rec[2]) if rec[4] != '' else 'null'
            num = str(rec[3])
            rn = str(rec[4]) if rec[4] != '' else 'null'
            VL += ','+'('+type_name+','+'"'+sku+'"'+','+tnum+','+'"'+ddate+'"'+','+num+','+rn+')'
        NEW_VL = VL.replace(",","",1)

        return NEW_VL

    def initData(self,ssql,rsql):
        try:
            result = o.execute_sql(ssql,
                                   hints={'odps.sql.allow.fullscan': 'true'})
            with result.open_reader() as reader:
                for record in reader:
                    dic = dict ()
                    sku = record[0]
                    tnum = record[1]
                    dic['sku'] = sku
                    dic['tnum'] = tnum
                    self.sku_records.append(dic)
        except Exception as e:
            print(e)

        try:
            result = o.execute_sql(rsql,
                                   hints={'odps.sql.allow.fullscan': 'true'})
            with result.open_reader() as reader:
                for record in reader:
                    dic1 = dict()
                    ddate = record[0]
                    sku = record[1]
                    num = record[2]
                    rn = record[3]
                    dic1['ddate'] = ddate
                    dic1['sku'] = sku
                    dic1['num'] = num
                    dic1['rn'] = rn
                    #?????????sku??????sku??????????????????
                    if dic1['sku'] not in self.allsku:
                        self.allsku.append(dic1['sku'])
                        records=[]
                        #???sku?????????????????????
                        records.append(dic1)
                        self.allrecords[dic1['sku']]=records
                    else:
                        #?????????sku???????????????sku??????????????????
                        self.allrecords[dic1['sku']].append(dic1)
        except Exception as e:
            print(e)
        new_vl = self.parseResult(self.sku_records,self.allrecords)
        return new_vl

    def splitStock(self,sku_recs,all_recs):
        for sku_record in sku_recs:
            #???????????????
            sum_num = 0
            sku = sku_record['sku']
            #sku?????????
            tnum = round(float(sku_record['tnum']))
            #?????????sku??????????????????????????????
            if sku not in all_recs:
                self.results.append((sku, tnum, '', tnum, '',))
                continue
            for rec in all_recs[sku]:
                #?????????????????????
                num = round(float(rec['num']))
                #?????????????????????
                ddate = rec['ddate']
                #?????????????????????
                rn = rec['rn']
                if num==0:
                    #????????????????????????0??????????????????????????????
                    continue
                sum_num = sum_num + num  #????????????
                if sum_num < tnum:
                    #??????????????????????????????????????????????????????
                    self.results.append((sku, tnum, ddate, num, rn,))
                else:
                    self.results.append((sku, tnum, ddate, tnum - sum_num + num, rn,))
                    #???????????????????????????????????????????????????????????????????????????
                    break
            if tnum > sum_num and sum_num > 0:
                #??????????????????????????????????????????????????????????????????
                self.results.append((sku, tnum, '', tnum - sum_num, '',))

        return self.results


    def parse_result_sql(self, result_sql, step=1000):
        new_arr = []
        res_arr = result_sql.split("),(")
        for i in res_arr:
            if '(' not in i and ')' not in i:
                new_arr.append('(' + i + ')')

            if '(' not in i and ')' in i:
                new_arr.append('(' + i)

            if '(' in i and ')' not in i:
                new_arr.append(i + ')')

        res = [str(new_arr[i:i+step]).replace('[', '').replace(']', '').replace("'", "") for i in range(0, len(new_arr), step)]

        return res


if __name__ =="__main__":
    exes = EXECUTE_SQL()
    date_s = (datetime.now() + timedelta(days=-1)).strftime('%Y-%m-%d')
    stock_sql = '''
            SELECT A.MATERIAL_CODE AS SKU,SUM(A.END_NUM) TNUM
            FROM DWS_NC_STOCK_RESULT A
            JOIN (
                    SELECT DISTINCT STORE_CODE, ORG_CODE, prodline_code
                    FROM DIM_FINANCE_MAP_FOR_STORE_AGE
                    WHERE STYPE = '????????????'
            ) B 
            ON   A.WAREHOUSE_CODE = B.STORE_CODE 
            AND  A.ORG_CODE = B.ORG_CODE
            AND  a.prodline_code=b.prodline_code
            WHERE A.yday = '{}'
            GROUP  BY MATERIAL_CODE;
        '''.format(date_s)
    record_sql = '''
            SELECT ddate,sku,num,rn FROM ADS_T01_03_NOWN_NC_INBILL_WEEK 
            ORDER BY sku,rn;
            '''

    NEW_VL = exes.initData(stock_sql,record_sql)
    print('NEW_VL', NEW_VL)
    print('date_s', date_s)
    o.execute_sql(
        '''TRUNCATE TABLE ADS_T01_03_NOWN_STOCK_SKU_PRE_WEEK;''',
        hints={'odps.sql.allow.fullscan': 'true'}
    )

    # ??????????????????????????????
    STEP = 10000  #?????????sql??????
    NEW_VL_ARR = exes.parse_result_sql(NEW_VL,step=STEP)
    for V in NEW_VL_ARR:  #?????????????????????
        o.execute_sql(
            "INSERT INTO TABLE ADS_T01_03_NOWN_STOCK_SKU_PRE_WEEK (type_name,sku,tnum,ddate,num,rn) VALUES {}".format(V),
            hints={'odps.sql.allow.fullscan':'true'})






# ???????????????
# #??????????????????
# import pymysql
# import csv
# #???????????????
# conn = pymysql.connect(host='offline-tech.ikunchi.com', user='root', password='WBvNbTVS2OzmYg',db='dataware_test', port=40080)
# cursor = conn.cursor()
# #??????????????????nc???????????????????????????
# # ADS_T01_03_NOWN_NC_INBILL
# # DWD_T01_03_DAY_IN_OUT_P PARTITION (YDAY)
# # stock_sql = '''SELECT sku,tnum from dataware_test.dm_audit_stock_20201112_nc_plus order by sku'''
# stock_sql = '''SELECT sku,tnum from (
# SELECT sku,sum(num) tnum from dataware_test.dm_audit_stock_20201031_nc
# where warehouse_name='?????????' GROUP BY sku) tab order by sku'''
# #?????????????????????????????????sku?????????????????????????????????????????????????????????
# # record_sql = '''SELECT ddate,sku,num,rn from dataware_test.audit_not_own_bills order by sku,rn'''
# record_sql = '''SELECT ddate,sku,num,rn from dataware_test.audit_20201031_bill_jp order by sku,rn'''
# # ??????sql?????????????????????????????????
# def initData(ssql,rsql):
#     try:
#         cursor.execute(ssql) #????????????
#     except Exception as e:
#         print(e)
#     sku_records = []
#     heads = [desc[0] for desc in cursor.description] #????????????????????????
#     for row in cursor.fetchall():
#         sku_record = {}
#         for head, col in zip(heads, row):
#             sku_record[head]=col
#         sku_records.append(sku_record)  #sku_records?????????????????????sku

#     try:
#         cursor.execute(rsql) #????????????
#     except Exception as e:
#         print(e)
#     allrecords = {}
#     allsku=[]
#     heads = [desc[0] for desc in cursor.description] #????????????????????????
#     for row in cursor.fetchall():
#         bill_record = {}
#         for head, col in zip(heads, row):
#             bill_record[head]=col
#         sku=bill_record['sku']
#         if sku not in allsku: #?????????sku??????sku??????????????????
#             allsku.append(sku)
#             records=[]
#             records.append(bill_record) #???sku?????????????????????
#             allrecords[sku]=records
#         else:
#             allrecords[sku].append(bill_record) #?????????sku???????????????sku??????????????????
#     return sku_records,allrecords
# def splitStock(sku_recs,all_recs):
#     results = []
#     for sku_record in sku_recs:
#         sum_num = 0  # ???????????????
#         sku = sku_record['sku']
#         tnum = round(float(sku_record['tnum']))  # sku?????????
#         if sku not in all_recs: #?????????sku??????????????????????????????
#             results.append((sku, tnum, '', tnum, ''))
#             continue
#         for rec in all_recs[sku]:
#             num = round(float(rec['num']))  # ?????????????????????
#             ddate = rec['ddate'] #?????????????????????
#             rn = rec['rn'] #?????????????????????
#             if num==0:
#                 continue  # ????????????????????????0??????????????????????????????
#             sum_num = sum_num + num  # ????????????
#             if sum_num < tnum:
#                 results.append((sku, tnum, ddate, num, rn))  # ??????????????????????????????????????????????????????
#             else:
#                 results.append((sku, tnum, ddate, tnum - sum_num + num, rn))
#                 break  # ???????????????????????????????????????????????????????????????????????????
#         if tnum > sum_num and sum_num > 0:
#             results.append((sku, tnum, '', tnum - sum_num, ''))  # ??????????????????????????????????????????????????????????????????
#     return results

# with open('E:/????????????kunchi/result_20201031jp.csv', 'w', newline='', encoding='utf8') as f: #??????????????????
#     csv.register_dialect('mydialect', delimiter=',', quoting=csv.QUOTE_NONE) #??????????????????
#     write = csv.writer(f, dialect='mydialect')
#     write.writerow(('sku','tnum','ddate','num','rn')) #????????????
#     skus,recs=initData(stock_sql,record_sql)
#     for rec in splitStock(skus,recs):
#         write.writerow(rec) #??????????????????


