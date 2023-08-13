import pandas as pd
# import numpy as np
import re

df = pd.read_excel('target.xlsx', sheet_name='Sheet1')

df['银行退单报错信息'].fillna('',inplace=True)

target_list=df['银行退单报错信息'].values

result=[]
result2=[]
for item in target_list:
    if item=='':
        result.append('')
        result2.append('')
    else:
        print(item)
        res1 = ''.join(re.findall('[\u4e00-\u9fa5]',item))
        result.append(res1)
        # res2 = item.split(res1[:1])[0]    
        if res1=='':       
            result2.append(item)
        elif len(item.split(res1[:1])[0])>19:
            result2.append(item.split(res1[:1])[0][:19])
        else:
            result2.append(item.split(res1[:1])[0])
# print(result)

df['银行退单报错信息']=result
df['银行退单报错信息单号']=result2

df.to_excel('result.xlsx')
print("Succeed！")