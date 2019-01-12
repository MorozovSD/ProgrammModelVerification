import getopt
import sys

from node import render_tree, paint_tree, build_tree
from yacc_parser import parse_tokens


def usage():
    print("""Run example:
    python run.py -i ../input/test_input.txt,../input/test_input1.txt -o ../output/
    Arguments:
    -i (--input)  - input files
    -o (--outpot) - outpit dir
    -v            - detaled output
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


    roots = []
    trees = []
    for file in input:
        file_name = file.split('/')[-1][:-4]
        root = build_tree(node=parse_tokens(file))
        tree = render_tree(root)
        paint_tree(root, output + file_name + '.png')
        with open(output + file_name + '.txt', 'w', encoding='utf-8') as f:
            print(tree, file=f)
        with open(output + 'simple_' + file_name + '.txt', 'w', encoding='utf-8') as f:
            for pre, _, node in tree:
                print("%s%s" % (pre, node.name), file=f)
        roots += [root]
        trees += [tree]


if __name__ == "__main__":
    main()
