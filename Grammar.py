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


first_index = []
first = []
follow = []

def first_set():
    global grammar
    global extend_grammar
    notT = init_notT()
    global first
    global first_index
    for i in range(0,len(notT)):
        first.append([-1])
        first_index.append([-1])
    first_end = [0]*len(extend_grammar)#判断扩展语句的每一条是否执行完
    while first_end.count(1)!=len(first_end):
        for i in range(0, len(extend_grammar)):
            sa = extend_grammar[i].split("->")
            index = first_isnT(sa[1], notT)  # 即首项是非终结符
            if index == -1 and first_end[i]== 0:  # 若首项不是非终结符且此语句尚未执行
                if first[extend_index[i]] == [-1]:
                    first[extend_index[i]] = []
                    first[extend_index[i]].append(sa[1][0])
                    first_index[extend_index[i]] = [i]
                    first_end[i] = 1
                else :
                    first[extend_index[i]].append(sa[1][0])
                    first_index[extend_index[i]].append(i)
                    first_end[i] = 1
            elif index != -1 and first_end[i]== 0:  # 若首项是非终结符且此语句尚未执行
                if first[index] != [-1]:  # 若当前第一项的first不为空
                    #index  非终结符序号
                    length = 0
                    end = ""
                    while 1:
                        rest = sa[1][length:]
                        index = first_isnT(rest, notT)  # 判断下一个非终结符
                        length = length + len(notT[index])  # 更新length
                        if first[index] == [-1]:  # 还没生成
                            end = "break"
                            break
                        elif index == -1:  # 终结符,加入并跳出
                            if first[extend_index[i]] == [-1]:  # 如果为第一次先清空
                                first[extend_index[i]] = []
                                first_index[extend_index[i]] = []
                            first[extend_index[i]].append(rest[0])
                            first_index[extend_index[i]].append(i)
                            end = "terminal"
                            break
                        elif len(sa[1]) == length: # 判断到头了,但最后一个没执行
                            end = "last"
                            break
                        elif first[index].count("%") == 0:
                            end = "without"
                            break
                        else:
                            if first[extend_index[i]] == [-1]:  # 如果为第一次先清空
                                first[extend_index[i]] = []
                                first_index[extend_index[i]] = []
                            for k in range(0, len(first[index])):  # 加入不重复且不为空的
                                if first[extend_index[i]].count(first[index][k]) == 0 and first[index][k] != "%":
                                    first[extend_index[i]].append(first[index][k])  # 把该非终结符的first并入
                                    first_index[extend_index[i]].append(i)

                    if end == "break": #没生成跳出
                        continue
                    elif end == "terminal": #终结符跳出，该语句执行完
                        first_end[i] = 1
                    elif end == "without":
                        if first[extend_index[i]] == [-1]:  # 如果为第一次先清空
                            first[extend_index[i]] = []
                            first_index[extend_index[i]] = []
                        for k in range(0, len(first[index])):
                            if first[extend_index[i]].count(first[index][k]) == 0:
                                first[extend_index[i]].append(first[index][k])
                                first_index[extend_index[i]].append(i)
                        first_end[i] = 1
                    elif end == "last": #全部判断完跳出，该语句执行完
                        if first[extend_index[i]] == [-1]:  # 如果为第一次先清空
                            first[extend_index[i]] = []
                            first_index[extend_index[i]] = []
                        for k in range(0, len(first[index])):
                            if first[extend_index[i]].count(first[index][k]) == 0 and first[index][k] != "%":
                                first[extend_index[i]].append(first[index][k])
                                first_index[extend_index[i]].append(i)
                        if first[index].count("%") != 0:
                            first[extend_index[i]].append("%")
                            first_index[extend_index[i]].append(i)
                        first_end[i] = 1
                else:  #当前第一项的first为空,跳过
                    continue
            # print("FIRST:", first)
            # print("endf:", first_end)


    print("first:", first)
    print("first_index:",first_index)
    return first


def follow_set():
    global grammar
    global extend_grammar
    global follow
    global first
    notT = init_notT()
    exp = []
    for i in range(0, len(extend_grammar)):
        sa = extend_grammar[i].split("->")
        exp.append(sa[1]) #所有表达式
    for i in range(0,len(notT)):
        follow.append([-1])
    follow[0] =['$']  #对开始项加入$
    flag = 1
    while flag :
        flag = 0
        for i in range(0, len(notT)):
            for j in range(0, len(exp)):
                x = exp[j].find(notT[i])
                if x != -1:  # 如果找到了非终结符
                    if x + len(notT[i]) >= len(exp[j]):  # 结尾
                        if follow[extend_index[j]] != [-1]:
                            if follow[i] == [-1]:
                                follow[i].clear()
                            for k in range(0, len(follow[extend_index[j]])):  # 加入到当前终结符的follow
                                if follow[i].count(follow[extend_index[j]][k]) == 0:
                                    follow[i].append(follow[extend_index[j]][k])
                                    flag = 1
                                    """mark"""

                    elif exp[j][x + len(notT[i])] != "'":  # 不是结尾 判断后面还有没有’
                        s = exp[j][x + len(notT[i]):]
                        index = find_notT(s, notT)  # 找该非终结符后面第一个是不是非终结符 若有 返回是第几个非终结符
                        if index == -1:  # 若不是 加入
                            if follow[i] == [-1]:
                                follow[i] = [exp[j][x + len(notT[i])]]
                            else:
                                if follow[i].count(exp[j][x + len(notT[i])]) == 0:
                                    follow[i].append(exp[j][x + len(notT[i])])
                                    flag = 1
                                    """mark"""
                        else:  # 若是 把该非终结符的first加入
                            if follow[i] == [-1]:
                                follow[i].clear()
                                for k in range(0, len(first[index])):
                                    if first[index][k] != '%':
                                        follow[i].append(first[index][k])
                            elif follow[i] != [-1]:
                                for k in range(0, len(first[index])):
                                    if follow[i].count(first[index][k]) == 0 and first[index][k] != '%':  # 加入不为空的
                                        follow[i].append(first[index][k])
                            if first[index].count('%') != 0:
                                mark = extend_index[j]
                                if follow[mark] != [-1]:
                                    for k in range(0, len(follow[mark])):
                                        if follow[i].count(follow[mark][k]) == 0:
                                            follow[i].append(follow[mark][k])
                                            flag = 1
                                            """mark"""
                    else:
                        continue
                        # print("skip")
                #print(follow)
    print("follow:",follow)
    return follow