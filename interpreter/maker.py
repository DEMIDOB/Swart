from parser import Parser
from interpreter.interpreter import interpret_element_in_dart, interpret_element_in_swift
from string_processing.prettifier import prettify


def make_swift(src: str, src_id: int = 0) -> str:
    parser = Parser(src, src_id)
    parser.parse()

    imports = set()
    interpreted = interpret_element_in_swift(parser.root_element, imports=imports)

    # print(imports)

    imports_text = ""
    for import_str in imports:
        imports_text += import_str + "\n"

    # if imports_text:
    #     imports_text += "\n"

    prettified = prettify(imports_text + interpreted)
    return prettified


def make_dart(src: str, src_id: int = 0) -> str:
    parser = Parser(src, src_id)
    parser.parse()

    imports = set()
    interpreted = interpret_element_in_dart(parser.root_element, imports=imports)

    imports_text = ""
    for import_str in imports:
        imports_text += import_str + "\n"

    # if imports_text:
    #     imports_text += "\n"

    prettified = prettify(imports_text + interpreted, tab="  ")
    return prettified
