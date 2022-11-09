import pandas as pd
import os
import csv
import matplotlib.pyplot as plt
from scipy import stats
import itertools
import math
#import statistics as stat# 標本分散の計算に利用
from statistics import variance,mean
import statistics
ROOT_PATH="./FIT_data_copy"
CSV_PATH="./FIT_data_copy/average_variance.csv"
CSV_PATH_get_FAR_FRR="./FIT_data_copy/FAR_FRR.csv"
CSV_PATH_inspection="./FIT_data_copy/inspection.csv"

csv_filepath="./FIT_data_copy/okada/fast/20220616_140737_exam.utf8.Complete.csv"
csv_filepath2="./FIT_data_copy/okada/normal/20220616_135928_exam.utf8.Complete.csv"
csv_filepath3="./FIT_data_copy/okada/slow/20220616_135047_exam.utf8.Complete.csv"
csv_filepath4="./FIT_data_copy/kasahara/slow/20220615_185529_exam.utf8.Complete.csv"
csv_filepath5="./FIT_data_copy/ando/fast/20220614_16373_exam.utf8.Complete.csv"

def recursive_file_check_get_average_variance(path):
    if os.path.isdir(path):
        #directoryだったら中のファイルに対して再帰的にこの関数を実行
        files=os.listdir(path)
        for file in files:
            recursive_file_check_get_average_variance(path+"/"+file)
    else:
        #exam.utf8.Complete.csvだったら処理を実行
        if path[-22:]=='exam.utf8.Complete.csv':
            print(path)
            to_df_of_lines(path)


#CSVtoDF
def get_df(csv_filepath):
    df=pd.read_csv(csv_filepath,index_col=0)
    return(df)

#str_to_time
def strTime_to_floatSeconds(df):
    for index,data in df.iterrows():
        time=data["time"]
        #print(time)
        hour=str(time[0:2])
        minute=str(time[3:5])
        seconds=str(time[6:8])
        milliseconds="0."+str(time[9:11])
        #print(milliseconds)
        sum_seconds=float(hour)*3600+float(minute)*60+float(seconds)+float(milliseconds)
        #print(hour+","+minute+","+seconds+","+milliseconds)
        #print(sum_seconds)
        #print("--------")
        df.loc[index,"time"]=sum_seconds

#何行改行したか取得する関数
def get_newline_number(df):
    count_Enter=0
    new_line=0
    for index,data in df.iterrows():
        time=data["time"]
        operation=data["operation"]
        key=data["key"]
        if not(key=="Enterボタン"):
            count_Enter=0
        elif (key=="Enterボタン"):
            count_Enter=count_Enter+1
        if(count_Enter>=4):
            new_line=new_line+1
            str_line=""
    return(new_line)

#改行した行の文字列を取得する関数
def get_Completelines(df):
    count_Enter=0
    new_line=0
    str_line=""
    lines=[]
    for index,data in df.iterrows():
        time=data["time"]
        operation=data["operation"]
        key=data["key"]
        if not(key=="Enterボタン"):
            count_Enter=0
            if (operation=="D") and ((len(key)==4) or (key=="OemPeriodボタン")):
                if (key=="OemPeriodボタン"):
                    str_line=str_line+"."
                else:
                    str_line=str_line+key[0:-3]
        elif (key=="Enterボタン"):
            count_Enter=count_Enter+1
        if(count_Enter>=4):
            lines.append(str_line)
            str_line=""
            new_line=new_line+1
    return(lines)

