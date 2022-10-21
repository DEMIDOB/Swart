from element import Element
from graphics.space.SwartAxis import SwartAxis


class ElementArrayBasedViedget:
    keyword: str
    element: Element
    interpret_recursive: any
    main_axis_alignment = "default"
    cross_axis_alignment = "default"

    swift_boilerplate = ""
    dart_boilerplate = ""

    swift_imports = set()
    dart_imports = set()

    def __init__(self, element: Element, interpret_recursive: any, keyword: str, main_axis: str = None, swift_additional_data_processing = None):
        self.element = element
        self.interpret_recursive = interpret_recursive
        self.keyword = keyword
        self.main_axis = main_axis
        self.swift_additional_data_processing = swift_additional_data_processing

        self.data = {}

        # TODO: error messages
        element.validate_argument(0, "AT_ELEMENT_ARRAY")
        assert element.keyword == self.keyword, ""

        # TODO: validate alignment values
        if self.main_axis:
            if self.main_axis in element:
                self.main_axis_alignment = element[self.main_axis].value

            if self.cross_axis in element:
                self.cross_axis_alignment = element[self.cross_axis].value

    @property
    def cross_axis(self):
        return SwartAxis.get_opposite(of=self.main_axis)

    def make_content(self, element_wrapper: str, content_postprocessor, sep="\n"):
        content = ""
        for child_element in self.element[0].value:
            new_element = f"\n{self.interpret_recursive(child_element)}" + sep
            content += element_wrapper.format(new_element)

        if content[len(content)-len(sep):len(content)] == sep:
            content = content[:-len(sep)]

        return content_postprocessor(content)

    @property
    def swift(self):
        main_axis_alignment_element_wrappers = {
            "default": "{0}",
            "start": "{0}",
            "center": "{0}",
            "end": "{0}",
            "space_between": "{0}\nSpacer()\n",
            "space_around": "\nSpacer()\n{0}"
        }

        main_axis_alignment_content_postprocessors = {
            "default": lambda x: x,
            "start": lambda x: x + "\n\nSpacer()",
            "center": lambda x: f"\nSpacer()\n{x}\n\nSpacer()",
            "end": lambda x: "\n\nSpacer()" + x,
            "space_between": lambda x: x[:-10],
            "space_around": lambda x: x + "\n\nSpacer()"
        }

        cross_axis_alignment = {
            "default": "alignment: .center",
            "start": "alignment: .leading",  # racist i know
            "end": "alignment: .trailing",  # and this one as well :)
            "center": "alignment: .center",
            "top": "alignment: .top",
            "bottom": "alignment: .bottom",
        }[self.cross_axis_alignment]

        self.data["swift_alignment"] = cross_axis_alignment
        self.data["content"] = self.make_content(main_axis_alignment_element_wrappers[self.main_axis_alignment], main_axis_alignment_content_postprocessors[self.main_axis_alignment])

        if self.swift_additional_data_processing:
            self.swift_additional_data_processing(self.data)

        return self.swift_boilerplate.format(**self.data)

    @property
    def dart(self):
        dart_params = ""

        main_axis_alignment = {
            "default": "mainAxisAlignment: MainAxisAlignment.start",
            "start": "mainAxisAlignment: MainAxisAlignment.start",
            "end": "mainAxisAlignment: MainAxisAlignment.end",
            "space_between": "mainAxisAlignment: MainAxisAlignment.spaceBetween",
            "space_around": "mainAxisAlignment: MainAxisAlignment.spaceAround",

        }[self.main_axis_alignment]

        cross_axis_alignment = {
            "default": "crossAxisAlignment: CrossAxisAlignment.center",
            "start": "crossAxisAlignment: CrossAxisAlignment.start",
            "end": "crossAxisAlignment: CrossAxisAlignment.end",
            "center": "crossAxisAlignment: CrossAxisAlignment.center",
        }[self.cross_axis_alignment]

        dart_params += f"\n{main_axis_alignment},\n"
        dart_params += f"{cross_axis_alignment},\n"

        self.data["dart_params"] = dart_params
        self.data["content"] = self.make_content(sep=",\n", element_wrapper="{0}", content_postprocessor=lambda x: x)
        return self.dart_boilerplate.format(**self.data)
