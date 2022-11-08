import pandas as pd
import os
ROOT_PATH="./FIT_data_copy"

#ファイルパスを作る関数
def makepath(path):
    i=-1
    while(1):
        if(path[i]=="."):
            break
        else:
            i=i-1
    #print(i)#デバック用
    txt_filepath=path
    #print(path[:i+1]+"New"+path[i+1:])#デバック用
    csv_filepath=txt_filepath[:i]+".csv"
    return(csv_filepath)

def toCSV(complete_filepath):
    names=["name","speed","date","time","operation","key"]
    read_text_file=pd.read_csv(complete_filepath,header=None,names=names,encoding="utf_8")
    csv_filepath=makepath(complete_filepath)
    read_text_file.to_csv(csv_filepath)

#ファイルを捜索する関数
def recursive_file_check(path):
    if os.path.isdir(path):
        #directoryだったら中のファイルに対して再帰的にこの関数を実行
        files=os.listdir(path)
        for file in files:
            recursive_file_check(path+"/"+file)
    else:
        #*exam.utf8.txtだったら処理
        if path[-22:]=='exam.utf8.Complete.txt':
            toCSV(path)

def main():
    recursive_file_check(ROOT_PATH)

main()