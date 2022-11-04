import pandas as pd
import os
from statistics import variance

csv_filepath="./FIT_data_copy/okada/fast/20220616_140737_exam.utf8.Complete.csv"
csv_filepath2="./FIT_data_copy/okada/normal/20220616_135928_exam.utf8.Complete.csv"
csv_filepath3="./FIT_data_copy/okada/slow/20220616_135047_exam.utf8.Complete.csv"
csv_filepath4="./FIT_data_copy/kasahara/slow/20220615_185529_exam.utf8.Complete.csv"
csv_filepath5="./FIT_data_copy/ando/fast/20220614_16373_exam.utf8.Complete.csv"

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

#改行した行を取得する関数
def get_Completelines(df):
    count_Enter=0
    new_line=0
    str_line=""
    lines=[]
    keystrokeDatas=[]
    keystrokeData=[]
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
    i=1
    for line in lines:
        s=format(i,'02')
        print(s +" : "+line)
        i=i+1
    for ksdata in keystrokeDatas:
        for a_ksdata in ksdata:
            print(a_ksdata)
        print("--------------------------------------")

#キーを押した時の時間をリストに入れて返す変数
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
    print(orinpikkuList)
    
def df_get_keystroke_orinnpikku(df_keystroke_line):
    orinpikkuList=[]
    keystrokes_line_list=[]
    keystrokes_line_list.clear()
    df_keystrokes_line_list=[]
    str1="orinnpikku"
    str2="orinpikku"#空白は文字列の長さを合わせるため
    for df_keystroke in df_keystroke_line:
        str_line=""
        print("--------------------")
        mp_time=0.0
        tmp_operation=""
        tmp_key=""
        for index,data in df_keystroke.iterrows():
            time=data["time"]
            operation=data["operation"]
            key=data["key"]
            print(time+":"+operation+":"+key)
            strlen=len(str_line)
            if strlen==0:
                str_line=str_line+key
                strlen=len(str_line)
                keystrokes_line_list.append([time,operation,key])
                print("一文字目を入力:"+str(strlen)+":"+str_line)
            else:
                if((str_line[0]==str1[0]) or (str_line[0]==str2[0])):
                    if((str1==str_line) or (str2==str_line)):
                        orinpikkuList.append([str_line])
                        df_keystrokes_line=pd.DataFrame(keystrokes_line_list,columns=['time','operation','key'])
                        df_keystrokes_line_list.append(df_keystrokes_line)
                        print("文字列完成:"+str(strlen)+":"+str_line)
                        str_line=""
                        strlen=len(str_line)
                        keystrokes_line_list.clear()
                        print("完成したので文字列を削除:"+str(strlen)+":"+str_line)
                    elif(str1[strlen]==key):
                        str_line=str_line+key
                        strlen=len(str_line)
                        keystrokes_line_list.append([time,operation,key])
                        tmp_time=time
                        tmp_operation=operation
                        tmp_key=key
                        print("文字列に文字を追加:"+str(strlen)+":"+str_line)
                    elif(str2[strlen]==key):
                        if(key=="p"):
                            str_line=str_line+key
                            strlen=len(str_line)
                            print(tmp_time,tmp_operation,tmp_key)
                            keystrokes_line_list.append([tmp_time,tmp_operation,tmp_key])
                            print("文字列にnの2個目を追加:"+str(strlen)+":"+str_line)
                            keystrokes_line_list.append([time,operation,key])
                            print("文字列に文字を追加:"+str(strlen)+":"+str_line)
                        else:
                            str_line=str_line+key
                            strlen=len(str_line)
                            keystrokes_line_list.append([time,operation,key])
                            tmp_time=time
                            tmp_operation=operation
                            tmp_key=key
                        print("文字列に文字を追加:"+str(strlen)+":"+str_line)
                    else:
                        str_line=""
                        strlen=len(str_line)
                        keystrokes_line_list.clear()
                        print("in文字列を削除:"+str(strlen)+":"+str_line)
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

def get_variance(diff_lines):
    len_list=len(diff_lines)
    print(len_list)
    max_len=len(diff_lines[0])
    print(max_len)
    one_keystroke_lists=[]
    for i in range(max_len):
        one_keystroke_list=[]
        # print(str(i+1)+"個め")
        for diff_line in diff_lines:
            #print(diff_line[i])
            one_keystroke_list.append(diff_line[i])
        one_keystroke_lists.append(one_keystroke_list)
    i=1
    sum_variance=0
    for one_phrase in one_keystroke_lists:
        print(str(i)+"個め")
        #print(one_phrase)
        print(variance(one_phrase))
        sum_variance=sum_variance+variance(one_phrase)
        i=i+1
    print("sum_variance:"+str(sum_variance))


def main():
    print(csv_filepath5)
    df=get_df(csv_filepath5)
    strTime_to_floatSeconds(df)
    newline_number=get_newline_number(df)
    print(newline_number)
    get_Completelines(df)
    df_keystroke_line=get_DtoD_keystroke(df)
    get_line_orinnpikku(df_keystroke_line)
    df_orinpikku=df_get_keystroke_orinnpikku(df_keystroke_line)
    diff_lines=get_DtoD_diff(df_orinpikku)
    get_variance(diff_lines)
    

main()