# #キーを押した時の時間をリストに入れて返す関数
def get_DtoD_keystroke(df):
    count_Enter=0
    new_line=0
    str_line=""
    lines=[]
    keystrokeDatas=[]
    line_keystrokeData=[]
    line_keystrokeData.clear()
    keystrokeDatas.clear()
    for index,data in df.iterrows():
        time=data["time"]
        operation=data["operation"]
        key=data["key"]
        if not(key=="Enterボタン"):
            if not((count_Enter==1) and (operation=="U") and (key=="OemPeriodボタン")) :
                
                count_Enter=0
                if (operation=="D") and ((len(key)==4) or (key=="OemPeriodボタン")):
                    if (key=="OemPeriodボタン"):
                        str_line=str_line+"."
                        keystrokeDatas.append([str(time),str(operation),str(key[0:-3])])
                        # print(keystrokeDatas)
                    else:
                        str_line=str_line+key[0:-3]
                        keystrokeDatas.append([str(time),str(operation),str(key[0:-3])])
                        # print(keystrokeDatas)
        elif (key=="Enterボタン"):
            count_Enter=count_Enter+1
        if(count_Enter>=4):
            lines.append(str_line)
            str_line=""
            new_line=new_line+1
            df_line=pd.DataFrame(keystrokeDatas,columns=['time','operation','key'])
            line_keystrokeData.append(df_line)
            keystrokeDatas.clear()
            # print(line_keystrokeData)
            # print("---------------------")
    return(line_keystrokeData)

##オリンピックと入力されているか確認する関数
def get_line_orinnpikku(df_keystroke_line):
    orinpikkuList=[]
    str1="orinnpikku"
    str2="orinpikku"
    for df_keystroke in df_keystroke_line:
        str=""
        for index,data in df_keystroke.iterrows():
            str=str+data["key"]
            strlen=len(str)
            if strlen==0:
                str=str+data["key"]
            elif((str[0]==str1[0]) and (str[0]==str2[0])):
                if((str1==str) or (str2==str)):
                    orinpikkuList.append([str])
                    str=""
                elif (str1[strlen-1:strlen]=="key"):
                    str=str+data["key"]
            else:
                str=""
    #print(orinpikkuList)

##オリンピックと入力されているキーストロークを取得し，dfに変換して返す関数
def df_get_keystroke_orinnpikku(df_keystroke_line):
    orinpikkuList=[]
    keystrokes_line_list=[]
    keystrokes_line_list.clear()
    df_keystrokes_line_list=[]
    str1="orinnpikku"
    str2="orinpikku"#空白は文字列の長さを合わせるため
    for df_keystroke in df_keystroke_line:
        str_line=""
        #print("--------------------")
        mp_time=0.0
        tmp_operation=""
        tmp_key=""
        for index,data in df_keystroke.iterrows():
            time=data["time"]
            operation=data["operation"]
            key=data["key"]
            #print(time+":"+operation+":"+key)
            strlen=len(str_line)
            if strlen==0:
                str_line=str_line+key
                strlen=len(str_line)
                keystrokes_line_list.append([time,operation,key])
                #print("一文字目を入力:"+str(strlen)+":"+str_line)
            else:
                if((str_line[0]==str1[0]) or (str_line[0]==str2[0])):
                    if((str1==str_line) or (str2==str_line)):
                        orinpikkuList.append([str_line])
                        df_keystrokes_line=pd.DataFrame(keystrokes_line_list,columns=['time','operation','key'])
                        df_keystrokes_line_list.append(df_keystrokes_line)
                        #print("文字列完成:"+str(strlen)+":"+str_line)
                        str_line=""
                        strlen=len(str_line)
                        keystrokes_line_list.clear()
                        #print("完成したので文字列を削除:"+str(strlen)+":"+str_line)
                    elif(str1[strlen]==key):
                        str_line=str_line+key
                        strlen=len(str_line)
                        keystrokes_line_list.append([time,operation,key])
                        tmp_time=time
                        tmp_operation=operation
                        tmp_key=key
                        #print("文字列に文字を追加:"+str(strlen)+":"+str_line)
                    elif(str2[strlen]==key):
                        if(key=="p"):
                            str_line=str_line+key
                            strlen=len(str_line)
                            #print(tmp_time,tmp_operation,tmp_key)
                            keystrokes_line_list.append([tmp_time,tmp_operation,tmp_key])
                            keystrokes_line_list.append([time,operation,key])
                        else:
                            str_line=str_line+key
                            strlen=len(str_line)
                            keystrokes_line_list.append([time,operation,key])
                            tmp_time=time
                            tmp_operation=operation
                            tmp_key=key
                        #print("文字列に文字を追加:"+str(strlen)+":"+str_line)
                    else:
                        str_line=""
                        strlen=len(str_line)
                        keystrokes_line_list.clear()
                        #print("in文字列を削除:"+str(strlen)+":"+str_line)
                else:
                    str_line=""
                    strlen=len(str_line)
                    keystrokes_line_list.clear()
                    #print("out文字列を削除:"+str(strlen)+":"+str_line)
            #print("---------")
        keystrokes_line_list.clear()
    print(orinpikkuList)
    # for line in df_keystrokes_line_list:
    #     print(line)
    #     # for idnex,data in line.iterrows():
    #     #     print(data)
    #     #     print("------")
    #     print("-------------------")
    return(df_keystrokes_line_list)

