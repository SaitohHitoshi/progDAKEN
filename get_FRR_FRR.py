import pandas as pd
import numpy as np
CSV_PATH_get_FAR_FRR="./FIT_data_copy/FAR_FRR.csv"
CSV_PATH_inspection="./FIT_data_copy/inspection.csv"

def get_FAR():
    get_FAR_FRR_names=('name','speed','authentication_distance','Euclid_average','k1','k2','k3','k4','k5','k6','k7','k8','k9','k10')
    df_get_FAR_FRR=pd.read_csv(CSV_PATH_get_FAR_FRR,names=get_FAR_FRR_names,header=None)
    print(df_get_FAR_FRR)
    inspection_names=('name','speed','k1','k2','k3','k4','k5','k6','k7','k8','k9','k10')
    df_inspection=pd.read_csv(CSV_PATH_inspection,names=inspection_names,header=None)
    print(df_inspection)
    for index,data in df_get_FAR_FRR.iterrows():
        ave_name=data['name']
        ave_speed=data['speed']
        authentication_distance=data['authentication_distance']
        Euclid_average=data['Euclid_average']
        ave_k1=data['k1']
        ave_k2=data['k2']
        ave_k3=data['k3']
        ave_k4=data['k4']
        ave_k5=data['k5']
        ave_k6=data['k6']
        ave_k7=data['k7']
        ave_k8=data['k8']
        ave_k9=data['k9']
        ave_k10=data['k10']
        average_keystroke=[]
        average_keystroke.extend([ave_k1,ave_k2,ave_k3,ave_k4,ave_k5,ave_k6,ave_k7,ave_k8,ave_k9,ave_k10])
        for index,data in df_inspection.iterrows():
            ins_name=data['name']
            ins_speed=data['speed']
            ins_k1=data['k1']
            ins_k2=data['k2']
            ins_k3=data['k3']
            ins_k4=data['k4']
            ins_k5=data['k5']
            ins_k6=data['k6']
            ins_k7=data['k7']
            ins_k8=data['k8']
            ins_k9=data['k9']
            ins_k10=data['k10']
            ins_keystroke=[]
            ins_keystroke.extend([ins_k1,ins_k2,ins_k3,ins_k4,ins_k5,ins_k6,ins_k7,ins_k8,ins_k9,ins_k10])
            np_average_keystroke=np.array()
            print(deff_keystroke)

get_FAR()