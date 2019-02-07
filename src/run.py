import getopt
import sys
import os

from graph_flow import Function, Graph
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
        print(ast.print(ast))
        ast.export(output_path=output, name=file_name, detailed=verbose)
        asts += [ast]
        funcs_flow = {}
        for ast in asts:
            funcs = ast.children
            # output_flow = funcs[0].statements.build_graph(funcs[0].statements.statements, funcs[0].name)
            # output_flow.print(output_flow)
            # output_flow.export(output_path=output, name=file_name, to_image=True, detailed=verbose)

            for i, func in enumerate(funcs):
                if func in funcs_flow:
                    print('Same functions in one file. This is UNACCEPTABLE!... For now')
                    sys.exit(2)
                # x = func.statements.build_graph(func.statements.statements, funcs[0].name)
                # for k, v in x.items():
                #     print(str(k) + '\t\t\t\t\t\t\t:::\t' + str(v))
                # Graph.graph_to_png(x, output + '/' + file_name + '_func' + str(i))
                # funcs += ast.find(pattern='funcDef', node=ast)


if __name__ == "__main__":
    main()
