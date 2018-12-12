from prettytable import PrettyTable
from Grammar import *
import sys

DFA = []
DFA_end = []
trans = []
dot_g = []

def dot():
    global extend_grammar
    global dot_g
    notT = init_notT()
    j = 0
    for i in range(0,len(notT)):
        temp = [notT[i]]
        while j < len(extend_grammar):
            sa = extend_grammar[j].split("->")
            if sa[0] == notT[i] and sa[1] != "%":
                temp.append(sa[0] + "->" + "·" + sa[1])
                j += 1
            else :
                break
        dot_g.append(temp)
    print(dot_g)

def generate_node(str):
    print("=====generate=====")
    global DFA
    node = [str]
    notT = init_notT()
    i = 0
    while i < len(node):
        g = node[i].split("->")
        temp = g[1].split("·")
        #print("gen:", temp)
        if temp[1] == "": #如果·已经在最后
            break
        else :
            index = find_notT(temp[1], notT)
            #print(index)
            if index == -1:
                break
            else:
                for j in range(1, len(dot_g[index])):
                    node.append(dot_g[index][j])
        i += 1
    node_end = [0]*len(node)
    DFA.append(node)
    DFA_end.append(node_end)
    trans.append([])
    print( "new node:", node)
    print("==========")

def move(s,mark,notT):
    print("=====move=====")
    print(s)
    s = s.split("->")  #s = S~ ,·S
    index = s[1].find("·")
    x = find_notT(s[1][index+1:],notT)
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
    print(res)
    print("=======")
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
            while j < len(DFA[i]) :
                sent = DFA[i][j].split("->")
                index = sent[1].find("·")
                print(sent)
                print(index)
                if index + 1 == len(sent[1]): #·已经在最后了
                    print("skip")
                    DFA_end[i][j] = 1
                else:
                    #print("now",index,len(sent[1]))
                    mark = find_notT(sent[1][index + 1:], notT)  # 找到·之后的第一个符号，返回非终结符脚标
                    str = move(DFA[i][j], mark, notT)  # 生成·移动后的式子
                    #spot = find_notT(sent[1][index + 1:], notT)
                    if mark != -1:
                        x = notT[mark]
                    else:
                        x = sent[1][1]  # 确定·后面的符号
                    res = check_node(str)
                    if res != -1:
                        trans[i].append(res)
                        trans[i].append(x)
                        DFA_end[i][j] = 1
                    else:
                        generate_node(str)
                        trans[i].append(len(DFA) - 1)
                        trans[i].append(x)
                        DFA_end[i][j] = 1
                j += 1
                print(DFA)
                print(DFA_end)
        i += 1

    print(DFA)
    print(trans)









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
    dot()
    create_DFA()
    """
    
    for i in range(0,len(DFA)):
        print("结点：",DFA[i])
        print("链接：",trans[i])
    """

if __name__=='__main__':
    main();


"""
S->aA
A->cA|d
0
"""
