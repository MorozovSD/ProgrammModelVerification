import sys
# from anytree import Node

from yacc_parser import build_tree

BASE_TERM = []

def main():
    for arg in sys.argv[1:]:
        print(arg)
    with open('test_input.txt') as file_handler:
        input_file = file_handler.read()

    result = build_tree(input_file)
    print(result)


if __name__ == "__main__":
    main()
