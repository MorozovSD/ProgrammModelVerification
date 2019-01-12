import sys
from anytree import Node

from node import render_tree, paint_tree
from yacc_parser import build_tree

BASE_TERM = []

def main():
    for arg in sys.argv[1:]:
        print(arg)
    with open('test_input.txt') as file_handler:
        input_file = file_handler.read()

    result = build_tree(input_file)

    print(result)
    root = result.build_tree(node=result)
    tree = render_tree(root)
    print(tree)
    paint_tree(root, 'tree.png')
    with open('tree_text.txt', 'w', encoding='utf-8') as f:
        print(tree, file=f)


if __name__ == "__main__":
    main()
