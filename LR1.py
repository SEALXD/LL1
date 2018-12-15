from prettytable import PrettyTable
from Grammar import *
import sys
from LL1 import first_set,follow_set

DFA = []
DFA_end = []
trans = []
dot_g = []
first = []
follow = []

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
    print(dot_g)

def generate_node(str,symb):
    #print("=====generate=====")
    global DFA
    global trans
    global first
    node = [str]
    notT = init_notT()
    """ A->c·Bb,a   First(ba)"""
    i = 0
    while i < len(node):
        g = node[i].split("->")
        temp = g[1].split("·")
        if temp[1] == "": #如果·已经在最后
            break
        else :
            index = find_notT(temp[1], notT) # """notT和dot_g脚标对应"""
            if index == -1:
                break
            else:
                A = g[0]
                c = temp[0]
                B = notT[index]
                b = temp[1][len(notT[index]):]
                for j in range(1, len(dot_g[index])):
                    if node.count(dot_g[index][j]) == 0:
                        node.append(dot_g[index][j])

        i += 1
    node_end = [0]*len(node)
    DFA.append(node)
    DFA_end.append(node_end)
    trans.append([])
    # print( "new node:", node)
    # print("==========")

def add_gen(id,str):
    global DFA
    node = [str]
    DFA[id].append(str)
    DFA_end[id].append(0)
    notT = init_notT()
    i = 0
    while i < len(node):
        g = node[i].split("->")
        temp = g[1].split("·")
        if temp[1] == "":  # 如果·已经在最后
            break
        else:
            index = find_notT(temp[1], notT)
            if index == -1:
                break
            else:
                for j in range(1, len(dot_g[index])):
                    if DFA[id].count(dot_g[index][j]) == 0:
                        node.append(dot_g[index][j])
                        DFA[id].append(dot_g[index][j])
                        DFA_end[id].append(0)
        i += 1


def move(s,mark,notT):
    # print("=====move=====")
    # print(s)
    s = s.split("->")  #s = S~ ,·S
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

def check_node(str):
    global DFA
    flag = 0
    for i in range(0,len(DFA)):
        for j in range(0,len(DFA[i])):
            if DFA[i][j] == str:
                return i
            else :
                flag = 1
    if flag == 1:
        return -1

def create_DFA():
    global DFA
    global DFA_end
    global trans
    notT = init_notT()
    generate_node(dot_g[0][1])

    i = 0
    while i < len(DFA):
        if DFA_end[i].count(0) != 0:
            j = 0
            while j < len(DFA[i]):
                sent = DFA[i][j].split("->")
                index = sent[1].find("·")
                if index + 1 == len(sent[1]):  # ·已经在最后了
                    DFA_end[i][j] = 1
                else:
                    mark = find_notT(sent[1][index + 1:], notT)  # 找到·之后的第一个符号，返回非终结符脚标
                    str = move(DFA[i][j], mark, notT)  # 生成·移动后的式子
                    if mark != -1:
                        x = notT[mark]
                    else:
                        spot = sent[1].find("·")
                        x = sent[1][spot + 1]  # 确定·后面的符号

                    if trans[i].count(x) != 0:  # 检查trans中是否已经有这个转换
                        id = trans[i].index(x)
                        id = trans[i][id - 1]
                        add_gen(id, str)  # 将对应的式子加入目标DFA
                    else:
                        res = check_node(str)  # trans中没有这个转换 检查是否有包含这个式子的结点
                        if res != -1:
                            trans[i].append(res)
                            trans[i].append(x)
                            DFA_end[i][j] = 1
                        else:  # trans中没有这个转换  也没有包含这个式子的结点 生成新的结点
                            generate_node(str)
                            trans[i].append(len(DFA) - 1)
                            trans[i].append(x)
                            DFA_end[i][j] = 1
                j += 1
                # print(DFA)
                # print(DFA_end)
        i += 1

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
    print(notT)
    first = first_set()
    follow = follow_set()
    dot()
    create_DFA()
    print("DFA:")
    for i in range(0, len(DFA)):
        print("序号：", i, "结点内容：", DFA[i], "链接：", trans[i])
    print("================")
    # res,row = chart(follow)
    # s = input()
    # check(s,res,row)


if __name__=='__main__':
    main();

"""
S->CC
C->cC|d
0

"""