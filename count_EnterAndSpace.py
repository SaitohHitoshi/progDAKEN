path='./EnterAndSpace_resolt.txt'

with open(path) as f:
    lines=f.readlines()
    lines_strip = [line.strip() for line in lines]
    EnterLine=[line for line in lines_strip if 'Enter' in line]
    SpaceLine=[line for line in lines_strip if 'Space' in line]
    
    # print(EnterLine)
    # print(SpaceLine)
    f.close()

countEnter=0
countSpace=0
for w in EnterLine:
    countEnter+=int(w[6:])
    
for w in SpaceLine:
    countSpace+=int(w[6:])

print(countEnter)
print(countSpace)
print("実験件数："+ str(len(EnterLine)))
print("平均Enter打鍵回数:"+ str(countEnter/len(EnterLine)))
print("平均Enter打鍵回数:"+ str(countSpace/len(EnterLine)))
