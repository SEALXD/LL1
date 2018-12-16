from prettytable import PrettyTable
from Grammar import *
import sys


DFA = []
DFA_end = []
trans = []
dot_g = []

""" 每个节点： [[str1,sign1],[str2,sign2],....] """
def dot():
    global extend_grammar
    global dot_g
    notT = init_notT()
    j = 0
    for i in range(0,len(notT)):
        temp = [notT[i]]
        while j < len(extend_grammar):
            sa = extend_grammar[j].split("->")
            if sa[0] == notT[i] :
                if sa[1] != "%":
                    temp.append(sa[0] + "->" + "·" + sa[1])
                else:
                    temp.append(sa[0] + "->" + "·" )
                j += 1
            else :
                break
        dot_g.append(temp)
    #print(dot_g)

def first_complex(b,a):
    global first
    b = list(b)
    notT = init_notT()
    res = []
    mark = 0
    # print("do",first,b)
    if len(b) != 0:
        while len(b) != 0:
            index = find_notT(b, notT)
            if index == -1:
                if res.count(b[0]) == 0:
                    res.append(b[0])
                break
            else:
                mark = 0
                for i in range(0, len(first[index])):
                    if first[index][i] == "%":
                        mark = 1
                    elif res.count(first[index][i]) == 0:
                        res.append(first[index][i])
                if len(b) == len(notT[index]):
                    break
                else:
                    b = b[len(notT[index]):]
    else:
        mark = 1
    if mark:
        if notT.count(a) == 0:
            res.append(a)
        else:
            index = notT.index(a)
            flag = 0
            for i in range(0, len(first[index])):
                if first[index][i] == "%":
                    flag = 1
                elif res.count(first[index][i]) == 0:
                    res.append(first[index][i])
            if flag:
                res.append("%")
    return res


def generate_node(str,sign):
    #print("=====generate=====")
    global DFA
    global trans
    global first
    node = []
    node.append([str,sign])
    notT = init_notT()
    ft = 0
    """ A->c·Bb,a   First(ba)"""
    i = 0
    while i < len(node):
        g = node[i][0].split("->")
        temp = g[1].split("·")
        if temp[1] != "": #如果·不在最后
            index = find_notT(temp[1], notT)
            if index != -1:
                b = temp[1][len(notT[index]):]
                a = sign
                f = first_complex(b, a)  # 返回对应的first集
                for k in range(0, len(f)):
                    for j in range(1, len(dot_g[index])):
                        if node.count([dot_g[index][j], f[k]]) == 0:
                            node.append([dot_g[index][j], f[k]])
        i += 1

    node_end = [0]*len(node)
    DFA.append(node)
    DFA_end.append(node_end)
    trans.append([])
    # print( "new node:", node)
    # print("==========")

def add_gen(id,str,sign):
    global DFA
    global first
    node =[[str,sign]]
    DFA[id].append([str,sign])
    DFA_end[id].append(0)
    notT = init_notT()
    ft = 0
    i = 0
    while i < len(node):
        g = node[i][0].split("->")
        temp = g[1].split("·")
        if temp[1] != "": #如果·不在最后
            index = find_notT(temp[1], notT)
            if index != -1:
                b = temp[1][len(notT[index]):]
                a = sign
                f = first_complex(b, a)  # 返回对应的first集
                for k in range(0, len(f)):
                    for j in range(1, len(dot_g[index])):
                        if node.count([dot_g[index][j], f[k]]) == 0:
                            node.append([dot_g[index][j], f[k]])
                            DFA[id].append([dot_g[index][j], f[k]])
                            DFA_end[id].append(0)
        i += 1


