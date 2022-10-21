from element import Element
from interpreter.viedgets.service.element_array_based_viedget import ElementArrayBasedViedget
from string_processing.cases import snake_to_camel


class StackViedget(ElementArrayBasedViedget):
    keyword = "stack"

    swift_boilerplate = """ZStack(alignment: .{alignment}) ~{content}
|"""

    dart_boilerplate = """Stack(
alignment: Alignment.{alignment},
children: [{content}
],
)"""

    @staticmethod
    def handle_swift_alignment(data):
        data["alignment"] = {
            "bottomLeft": "bottomLeading",
            "bottomCenter": "bottom",
            "bottomRight": "bottomTrailing",
            "topLeft": "topLeading",
            "topCenter": "top",
            "topRight": "topTrailing",
            "centerLeft": "centerLeading",
            "center": "center",
            "centerRight": "centerTrailing",
        }[data["alignment"]]

    def __init__(self, element: Element, interpret_recursive):
        super().__init__(element, interpret_recursive, self.keyword,
                         swift_additional_data_processing=StackViedget.handle_swift_alignment)

        self.data["alignment"] = "center"

        if "alignment" in element:
            element.validate_argument("alignment", "AT_STRING")
            self.data["alignment"] = snake_to_camel(element["alignment"].value)
