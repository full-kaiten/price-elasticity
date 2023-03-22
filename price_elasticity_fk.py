# -*- coding: utf-8 -*-
#GitHub @batayan
import pandas as pd
import datatable as dt
#statsmodels
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt
import statsmodels.api as sm

import datetime as dtime
now = dtime.datetime.now()
time = now.strftime('%Y%m%d-%H%M%S')

#マスターテーブル抽出関連
df = dt.fread("ml_ts_dataset_test.csv")
df = df.to_pandas()
m_product_group_id_array = pd.unique(df["product_group_id1"])
m_sku_id = pd.unique(df["sku_id"])

m_df = dt.fread("skus.csv")
m_df = m_df.to_pandas()
m_product_code_id_array = pd.unique(m_df["product_code_id"])


#どのSKUをターゲットにするか sku単位では見ないケースでは使わない
#sku_id_uniq = "0d42a3d5-c2a1-56d5-9567-8406fbb6502c"
seller_id_uniq = "1d5663db-c2c3-512b-8746-d49f1de92e0d"
sku_id_uniq = "0cf4cfa9-4d2f-526f-88c9-f7b2ba6dc436"

#list_priceはwhole_sales_priceに集約するのに使っていた。as of Feb 13 2023以降は使っていない
list_price = 11500

#product_group_id用にサンプル数を設定（10,000レコード程度でOLS結果が返ってくる）
sampling_amt=10000

#調べるproduct_code_idをproduct_code_id_uniqの中から指定。
#Hanesシャツ
product_code_id_uniq="225e4cb3-eaa2-5559-9a85-fbdc3e3deff7"
#product_code_id_uniq="33d48ba0-d194-5c30-a8a3-66227d753e5b"
#主要なproduct_code_idを以下からピックアップしてもよい。
"""
主要product_code_idとレコード件数　降順
169702e4-87b3-56c5-861f-20e548690d37 33114
33d48ba0-d194-5c30-a8a3-66227d753e5b	 23820
09d756da-bcc1-5277-9a91-b3d663adabc6	 22546
83f245ca-3632-5ad9-9aee-b9a1a2fe3625	 18312
dfda16f6-468c-57aa-ae32-a377a00a4ebd	 18230
d1029cd2-1342-5d2a-94fe-03dc1a2de577	 17295
8eb9b339-b4f7-5b87-afee-3da3df72a6f6	 16981
30f1051a-e7ae-5f6f-a427-88f10a58f49c	 16935
aaca953e-41eb-5d6f-9456-8850e96579b8	 16378
7d22ebcd-f0dc-57fb-9d73-1b68a0e2bb73	 16299
81886963-9890-5a26-8393-897085eafb70	 14963
7afb9e26-5c82-51ab-a795-4490538459e5	 14777
fbe72309-5501-5b02-9a1e-c4d8e95bf225	 14612
e265acfb-29ec-51b6-a8e4-d223ba874cd5	 14275
40a4659d-bd62-59f6-9176-96c78cb18797	 14243
27077e14-1547-5aac-ab8a-8126b952c185	 13377
849eaf8b-8b54-5c95-8ac9-dd1890ad2af7	 12795
446b9306-f11d-53a5-8988-75d433353160	 12491
117fe46c-aae2-54c5-bd9e-42990e8e20bd	 12331
36ede093-5e85-5490-9902-ac9b0bd02d15	 11909
Hanesシャツ"225e4cb3-eaa2-5559-9a85-fbdc3e3deff7" 11001
"""

#product_code_id別にレコード件数を出力
#df_product_code_id_size = df.groupby("product_code_id").size().sort_values(ascending=False)
product_group_id_uniq="b6c54489-38a0-5f50-a60a-fd8d76219cae"
#調べるproduct_group_idをproduct_group_id_uniqの一覧から指定。
"""
product_group_id_uniq一覧
11116e73-1c03-5de6-9130-5f9925ae8ab4	1	梅春
1087ebe8-1ef8-5d97-8873-735b4949004d	2	春
7e57d004-2b97-5e7a-b45f-5387367791cd	3	初夏
1dd80df1-492c-5dc5-aec2-6bf0e104f923	4	盛夏
f797f61e-a392-5acf-af25-b46057f1c8e8	5	晩夏
e02c9780-2fc5-5d57-b92f-4cc3a64bff16	6	初秋
94167980-f909-527e-a4af-bc3155f586d3	7	秋
9e3eefda-b56e-56bd-8a3a-0b8009d4a536	8	冬
9b75648e-d38c-54e8-adee-1fb295a079c9	9	通年
b6c54489-38a0-5f50-a60a-fd8d76219cae	0	無し
#　1 梅春
product_group_id_uniq="11116e73-1c03-5de6-9130-5f9925ae8ab4"
# 2 春
product_group_id_uniq="1087ebe8-1ef8-5d97-8873-735b4949004d"
# 3 初夏
product_group_id_uniq="7e57d004-2b97-5e7a-b45f-5387367791cd"
# 4 盛夏
product_group_id_uniq="1dd80df1-492c-5dc5-aec2-6bf0e104f923"
# 5 晩夏
product_group_id_uniq="f797f61e-a392-5acf-af25-b46057f1c8e8"
# 6 初秋
product_group_id_uniq="e02c9780-2fc5-5d57-b92f-4cc3a64bff16"
# 7 秋
 product_group_id_uniq="94167980-f909-527e-a4af-bc3155f586d3"
# 8　冬
product_group_id_uniq="9e3eefda-b56e-56bd-8a3a-0b8009d4a536"
# 9　通年
product_group_id_uniq="9b75648e-d38c-54e8-adee-1fb295a079c9"
# 0　無し
product_group_id_uniq="b6c54489-38a0-5f50-a60a-fd8d76219cae"
"""

