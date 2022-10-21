from element import Element
from graphics.space.SwartAxis import SwartAxis
from interpreter.viedgets.service.element_array_based_viedget import ElementArrayBasedViedget


class ColumnViedget(ElementArrayBasedViedget):
    keyword = "column"

    swift_boilerplate = """VStack({swift_alignment}) ~{content}
|"""

    dart_boilerplate = """Column({dart_params}
children: [{content}
],
)"""

    def __init__(self, element: Element, interpret_recursive):
        super().__init__(element, interpret_recursive, self.keyword, main_axis=SwartAxis.VERTICAL)
