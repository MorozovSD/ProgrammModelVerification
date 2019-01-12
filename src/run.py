import sys

from node import render_tree, paint_tree, build_tree
from yacc_parser import parse_tokens


def main():
    for arg in sys.argv[1:]:
        print(arg)
    root = build_tree(node=parse_tokens('test_input.txt'))

    tree = render_tree(root)
    paint_tree(root, 'tree.png')
    with open('tree_text.txt', 'w', encoding='utf-8') as f:
        print(tree, file=f)

    with open('tree_text_simple.txt', 'w', encoding='utf-8') as f:
        for pre, _, node in tree:
            print("%s%s" % (pre, node.name), file=f)


if __name__ == "__main__":
    main()
