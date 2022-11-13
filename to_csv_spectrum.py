import pandas as pd
import os
import csv
ROOTPATH='./spectrum_copy'
txt_file = "./spectrum_copy/hasimoto/keizokuninnsyou/spectrum1.txt"
#csv_file = "./spectrum_copy/hasimoto/keizokuninnsyou.csv"

##データフレームの列名を取得
def get_name_list():
    names=['Hz','dB']
    df_text = pd.read_csv(txt_file, header=1,delimiter='\t',names=names)
    #print(df_text)
    names_list=[]
    for index,data in df_text.iterrows():
        Hz=data['Hz']
        names_list.extend([Hz])
    return(names_list)

##全部見つけてくるやつ
def recursive_file_check_txet_to_csv(path):
    if os.path.isdir(path):
        #directoryだったら中のファイルに対して再帰的にこの関数を実行
        files=os.listdir(path)
        for file in files:
            # print('ディレクトリだった')
            # print(path)
            recursive_file_check_txet_to_csv(path+"/"+file)
    else:
        #.txtだったら処理を実行
        if path[-4:]=='.txt':
            # print(path)
            # print('テキストファイル発見')
            txet_to_csv(path)

def initialize_csv(path,names_list):
    f = open(path, 'w')
    writer = csv.writer(f)
    writer.writerow(names_list)
    f.close()

def recursive_file_check_initialize_csv(path,names_list):
    if os.path.isdir(path):
        #directoryだったら中のファイルに対して再帰的にこの関数を実行
        files=os.listdir(path)
        for file in files:
            # print('ディレクトリだった')
            # print(path)
            recursive_file_check_initialize_csv(path+"/"+file,names_list)
    else:
        #.txtだったら処理を実行
        if path[-4:]=='.csv':
            # print(path)
            # print('テキストファイル発見')
            initialize_csv(path,names_list)

##
def get_name_and_keystrokestring(path):
    #print(path)
    path_list=list(path)
    #print(path_list)
    count_slash=0
    fname=[]
    name=[]
    keystrokestring=[]
    for one in path_list:
        if (one=='/'):
            count_slash=count_slash+1
        elif(count_slash==1):
            fname.append(one)
        elif(count_slash==2):
            name.append(one)
        elif(count_slash==3):
            keystrokestring.append(one)
    str_fname="".join(fname)
    str_name="".join(name)
    str_keystrokestring="".join(keystrokestring)
    return(str_fname,str_name,str_keystrokestring)

def write_csv(fnames,dB_list,names_list):
    path='./'+fnames[0]+'/'+fnames[1]+'/'+fnames[2]+'_origin.csv'
    print(path)
    f = open(path,'a')
    writer = csv.writer(f)
    writer.writerow(dB_list)
    f.close()

##
def txet_to_csv(path):
    #print(path)
    fnames=get_name_and_keystrokestring(path)
    print(fnames)
    names=['Hz','dB']
    dB_list=[]
    df_text = pd.read_csv(path, header=1,delimiter='\t',names=names)
    for index,data in df_text.iterrows():
        dB=data['dB']
        dB_list.append(dB)
    #print(df_text)
    #print(dB_list)
    names_list=get_name_list()
    write_csv(fnames,dB_list,names_list)

def main():
    names_list=get_name_list()
    #print(names_list)
    recursive_file_check_initialize_csv(ROOTPATH,names_list)
    recursive_file_check_txet_to_csv(ROOTPATH)
    

main()