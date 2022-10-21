from element import Element
from parser import Parser
from interpreter.viedgets.service.viedget import Viedget


class TextViedget(Viedget):
    keyword = "text"

    swift_boilerplate = """Text("{text}"){swift_style}"""

    dart_boilerplate = """Text(
"{text}",
style: TextStyle({dart_style}
)
)"""

    dart_short_boilerplate = """Text("{text}",)"""

    def __init__(self, element: Element, *args, **kwargs):
        # assert element.keyword == self.keyword

        data = {"text": element[0].value, "swift_style": "", "dart_style": ""}

        if "font_size" in element and element["font_size"].type == "AT_INTEGER":
            font_size = element['font_size'].value
            data["swift_style"] += f"\n    .font(.system(size: {font_size}))"
            data["dart_style"] += f"\nfontSize: {font_size},"

        if "font_weight" in element and element["font_weight"].type == "AT_STRING":
            font_weight = element['font_weight'].value
            data["swift_style"] += f"\n    .fontWeight(.{font_weight})"
            data["dart_style"] += f"\nfontWeight: FontWeight.{font_weight},"

        if "color" in element and element["color"].type == "AT_STRING":
            color = element['color'].value
            data["swift_style"] += f"\n    .foregroundColor(.{color})"
            data["dart_style"] += f"\ncolor: Colors.{color},"

        if "background_color" in element and element["background_color"].type == "AT_STRING":
            background_color = element['background_color'].value
            data["swift_style"] += f"\n    .background(.{background_color})"
            data["dart_style"] += f"\nbackgroundColor: Colors.{background_color},"

        self.element = element

        super().__init__(element, interpret_recursive=None, **data)

    @property
    def dart(self):
        if "color" in self.element:
            return self.dart_boilerplate.format(**self.data)

        return self.dart_short_boilerplate.format(**self.data)


def main():
    with open("../text_test.swart", "r") as file:
        parser = Parser(file.read())
        parser.parse()
        t = TextViedget(parser.root_element)
        print(t.swift)
        print(t.dart)


if __name__ == '__main__':
    main()