def create_uniq_df():
    df_sku_id_uniq = df[(df["quantity"]>0) & (df["sku_id"]==sku_id_uniq)]
    df_sku_id_uniq["unit_avg_price"] = df_sku_id_uniq["selling_price"] / df_sku_id_uniq["quantity"]
    df_sku_id_uniq["discount_rate_from_list_price"] = (1 - df_sku_id_uniq["unit_avg_price"]/list_price) * 100
    return df_sku_id_uniq

#quantityが0より大きいレコードを抽出する
def clean_quantity_df(df):
    df_clean =  df[df["quantity"]>0]
    return df_clean

#外れ値除去。1日100個以上売れるものは省く。位置で指定しているので少しsliceでずれているかも
def drop_outlier_df(df):
    df = df.iloc[:, :100]
    return df

#割引率が0より小さいレコード、100より大きいレコードを削除
def clean_discount_rate_from_whole_price(df):
    df_clean = df[(df["discount_rate_from_wholesale_price"]>=0) & (df["discount_rate_from_wholesale_price"]<=100)]
#    df_clean = df[df["discount_rate_from_wholesale_price"]>=0]
    return df_clean

#20230307 standardized_avg_quantityが0になっているレコードを削除
def clean_standardized_avg_quantity(df):
    df_clean = df[df["standardized_avg_quantity"]>0]
    return df_clean

#seller idに紐づくレコードを抽出する
def create_uniq_seller_id(df,seller_id_uniq):
    #df_seller_id_uniq = df[(df["quantity"]>0) & (df["seller_id"]==seller_id_uniq)]
    df_seller_id_uniq = df[df["seller_id"]==seller_id_uniq]
    #sku毎の定価が分からないため、merge_skus_retail_price関数を後で呼ぶ
    return df_seller_id_uniq

#product_code_idに紐づくレコードを抽出する
def create_uniq_product_code_id(df,product_code_id_uniq):
    df_product_code_id_uniq = df[df["product_code_id"]== product_code_id_uniq]
    return df_product_code_id_uniq

#product_group_idに紐づくレコードを抽出する
def create_uniq_product_group_id(df,product_group_id_uniq):
    df_product_group_id_uniq = df[df["product_group_id1"]== product_group_id_uniq]
    return df_product_group_id_uniq

#skuのマスターテーブルにあるretail_price列を追加する。df1はマージ先。df2はマージ元。df3はleft joinした後のreturn
def merge_skus_retail_price(df1,df2):
    #df1['retail_price'] = df1['sku_id'].map(df2.set_index(df2.))
    df3 = pd.merge(df1,df2,left_on=['sku_id'],right_on=['id'],how='left')
    return df3

#最小のmin_avg_quantityを保持するように結合
def merge_min_avg_quantity(df1,df2):
#    df3 = pd.merge(df1,df2,left_on=['sku_id','discount_rate_from_wholesale_price'],right_on=['sku_id','discount_rate_from_wholesale_price'],how='left')
    df3 = pd.merge(df1,df2,left_on=['sku_id'],right_on=['sku_id'],how='left')
    return df3

#マスターとトランザクションのdfをマージした後の計算
def add_unit_avg_price_discount_rate (df):
    df["unit_avg_price"] = df["selling_price"] / df["quantity"]
    df["discount_rate_from_retail_price"]= (1 - df["unit_avg_price"]/df["retail_price"])*100
    df["discount_rate_from_wholesale_price"]= (1 - df["unit_avg_price"]/df["wholesale_price"])*100
    return df


def drop_duplicate():
    df_drop_duplicate = df.drop_duplicates(subset=["sku_id"])
    print(df_drop_duplicate)

