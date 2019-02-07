import getopt
import sys

from graph_flow import Graph
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
    graphs = []
    for file in input:
        file_name = file.split('/')[-1][:-4]
        ast = parse_tokens(file)
        ast.export(output_path=output, name=file_name, detailed=verbose)
        asts.append(ast)
        funcs = ast.children
        for func in funcs:
            func_path = file_name + '_' + func.signature.name
            graph_flow = Graph(func, ast.source_name + '/' + func.signature.name)
            graphs.append(graph_flow)
            graph_flow.print()
            graph_flow.to_png(path=output, name=func_path + '_graph')
    print(1)


if __name__ == "__main__":
    main()
