#!/bin/sh

# dir_path="/home/karaaage/code/progDAKEN/FIT_data/*"
# dirs='find $dir_path -type f -name *exam.utf8.txt'

# for dir in $dirs;
# do
#   echo $dir
#   python readtext.py $dir
# done

# # dir_path="*"
# # dirs='find $dir_path -name *utf8.txt'

find /home/karaaage/code/progDAKEN/FIT_data/ -type f -name *exam.utf8.txt | xargs -I FILE python readtext.py FILE