def run_avg_quantity_ols(df):
    beams_model_ols = sm.OLS(df['quantity'],df["discount_rate_from_wholesale_price"]).fit()
    print(beams_model_ols.summary())
    
def run_standardized_quantity_ols(df):
    beams_model_ols = sm.OLS(df["standardized_avg_quantity"],df["discount_rate_from_wholesale_price"]).fit()
    print(beams_model_ols.summary())
    
def to_csv(df,time,tex):
    df.to_csv('export_{}{}.csv'.format(time,tex), index=True, header=True)
    
#mainここから
df = clean_quantity_df(df)
df_product_code_id_uniq = create_uniq_product_code_id(df, product_code_id_uniq)
df_product_group_id_uniq = create_uniq_product_group_id(df, product_group_id_uniq)

#ターゲット商品グループ、商品コードのレコード数を出す
ttl_record_code = len(df_product_code_id_uniq)
ttl_record_group = len(df_product_group_id_uniq)

#分析対象のdfに対して、マスターをrightとしてトランザクションデータにleft mergeする
#df_seller_id_uniq = merge_skus_retail_price(df_seller_id_uniq, m_df)
df_product_code_id_uniq = merge_skus_retail_price(df_product_code_id_uniq, m_df)
df_product_group_id_uniq = merge_skus_retail_price(df_product_group_id_uniq, m_df)

#retail_priceやwholesale_priceを基準にした割引率を含めて
df_product_code_id_uniq = add_unit_avg_price_discount_rate(df_product_code_id_uniq)
df_product_group_id_uniq = add_unit_avg_price_discount_rate(df_product_group_id_uniq)

#discount_rate_from_whole_priceが0以上のものをクレンジング
df_product_code_id_uniq = clean_discount_rate_from_whole_price(df_product_code_id_uniq)
df_product_group_id_uniq = clean_discount_rate_from_whole_price(df_product_group_id_uniq)

#20230301 Bata dataframeに対してピボットをする。product_group_idなどは件数が非常に多いのでdf名に+smpl
df_pivot_product_code_id_uniq = pd.pivot_table(df_product_code_id_uniq,
                     index=["sku_id","wholesale_price","seller_id","discount_rate_from_wholesale_price","unit_avg_price"],
                     columns="quantity",
                     values="selling_price",
                     aggfunc='count',
                     fill_value=0
                     )
#df_pivot_product_code_id_smpl = df_pivot_product_code_id_uniq.head(sampling_amt)
df_pivot_product_code_id_smpl = df_pivot_product_code_id_uniq.head(ttl_record_code)
df_pivot_product_code_id_smpl =drop_outlier_df(df_pivot_product_code_id_smpl)
    
#同様にproduct_group_idに対しても適用
df_pivot_product_group_id_uniq = pd.pivot_table(df_product_group_id_uniq,
                     index=["sku_id","wholesale_price","discount_rate_from_wholesale_price","unit_avg_price"],
                     columns="quantity",
                     values="selling_price",
                     aggfunc='count',
                     fill_value=0
                     )
#product_group_idはサンプル数が多いので、サンプル数全体で行うか、スイッチするかで切り替える
df_pivot_product_group_id_smpl = df_pivot_product_group_id_uniq.head(sampling_amt)
#df_pivot_product_group_id_smpl = df_pivot_product_group_id_uniq.head(ttl_record_group)

df_pivot_product_group_id_smpl = drop_outlier_df(df_pivot_product_group_id_smpl)

#経験的に一日当たり10件売り上げ超は外れ値と判断したが明確な根拠は未だなし。→場合によっては変更要
def sum_quantities(df):
    df["sum_ttl_quantity"] = 0
    df["sum_ttl_quantity"] = df[1]*1 + df[2]*2 + df[3]*3 + df[4]*4 + df[5]*5 + df[6]*6 + df[7]*7 + df[8]*8 + df[9]*9 + df[10]*10
    return df["sum_ttl_quantity"]


#20230221　平均販売数量と割引率の２軸でピボットデータを更に加工
df_pivot_product_code_id_smpl["sum_quantity"] = df_pivot_product_code_id_smpl.sum(axis=1)
df_pivot_product_code_id_smpl["sum_ttl_quantity"] = sum_quantities(df_pivot_product_code_id_smpl)
df_pivot_product_code_id_smpl["avg_quantity"] = df_pivot_product_code_id_smpl["sum_ttl_quantity"]/df_pivot_product_code_id_smpl["sum_quantity"]

df_pivot_product_group_id_smpl["sum_quantity"] = df_pivot_product_group_id_smpl.sum(axis=1)
df_pivot_product_group_id_smpl["sum_ttl_quantity"] = sum_quantities(df_pivot_product_group_id_smpl)
df_pivot_product_group_id_smpl["avg_quantity"] = df_pivot_product_group_id_smpl["sum_ttl_quantity"]/df_pivot_product_group_id_smpl["sum_quantity"]

