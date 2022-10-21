import queue

from element import Element


class Parser:
    def __init__(self, src, src_id: int = 0):
        self.src = src
        self.id = src_id

        self.parser_fields = {
            "tasks": queue.Queue(),
            "elements_amount": 0,
            "elements": {},
            "get_new_element_id": self.get_new_element_id,
        }

        self.root_element = Element(src, parser_fields=self.parser_fields, global_offset=0)
        self.parser_fields["tasks"].put(self.root_element.preprocess)
        self.parser_fields["tasks"].put(self.root_element.parse)

    @property
    def elements_amount(self):
        return self.parser_fields["elements_amount"]

    @elements_amount.setter
    def elements_amount(self, value):
        self.parser_fields["elements_amount"] = value

    def get_new_element_id(self) -> int:
        val = self.id * 10 ** 5 + self.elements_amount
        self.elements_amount += 1
        return val

    def parse(self):
        while not self.parser_fields["tasks"].empty():
            task = self.parser_fields["tasks"].get()
            task()