##DtoDでキーストロークの差を計算する関数
def get_DtoD_diff(df_orinpikku):
    diff_lines=[]
    for line in df_orinpikku:
        diff_line=[]
        tmp=0
        i=0
        for index,data in line.iterrows():
            time=data["time"]
            if(i==0):
                tmp=time
            # print(float(time)-float(tmp))
            diff_line.append(float(time)-float(tmp))
            tmp=float(time)
            i=i+1
        # print(diff_line)
        diff_lines.append(diff_line)
        # print("---------------")
        # print(diff_lines)
    i=1
    # for line in diff_lines:
    #     print(i)
    #     i=i+1
    #     print(line)
    return(diff_lines)

##一つのキーのキーストロークをリストにして返す関数
def get_one_keystroke_lists(diff_lines):
    len_list=len(diff_lines)
    # print(len_list)
    max_len=len(diff_lines[0])
    # print(max_len)
    one_keystroke_lists=[]
    for i in range(max_len):
        one_keystroke_list=[]
        # print(str(i+1)+"個め")
        for diff_line in diff_lines:
            #print(diff_line[i])
            one_keystroke_list.append(diff_line[i])
        one_keystroke_lists.append(one_keystroke_list)
    return(one_keystroke_lists)

##分散を計算する関数
def get_variance(diff_lines):
    len_list=len(diff_lines)
    # print(len_list)
    max_len=len(diff_lines[0])
    # print(max_len)
    one_keystroke_lists=[]
    for i in range(max_len):
        one_keystroke_list=[]
        # print(str(i+1)+"個め")
        for diff_line in diff_lines:
            #print(diff_line[i])
            one_keystroke_list.append(diff_line[i])
        one_keystroke_lists.append(one_keystroke_list)
    count_line_number=1
    sum_variance=0
    for one_phrase in one_keystroke_lists:
        # print(str(count_line_number)+"個め")
        #print(one_phrase)
        # print(variance(one_phrase))
        sum_variance=sum_variance+variance(one_phrase)
        count_line_number=count_line_number+1
    # print(count_line_number-1)
    print("sum_variance:"+str(sum_variance/(count_line_number-1)))
    average_variance=sum_variance/(count_line_number-1)
    return(sum_variance/(count_line_number-1))

##被験者の名前と打鍵スピードを取得する関数
def get_nameAndspeed(df):
    # print(df.iat[1,0])
    name=df.iat[1,0]
    # print(df.iat[1,1])
    speed=df.iat[1,1]
    return(name,speed)

##分散を計算した結果をCSVに書き込む関数
def write_average_variance_csv(name,speed,average_variance):
    with open(CSV_PATH,'a') as f:
        writer=csv.writer(f)
        writer.writerow([name,speed,average_variance])
        print("書き込み完了")
        f.close()

##正規分布してるか確認がしたい関数
def t_test(one_keystroke_lists):
    list_shapiro=[]
    for one_keystroke_list in one_keystroke_lists:
        # print(mean(one_keystroke_list))
        # plt.hist(one_keystroke_list,bins=10,range=(0,0.2))
        #plt.show()
        p=stats.shapiro(one_keystroke_list)[1]
        list_shapiro.append(p)
    return(list_shapiro)

