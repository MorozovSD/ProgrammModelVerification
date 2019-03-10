import getopt
import operator
import sys

bin_ops = {'ADD'    : operator.add,
           'MINUS'  : operator.sub,
           'DIVIDE' : operator.truediv,
           'MUL'    : operator.mul,
           'AND'    : operator.and_,
           'OR'     : operator.or_,
           'LESSEQ' : operator.le,
           'LESS'   : operator.lt,
           'MOREEQ' : operator.ge,
           'MORE'   : operator.gt,
           'NOTEQ'  : operator.ne,
           'EQ'     : operator.eq}

un_ops = {'UMINUS'  : operator.neg,
          'NOT'     : operator.not_}

integer = {'DEC':   10,
           'HEX':   16,
           'BITS':  2,
           'INT':   10,
           'UINT':  10,
           'LONG':  10,
           'ULONG': 10}


class Interpreter:
    def __init__(self, path, start):
        with open(path, 'rb') as f:
            self.commands = f.read().decode().split('\n')
        self.index = self.commands.index('FUNC ' + start)
        self.context = {}
        self.stack = []

    def current(self):
        return self.commands[self.index].split(' ')

    def next(self):
        self.index += 1
        return self.commands[self.index].split(' ')

    def goto(self, index):
        self.index = index
        return self.commands[self.index].split(' ')

    def start_execute(self):
        self.context['stack_trace'] = self.current()[1]
        self.next()
        self.func_executor()

    def func_executor(self):
        if self.current()[0] == 'EXPR':
            self.expr_executor()
            print(self.stack)

    def expr_executor(self):
        self.next()
        expr_stack = []
        while True:
            if self.current()[0] in bin_ops.keys():
                print(self.current()[0])
                expr_stack.append(bin_ops[self.current()[0]](expr_stack.pop(), expr_stack.pop()))
                self.next()
                continue

            if self.current()[0] in un_ops.keys():
                print(self.current()[0])
                expr_stack.append(un_ops[self.current()[0]](expr_stack.pop()))
                self.next()
                continue

            # if self.current()[0] == 'VAR':
            #     self.next()
            #     expr_stack.append(self.current()[0])
            #     self.next()
            #     continue

            if self.current()[0] in integer.keys():
                type = self.current()[0]
                value = self.next()[0]
                expr_stack.append(int(value, base=integer[type]))
                self.next()
                continue

            if self.current()[0] == 'ENDEXPR':
                self.stack.extend(expr_stack)
                return

            exit(5)


def usage():
    print("""Run example:
    python interpreter.py -i ../output/linear_code.bin, -s test_binary
    Arguments:
    -i (--input)  - input files
    -s (--start)  - starting function
    -v            - detailed output
    --help        - help
    """)


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'vi:o:v', ['help', 'start=', 'input='])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    start_func = ''
    input = None
    verbose = False
    for o, a in opts:
        if o == '-v':
            verbose = True
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        if o in ('-s', '--start'):
            start_func = a
        if o in ('-i', '--input'):
            input = a.split(',')
    if input is None:
        print('Input file doesn\'t set. Use -i to set input files')
        usage()
        sys.exit(2)

    interpreter = Interpreter(input, start_func)
    interpreter.start_execute()


if __name__ == "__main__":
    main()
