import os, sys
import llvmlite.binding as llvm
from antlr4 import *
from lexer_parser.antlr.PascalLexer import PascalLexer
from lexer_parser.antlr.PascalParser import PascalParser
from graphviz import Digraph
from ir_builder.ParserVisitor import ParserVisitor
from ir_builder.exceptions.CompileException import CompileException
from ctypes import CFUNCTYPE, c_int32
from IPython.display import display


def main(argv=['', './examples/benchmarks/bubble_sort_array.pas']):       # './examples/HelloWorld.pas'
    input_stream = FileStream(argv[1])
    lexer = PascalLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = PascalParser(stream)
    tree = parser.program()

    if parser.getNumberOfSyntaxErrors() > 0:
        raise CompileException("Syntax error!")
    else:
        visitor = ParserVisitor()
        program = visitor.visit(tree)
        engine = init_execution_engine()
        #print(program.module)
        compile_ir(engine, program.module)
        print("="*100)
        filename = os.path.splitext(os.path.basename(argv[1]))[0].lower()
        ll_file_path = argv[1].replace(os.path.basename(argv[1]), f'{filename}.ll')
        file = open(f"{ll_file_path}", 'w')
        file.write(str(program.module))
        file.close()
        print(f"\nIR-representation have saved in {ll_file_path}")
        #input('Press <Enter> to execute')
        print("\n" + "="*43 + 'PROGRAM OUTPUT' + '='*43)
        func_main_name = f"{filename}_main"
        execute(engine, func_main_name)

        #print_tree(tree).render("tree", view=True)


def init_execution_engine():
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()     # opt=3

    default_mod = llvm.parse_assembly("")
    return llvm.create_mcjit_compiler(default_mod, target_machine)


def execute(engine, func_name="main"):
    func_ptr = engine.get_function_address(func_name)
    func = CFUNCTYPE(c_int32)(func_ptr)
    display(func(), clear=True)
    #print()


def compile_ir(engine, ir_module):
    mod = llvm.parse_assembly(str(ir_module))
    mod.verify()

    engine.add_module(mod)
    engine.finalize_object()
    engine.run_static_constructors()
    return mod


def print_tree(tree):
    def dfs(tree, graph, id=0):
        p_id = id
        graph.node(str(p_id), str(tree.__class__))
        for i in range(tree.getChildCount()):
            next_id = dfs(tree.getChild(i), graph, id+1)
            graph.edge(str(p_id), str(id+1))
            id = next_id

        return id

    graph = Digraph()
    graph.node_attr["shape"] = "plain"
    dfs(tree, graph)
    return graph


if __name__ == '__main__':
    #main()
    main(sys.argv)
