import sys
import model_verivication

BASE_TERM = []

def main():
    for arg in sys.argv[1:]:
        print(arg)
    with open('test_input.txt') as file_handler:
        input_file = file_handler.read()
    print(input_file)
    sintax_tree = model_verivication.SintaxTreeParser()
    sintax_tree.parse(input_file)
    # sintax_tree.print()


if __name__ == "__main__":
    main()
