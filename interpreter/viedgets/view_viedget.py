from element import Element
from interpreter.viedgets.service.viedget import Viedget


class ViewViedget(Viedget):
    keyword = "view"

    swift_boilerplate = """
struct {name}: View ~
var body: some View ~
{content}
|
|"""

    dart_boilerplate = """
class {name} extends StatefulWidget ~
@override
State<StatefulWidget> createState() => _{name}State();
|

class _{name}State extends State<{name}> ~
@override
Widget build(BuildContext context) ~
return {content};
|
|"""

    def __init__(self, element: Element, interpret_recursive):
        assert element.keyword == self.keyword, f"Wrong element keyword ({element}) encountered while " \
                                                f"interpreting. Expected: {self.keyword} "
        assert 0 in element, f"An ordered argument#0 is required for Viedget({self.keyword}). Provided element: {element}"
        assert element[0].type == "AT_STRING", f"A non-string attribute#0 value in {element}"
        assert element["content"].type == "AT_ELEMENT", f"A non-element attribute#content value in {element}"

        data = {
            "name": element[0].value,
            "content": ""
        }

        self.element = element

        super().__init__(element, interpret_recursive=interpret_recursive, **data)

        self.add_import("import SwiftUI", """import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';""")

    @property
    def swift(self):
        swift_data = {
            "name": self.element[0].value,
            "content": self.interpret_recursive(self.element["content"].value)
        }

        return self.swift_boilerplate.format(**swift_data)

    @property
    def dart(self):
        dart_data = {
            "name": self.element[0].value,
            "content": self.interpret_recursive(self.element["content"].value)
        }

        return self.dart_boilerplate.format(**dart_data)