df_pivot_product_group_id_smpl = df_pivot_product_group_id_smpl.reset_index()

#index化をはずす
df_reset_pivot_product_code_id_smpl = df_pivot_product_code_id_smpl.reset_index()
df_reset_pivot_product_group_id_smpl = df_pivot_product_group_id_smpl.reset_index()

#reset_indexでインデックスを削除するバージョン
df_product_code_id_min = df_reset_pivot_product_code_id_smpl.loc[df_reset_pivot_product_code_id_smpl.groupby("sku_id").discount_rate_from_wholesale_price.idxmin()].reset_index(drop=True)
df_product_group_id_min = df_reset_pivot_product_group_id_smpl.loc[df_reset_pivot_product_group_id_smpl.groupby("sku_id").discount_rate_from_wholesale_price.idxmin()].reset_index(drop=True)

#必要なものだけ。その後フィールド名を変更
df_product_code_id_min_extract = df_product_code_id_min.loc[:,["sku_id","discount_rate_from_wholesale_price","avg_quantity"]]
df_product_code_id_min_extract = df_product_code_id_min_extract.rename(columns={"avg_quantity":"min_avg_quantity"})

df_product_group_id_min_extract = df_product_group_id_min.loc[:,["sku_id","discount_rate_from_wholesale_price","avg_quantity"]]
df_product_group_id_min_extract = df_product_group_id_min_extract.rename(columns={"avg_quantity":"min_avg_quantity"})

#結合前に元のdiscount_rate_from_whole_sale_priceをdropする
df_product_code_id_min_extract.drop (["discount_rate_from_wholesale_price"], axis=1,inplace=True)
df_product_group_id_min_extract.drop(["discount_rate_from_wholesale_price"], axis=1,inplace=True)


#結合。min_agv_quantityを持つものだけ抽出
df_reset_pivot_product_code_id_smpl = merge_min_avg_quantity(df_reset_pivot_product_code_id_smpl, df_product_code_id_min_extract)
df_reset_pivot_product_code_id_smpl["standardized_avg_quantity"] = df_reset_pivot_product_code_id_smpl["avg_quantity"]/df_reset_pivot_product_code_id_smpl["min_avg_quantity"]
df_reset_pivot_product_code_id_smpl = clean_standardized_avg_quantity(df_reset_pivot_product_code_id_smpl)

df_reset_pivot_product_group_id_smpl = merge_min_avg_quantity(df_reset_pivot_product_group_id_smpl, df_product_group_id_min_extract)
df_reset_pivot_product_group_id_smpl["standardized_avg_quantity"] = df_reset_pivot_product_group_id_smpl["avg_quantity"]/df_reset_pivot_product_group_id_smpl["min_avg_quantity"]
df_reset_pivot_product_group_id_smpl = clean_standardized_avg_quantity(df_reset_pivot_product_group_id_smpl)


#20230307 scatter plot https://note.nkmk.me/python-pandas-plot/
# product_code_id切り口だと母体数が少ないためドット大き目、透過度低めでplot
ax = df_reset_pivot_product_code_id_smpl.plot.scatter(x="discount_rate_from_wholesale_price", y="standardized_avg_quantity", s=0.3, alpha=0.9)
plt.title('Standardized avg_quantity ~ Discount rate ' + 'total_record_amt= "' + str(ttl_record_code) + '" product_code_id = "' + product_code_id_uniq + '"', fontsize=5)
plt.savefig('plot_product_code' + time + '.png',format="png",dpi=600)
plt.show()

#規格化済　相関結果出力　product_code_id
run_standardized_quantity_ols(df_reset_pivot_product_code_id_smpl)

# product_group_id切り口だと母体数が多いためドット小さめ、透過度高めでplot
ax = df_reset_pivot_product_group_id_smpl.plot.scatter(x="discount_rate_from_wholesale_price", y="standardized_avg_quantity", s=0.1, alpha=0.3)
#plt.title('Standardized avg_quantity / ' + 'sampling amt= "' + str(sampling_amt) + '" product_group_id = "' + product_group_id_uniq + '"', fontsize=5)
plt.title('Standardized avg_quantity ~ Discount rate ' + 'total_record_amt= "' + str(ttl_record_group) + '" product_group_id = "' + product_group_id_uniq + '"', fontsize=5)
plt.savefig('plot_product_group' + time + '.png',format="png",dpi=600)
plt.show()

#規格化済　相関結果出力　product_group_id
run_standardized_quantity_ols(df_reset_pivot_product_group_id_smpl)

#csvによるエクスポート　product_group_id向け
to_csv(df_pivot_product_group_id_smpl, time, "avg_quantity")
