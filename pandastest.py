import pandas as pd
from pathlib import Path

#インデックスの名前宣言
names=['dataname', 'name', 'word', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10']
#カウンター
count=0
#カウンター配列
orinpikkulist=[]

#csvの読み込み
filepath = 'out2.csv'
df=pd.read_csv(filepath,names=names)

#df.indexの長さを取得
dflength=len(df.index)
print(dflength)



#dfの表示
#print(df)

# for line in df.values:
#     print(line)

# #orinpikkuの検索
# dforinpikku=(df['word']=='orinpikku')

# #orinpikkuのインデックス格納
# for i in dforinpikku:
#     if i==True:
#         #print(count)
#         orinpikkulist.append(count)
#     count+=1

# for x in orinpikkulist:
#     #print(df[x:x+1])
#     df_flag=df[x:x+1].values
#     df_flag[0][12]=df_flag[0][11]
#     df_flag[0][11]=df_flag[0][10]
#     df_flag[0][10]=df_flag[0][9]
#     df_flag[0][9]=df_flag[0][8]
#     df_flag[0][8]=df_flag[0][7]
#     df_flag[0][7]=df_flag[0][6]
#     df_flag[0][6]=0.0
    
#     #print(df_flag[0][12])
#     print(df_flag)

# #print(df_flag)

# #print(df_flag['name'])

