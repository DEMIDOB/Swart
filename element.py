import re
from dataclasses import dataclass

from splitting import split_for_current_scope

ELEMENT_KEYWORD_RE = re.compile(r"[a-z][a-z_]*")
ATTRIBUTE_KEY_RE = re.compile(r"[a-z][a-z_]*:")

ELEMENT_RE = re.compile(r'\(.*\)')
VALID_STRING_RE = re.compile(r'.*')

ATTRIBUTE_TYPES = {
    ELEMENT_RE: "AT_ELEMENT",
    re.compile(r'\[.*]'): "AT_ELEMENT_ARRAY",
    # re.compile(r'[1-9][0-9]*px'): "AT_SIZE_PX",
    re.compile(r'[0-9]*'): "AT_INTEGER",
    VALID_STRING_RE: "AT_STRING",
}


@dataclass
class Attribute:
    alias: str or int
    value: any
    type: str

    def __init__(self, alias: str or int, value: str, parser_fields: dict, global_offset: int):
        self.alias = alias
        self.value = value
        self.raw_value = value
        self.type = ""
        self.global_offset = global_offset

        for type_re in ATTRIBUTE_TYPES:
            if re.fullmatch(type_re, value):
                self.type = ATTRIBUTE_TYPES[type_re]
                break

        assert self.type, f"Unknown attribute type. Value: {value}"

        self.handle_type(parser_fields)

    @property
    def value_start_global_offset(self):
        if isinstance(self.alias, int):
            return self.global_offset

        return self.global_offset + len(self.alias) + 1

    def handle_type(self, parser_fields: dict):
        if self.type == "AT_ELEMENT":
            current_element = Element(self.raw_value[1:-1].strip(), parser_fields,
                                      global_offset=self.value_start_global_offset)
            self.value = current_element

            parser_fields["tasks"].put(current_element.preprocess)
            parser_fields["tasks"].put(current_element.parse)
        elif self.type == "AT_ELEMENT_ARRAY":
            elements_src = split_for_current_scope(self.raw_value[1:-1], list(range(
                self.value_start_global_offset + 1,len(self.raw_value) + self.value_start_global_offset -1)))
            elements = []

            for element_src in elements_src[::-1]:
                current_element = Element(element_src[1:-1].strip(), parser_fields)
                parser_fields["tasks"].put(current_element.preprocess)
                parser_fields["tasks"].put(current_element.parse)
                elements.append(current_element)

            self.value = elements


class Element:
    def __init__(self, src: str, parser_fields: dict, global_offset: int = 0):
        self.clean_src_global_offsets = []
        self.keyword = ""
        self.clean_src = ""

        self.src = src
        self.global_id = parser_fields["get_new_element_id"]()
        self.global_offset = global_offset

        self.attributes = {}
        self.ordered_attributes = 0

        self.parser_fields = parser_fields

    def preprocess(self):
        self.clean_src = ""
        self.clean_src_global_offsets = []

        offset = self.global_offset - 1

        ignore = False

        for c in self.src:
            offset += 1

            if c == "#":
                ignore = not ignore
                continue

            if c == "\n":
                ignore = False
                c = " "  # treat c just as space

            if not ignore and not (c in {" ", "\n"} and self.clean_src and self.clean_src[-1] == " "):
                self.clean_src_global_offsets.append(offset)
                self.clean_src += c

        self.clean_src = self.clean_src.strip()

    def parse(self):
        assert self.clean_src, "Preprocessing should be made before parsing"

        split, split_offsets = split_for_current_scope(self.clean_src, self.clean_src_global_offsets,
                                                       capture_offsets=True, inverse=True)

        self.keyword = split.pop()
        self.validate_new_attr_keyword()

        while split:
            word = split.pop()
            offset = split_offsets.pop()

            if re.fullmatch(ATTRIBUTE_KEY_RE, word):
                assert split, f"No attribute value for key at symbol {offset}"

                next_word = split.pop()
                next_offset = split_offsets.pop()

                assert not re.fullmatch(ATTRIBUTE_KEY_RE, next_word), f"No attribute value for key at symbol " \
                                                                      f"{next_offset}, another attribute key instead"

                self.add_keyword_attribute(word[:-1], next_word, self.parser_fields, offset)
            else:
                self.add_order_attribute(word, self.parser_fields, offset)

    def validate_new_attr_keyword(self):
        assert re.fullmatch(ELEMENT_KEYWORD_RE, self.keyword), f"Invalid element keyword: `{self.keyword}`"

    def add_order_attribute(self, value, parser_fields: dict, global_offset):
        self.attributes[self.ordered_attributes] = Attribute(
            alias=self.ordered_attributes,
            value=value,
            parser_fields=parser_fields,
            global_offset=global_offset
        )

        self.ordered_attributes += 1
        return self.ordered_attributes - 1

    def add_keyword_attribute(self, key, value, parser_fields: dict, global_offset):
        assert key not in self.attributes, f"Redefining an attribute is prohibited. Symbol " \
                                           f"{global_offset}: \"{key}: {value}\""

        self.attributes[key] = Attribute(
            alias=key,
            value=value,
            parser_fields=parser_fields,
            global_offset=global_offset
        )

        return key

    def validate_argument(self, required_key: str or int, required_type: str):
        assert required_key in self, f"An argument#{required_key} is required for Viedget({self.keyword}). Provided " \
                                     f"element: {self} "
        assert self[required_key].type == required_type, f"An argument#{required_key} is required for" \
                                                         f"Viedget({self.keyword}) to be of {required_type} type. " \
                                                         f"Provided element: {self} "

    def __str__(self):
        return f"Element#{self.global_id}({self.keyword}, {self.attributes})"

    def __getitem__(self, item) -> Attribute:
        return self.attributes[item]

    def __contains__(self, item):
        return item in self.attributes

    def __iter__(self):
        for attribute_alias in self.attributes:
            yield attribute_alias
