import os
import sys
import pathlib
ROOT_PATH="./FIT_data_copy"

#ファイルを捜索する関数
def recursive_file_check(path):
    if os.path.isdir(path):
        #directoryだったら中のファイルに対して再帰的にこの関数を実行
        files=os.listdir(path)
        for file in files:
            recursive_file_check(path+"/"+file)
    else:
        #*exam.utf8.txtだったら処理
        if path[-13:]=='exam.utf8.txt':
            toCSV(path)

#ファイルパスを作る関数
def makepath(path):
    i=-1
    while(1):
        if(path[i]=="."):
            break
        else:
            i=i-1
    #print(i)#デバック用
    exam_filepath=path
    #print(path[:i+1]+"New"+path[i+1:])#デバック用
    new_filepath=path[:i]+".New"+path[i:]
    #print(path[:i+1]+"Complete"+path[i+1:])#デバック用
    complete_filepath=path[:i]+".Complete"+path[i:]
    return(exam_filepath,new_filepath,complete_filepath)

# #被験者の名前と打鍵速度を取得しreturnする関数
def get_subnameAndspeed(exam_filepath):
    exam_dir=os.path.dirname(exam_filepath)
    #print(exam_dir)#デバック用
    slash=0
    i=-1
    firstslash=0
    secondslash=0
    while(slash<3):
        if(exam_dir[i]=="/"):
            slash=slash+1
            i=i-1
            if(slash==1):
                firstslash=i
            if(slash==2):
                secondslash=i
        else:
            i=i-1
    #print(exam_dir[firstslash+2:])#デバック用
    keystroke_speed=exam_dir[firstslash+2:]
    #print(exam_dir[secondslash+2:firstslash+1])#デバック用
    subname=exam_dir[secondslash+2:firstslash+1]
    return(keystroke_speed,subname)

#new_fileを生成する関数
def split_text(exam_filepath,new_filepath,subname,speed):
    f=open(exam_filepath, 'r', encoding='utf-8')
    f2=open(new_filepath, 'w', encoding='utf-8')
    exam_data=f.readlines()
    exam_data.pop(0)
    subnameAndspeed=get_subnameAndspeed(exam_filepath)
    for exam_line in exam_data:
        if (not(exam_line == "\n")):
            exam_line=exam_line[0:10]+","+exam_line[11:22]+","+exam_line[24:25]+","+exam_line[27:]
            exam_line=subname+","+speed+","+exam_line
            f2.write(exam_line)
            #f2.write("\n")
    f.close()
    f2.close()

#テキストの差の秒数を削除する関数
def delete_last_second(new_filepath,complete_filepath):
    f1=open(new_filepath,'r', encoding='utf-8')
    f2=open(complete_filepath,'w', encoding='utf-8')
    new_exam_lines=f1.readlines()
    for new_exam_line in new_exam_lines:
        new_exam_line_length=len(new_exam_line)
        i=0
        str_Complete_line=""
        while i<new_exam_line_length:
            if new_exam_line[i]==" " or new_exam_line=="\n":
                break
            else:
                str_Complete_line+=new_exam_line[i]
                i=i+1
        str_Complete_line+="\n"
        #print(str_Complete_line)
        f2.write(str_Complete_line)
    f1.close()
    f2.close()

#謎の改行をPOPさせる関数
def delet_new_line(complete_filepath):
    f1=open(complete_filepath,"r", encoding="utf8")
    pop_variable=0
    pop_Complete_lines=[]
    Complete_lines=f1.readlines()
    for Complete_line in Complete_lines:
        if(Complete_line[0]=="\n"):
            pop_Complete_lines.append(pop_variable)
            pop_variable=pop_variable+1
        else:
            pop_variable=pop_variable+1
    f1.close()
    #print(pop_Complete_lines)#デバック用
    for pop_Complete_line in reversed(pop_Complete_lines):
        #print(pop_Complete_line)#デバック用
        Complete_lines.pop(pop_Complete_line)
    f1=open(complete_filepath,"w", encoding="utf8")
    for Complete_line in Complete_lines:
        f1.write(Complete_line)
    f1.close()

#１行目に被験者名と打鍵スピードを追加する関数
def add_subnameAndSpeed(complete_filepath,subname,keystroke_speed):
    f1=open(complete_filepath,"r",encoding="utf8")
    Complete_lines=f1.readlines()
    f1.close()
    list_subnameAndSpeed=[subname+","+keystroke_speed+"\n"]
    Complete_lines=list_subnameAndSpeed+Complete_lines
    f1=open(complete_filepath,"w", encoding="utf8")
    for Complete_line in Complete_lines:
        f1.write(Complete_line)
    f1.close()


#ファイルパスを受け取ってCSVに変換してく中枢の関数
def toCSV(path):
    #使うpathを生成する
    all_filepath=makepath(path)
    #print(exam_filepath)#デバック用
    exam_filepath=all_filepath[0]
    #print(new_filepath)#デバック用
    new_filepath=all_filepath[1]
    #print(complete_filepath)#デバック用
    complete_filepath=all_filepath[2]
    
    #被験者と打鍵スピードを取得する
    subnameAndspeed=get_subnameAndspeed(exam_filepath)
    speed=subnameAndspeed[0]
    subname=subnameAndspeed[1]
    #newfileを生成する
    split_text(exam_filepath,new_filepath,subname,speed)
    #completefileを生成する
    delete_last_second(new_filepath,complete_filepath)
    #謎の改行の削除
    delet_new_line(complete_filepath)
    #１行目に被験者名と打鍵スピードを追加する関数
    #add_subnameAndSpeed(complete_filepath,subname,speed)

def main():
    recursive_file_check(ROOT_PATH)

main()

