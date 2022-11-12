import pandas as pd

txt_file = "./spectrum_copy/hasimoto/keizokuninnsyou/spectrum1.txt"
csv_file = "./spectrum_copy/hasimoto/keizokuninnsyou.csv"

names=['Hz','dB']
df_text = pd.read_csv(txt_file, header=1,delimiter='\t',names=names)
print(df_text)