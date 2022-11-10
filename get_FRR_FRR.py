import pandas as pd
import numpy as np
import math
import csv
CSV_PATH_get_FAR_FRR="./FIT_data_copy/FAR_FRR.csv"
CSV_PATH_inspection="./FIT_data_copy/inspection.csv"

def get_FAR():
    get_FAR_FRR_names=('ave_name','ave_speed','authentication_distance','Euclid_average','ave_k1','ave_k2','ave_k3','ave_k4','ave_k5','ave_k6','ave_k7','ave_k8','ave_k9','ave_k10')
    df_get_FAR_FRR=pd.read_csv(CSV_PATH_get_FAR_FRR,names=get_FAR_FRR_names,header=None)
    print(df_get_FAR_FRR)
    inspection_names=('ins_name','ins_speed','ins_k1','ins_k2','ins_k3','ins_k4','ins_k5','ins_k6','ins_k7','ins_k8','ins_k9','ins_k10')
    df_inspection=pd.read_csv(CSV_PATH_inspection,names=inspection_names,header=None)
    print(df_inspection)
    for index,data in df_get_FAR_FRR.iterrows():
        ave_name=data['ave_name']
        ave_speed=data['ave_speed']
        authentication_distance=data['authentication_distance']
        Euclid_average=data['Euclid_average']
        ave_k1=data['ave_k1']
        ave_k2=data['ave_k2']
        ave_k3=data['ave_k3']
        ave_k4=data['ave_k4']
        ave_k5=data['ave_k5']
        ave_k6=data['ave_k6']
        ave_k7=data['ave_k7']
        ave_k8=data['ave_k8']
        ave_k9=data['ave_k9']
        ave_k10=data['ave_k10']
        average_keystroke=[]
        average_keystroke.extend([ave_k1,ave_k2,ave_k3,ave_k4,ave_k5,ave_k6,ave_k7,ave_k8,ave_k9,ave_k10])
        #print(average_keystroke)
        np_average_keystroke=np.array(average_keystroke)
        #print(np_average_keystroke)
        #print("authentication_distance : "+str(authentication_distance))
        initialize_csv(ave_name,ave_speed)
        for threshhold in np.arange(0,authentication_distance*15,0.005):
            print(ave_name,ave_speed)
            result=[]
            for index,data in df_inspection.iterrows():
                ins_name=data['ins_name']
                ins_speed=data['ins_speed']
                ins_k1=data['ins_k1']
                ins_k2=data['ins_k2']
                ins_k3=data['ins_k3']
                ins_k4=data['ins_k4']
                ins_k5=data['ins_k5']
                ins_k6=data['ins_k6']
                ins_k7=data['ins_k7']
                ins_k8=data['ins_k8']
                ins_k9=data['ins_k9']
                ins_k10=data['ins_k10']
                ins_keystroke=[]
                ins_keystroke.extend([ins_k1,ins_k2,ins_k3,ins_k4,ins_k5,ins_k6,ins_k7,ins_k8,ins_k9,ins_k10])
                np_ins_keystroke=np.array(ins_keystroke)
                #print(np_ins_keystroke)
                deff_keystroke=np_average_keystroke-np_ins_keystroke
                #print("deff_keystroke"+str(deff_keystroke))
                square_deff_keystroke=deff_keystroke**2
                sum_deff_keystroke=np.sum(square_deff_keystroke)
                #print("square_deff_keystroke"+str(square_deff_keystroke))
                Euclid=math.sqrt(sum_deff_keystroke)
                #print("authentication_distance : "+str(authentication_distance))
                #print("Euclid : "+str(Euclid))
                comparison=Euclid_average-Euclid
                abusolute_value_comparison=math.sqrt(comparison*comparison)
                #print("abusolute_value_comparison : "+str(abusolute_value_comparison))
                tmp_result=judgement_Euclid(abusolute_value_comparison,threshhold,ave_name,ave_speed,ins_name,ins_speed)
                result.extend([tmp_result])
                #print("--------")
                #print(sum_deff_keystroke.dtype)
                #print(ins_name+" "+ins_speed+" "+"sum_deff_keystroke : "+str(sum_deff_keystroke))
            print("authentication_distance : "+str(threshhold))
            print("authentication_distance : "+str(authentication_distance))
            print(result)
            len_result=len(result)
            count_SA=result.count("SA")
            count_FR=result.count("FR")
            count_FA=result.count("FA")
            count_SR=result.count("SR")
            print("len_result : "+str(len_result))
            print("count_SA : "+str(count_SA))
            print("count_FR : "+str(count_FR))
            print("count_FA : "+str(count_FA))
            print("count_SR : "+str(count_SR))
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
            print("FRR : "+str(FRR)+"%")
            print("FAR : "+str(FAR)+"%")
            print("-----------------")
            write_csv(threshhold,FRR,FAR,ave_name,ave_speed)

def judgement_Euclid(abusolute_value_comparison,threshhold,ave_name,ave_speed,ins_name,ins_speed):
    if(abusolute_value_comparison < threshhold):
        if(ave_name==ins_name):
            return("SA")
        else:
            return("FA")
    else:
        if(ave_name==ins_name):
            return("FR")
        else:
            return("SR")

def write_csv(threshhold,FRR,FAR,ave_name,ave_speed):
    filepath="./FIT_data_copy/"+ave_name+"/"+ave_speed+"/"+ave_name+"_"+ave_speed+"_"+"FARandFRR.csv"
    with open(filepath,'a') as f:
        writer = csv.writer(f)
        writer.writerow([threshhold,FRR,FAR])
        f.close()

def initialize_csv(ave_name,ave_speed):
    filepath="./FIT_data_copy/"+ave_name+"/"+ave_speed+"/"+ave_name+"_"+ave_speed+"_"+"FARandFRR.csv"
    with open(filepath,'w') as f:
        writer = csv.writer(f)
        writer.writerow(["threshhold","FRR","FAR"])
        print("initialize完了")
        f.close()

def main():
    get_FAR()

main()