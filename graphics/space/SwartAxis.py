class SwartAxis:
    VERTICAL = "vertical_alignment"
    HORIZONTAL = "horizontal_alignment"

    AXES = [VERTICAL, HORIZONTAL]

    @staticmethod
    def get_opposite(*, of: str):
        assert of in SwartAxis.AXES, f"Unrecognized alignment token {of}"

        for axis in SwartAxis.AXES:
            if axis != of:
                return axis
