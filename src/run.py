from src import sintax_tree

input_file = None
with open("test.txt") as file_handler:
    print('Исходная программа')
    for line in file_handler:
        print(line)
    input_file = [line.strip() for line in file_handler]

sintax_tree = sintax_tree.parse(input_file)
sintax_tree.print()
