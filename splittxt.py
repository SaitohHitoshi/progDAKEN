import os


exam_filepath="./FIT_data/ando/fast/20220614_16373_exam.utf8.txt"
new_filepath="./FIT_data/ando/fast/"+"New_"+"20220614_16373_exam.utf8.txt"

#被験者の名前と打鍵スピードを取得する関数
def get_subnameAndspeed(exam_filepath):
    exam_dirname=os.path.dirname(exam_filepath)
    #print(exam_dirname)
    split_exam_dirname=exam_dirname
    subject_name=split_exam_dirname[11:15]
    keystroke_speed=split_exam_dirname[16:20]
    # print(subject_name)
    # print(keystroke_speed)
    return(subject_name,keystroke_speed)

#空白行を消す関数
def delete_text(exam_filepath):
    f1=open(exam_filepath, 'r', encoding='utf-8')
    exam_data=f1.readlines()
    for exam_line in exam_data:
        if (not(exam_line[0:1] == "\n")):
            delete_examline=exam_line+"\n"
    f1.close()
    f2=open(exam_filepath, 'w', encoding='utf-8')
    for exam_line in delete_examline:
        f2.write(exam_line)
    f2.close()

# def add_period(exam_line):
#     str_exam_line=str(exam_line)
#     str_exam_line=exam_line.replace(' ',',')
#     str_exam_line[36:37]=","
#     exam_line=str_exam_line
#     return(exam_line)

#テキストをcsv形式に変換する関数
def split_text(exam_filepath):
    f=open(exam_filepath, 'r', encoding='utf-8')
    f2=open(new_filepath, 'w', encoding='utf-8')
    exam_data=f.readlines()
    subnameAndspeed=get_subnameAndspeed(exam_filepath)
    for exam_line in exam_data:
        if (not(exam_line == "\n")):
            exam_line=subnameAndspeed[0]+","+subnameAndspeed[1]+","+exam_line
            exam_line=exam_line[0:20]+","+exam_line[21:]
            exam_line=exam_line[:31]+","+exam_line[34:]
            exam_line=exam_line[:34]+exam_line[35:]
            exam_line=exam_line[:34]+","+exam_line[34:]
            exam_line=exam_line[:33]+exam_line[35:]
            exam_line=exam_line[:33]+","+exam_line[33:]
            print(exam_line)
            f2.write(exam_line)
            #f2.write("\n")
    f.close()
    f2.close()
    #delete_text(exam_filepath)

split_text(exam_filepath)
# subnameAndspeed=get_subnameAndspeed(exam_filepath)
# print(subnameAndspeed[0])
# print(subnameAndspeed[1])
