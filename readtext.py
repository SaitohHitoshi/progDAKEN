import os
import sys
import pathlib
ROOT_PATH="./FIT_data"

def getEnterandSpace_result(file_path):
    path_exam = file_path
    path_result='EnterAndSpace_resolt.txt'
    with open(path_exam,'r') as f_exam:
        lines = f_exam.readlines()
        #参照するpathを表示
        #print(path_exam)
        #/nを,に変更しline_stripに代入
        lines_strip = [line.strip() for line in lines ] 
        #行の中にEnterがある行をlist化
        list_of_Enter=[i for i,line_s in enumerate(lines_strip) if 'Enter' in line_s] 
        #行の中にSpaceがある行をlist化
        list_of_Space=[i for i,line_s in enumerate(lines_strip) if 'Space' in line_s] 
        #EnterとSpaceの数をカウント
        count_list_of_Enter=len(list_of_Enter)
        count_list_of_Space=len(list_of_Space)
        #表示
        # print(list_of_Enter)
        # print(count_list_of_Enter)
        # print(list_of_Space)
        # print(count_list_of_Space)
        exam_filename=os.path.basename(path_exam)
        f_exam.close()
    with open(path_result,'a') as f_result:
        f_result.write(exam_filename)
        f_result.write('\n')
        f_result.write('Enter:'+ str(count_list_of_Enter))
        f_result.write('\n')
        f_result.write('Space:'+str(count_list_of_Space))
        f_result.write('\n')
        f_result.close()

def recursive_file_check(path):
    if os.path.isdir(path):
        #directoryだったら中のファイルに対して再帰的にこの関数を実行
        files=os.listdir(path)
        for file in files:
            recursive_file_check(path+"/"+file)
    else:
        #*exam.utf8.txtだったら処理
        if path[-13:]=='exam.utf8.txt':
            getEnterandSpace_result(path)

def countEnterAndSpace():
    path='./EnterAndSpace_resolt.txt'

    with open(path) as f:
        lines=f.readlines()
        lines_strip = [line.strip() for line in lines]
        EnterLine=[line for line in lines_strip if 'Enter' in line]
        SpaceLine=[line for line in lines_strip if 'Space' in line]
        
        # print(EnterLine)
        # print(SpaceLine)
        f.close()

    countEnter=float(0)
    countSpace=float(0)
    for w in EnterLine:
        countEnter+=int(w[6:])
    for w in SpaceLine:
        countSpace+=int(w[6:])

    with open(path,'a') as f:
        f.write("合計Enter打鍵回数" + str(countEnter))
        f.write('\n')
        f.write("合計Space打鍵回数" +str(countSpace))
        f.write('\n')
        f.write("実験件数："+ str(len(EnterLine)))
        f.write('\n')
        f.write("平均Enter打鍵回数:"+ str(countEnter/len(EnterLine)))
        f.write('\n')
        f.write("平均Space打鍵回数:"+ str(countSpace/len(EnterLine)))
        f.write('\n')
        f.close()
    
def initialize():
    path_result='EnterAndSpace_resolt.txt'
    with open(path_result,'w') as f_exam:
        pass
    f_exam.close()

initialize()
recursive_file_check(ROOT_PATH)
countEnterAndSpace()

