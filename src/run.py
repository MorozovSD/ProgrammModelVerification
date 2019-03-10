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
    external = []
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
        ast_external = ast.get_external()
        ast_class = ast.get_class()
        ast_functions = ast.get_functions()
        external += ast_external
        functions += ast_functions

        for external in ast_external:
            byte_code += external.byte_code()

        for _class in ast_class:
            class_func = _class.get_functions()
            class_external = _class.get_external()
            functions += class_func
            for func in class_func:
                func_usage[func] = []
                func_path = ast.source_name.split('/')[-1][:-4] + '_' + str(_class.name) + '_' + func.signature.name
                graph_flow = GraphFlow(func, ast.source_name + '/' + func.signature.name)
                graphs.append(graph_flow)
                graph_flow.to_png(path=output, name=func_path + '_graph')
                byte_code_func[ast.source_name + '/' + func.signature.name] = len(byte_code)
                byte_code += func.byte_code()
            external += class_external
            byte_code += _class.byte_code()

        for func in ast_functions:
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
    with open(output + 'linear_code.bin', 'wb') as f:
        for line in byte_code:
            f.write((line + '\n').encode())

    print('linear_code_func_start')
    with open(output + 'linear_code_func_start.txt', 'w', encoding='utf-8') as f:
        for func, place in byte_code_func.items():
            print(str(place) + '\t' + str(func), file=f)


def inverse_mapping(f):
    inv_map = {}
    for k, values in f.items():
        for value in values:
            inv_map[value] = inv_map.get(value, [])
            inv_map[value].append(k)
    return inv_map


if __name__ == "__main__":
    main()
