from element import Element
from graphics.space.SwartAxis import SwartAxis
from interpreter.viedgets.service.element_array_based.dart_params import DartParams, DartParam


class ElementArrayBasedViedget:
    keyword: str
    element: Element
    _interpret_recursive: any
    main_axis_alignment = "default"
    cross_axis_alignment = "default"

    swift_boilerplate = ""
    dart_boilerplate = ""

    swift_imports = set()
    dart_imports = set()

    def __init__(self, element: Element, interpret_recursive: any, keyword: str, main_axis: str = None, swift_additional_data_processing = None):
        self.element = element
        self.keyword = keyword
        self.main_axis = main_axis

        self._interpret_recursive = interpret_recursive
        self._swift_additional_data_processing = swift_additional_data_processing
        self._dart_params = DartParams()
        self._data = {}

        # TODO: error messages
        element.validate_argument(0, "AT_ELEMENT_ARRAY")
        assert element.keyword == self.keyword, ""

        # TODO: validate alignment values
        if self.main_axis:
            if self.main_axis in element:
                self.main_axis_alignment = element[self.main_axis].value

            if self.cross_axis in element:
                self.cross_axis_alignment = element[self.cross_axis].value

        self._make_dart_params()

    def _make_dart_params(self):
        main_axis_alignment = {
            "default": DartParam("mainAxisAlignment", "MainAxisAlignment.start"),
            "start": DartParam("mainAxisAlignment", "MainAxisAlignment.start"),
            "end": DartParam("mainAxisAlignment", "MainAxisAlignment.end"),
            "space_between": DartParam("mainAxisAlignment", "MainAxisAlignment.spaceBetween"),
            "space_around": DartParam("mainAxisAlignment", "MainAxisAlignment.spaceAround"),

        }[self.main_axis_alignment]

        cross_axis_alignment = {
            "default": DartParam("crossAxisAlignment", "CrossAxisAlignment.center"),
            "start": DartParam("crossAxisAlignment", "CrossAxisAlignment.start"),
            "center": DartParam("crossAxisAlignment", "CrossAxisAlignment.center"),
            "end": DartParam("crossAxisAlignment", "CrossAxisAlignment.end"),
        }[self.cross_axis_alignment]

        self.add_dart_param(main_axis_alignment)
        self.add_dart_param(cross_axis_alignment)

    @property
    def cross_axis(self):
        return SwartAxis.get_opposite(of=self.main_axis)

    def make_content(self, element_wrapper: str, content_postprocessor, sep="\n"):
        content = ""
        for child_element in self.element[0].value:
            new_element = f"\n{self._interpret_recursive(child_element)}" + sep
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

        self._data["swift_alignment"] = cross_axis_alignment
        self._data["content"] = self.make_content(main_axis_alignment_element_wrappers[self.main_axis_alignment], main_axis_alignment_content_postprocessors[self.main_axis_alignment])

        if self._swift_additional_data_processing:
            self._swift_additional_data_processing(self._data)

        return self.swift_boilerplate.format(**self._data)

    @property
    def dart(self):
        self._data["dart_params"] = self._dart_params
        self._data["content"] = self.make_content(sep=",\n", element_wrapper="{0}", content_postprocessor=lambda x: x)

        return self.dart_boilerplate.format(**self._data)

    def add_dart_param(self, param: DartParam):
        self._dart_params.add(param)

    def add_dart_param_kv(self, key: str, value: str):
        new_param = DartParam(key, value)
        self._dart_params.add(new_param)
        return new_param

    def remove_dart_param(self, key: str):
        self._dart_params.remove(key)

