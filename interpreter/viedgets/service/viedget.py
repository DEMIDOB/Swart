from element import Element


class Viedget:
    keyword = ""

    swift_boilerplate = ""
    dart_boilerplate = ""

    def __init__(self, element: Element, interpret_recursive, required_attributes: dict = None, **kwargs):
        assert element.keyword == self.keyword, f"Expected an element with keyword '{self.keyword}', got instead " \
                                                f"{element}"

        self.swift_imports = set()
        self.dart_imports = set()

        if required_attributes is None:
            required_attributes = {}

        for attribute_alias in required_attributes:
            assert attribute_alias in element, f"An ordered attribute#{attribute_alias} is " \
                                               f"required for Viedget({element.keyword}). " \
                                               f"Provided element: {element} "
            # TODO: error message
            assert required_attributes[attribute_alias] == element[attribute_alias].type

        self.data = kwargs
        self.interpret_recursive = interpret_recursive

    def add_import(self, swift_import, dart_import):
        self.swift_imports.add(swift_import)
        self.dart_imports.add(dart_import)

    @property
    def swift(self):
        return self.swift_boilerplate.format(**self.data)

    @property
    def dart(self,):
        return self.dart_boilerplate.format(**self.data)
