import pandas as pd

month=input('欢迎Lily！ 请输入月份：')
if int(month)<10:
	month1 = '0'+str(month)
else:
	month1=month

last_month = str(int(month)-1)
if int(last_month)<10:
	last_month1 = '0'+str(last_month)
else:
	last_month1=last_month

result=[0]*14
# 上月末预存款累计
df = pd.read_excel('2020%s/2020年预存款统计报表--2020年%s月.xlsx'%(
    last_month1,last_month), sheet_name='Sheet1')
result[0]=df.loc[2:13]['Unnamed: 13'][-df.loc[2:13]['Unnamed: 13'].isna()].values[-1]
result[1]=round(df.loc[2:13]['Unnamed: 14'][-df.loc[2:13]['Unnamed: 14'].isna()].values[-1],2)

# 本月预存款增加
df2 = pd.read_excel('2020%s/%s月银行凭证.xlsx'%(month1,month), sheet_name='Sheet1')
result[2]=int(len(df2[-df2['摘要'].isna()])/2)
result[3]=df2[-df2['摘要'].isna()]['贷方'].sum()

# 本月boss销本月进账、本月boss销往月进账
df3 = pd.read_excel('2020%s/1221229702.xls'%month1,usecols=[2,3,4,5,6,7])
df3.dropna(inplace=True)

df3 = df3[df3['贷方']!=0]

# 本月boss销本月进账
result[4]=len(df3['贷方'][df3['摘要'].map(lambda x: True if '2020-%s'%month1 in x else False)])
result[5]=df3['贷方'][df3['摘要'].map(lambda x: True if '2020-%s'%month1 in x else False)].sum()
# 本月boss销往月进账
result[6]=len(df3['贷方'][df3['摘要'].map(lambda x: False if '2020-%s'%month1 in x else True)])
result[7]=df3['贷方'][df3['摘要'].map(lambda x: False if '2020-%s'%month1 in x else True)].sum()

# 本月预存未销挂账、本月预存款累计
df4 = pd.read_excel('2020%s/2020年%s月预存未销帐明细.xlsx'%(
    month1,month), sheet_name='Sheet1')

# 本月预存款累计
result[12] = len(df4[-df4['凭证号数'].isna()]['贷方'])
result[13] = df4[-df4['凭证号数'].isna()]['贷方'].sum()

# 本月预存未销挂账
df5 = df4[-df4['凭证号数'].isna()]
df6 = df5[df5['日期'].map(lambda x: True if '2020-%s'%month1 in str(x)[:10] else False)]
df7 = df6[df6['摘要'].map(lambda x: True if ('2020-%s'%month1 in x) or ('见本月银' in x) else False)]
result[10] = len(df7)
result[11] = df7['贷方'].sum()

# 其他进销账
result[8] = 0
result[9] = round(result[1]+result[3]-result[5]-result[7]-result[13],2)

col_name =[
    '上月末预存款累计笔数','上月末预存款累计金额','本月预存款增加笔数','本月预存款增加金额',
    '本月boss销本月进账笔数','本月boss销本月进账金额','本月boss销往月进账笔数','本月boss销往月进账金额',
    '其他进销账笔数','其他进销账金额','本月预存未销挂账笔数','本月预存未销挂账金额',
    '本月预存款累计笔数','本月预存款累计金额']

result_dict = dict(zip(col_name,result))

pd.DataFrame([result_dict],columns=col_name).to_excel('result.xlsx', index=False)

print('执行成功，请查看result.xlsx！')