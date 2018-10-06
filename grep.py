import argparse
import sys
import re


def output(line):
    print(line)

def simple_out(params, lines, i, realline):

    if params.ignore_case:
        lines[i]=lines[i].lower()
    if not(params.invert):
        if re.findall(params.pattern, lines[i]):
            if params.line_number:
                output(str(i+1)+':'+realline.rstrip())
            if not(params.line_number):
                output(realline.rstrip())
    if params.invert:
        if not(re.findall(params.pattern, lines[i])):
            if params.line_number:
                output(str(i+1)+':'+realline.rstrip())
            if not(params.line_number):
                output(realline.rstrip())

        
def findall(lines, params, string1, string2, i, nums):
    
    if params.before_context:
        params.context = params.before_context
    if params.after_context:
        params.context = params.after_context
    for key in range(0, params.context+1,):
        if params.context:
            D = int(i-params.context/2+key)
        if params.before_context:
            D = int(i-params.before_context+key)
        if params.after_context:
            D = int(i+key)
        if not (D) in nums:
            if (D>=0):
                if (D<len(lines)):
                    if params.line_number:
                        if re.findall(params.pattern, lines[D]):
                            output(str(D+1)+string1+lines[D].rstrip())
                            nums.append(D)
                        else:
                            output(str(D+1)+string2+lines[D].rstrip())
                            nums.append(D)
                    else:
                        output(lines[D].rstrip())
                        nums.append(D)

def context_(lines, params):

    if params.context:
        params.context *= 2
        
    nums =[]
    for i in range(len(lines)):
        if not(params.invert):
            if re.findall(params.pattern, lines[i]):
                findall(lines, params, ':', '-', i, nums)
                                    
        if params.invert:
            if not(re.findall(params.pattern, lines[i])):
                findall(lines, params, '-', ':', i, nums)
    nums = []
    

def count(lines, pattern, invert):
    """Считает количество строк,
       в которых есть совпадения с шаблоном.
       Учитывает флаг 'invert'.
    """
    k = -1
    if not(invert):
        for i in range(len(lines)):
            if re.findall(pattern, lines[i]):
                k += 1
        output(str(k))
    if (invert):
        for i in range(len(lines)):
            if not(re.findall(pattern, lines[i])):
                k += 1
        output(str(k))

            
def grep(lines, params):

    #если введено несколько '*' подряд - заменим на одну
    params.pattern = re.sub('\*+','\w*', params.pattern)
    #заменим '?' на '.'
    params.pattern = re.sub('\?',r'.',params.pattern)
    
    if params.count:
        return(count(lines, params.pattern, params.invert))

    if not(params.context or params.before_context or params.after_context):
        for i in range(len(lines)):
            realline = str(lines[i])
            simple_out(params, lines, i, realline)
            
    if params.context:
        context_(lines, params)
        
    if params.before_context:
        context_(lines, params)

    if params.after_context:
        context_(lines, params)

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
    
