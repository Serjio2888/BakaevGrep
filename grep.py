import argparse
import sys
import re

#line = input()

def output(line):
    print(line)


def grep(lines, params):
    
    """Собирает номера строк, подходящих под шаблон
       Обрабатывает их в соответсвии с указанными флагами(так как с цифрами работать намного проще и быстрее)
       И в конце передаёт их в output в виде lines[номер строки]
    """
    
    reallines = list(lines)#создаём, так как планируется изменять массив lines
                           #в частности, для правильной работы ignore_case
    
    #удаляем \n в конце строчек (образуется при вводе с клавиатуры,
    #и не нужно для корректной работы тестов
    for i in range(len(lines)):
        lines[i] = (lines[i]).rstrip()

    #Переводим в нижний регистр всё, что подали на вход, шаблон, если стоит -i
    if params.ignore_case:
        params.pattern = params.pattern.lower()
        for key in range(len(lines)):
            lines[key]=lines[key].lower()

    #если введено несколько '*' подряд - заменим на одну
    params.pattern = re.sub('\*+','\w*', params.pattern)

    #заменим '?' на '.'
    params.pattern = re.sub('\?',r'.',params.pattern)

    A = [None]*len(lines)#в будущем - список номеров строк из lines, которые совпали с шаблоном

    #Получим в А список номеров строк, в которых есть/нет совпадений с шаблоном
    if not(params.invert):
        for i in range(len(lines)):
            if re.findall(params.pattern, lines[i]):
                A[i]=i
        A=set(A) 
        A=list(A)
        if None in A:
            A.pop()
    if params.invert:
        for i in range(len(lines)):
            if not(re.findall(params.pattern, lines[i])):
                A[i]=i
        A=set(A)
        A=list(A)
        if None in A:
            A.pop()


    #ТУТ БУДЕМ СЧИТАТЬ КОЛИЧЕСТВО СОПАДЕНИЙ С ШАБЛОНОМ В СЛУЧАЕ count=True
    if params.count:
        k = (len(A)-1)
        return(output(str(k)))#так как тест, почему-то, требует именно строку, а не число

    con = params.context
    befo = params.before_context
    afte = params.after_context

    L = [] #новый массив, в который запишем номера строк контекста
    if con:
        for i in A:
            for k in range(0, 2*con+1,):
                L.append(i-con+k)       
        L=set(L)
        L=list(L)
        for num in range(len(L)):
            if (L[num])<0:
                L.pop()
            if (L[num])>=(len(lines)):
                L.pop()
        #выведем полученное
        if not(params.line_number):
            for i in L:
                output(reallines[i])
        if params.line_number:
            for i in L:
                if i in A:
                    answer = (str(i+1)+':'+reallines[i])
                    output(answer)
                else:
                    answer = (str(i+1)+'-'+reallines[i])
                    output(answer)

    elif befo:
        for i in A:
            for k in range(0, befo+1,):
                L.append(i-befo+k)        
        L=set(L)
        L=list(L)
        for num in range(len(L)):
            if (L[num])<0:
                L.pop()
            if (L[num])>=(len(lines)):
                L.pop()
        #выведем полученное
        if not(params.line_number):
            for i in L:
                output(reallines[i])
        if params.line_number:
            for i in L:
                if i in A:
                    answer = (str(i+1)+':'+reallines[i])
                    output(answer)
                else:
                    answer = (str(i+1)+'-'+reallines[i])
                    output(answer)

    elif afte:
        for i in A:
            for k in range(0, afte+1,):
                L.append(i+afte-k)       
        L=set(L)
        L=list(L)
        for num in range(len(L)):
            if (L[num])<0:
                L.pop()
            if (L[num])>=(len(lines)):
                L.pop()
        #выведем полученное
        if not(params.line_number):
            for i in L:
                output(reallines[i])
        if params.line_number:
            for i in L:
                if i in A:
                    answer = (str(i+1)+':'+reallines[i])
                    output(answer)
                else:
                    answer = (str(i+1)+'-'+reallines[i])
                    output(answer)

    #вывод в случае, если не используются флаги контекста
    else:
        if not(params.line_number):
            for i in A:
                output(reallines[i])
        if params.line_number:
            for i in A:
                answer = (str(i+1)+':'+reallines[i])
                output(answer)


def parse_args(args):

    parser = argparse.ArgumentParser(description='This is a grep on python')

    parser.add_argument(
        '-v', action="store_true",
        dest="invert",
        default=False,
        help='Selected lines are those not matching pattern.')

    parser.add_argument(
        '-i', action="store_true",
        dest="ignore_case",
        default=False,
        help='Perform case insensitive matching.')

    parser.add_argument(
        '-c',
        action="store_true",
        dest="count",
        default=False,
        help='Only a count of selected lines is written to standard output.')

    parser.add_argument(
        '-n',
        action="store_true",
        dest="line_number",
        default=False,
        help='Each output line is preceded by its relative \
        line number in the file, starting at line 1.')

    parser.add_argument(
        '-C',
        action="store",
        dest="context",
        type=int,
        default=0,
        help='Print num lines of leading and trailing context surrounding each match.')

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



def main():

    params = parse_args(sys.argv[1:])
    grep(sys.stdin.readlines(), params)



if __name__ == '__main__':

    main()
    
