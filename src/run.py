import argparse
import getopt
import sys

from node import render_tree, paint_tree, build_tree
from yacc_parser import parse_tokens


def usage():
    print(""" Список агрументов:
    -i (--input)  - список входных файлов 
    -o (--outpot) - список выходных файлов 
    -v            - Вывод в консоль результатов работы  
    --help        - Подсказка
    """)


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:o:v', ['help', 'output=', 'input='])
    except getopt.GetoptError:
        # print help information and exit:
        usage()
        sys.exit(2)
    output = None
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
