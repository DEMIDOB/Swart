from dataclasses import dataclass

import numpy as np


@dataclass
class Vector:
    x: float
    y: float
    z: float = 0

    @property
    def np(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z])

    @property
    def spacial(self) -> float:
        val = self.x

        if self.y != 0:
            val *= self.y

            if self.z != 0:
                val *= self.z

        return val

    @staticmethod
    def zero():
        return Vector(0, 0)


class Frame:
    def __init__(self, size: Vector = None, child=None):
        self.size = size
        self.child = child

    def render(self, size: Vector = None):
        render_size = size if size else self.size  # passed size is preferred over the one provided on initialization
        assert render_size is not None

        if self.child is None:
            return np.zeros((self.size.x, self.size.y))

        return self.child.render(self.size)


class Fill(Frame):
    def __init__(self, color: Vector):
        super().__init__()
        self.color = color

    def render(self, size: Vector = None):
        render_size = size if size else self.size  # passed size is preferred over the one provided on initialization
        return np.repeat(self.color.np).reshape(render_size.y, render_size.x)
