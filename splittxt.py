import os


exam_filepath="./FIT_data/ando/fast/20220614_16373_exam.utf8.txt"

def get_subnameAndspeed(exam_filepath):
    exam_dirname=os.path.dirname(exam_filepath)
    #print(exam_dirname)
    split_exam_dirname=exam_dirname
    subject_name=split_exam_dirname[11:15]
    keystroke_speed=split_exam_dirname[16:20]
    # print(subject_name)
    # print(keystroke_speed)
    return(subject_name,keystroke_speed)

def split_text(exam_filepath):
    f=open(exam_filepath, 'r', encoding='utf-8')
    exam_data=f.readlines()
    for exam_line in exam_data:
        subnameAndspeed=get_subnameAndspeed(exam_filepath)
        exam_line=subnameAndspeed[0]+","+subnameAndspeed[1]+","+exam_line
        print(exam_line)
    f.close()

split_text(exam_filepath)
# subnameAndspeed=get_subnameAndspeed(exam_filepath)
# print(subnameAndspeed[0])
# print(subnameAndspeed[1])
