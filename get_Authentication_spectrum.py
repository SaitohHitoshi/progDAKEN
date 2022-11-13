import pandas as pd
import os
import csv
average_spectrum_path="./spectrum_copy/average_spectrum.csv"
measure_supectrum_path="./spectrum_copy/measure_supectrum.csv"
ROOT_PATH='./spectrum_copy'
txt_file = "./spectrum_copy/hasimoto/keizokuninnsyou/spectrum1.txt"

def initialize_measure_supectrum_csv(names_list):
    f = open(measure_supectrum_path, 'w')
    writer = csv.writer(f)
    initialize_names_list=names_list
    initialize_names_list.insert(0,"keystrokestring")
    initialize_names_list.insert(0,"name")
    writer.writerow(names_list)
    f.close()

def recursive_file_check_get_csv(path,names_list):
    if os.path.isdir(path):
        #directoryだったら中のファイルに対して再帰的にこの関数を実行
        files=os.listdir(path)
        for file in files:
            # print('ディレクトリだった')
            # print(path)
            recursive_file_check_get_csv(path+"/"+file,names_list)
    else:
        #_origin.csvだったら処理を実行
        if path[-11:]=='_origin.csv':
            # print(path)
            # print('テキストファイル発見')
            get_csv(path,names_list)

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

def get_name_list():
    names=['Hz','dB']
    df_text = pd.read_csv(txt_file, header=1,delimiter='\t',names=names)
    #print(df_text)
    names_list=[]
    for index,data in df_text.iterrows():
        Hz=data['Hz']
        names_list.extend([Hz])
    return(names_list)

def write_csv_learning(learning,fnames):
    fname=fnames[0]
    name=fnames[1]
    keystrokestring=fnames[2]
    keystrokestring=keystrokestring[0:-11]
    # print(fname)
    # print(name)
    # print(keystrokestring)
    write_path="./"+fname+"/"+name+"/"+keystrokestring+"_learning"+".csv"
    # print(write_path)
    f = open(write_path,'w')
    writer = csv.writer(f)
    for line in learning:
        writer.writerow(line)
    f.close()

def write_csv_inspection(inspection,fnames):
    fname=fnames[0]
    name=fnames[1]
    keystrokestring=fnames[2]
    keystrokestring=keystrokestring[0:-11]
    # print(fname)
    # print(name)
    # print(keystrokestring)
    write_path="./"+fname+"/"+name+"/"+keystrokestring+"_inspection"+".csv"
    # print(write_path)
    f = open(write_path,'w')
    writer = csv.writer(f)
    for line in inspection:
        writer.writerow(line)
    f.close()

def write_csv_measure(measure,fnames):
    fname=fnames[0]
    name=fnames[1]
    keystrokestring=fnames[2]
    keystrokestring=keystrokestring[0:-11]
    # print(fname)
    # print(name)
    # print(keystrokestring)
    write_path=measure_supectrum_path
    # print(write_path)
    f = open(write_path,'a')
    writer = csv.writer(f)
    for line in measure:
        writer.writerow(line)
    f.close()

def get_csv(path,names_list):
    fnames=get_name_and_keystrokestring(path)
    write_path='./'+fnames[0]+'/'+fnames[1]+'/'+fnames[2]
    print(path)
    print(names_list)
    learning=[]
    inspection=[]
    measure=[]
    df_csv= pd.read_csv(path, header=0)
    print(df_csv)
    cout_i=0
    for index,data in df_csv.iterrows(): 
        tmp_list=[]
        for one in names_list:
            one_data=data[one]
            tmp_list.extend([one_data])
        if(cout_i<10):
            learning.append(tmp_list)
            cout_i=cout_i+1
        elif(10<=cout_i and cout_i<20):
            inspection.append(tmp_list)
            cout_i=cout_i+1
        elif(20<=cout_i):
            measure.append(tmp_list)
            cout_i=cout_i+1
    print(len(learning))
    print("--------------------------------")
    print(len(inspection))
    print("--------------------------------")
    print(len(measure))
    print("--------------------------------")
    write_csv_learning(learning,fnames)
    write_csv_inspection(inspection,fnames)
    #write_csv_measure(measure,fnames)

def main():
    names_list=get_name_list()
    initialize_measure_supectrum_csv(names_list)
    recursive_file_check_get_csv(ROOT_PATH,names_list)

main()