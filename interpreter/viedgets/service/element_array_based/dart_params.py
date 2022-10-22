class DartParam:
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

    def __str__(self):
        return f"{self.key}: {self.value}"


class DartParams:
    def __init__(self):
        self._params = []

    def add(self, param: DartParam):
        # TODO: error message
        assert isinstance(param, DartParam)
        self._params.append(param)

    def remove(self, key: str):
        idx = None

        for i, param in enumerate(self._params):
            if param.key == key:
                idx = i
                break

        if idx is not None:
            self._params.pop(idx)

    def __str__(self):
        out = ""

        for param in self._params:
            out += f"\n{param},\n"

        return out
