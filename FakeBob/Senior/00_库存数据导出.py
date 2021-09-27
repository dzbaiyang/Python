
import pandas as pd
import pymysql

conn = pymysql.connect(
    host='offline-tech.ikunchi.com',
    user = "bi_pro",
    passwd = 'EpKgKepLOFdVeClk',
    port = 43005,
    db = 'ads',
    charset='utf8'
)

df = pd.read_sql("""
select ds as 库存时间,
warehouse_type as 仓库属性,
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
where a.ds = '20210822'
""",con=conn)
df.to_excel("E:\2021年8月15日库龄明细数据",index = False)

