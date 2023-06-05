import numpy as np


class Vector:
    def __init__(self, vector):
        self.vector = np.array(vector)

    def __str__(self):
        return str(self.vector)

    @staticmethod
    def from_np(vector):
        if not vector.shape == (3,):
            raise TypeError(
                f"vector has incorrect shape {vector.shape}. should be (3,)"
            )
        return Vector(vector)

    @staticmethod
    def i():
        return Vector([1, 0, 0])

    @staticmethod
    def j():
        return Vector([0, 1, 0])

    @staticmethod
    def k():
        return Vector([0, 0, 1])


class Matrix:
    def __init__(self, row1, row2, row3):
        self.matrix = np.array([row1, row2, row3])

    def __str__(self):
        return str(self.matrix)

    @staticmethod
    def from_np(matrix):
        if not matrix.shape == (3, 3):
            raise TypeError(
                f"matrix has incorrect shape {matrix.shape}. should be (3, 3)"
            )
        row1, row2, row3 = matrix
        return Matrix(row1, row2, row3)

    def __mul__(self, other):
        if isinstance(other, int):
            return Matrix.from_np(self.matrix * other)
        if isinstance(other, Vector):
            return Vector.from_np(np.dot(self.matrix, other.vector))

    @staticmethod
    def identity():
        return Matrix([1, 0, 0], [0, 1, 0], [0, 0, 1])


T = Matrix([1, 0, 0], [1, 0, 0], [1, 0, 0])

v = Vector.i()

print(T * v)