##Welch_t_testがしたい関数
def Welch_t_test(one_keystroke_lists):
    # list_shapiro=t_test(one_keystroke_lists)
    Appropriate_one_keystroke_lists=[]
    list_shapiro_Appropriate_index=[]
    i=1
    for one_keystroke_list in one_keystroke_lists:
        p=stats.shapiro(one_keystroke_list)[1]
        i=str(i)
        i=i.zfill(2)
        if(p<=0.05):
            print(i+":正規分布である:"+str(p))
            Appropriate_one_keystroke_lists.append(one_keystroke_list)
        else:
            print(i+":正規分布ではない:"+str(p))
        i=int(i)
        i=i+1
    # for p in list_shapiro:
    #     i=str(i)
    #     i=i.zfill(2)
    #     if(p<=0.05):
    #         print(i+":正規分布である:"+str(p))
    #         Appropriate_one_keystroke_lists.append()
    #     else:
    #         print(i+":正規分布ではない:"+str(p))
    #     i=int(i)
    #     i=i+1
    i=0
    for line in Appropriate_one_keystroke_lists:
        # print(i)
        # print(line)
        # print("-------------")
        list_shapiro_Appropriate_index.append(i)
        i=i+1
    print(list_shapiro_Appropriate_index)
    for pair in itertools.combinations(list_shapiro_Appropriate_index, 2):
        # print(pair[0])
        # print(pair[1])
        # print(Appropriate_one_keystroke_lists[pair[0]])
        # print(Appropriate_one_keystroke_lists[pair[1]])
        welch=stats.ttest_ind(Appropriate_one_keystroke_lists[pair[0]],Appropriate_one_keystroke_lists[pair[1]], equal_var=False)
        print(welch[1])
        if(welch[1]<0.05):
            print("2つの標本平均に差がないとは言えない:"+str(welch))
        else:
            print("2つの標本平均に差がない"+str(welch))
        print("-------------")
    
##分散を計算するmain関数的な奴
def to_df_of_lines(path):
    ##csvを読み込みdfに変換
    df=get_df(path)
    ##dfの中から名前と打鍵スピードを取得
    nameAndspeed=get_nameAndspeed(df)
    name=nameAndspeed[0]
    speed=nameAndspeed[1]
    ##dfの中にあるtimeをhh:mm:ss.msからss.msに変換し代入
    strTime_to_floatSeconds(df)
    ##改行の数を取得
    newline_number=get_newline_number(df)
    # print(newline_number)
    ##改行した中身を取得
    lines=get_Completelines(df)
    #i=1
    # for line in lines:
    #     s=format(i,'02')
    #     print(s +" : "+line)
    #     i=i+1
    ##キーを押した時の時間をリストに入れて返す変数
    df_keystroke_line=get_DtoD_keystroke(df)
    #print(df_keystroke_line[0])
    ##get_DtoD_keystroke(df)で得られたリストの中から文字列orinnpikkuを取得
    get_line_orinnpikku(df_keystroke_line)
    ##get_DtoD_keystroke(df)で得られたリストの中から文字列orinnpikkuを取得しtime,operation,keyをlistに格納し返す
    df_orinpikku=df_get_keystroke_orinnpikku(df_keystroke_line)
    ##キーストロークの差分を計算
    diff_lines=get_DtoD_diff(df_orinpikku)
    ##各文字ごとにリストに格納し，リスト内の分散を計算する関数
    average_variance=get_variance(diff_lines)
    ##csvファイルに計算結果を書き込む
    write_average_variance_csv(name,speed,average_variance)
    print("-----------------------")

def get_average_variance():
    with open(CSV_PATH,'w') as f:
        f.close()
    recursive_file_check_get_average_variance(ROOT_PATH)

