from interpreter.viedgets.service.viedget import Viedget

PADDING_DIRECTIONS = ("top", "bottom", "left", "right")


class PaddingViedget(Viedget):
    keyword = "padding"
    required_arguments = {0: "AT_ELEMENT"}

    swift_boilerplate = "{content}{swift_padding_data}"

    dart_boilerplate = """Padding(
padding: EdgeInsets.{dart_padding_data},
child: {content}
)"""

    def __init__(self, element, interpret_recursive, **kwargs):
        assert element.keyword == self.keyword, f"Wrong element keyword ({element}) encountered while " \
                                                f"interpreting. Expected: {self.keyword} "

        contains_either = ("all" in element or any(list(map(lambda x: x in element, PADDING_DIRECTIONS))))
        contains_both = ("all" in element and any(list(map(lambda x: x in element, PADDING_DIRECTIONS))))
        assert contains_either and not contains_both, f"Padding requires only `all` or any " \
                                                      f"of other attrs {PADDING_DIRECTIONS} "

        super().__init__(element, interpret_recursive=interpret_recursive, **kwargs)

        self.data["swift_padding_data"] = ""
        self.data["dart_padding_data"] = ""

        if "all" in element:
            self.data["swift_padding_data"] = f"\n    .padding({element['all'].value})"
            self.data["dart_padding_data"] = f"all({element['all'].value})"
        else:
            if "top" in element:
                self.data["swift_padding_data"] += f"\n    .padding(.top, {element['top'].value})"
            if "bottom" in element:
                self.data["swift_padding_data"] += f"\n    .padding(.bottom, {element['bottom'].value})"
            if "left" in element:
                self.data["swift_padding_data"] += f"\n    .padding(.leading, {element['left'].value})"
            if "right" in element:
                self.data["swift_padding_data"] += f"\n    .padding(.trailing, {element['right'].value})"

            self.data["dart_padding_data"] = "only("
            for attribute_alias in element:
                if attribute_alias in PADDING_DIRECTIONS:
                    self.data[
                        "dart_padding_data"] += f"{attribute_alias}: {element.attributes[attribute_alias].value}, "

            self.data["dart_padding_data"] = self.data["dart_padding_data"].strip() + ")"

        self.data["content"] = interpret_recursive(element[0].value)
