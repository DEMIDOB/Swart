from element import Element
from graphics.space.SwartAxis import SwartAxis
from interpreter.viedgets.service.element_array_based.element_array_based_viedget import ElementArrayBasedViedget


class ScrollableViedget(ElementArrayBasedViedget):
    keyword = "scrollable"

    swift_boilerplate = """ScrollView(.{direction}) ~{content}
|"""

    dart_boilerplate = """ScrollView({dart_params}
children: [{content}
],
)"""

    def __init__(self, element: Element, interpret_recursive):
        super().__init__(element, interpret_recursive, self.keyword, main_axis=SwartAxis.VERTICAL)

        self.direction = "vertical"
        if "direction" in element:
            element.validate_argument("direction", "AT_STRING")
            self.direction = element["direction"].value
            self.add_dart_param_kv("scrollDirection", f"Axis.{self.direction}")

            # TODO: AssertionError message
            assert self.direction in ("vertical", "horizontal")
        self._data["direction"] = self.direction