def get_welch():
    ##csvを読み込みdfに変換
    df=get_df(csv_filepath)
    # print(df)
    ##dfの中から名前と打鍵スピードを取得
    nameAndspeed=get_nameAndspeed(df)
    name=nameAndspeed[0]
    speed=nameAndspeed[1]
    # print(name,speed)
    ##dfの中にあるtimeをhh:mm:ss.msからss.msに変換し代入
    strTime_to_floatSeconds(df)
    # print(df)
    ##キーを押した時の時間をリストに入れて返す変数
    df_keystroke_line=get_DtoD_keystroke(df)
    #print(df_keystroke_line[0])
    ##get_DtoD_keystroke(df)で得られたリストの中から文字列orinnpikkuを取得
    get_line_orinnpikku(df_keystroke_line)
    ##get_DtoD_keystroke(df)で得られたリストの中から文字列orinnpikkuを取得しtime,operation,keyをlistに格納し返す
    df_orinpikku=df_get_keystroke_orinnpikku(df_keystroke_line)
    ##キーストロークの差分を計算
    diff_lines=get_DtoD_diff(df_orinpikku)
    count_orinpikku=0
    # for line in diff_lines:
    #     print(line)
    #     count_orinpikku=count_orinpikku+1
    # print(count_orinpikku)
    # print("------------")
    ##各キーのキーストロークをリストにして返す関数
    one_keystroke_lists=get_one_keystroke_lists(diff_lines)
    # for line in one_keystroke_lists:
    #     print(line)
    # print("------------")
    Welch_t_test(one_keystroke_lists)

def split_list(one_keystroke_lists):
    len_one_keystroke_lists=len(one_keystroke_lists[0])
    #print(len_one_keystroke_lists)
    split_list_number=int(len_one_keystroke_lists/3)
    #print(int(len_one_keystroke_lists/3))
    learning=[]
    inspection=[]
    measure=[]
    #n = 5
    for one_keystroke_list in one_keystroke_lists:
        leng_number=0
        tmp_learning=[]
        for i in range(0, len(one_keystroke_list), split_list_number):
            # print(one_keystroke_list[i: i+split_list_number])
            if(leng_number==0):
                tmp_learning.extend(one_keystroke_list[i: i+split_list_number])
            elif(leng_number==1):
                inspection.append(one_keystroke_list[i: i+split_list_number])
            elif(leng_number==2):
                measure.append(one_keystroke_list[i: i+split_list_number])
            elif(leng_number==3):
                tmp_learning.extend(one_keystroke_list[i: i+split_list_number])
            leng_number=leng_number+1
            # print("-----")
        #print("--------------------------")
        learning.append(tmp_learning)
    # print(learning)
    # print("-----")
    # print(measure)
    # print("-----")
    # print(inspection)
    # print("-----")
    return(learning,measure,inspection)

def average_keystroke(learning):
    average_learning=[]
    for line in learning:
        #print(mean(line))
        average_learning.append(mean(line))
        #print(mean(line))
    return(average_learning)

def measure_keystroke(average_learning,measure):
    i=0
    measure_deff=[]
    measure_Euclid_list=[]
    for line in measure:
        deff_measure=[]
        for one in line:
            ##二乗して数値をプラスにしたもの
            deff_measure.extend([(average_learning[i]-one)*(average_learning[i]-one)])
            #print((average_learning[i]-one)*(average_learning[i]-one))
        measure_deff.append(deff_measure)
        i=i+1
    line_len=len(measure_deff[0])
    for i in range(line_len):
        tmp_measure=[]
        for line in measure_deff:
            # print(line[i])
            tmp_measure.extend([line[i]])
        # print(tmp_measure)
        # print("----------")
        measure_Euclid=math.sqrt(sum(tmp_measure))
        measure_Euclid_list.extend([measure_Euclid])
    #print(measure_Euclid_list)
    Euclid_average=mean(measure_Euclid_list)
    # print("Euclid_average"+str(Euclid_average))
    E_def_E_Avg_Absolute_value=[]
    for one in measure_Euclid_list:
        # print(math.sqrt((one-Euclid_average)*(one-Euclid_average)))
        E_def_E_Avg_Absolute_value.extend([math.sqrt((one-Euclid_average)*(one-Euclid_average))])
    # print(E_def_E_Avg_Absolute_value)
    Avg_E_def_E_Avg_Absolute_value=mean(E_def_E_Avg_Absolute_value)
    print("Avg_E_def_E_Avg_Absolute_value:"+str(Avg_E_def_E_Avg_Absolute_value))
    # print("----------")
    # print(Avg_E_def_E_Avg_Absolute_value)
    return(Avg_E_def_E_Avg_Absolute_value,Euclid_average)