def move(s,mark,notT):
    # print("=====move=====")
    # print(s)
    s = s[0].split("->")  #s = S~ ,·S
    index = s[1].find("·")
    x = mark
    if index == 0 :
        if x == -1:
            if len(s[1][index+1:]) > 1:
                res = s[0] + "->" + s[1][1] + "·" + s[1][2:]
            else:
                res = s[0] + "->" + s[1][1] + "·"
        else:
            if len(s[1][index+1:]) > len(notT[x]):
                res = s[0] + "->" + s[1][1:len(notT[x])+1] + "·" + s[1][len(notT[x])+1:]
            else:
                res = s[0] + "->" + s[1][1:len(notT[x]) + 1] + "·"
    else:
        if x == -1:
            if len(s[1][index + 1:]) > 1:
                res = s[0] + "->" + s[1][0:index] + s[1][index + 1:index + 2] + "·" + s[1][index + 2:]
            else:
                res = s[0] + "->" + s[1][0:index] + s[1][index + 1:index + 2] + "·"
        else:
            if len(s[1][index + 1:]) > len(notT[x]):
                res = s[0] + "->" + s[1][0:index] + s[1][index + 1:index + 1 + len(notT[x])] + "·" + s[1][index + 1 + len(notT[x]):]
            else:
                res = s[0] + "->" + s[1][0:index] + s[1][index + 1:index + 1 + len(notT[x])] + "·"
    # print(res)
    # print("=======")
    return res

def check_node(str,sign):
    global DFA
    flag = 0
    for i in range(0,len(DFA)):
        for j in range(0,len(DFA[i])):
            if DFA[i][j] == [str,sign]:
                return i
    return -1

def create_DFA():
    global DFA
    global DFA_end
    global trans
    notT = init_notT()
    generate_node(dot_g[0][1],"$") #生成第一个节点
    i = 0
    while i < len(DFA):
        if DFA_end[i].count(0) != 0:
            j = 0
            while j < len(DFA[i]):
                sent = DFA[i][j][0].split("->")
                index = sent[1].find("·")
                if index + 1 == len(sent[1]):  # ·已经在最后了
                    DFA_end[i][j] = 1
                else:
                    mark = find_notT(sent[1][index + 1:], notT)  # 找到·之后的第一个符号，返回非终结符脚标
                    str = move(DFA[i][j], mark, notT)  # 生成·移动后的式子
                    sign = DFA[i][j][1]
                    if mark != -1:
                        x = notT[mark]
                    else:
                        spot = sent[1].find("·")
                        x = sent[1][spot + 1]  # 确定·后面的符号

                    if trans[i].count(x) != 0:  # 检查trans中是否已经有这个转换
                        id = trans[i].index(x)
                        id = trans[i][id - 1]
                        if DFA[id].count([str,sign]) == 0:
                            add_gen(id, str, sign)  # 将对应的式子加入目标DFA
                        DFA_end[i][j] = 1
                        #print("case 1")
                    else:
                        res = check_node(str,sign)  # trans中没有这个转换 检查是否有包含这个式子的结点
                        if res != -1:
                            trans[i].append(res)
                            trans[i].append(x)
                            DFA_end[i][j] = 1
                            #print("case 2")
                        else:  # trans中没有这个转换  也没有包含这个式子的结点 生成新的结点
                            generate_node(str,sign)
                            trans[i].append(len(DFA) - 1)
                            trans[i].append(x)
                            DFA_end[i][j] = 1
                            #print("case 3")
                j += 1
                # print(i,j)
                # print("DFA")
                # for m in range(0,len(DFA)):
                #     print(DFA[m])
        i += 1

