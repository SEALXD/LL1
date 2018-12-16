"""只能处理字母，认为一个字母是一个标识符  终结符必须是一个字母"""
"""可以发现二义性冲突 没有检测回溯"""
from prettytable import PrettyTable
from Grammar import *
import sys

"""  求First和Follow   """
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
    row = []
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
                        #print("isend")
                        #print(x, notT[i])
                        #print(extend_index[j], notT[extend_index[j]])
                        if follow[extend_index[j]] != [-1]:
                            if follow[i] == [-1]:
                                follow[i].clear()
                            for k in range(0, len(follow[extend_index[j]])):  # 加入到当前终结符的follow
                                if follow[i].count(follow[extend_index[j]][k]) == 0:
                                    follow[i].append(follow[extend_index[j]][k])
                                    flag = 1
                                    """mark"""

                        # print(follow[extend_index[j]])
                        # print(follow[i])
                    elif exp[j][x + len(notT[i])] != "'":  # 不是结尾 判断后面还有没有’
                        # print("notend")
                        # print(x, notT[i])
                        s = exp[j][x + len(notT[i]):]
                        index = find_notT(s, notT)  # 找该非终结符后面第一个是不是非终结符 若有 返回是第几个非终结符
                        # print(index)
                        # print(follow[i])
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

"""global"""
T = []

def print_chart():
    global first
    global first_index
    global follow
    global T
    for i in range(0,len(first)):
        for j in range(0,len(first[i])):
            if T.count(first[i][j]) == 0 and first[i][j] != '%':
                T.append(first[i][j])
    for i in range(0, len(follow)):
        for j in range(0, len(follow[i])):
            if T.count(follow[i][j]) == 0 and follow[i][j] != '$':
                T.append(follow[i][j])
    T.append('$')
    notT = init_notT()
    res = []
    for i in range(0,len(notT)):
        temp = [" "]*len(T)
        res.append(temp)

    for i in range(0,len(first)):
        for j in range(0,len(first[i])):
            if first[i][j] != '%':
                index = T.index(first[i][j])
                res[i][index] = first_index[i][j]
            else :
                for k in range(0,len(follow[i])):
                    index = T.index(follow[i][k])
                    if res[i][index] !=" ":
                        print("conflict grammar")
                        sys.exit()
                    else :
                        res[i][index] = first_index[i][j]

    print("Terminal:",T)
    print("None Terminal:",notT)
    resT = [" "] + T
    x = PrettyTable(resT)
    for i in range(0,len(res)):
        temp = [notT[i]]+res[i]
        x.add_row(temp)
    print(x)
    return res

def check(s,res):
    global T
    global extend_grammar
    stack_anyl= []
    stack_input = []
    notT = init_notT()
    stack_anyl.append('$')
    stack_anyl.append(notT[0])
    stack_input.append('$')
    for i in range(0,len(s)):
        stack_input.append(s[len(s) - i - 1])

    warn = 0
    while len(stack_anyl) > 1:
        if stack_input[-1] == stack_anyl[-1]:
            stack_input.pop()
            stack_anyl.pop()
        elif stack_anyl[-1] == "%":
            stack_anyl.pop()
        else:
            try:
                indexx = notT.index(stack_anyl[-1])
                indexy = T.index(stack_input[-1])
            except:
                print("wrong")
                warn = 1
                break
            else:
                gnum = res[indexx][indexy]
                if gnum == " ":
                    print("wrong")
                    break
                stack_anyl.pop()
                sa = extend_grammar[gnum].split("->")
                backstack = []
                temp = sa[1][0]
                for i in range(1, len(sa[1])):
                    if sa[1][i] == "'":
                        temp = temp + "'"
                    else:
                        backstack.append(temp)
                        temp = sa[1][i]
                backstack.append(temp)
                backstack.reverse()
                stack_anyl += backstack
        print(stack_anyl)
    if stack_anyl[-1] == "$" and stack_input[-1] == "$" and warn == 0:
        print("accept")


def main():
    global grammar
    wenfa=input()
    while wenfa!='0':
        grammar.append(wenfa)
        wenfa=input()
    print("所有文法：",grammar)
    normalleft()
    for i in range(0,len(grammar)):
        del_leftfact(i)
    extend()
    print("消除递归和因子：",grammar)
    print("扩展文法：",extend_grammar)
    print("extend_index:",extend_index)
    first_set()
    follow_set()
    res = print_chart()
    s = input()
    print("分析栈：")
    check(s, res)

"""
E->EAT|T
A->+|-
T->TMF|F
M->*
F->(E)|N
0
"""



if __name__=='__main__':
    main();

    """
A->Ba|Aa|c
B->Bb|Ab|d
D->abc|ac|ab|bcde|bcd 
0
    
    """