def inspection_keystroke(average_learning,inspection,Avg_E_def_E_Avg_Absolute_value,Euclid_average):
    i=0
    inspection_deff=[]
    inspection_deff_list=[]
    inspection_Euclid_list=[]
    inspection_E_def_E_Avg_Absolute_value_list=[]
    for line in inspection:
        # print(line)
        # print(average_learning[i])
        # print("---------------")
        deff_inspection=[]
        for one in line:
            #print(one)
            #print(math.sqrt((average_learning[i]-one)*(average_learning[i]-one)))
            ##二乗して数値を絶対値にしたもの
            deff_inspection.extend([(average_learning[i]-one)*(average_learning[i]-one)])
            #print("-----")
            #print((average_learning[i]-one)*(average_learning[i]-one))
        inspection_deff.append(deff_inspection)
        i=i+1
    # for line in inspection_deff:
    #     print(line)
    #     print("-----")
    line_len=len(inspection_deff[0])
    #print(line_len)
    for i in range(line_len):
        tmp_inspection=[]
        for line in inspection_deff:
            #print(line[i])
            tmp_inspection.extend([line[i]])
        inspection_deff_list.append(tmp_inspection)
        inspection_Euclid=math.sqrt(sum(tmp_inspection))
        inspection_Euclid_list.extend([inspection_Euclid])
    # print("-------")
    for line in inspection_Euclid_list:
        #print(math.sqrt((line-Euclid_average)*(line-Euclid_average)))
        inspection_E_def_E_Avg_Absolute_value_list.extend([math.sqrt((line-Euclid_average)*(line-Euclid_average))])
        #print("-----")
    #average_learning-inspection_deff_listの処理を書く
    print("inspection_E_def_E_Avg_Absolute_value_list:"+str(inspection_E_def_E_Avg_Absolute_value_list))
    # print("Avg_E_def_E_Avg_Absolute_value:"+str(Avg_E_def_E_Avg_Absolute_value))
    inspection_succsess_number_of_times=0
    inspection_number_of_times=0
    print("----")
    for line in inspection_E_def_E_Avg_Absolute_value_list:
        if(line<=Avg_E_def_E_Avg_Absolute_value):
            print("succsess!!")
            inspection_succsess_number_of_times=inspection_succsess_number_of_times+1
            inspection_number_of_times=inspection_number_of_times+1
        else:
            print("fail")
            inspection_number_of_times=inspection_number_of_times+1
    succsess_rate=(inspection_succsess_number_of_times/inspection_number_of_times)*100
    print("succsess_rate:"+str(succsess_rate)+"%")
    print("----")
    # print("------------------------------")
    # print("average_learning:"+str(average_learning))
    # print("Euclid_average:"+str(Euclid_average))
    len_inspection=len(inspection[0])
    # print("len_inspection:"+str(len_inspection))
    return(len_inspection,inspection_succsess_number_of_times,succsess_rate)


def write_get_FAR_FRR_csv(name,speed,Avg_E_def_E_Avg_Absolute_value,Euclid_average,average_learning):
    with open(CSV_PATH_get_FAR_FRR,'a') as f:
        writer=csv.writer(f)
        write_list=[name,speed,Avg_E_def_E_Avg_Absolute_value,Euclid_average]
        write_list.extend(average_learning)
        writer.writerow(write_list)
        print("FAR_FRR_csv書き込み完了")
        f.close()

