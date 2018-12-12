"""  处理文法   """
grammar=[]
extend_grammar = []
extend_index = [] #记录对应的表达式的脚标


"""提取左公因子"""
def del_leftfact(sentence:int):
    global grammar
    sa = grammar[sentence].split("->")
    sb = sa[1].split("|")  # 拆分出每个分支
    count = 1 #控制有多少’
    while 1:
        s=""
        for i in range(0,count):
            s=s+"'"
        index = []  # 含有最长子序列的元素的脚标
        marki = -1
        maxj = -1
        for i in range(0, len(sb)):
            for j in range(1, len(sb[i])+1):
                newindex = []  # 含有当前子序列的元素的脚标
                for k in range(0, len(sb)):
                    res = sb[k].find(sb[i][0:j])
                    if res == 0:  # 如果在其他表达式内找到了相同开头
                        newindex.append(k)
                if j== 0 :
                    index = newindex
                    marki = i
                    maxj = j
                elif len(newindex) > 1 and j > maxj :# 序列不空且长度比之前长
                    index = newindex
                    marki = i
                    maxj = j
                #print("res:",marki,maxj)
        #print(sb[marki][0:maxj])  # 最大公因子
        #print(index)
        if len(index) == 0:
            break
        else:
            if len(index) != 0:
                resb = sa[0] + s + "->"
                for i in range(0, len(index)):
                    if i == 0:
                        if maxj != len(sb[index[i]]):
                            resb = resb + sb[index[i]][maxj:]
                        else:
                            resb = resb + "%"
                    else:
                        if maxj != len(sb[index[i]]):
                            resb = resb + "|" + sb[index[i]][maxj:]
                        else:
                            resb = resb + "|" + "%"
                sb.append(sb[marki][0:maxj] + sa[0] + s)
                for i in range(0, len(index)):
                    del sb[index[i] - i]
                #print("sb:",sb)
                grammar.append(resb)
                count += 1
    #print("res:",sb)
    newgrammar = sa[0]+"->"
    if len(sb) > 1:
        for i in range(0, len(sb) - 1):
            newgrammar = newgrammar + sb[i] + "|"
        newgrammar = newgrammar + sb[i + 1]
    else :
        newgrammar = newgrammar + sb[0]

    grammar[sentence] = newgrammar

"""消除直接左递归"""
def del_leftrec(sentence:int):
    global grammar
    sa=grammar[sentence].split("->")
    resa=sa[0]+"->"
    resb=sa[0]+"'"+"->"
    #递归的符号sa[0]
   #右侧的式子 sa[1]
    sb=sa[1].split("|") #拆分出每个分支
     #A->As1|As2|As3|b1|b2|b3|As4|b4  A->b1A|c|d2
    count=0
    flag=0#判断是否存在递归
    for i in range(0,len(sb)):
        index=sb[i].find(sa[0])
        if index==0:
            resb=resb+sb[i][1:]+sa[0]+"'"+"|"
            flag=1
        else:
            if count==0:
                resa=resa+sb[i] + sa[0] + "'"
                count+=1
            else:
                resa=resa+"|"+sb[i] + sa[0] + "'"
    resb=resb+"%"#最后加入空
    if flag:
        grammar[sentence] = resa
        grammar.append(resb)
    #print(resa)
    #print(resb)
    return 0

"""消除一般左递归"""
def normalleft():
    global grammar
    n = len(grammar)
    notT = []
    exp = []
    for i in range(0, n):
        sa = grammar[i].split("->")
        notT.append(sa[0])
        exp.append(sa[1])

    for i in range(0, n):
        elementi = exp[i].split("|")
        #print("i:",elementi)
        for j in range(0, i):
            for k in range(0, len(elementi)):
                index = elementi[k].find(notT[j])  # 对Ai用|分割的每一项寻找是否以Aj开头
                if index == 0:  # 找到Ai->Aj
                    elementj = exp[j].split("|")  # 分割成元素
                    #print("j:",elementj)
                    rest = elementi[k][len(notT[j]):]  # 截取该元素中剩下的部分
                    #print(rest,j)
                    #print(elementi)
                    elementi[k] = elementj[0] + rest
                    for m in range(1, len(elementj)):
                        elementi.insert(k, elementj[m] + rest)
                    #print(elementi)
                    #print(elementj)

        exp[i] = "" #clear
        if len(elementi) > 1:
            for l in range(0, len(elementi) - 1):
                exp[i] = exp[i] + elementi[l] + "|"
            exp[i] = exp[i] + elementi[l + 1]
        else:
            exp[i] = exp[i] + elementi[0]
        s = notT[i]+"->"+exp[i]
        #print(s)
        grammar[i] = s
       # print("处理前")
        #print(grammar)
        del_leftrec(i)
        sa = grammar[i].split("->")
        exp[i] = sa[1]
        #print("处理后")
        #print(grammar)

"""扩展文法，去掉|"""
def extend():
    if grammar[0].find("|"):
        sa = grammar[0].split("->")
        grammar.insert(0,sa[0] + "~" + "->" + sa[0])
    for i in range(0,len(grammar)):
        sa = grammar[i].split("->")
        sb = sa[1].split("|")
        for j in range(0,len(sb)):
            res = sa[0]+"->"+sb[j]
            extend_grammar.append(res)
            extend_index.append(i)

"""求非终结符"""
def init_notT():
    global grammar
    notT = []
    for i in range(0, len(grammar)):
        sa = grammar[i].split("->")
        notT.append(sa[0])  # 得到所有非终结符
    return notT

""" """
def first_isnT(str,notT):
    for i in range(0,len(notT)):
        if str.find(notT[i]) == 0:
            return i
    return -1

"""求字符串开头是否为非终结符"""
def find_notT(s,notT):
    res = s[0]
    for j in range(1, len(s)):
        if s[j] == "'":
            res = res + "'"
        else:
            break
    for i in range(0, len(notT)):
        if res == notT[i]:
            return i
    return -1