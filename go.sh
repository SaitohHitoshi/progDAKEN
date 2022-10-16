#/bin/sh
find -name "*.utf8.txt" -exec ./getlog {} \; | grep -v "^$" >out.txt
grep -v '(' out.txt | grep -v '\[' | grep -v Mode | grep -v User | grep -v File >out2.txt
