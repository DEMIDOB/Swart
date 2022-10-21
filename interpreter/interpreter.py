from element import Element
from parser import Parser
from string_processing.prettifier import prettify
from interpreter.viedgets.service.viedgets import VIEDGETS


def interpret_element_in_swift(element: Element, imports=None):
    if imports is None:
        imports = set()

    assert element.keyword in VIEDGETS, f"Unknown keyword: {element.keyword}"
    viedget = VIEDGETS[element.keyword](element, lambda e: interpret_element_in_swift(e, imports=imports))

    for viedget_import in viedget.swift_imports:
        imports.add(viedget_import)

    return viedget.swift.replace("~", "{").replace("|", "}")


def interpret_element_in_dart(element: Element, imports=None):
    if imports is None:
        imports = set()

    assert element.keyword in VIEDGETS, f"Unknown keyword: {element.keyword}"
    viedget = VIEDGETS[element.keyword](element, lambda e: interpret_element_in_dart(e, imports=imports))

    for viedget_import in viedget.dart_imports:
        imports.add(viedget_import)

    return viedget.dart.replace("~", "{").replace("|", "}")


def main():
    with open("text_test.swart", "r") as file:
        parser = Parser(file.read())
        parser.parse()

        swift_imports = set()
        dart_imports = set()

        swift_interpretation = interpret_element_in_swift(parser.root_element, imports=swift_imports)
        dart_interpretation = interpret_element_in_dart(parser.root_element, imports=dart_imports)

        print(prettify(swift_interpretation))
        print(prettify(dart_interpretation))


if __name__ == '__main__':
    main()
