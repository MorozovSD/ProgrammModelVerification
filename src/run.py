import getopt
import sys

from Exeptions import *
from graph_flow import Graph, GraphFlow
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
    calls = {}
    functions = []
    func_usage = {'CurrentlyUnknown': []}
    byte_code = []
    byte_code_func = {}
    for file in input:
        file_name = file.split('/')[-1][:-4]
        ast = parse_tokens(file)
        ast.export(output_path=output, name=file_name, detailed=verbose)
        asts.append(ast)

    for ast in asts:
        ast_functioons = ast.get_functions()
        functions += ast_functioons
        for func in ast_functioons:
            func_usage[func] = []
            func_path = ast.source_name.split('/')[-1][:-4] + '_' + func.signature.name
            graph_flow = GraphFlow(func, ast.source_name + '/' + func.signature.name)
            graphs.append(graph_flow)
            graph_flow.to_png(path=output, name=func_path + '_graph')
            byte_code_func[ast.source_name + '/' + func.signature.name] = len(byte_code)
            byte_code += func.byte_code()
        calls.update(ast.get_calls())

    for calls_path, _calls in calls.items():
        for call in filter(None, _calls):
            for func in functions:
                if str(call.expr) == str(func.signature.name):
                    try:
                        if not call.call_func:
                            call.call_func = func
                            if calls_path not in func_usage[func]:
                                func_usage[func].append(calls_path)
                        else:
                            raise FunctionSourceException()
                    except FunctionSourceException as e:
                        print(e.message % (call.expr, calls_path, call.call_func))
                        exit(3)
                else:
                    func_usage[call.uniq_str()] = []
                    if call.call_func == 'CurrentlyUnknown' and calls_path not in func_usage[call.uniq_str()]:
                        func_usage[call.uniq_str()] = [calls_path]

    for calls_path, _calls in calls.items():
        for call in filter(None, _calls):
            try:
                if not call.call_func:
                    raise UnknownFunctionException()
                else:
                    print(call.call_func)
            except UnknownFunctionException as e:
                print(e.message % call.expr)
                exit(3)

    Graph.print(func_usage)
    Graph.print(inverse_mapping(func_usage))
    Graph.to_png(inverse_mapping(func_usage), output, 'Functions Calls')

    print('linear_code')
    with open(output + 'linear_code.txt', 'w', encoding='utf-8') as f:
        for i, line in enumerate(byte_code):
            print(str(i) + '\t' + str(line), file=f)
            print(str(i) + '\t' + str(line))

    print('linear_code_func_start')
    with open(output + 'linear_code_func_start.txt', 'w', encoding='utf-8') as f:
        for func, place in byte_code_func.items():
            print(str(place) + '\t' + str(func), file=f)
            print(str(place) + '\t' + str(func))







def inverse_mapping(f):
    inv_map = {}
    for k, values in f.items():
        for value in values:
            inv_map[value] = inv_map.get(value, [])
            inv_map[value].append(k)
    return inv_map


if __name__ == "__main__":
    main()