def write_get_CSV_PATH_inspection_csv(name,speed,inspection):
    with open(CSV_PATH_inspection,'a') as f:
        writer=csv.writer(f)
        len_inspection=len(inspection[0])
        #print(len_inspection)
        for i in range(len_inspection):
            write_list=[name,speed]
            for line in inspection:
                #print(line)
                write_list.extend([line[i]])
            writer.writerow(write_list)
        print("inspection_csv書き込み完了")
        f.close()

def get_FAR_FRR(path):
    ##csvを読み込みdfに変換
    df=get_df(path)
    # print(df)
    ##dfの中から名前と打鍵スピードを取得
    nameAndspeed=get_nameAndspeed(df)
    name=nameAndspeed[0]
    speed=nameAndspeed[1]
    # print(name,speed)
    ##dfの中にあるtimeをhh:mm:ss.msからss.msに変換し代入
    strTime_to_floatSeconds(df)
    # print(df)
    ##キーを押した時の時間をリストに入れて返す変数
    df_keystroke_line=get_DtoD_keystroke(df)
    #print(df_keystroke_line[0])
    ##get_DtoD_keystroke(df)で得られたリストの中から文字列orinnpikkuを取得
    get_line_orinnpikku(df_keystroke_line)
    ##get_DtoD_keystroke(df)で得られたリストの中から文字列orinnpikkuを取得しtime,operation,keyをlistに格納し返す
    df_orinpikku=df_get_keystroke_orinnpikku(df_keystroke_line)
    ##キーストロークの差分を計算
    diff_lines=get_DtoD_diff(df_orinpikku)
    count_orinpikku=0
    # for line in diff_lines:
    #     print(line)
    #     count_orinpikku=count_orinpikku+1
    # print(count_orinpikku)
    # print("------------")
    ##各キーのキーストロークをリストにして返す関数
    one_keystroke_lists=get_one_keystroke_lists(diff_lines)
    # for line in one_keystroke_lists:
    #     print(line)
    # print("------------")
    split_text=split_list(one_keystroke_lists)
    learning=split_text[0]
    measure=split_text[1]
    inspection=split_text[2]
    # for line in inspection:
    #     print(line)
    # print("------------")
    average_learning=average_keystroke(learning)
    # print(average_learning)
    Avg_E_def_E_Avg_Absolute_value=measure_keystroke(average_learning,measure)
    Euclid_average=Avg_E_def_E_Avg_Absolute_value[1]
    Avg_E_def_E_Avg_Absolute_value=Avg_E_def_E_Avg_Absolute_value[0]
    inspection_keystroke_return=inspection_keystroke(average_learning,inspection,Avg_E_def_E_Avg_Absolute_value,Euclid_average)
    len_inspection=inspection_keystroke_return[0]
    inspection_succsess_number_of_times=inspection_keystroke_return[1]
    succsess_rate=inspection_keystroke_return[2]
    write_get_CSV_PATH_inspection_csv(name,speed,inspection)
    write_get_FAR_FRR_csv(name,speed,Avg_E_def_E_Avg_Absolute_value,Euclid_average,average_learning)
    print("------------------------")

def recursive_file_check_get_FAR_FRR(path):
    if os.path.isdir(path):
        #directoryだったら中のファイルに対して再帰的にこの関数を実行
        files=os.listdir(path)
        for file in files:
            recursive_file_check_get_FAR_FRR(path+"/"+file)
    else:
        #exam.utf8.Complete.csvだったら処理を実行
        if path[-22:]=='exam.utf8.Complete.csv':
            print(path)
            get_FAR_FRR(path)

def main_get_FAR_FRR():
    with open(CSV_PATH_inspection,'w') as f:
        f.close()
    with open(CSV_PATH_get_FAR_FRR,'w') as f:
        f.close()
    recursive_file_check_get_FAR_FRR(ROOT_PATH)

#get_average_variance()
#get_FAR_FRR()
get_welch()
#main_get_FAR_FRR()
