import pandas as pd
import os
import csv
import copy
import numpy as np
import math
Certification_distance_path="./spectrum_copy_copy/Certification_distance.csv"
measure_supectrum_path="./spectrum_copy_copy/measure_supectrum.csv"
ROOT_PATH='./spectrum_copy_copy'
txt_file = "./spectrum_copy_copy/hasimoto/keizokuninnsyou/spectrum1.txt"

def initialize_FARandFRR_csv(path):
    f = open(path, 'w')
    writer = csv.writer(f)
    initialize_names_list=["threshhold","FRR","FAR"]
    writer.writerow(initialize_names_list)
    #print(initialize_names_list)
    f.close()

def recursive_file_check_FARandFRR_csv(path):
    if os.path.isdir(path):
        #directoryだったら中のファイルに対して再帰的にこの関数を実行
        files=os.listdir(path)
        for file in files:
            # print('ディレクトリだった')
            # print(path)
            recursive_file_check_FARandFRR_csv(path+"/"+file)
    else:
        #_learning.csvだったら処理を実行
        if path[-14:]=='_FARandFRR.csv':
            print(path)
            print('FARandFRR_CSVファイル発見')
            initialize_FARandFRR_csv(path)

def get_name_list():
    names=['Hz','dB']
    df_text = pd.read_csv(txt_file, header=1,delimiter='\t',names=names)
    #print(df_text)
    names_list=[]
    for index,data in df_text.iterrows():
        Hz=data['Hz']
        names_list.extend([Hz])
    return(names_list)

def get_FAR_FRR(names_list):
    df_Certification_distance=pd.read_csv(Certification_distance_path,header=0)
    df_measure_supectrum=pd.read_csv(measure_supectrum_path,header=0)
    print(df_Certification_distance)
    for index,data in df_Certification_distance.iterrows():
        ave_name=data['cd_name']
        ave_keystrokestring=data['cd_keystrokestring']
        authentication_distance=data['authentication_distance']
        Euclid_average=data['average_Euclid']
        average_list=[]
        for one in names_list:
            tmp_spectrum=data[str(one)]
            average_list.append(tmp_spectrum)
        np_average_array=np.array(average_list)
        # print()
        # print(ave_name)
        # print(ave_keystrokestring)
        # print(authentication_distance)
        # print(Euclid_average)
        #print(average_list)
        for threshhold in np.arange(0,authentication_distance*15,0.1):
            result=[]
            for index,data in df_measure_supectrum.iterrows():
                measure_name=data['measure_name']
                measure_keystrokestring=data['measure_keystrokestring']
                measure_list=[]
                for one in names_list:
                    tmp_spectrum=data[str(one)]
                    measure_list.append(tmp_spectrum)
                ##距離の計算
                np_measure_array=np.array(measure_list)
                deff_spectrum=np_average_array-np_measure_array
                square_deff_supectrum=np.square(deff_spectrum)
                sum_square_deff_spectrum=np.sum(square_deff_supectrum)
                Euclid_spectrum=np.sqrt(sum_square_deff_spectrum)
                comparison=Euclid_average-Euclid_spectrum
                abusolute_value_comparison=math.sqrt(comparison*comparison)
                ##判定処理
                tmp_result=judgement_Euclid(abusolute_value_comparison,threshhold,ave_name,ave_keystrokestring,measure_name,measure_keystrokestring)
                result.extend([tmp_result])
            # print("authentication_distance : "+str(threshhold))
            # print("authentication_distance : "+str(authentication_distance))
            # print(result)
            len_result=len(result)
            count_SA=result.count("SA")
            count_FR=result.count("FR")
            count_FA=result.count("FA")
            count_SR=result.count("SR")
            # print("len_result : "+str(len_result))
            # print("count_SA : "+str(count_SA))
            # print("count_FR : "+str(count_FR))
            # print("count_FA : "+str(count_FA))
            # print("count_SR : "+str(count_SR))
            FAR=(count_FA/(count_FA+count_SR))*100
            FRR=(count_FR/(count_SA+count_FR))*100
            # try:
            #     FRR=(count_FA/(count_FR+count_FA))*100
            # except ZeroDivisionError:
            #     FRR=0
            # #FAR=(1-(count_FR/(count_FR+count_SR)))*100
            # try:
            #     FAR=(count_FR/(count_FR+count_SA))*100
            # except ZeroDivisionError:
            #     FAR=0
            # print("FRR : "+str(FRR)+"%")
            # print("FAR : "+str(FAR)+"%")
            # print("-----------------")
            write_csv(threshhold,FRR,FAR,ave_name,ave_keystrokestring)
            print(str(ave_name)+"の処理中")
        print(str(ave_name)+"の処理終わったよ")
    print("処理が終わったよ")

def write_csv(threshhold,FRR,FAR,ave_name,ave_keystrokestring):
    filepath="./spectrum_copy_copy/"+ave_name+"/"+ave_keystrokestring+"/"+ave_name+"_"+ave_keystrokestring+"_"+"FARandFRR.csv"
    with open(filepath,'a') as f:
        writer = csv.writer(f)
        writer.writerow([threshhold,FRR,FAR])
        f.close()



def judgement_Euclid(abusolute_value_comparison,threshhold,ave_name,ave_keystrokestring,measure_name,measure_keystrokestring):
    if(abusolute_value_comparison < threshhold):
        if(ave_name==measure_name):
            return("SA")
        else:
            return("FA")
    else:
        if(ave_name==measure_name):
            return("FR")
        else:
            return("SR")

def main():
    recursive_file_check_FARandFRR_csv(ROOT_PATH)
    names_list=get_name_list()
    #print(names_list)
    get_FAR_FRR(names_list)

main()