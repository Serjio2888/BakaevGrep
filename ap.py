import argparse
import sys
import re

parser = argparse.ArgumentParser(description='Using PARSERS')
    
def output(line):
    print(line)
    
def grep(lines, params):

    for line in lines:
        line = line.rstrip()
        if params.pattern in line:
            output(line)

def parse_args(args):

    parser.add_argument(
        '-i', action="store_true",
        dest="ignore_case",
        default=False,
        help='Perform case insensitive matching.')

    parser.add_argument(
        '-n',
        action="store_true",
        dest="line_number",
        default=False,
        help='Each output line is preceded by its relative \
        line number in the file, starting at line 1.')    
    
    parser.add_argument(
        '-v', action="store_true",
        dest="invert",
        default=False,
        help='Selected lines are those not matching pattern.')

    parser.add_argument(
        '-c',
        action="store_true",
        dest="count",
        default=False,
        help='Only a count of selected lines is written to standard output.')

    parser.add_argument(
        '-C',
        action="store",
        dest="context",
        type=int,
        default=0)

    parser.add_argument(
        '-B',
        action="store",
        dest="before_context",
        type=int,
        default=0,
        help='Print num lines of trailing context after each match')

    parser.add_argument(
        '-A',
        action="store",
        dest="after_context",
        type=int,
        default=0,
        help='Print num lines of leading context before each match.')
    
    parser.add_argument('pattern', action="store",
                        help='Search pattern. Can contain magic symbols: ?*')
    
    return parser.parse_args(args)


params = parse_args(sys.argv[1:])
strings = sys.stdin.readlines() #массив строк, подаваемых на вход


lol = parser.parse_args()

#Переводим в нижний регистр всё, что подали на вход, шаблон, если стоит -i
if parser.parse_args().ignore_case:
    lol.pattern = lol.pattern.lower()
    for key in range(len(strings)):
        strings[key]=strings[key].lower()

#удаляем \n в конце строчек
for i in range(len(strings)):
    strings[i] = (strings[i]).rstrip()


#если введено несколько '*' подряд - заменим на одну
lol.pattern = re.sub('\*+','\w*', lol.pattern)

#заменим '?' на '.'
lol.pattern = re.sub('\?',r'.',lol.pattern)

k = 0
A = [None]*len(strings)#в будущем - список номеров строк из strings, которые совпали с шаблоном

if not(parser.parse_args().invert):
    for i in range(len(strings)):
        if re.findall(lol.pattern, strings[i]):
            A[i]=i
    A=set(A) 
    A=list(A)
    if None in A:
        A.pop()


if parser.parse_args().invert:
    for i in range(len(strings)):
        if not(re.findall(lol.pattern, strings[i])):
            A[i]=i
    A=set(A)
    A=list(A)
    if None in A:
        A.pop()
#Получили список номеров строк, вкоторых есть/нет совпадений с шаблоном



#ТУТ БУДЕМ СЧИТАТЬ КОЛИЧЕСТВО СОПАДЕНИЙ С ШАБЛОНОМ В СЛУЧАЕ count=True
if parser.parse_args().count:
    for i in A:
        k += (len(re.findall(lol.pattern,strings[i])))
    print(k)

con = parser.parse_args().context
befo = parser.parse_args().before_context
afte = parser.parse_args().after_context

B = []
C = []
D = []#сделаем ещё три списка, в которые
      #будем помещать номера строк контекста
R = []
N = []
M = []

L = [] 

if con:
    for i in A:
        for k in range(0, 2*con+1,):
            B.append(i-con+k)       
    B=set(B)
    B=list(B)
    R = list(B)
    for num in range(len(B)):
        if (B[num])<0:
            R.pop()
        if (B[num])>=(len(strings)):
            R.pop()
    L = list(R)
    #выведем полученное
    if not(parser.parse_args().line_number):
        for i in L:
            print(strings[i])
    if parser.parse_args().line_number:
        for i in L:
            if i in A:
                print(i+1,':',strings[i])
            else:
                print(i+1,'-',strings[i])


if befo:
    for i in A:
        for k in range(0, befo+1,):
            C.append(i-befo+k)        
    C=set(C)
    C=list(C)
    N = list(C)
    for num in range(len(C)):
        if (C[num])<0:
            N.pop()
        if (C[num])>=(len(strings)):
            N.pop()
    L = list(N)
    #выведем полученное
    if not(parser.parse_args().line_number):
        for i in L:
            print(strings[i])
    if parser.parse_args().line_number:
        for i in L:
            if i in A:
                print(i+1,':',strings[i])
            else:
                print(i+1,'-',strings[i])
        

if afte:
    for i in A:
        for k in range(0, afte+1,):
            D.append(i+afte-k)       
    D=set(D)
    D=list(D)
    M = list(D)
    for num in range(len(D)):
        if (D[num])<0:
            M.pop()
        if (D[num])>=(len(strings)):
            M.pop()
    L = list(M)
    #выведем полученное
    if not(parser.parse_args().line_number):
        for i in L:
            print(strings[i])
    if parser.parse_args().line_number:
        for i in L:
            if i in A:
                print(i+1,':',strings[i])
            else:
                print(i+1,'-',strings[i])


#вывод в случае, если не используются флаги контекста
if not(afte and con and befo):
    if not(parser.parse_args().line_number):
        for i in A:
            print(strings[i])
    if parser.parse_args().line_number:
        for i in A:
            print(i+1,':',strings[i])



#Мне кажется, глупо использовать более одного контекста,
# по-этому не учитываем их совместное использование:
















