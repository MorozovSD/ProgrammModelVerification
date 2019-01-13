import getopt
import sys
import os

from graph_flow import Function
from syntax_tree_parser import parse_tokens


def usage():
    print("""Run example:
    python run.py -i ../input/test_input.txt,../input/test_input1.txt -o ../output/
    Arguments:
    -i (--input)  - input files
    -o (--outpot) - output dir
    -v            - detailed output
    --help        - help
    """)


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'vi:o:v', ['help', 'output=', 'input='])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    output = ''
    input = None
    verbose = False
    for o, a in opts:
        if o == '-v':
            verbose = True
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        if o in ('-o', '--output'):
            output = a
        if o in ('-i', '--input'):
            input = a.split(',')
    if input is None:
        print('Input file doesn\'t set. Use -i to set input files')
        usage()
        sys.exit(2)

    asts = []
    funcs = []
    for file in input:
        file_name = file.split('/')[-1][:-4]
        ast = parse_tokens(file)
        ast.export(output_path=output, name=file_name, to_image=True, detailed=verbose)
        asts += [ast]
        funcs_flow = {}
        for ast in asts:
            source = os.path.abspath(ast.value.name)
            ast.update_func_names(pattern='funcSignature', value=source + ' :: ', node=ast)
            funcs = Function.get_func(ast)
            for i, func in enumerate(funcs):
                if func in funcs_flow:
                    print('Same func in one file. This is UNACCEPTABLE!... For now')
                    sys.exit(2)
                # funcs_flow[funcs.]
                # func.export(output_path=output, name=file_name + '_func' + str(i), to_image=True, detailed=verbose)
                # funcs += ast.find(pattern='funcDef', node=ast)




if __name__ == "__main__":
    main()