def chart():
    global trans
    notT = init_notT()
    T = []
    res = []
    for i in range(0,len(extend_grammar)):
        sa =  extend_grammar[i].split("->")
        for j in range(0,len(sa[1])):
            if sa[1][j] != "'"and sa[1][j] != "%" and notT.count(sa[1][j]) == 0 and T.count(sa[1][j]) == 0:
                T.append(sa[1][j])
    T.append("$")
    row = T + notT
    res = [""]*(len(DFA))
    for i in range(0,len(res)):
        res[i] = [""]*len(row)

    for i in range(0,len(trans),1):
        for j in range(0, len(DFA[i])):
            if DFA[i][j][0].endswith("·"):
                sa = DFA[i][j][0].split("->")
                if sa[1] == "·":
                    s = sa[0] + "->" + "%"
                else:
                    s = DFA[i][j][0][:len(DFA[i][j][0]) - 1]
                index = extend_grammar.index(s)
                sign = DFA[i][j][1]
                id = row.index(sign)
                if res[i][id] == "":
                    res[i][id] = "r" + str(index)
                else:
                    print("conflict grammar")
                    sys.exit()

        if len(trans[i]) != 0:
            for j in range(0, len(trans[i]), 2):
                index = row.index(trans[i][j + 1])
                if index < len(T):
                    if res[i][index] == "":
                        res[i][index] = "s" + str(trans[i][j])
                    else:
                        print("conflict grammar")
                        sys.exit()
                else:
                    if res[i][index] == "":
                        res[i][index] = trans[i][j]
                    else:
                        print("conflict grammar")
                        sys.exit()
        #print(res[i])
    res[1][len(T)-1] = "acc"
    row[len(T)] = ""
    reschart = [" "] + row
    x = PrettyTable(reschart)
    for i in range(0,len(res)):
        temp = [i] + res[i]
        x.add_row(temp)
    print(x)
    # for i in range(0,len(res)):
    #     print(res[i])
    return res,row

def count(str):
    notT = init_notT()
    num = 0
    while len(str) != 0:
        index = find_notT(str, notT)
        if index == -1:
            str = str[1:]
            num += 1
        else:
            str = str[len(notT[index]):]
            num += 1
    return num


def check(s,res,row):
    global extend_grammar
    stack_anyl = []
    stack_input = []
    notT = init_notT()
    stack_anyl.append("$")
    stack_anyl.append("s0")
    point = 0
    stack_input.append('$')
    for i in range(0,len(s)):
        stack_input.append(s[len(s) - i - 1])

    print("分析：", stack_anyl, "输入：", stack_input, "动作： None")

    while 1 :
        index = row.index(stack_input[-1])
        if res[point][index] == "acc":
            break
        elif res[point][index] == "":
            print("error")
            sys.exit()
        elif res[point][index].startswith("r"):
            id = int(res[point][index][1:])
            case = "reduce" + extend_grammar[id]
            sa = extend_grammar[id].split("->")
            if sa[1] == "%":
                l = 0
            else:
                l = count(sa[1])  # 得到撒sa1的长度
            for i in range(0, l * 2):
                stack_anyl.pop()
            point = int(stack_anyl[-1][1:])
            index = row.index(sa[0])
            stack_anyl.append(sa[0])
            stack_anyl.append("s" + str(res[point][index]))
            point = res[point][index]
        else:
            if res[point][index].startswith("s"):
                case = "shift"
                stack_anyl.append(stack_input[-1])
                point = int(res[point][index][1:])
                stack_anyl.append("s" + str(point))
                stack_input.pop()
            else:
                print("error")
                sys.exit()
        print("分析：",stack_anyl,"输入：",stack_input,"动作：",case)
    print("accept")



def main():
    global grammar
    global first
    global follow
    wenfa=input()
    while wenfa!='0':
        grammar.append(wenfa)
        wenfa=input()
    print("所有文法：",grammar)
    extend()
    print("拓展文法：",extend_grammar)
    print("extend_index:",extend_index)
    notT = init_notT()
    print("非终结符：")
    print(notT)
    first = first_set()
    follow = follow_set()
    dot()
    create_DFA()
    print("DFA:")
    for i in range(0, len(DFA)):
        print("序号：", i, "结点内容：", DFA[i], "链接：", trans[i])
    print("================")
    res,row = chart()
    s = input()
    check(s,res,row)


if __name__=='__main__':
    main();

"""
S->CC
C->cC|d
0

S->i|V=E
V->i
E->V|n
0

A->(A)|a
0

S->aAd|bBd|aBe|bAe
A->c
B->c
0

"""