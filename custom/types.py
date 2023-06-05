import numpy as np


class Point:
    def __init__(self, xyz: np.ndarray):
        self.x, self.y, self.z = xyz

    @staticmethod
    def cart(x: float, y: float, z: float) -> "Point":
        return Point(np.array([x, y, z]))

    def xyz(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z])

    @staticmethod
    def zero() -> "Point":
        return Point.cart(0, 0, 0)

    def reflect_on(self, anchor: "Point"):
        x = 2 * anchor.x - self.x
        y = 2 * anchor.y - self.y
        z = 2 * anchor.z - self.z
        return Point.cart(x, y, z)

    def shrink_by(self, length: float) -> "Point":
        return Direction.from_points(Point.zero(), self).shrink_by(length).point()


class Direction:
    @staticmethod
    def __get_xyz(r, incl, azim) -> np.ndarray:
        x = r * np.sin(incl) * np.cos(azim)
        y = r * np.sin(incl) * np.sin(azim)
        z = r * np.cos(incl)
        return np.array([x, y, z])

    @staticmethod
    def __get_ria(x, y, z) -> np.ndarray:
        r = np.sqrt(x**2 + y**2 + z**2)
        incl = np.arccos(z / r)
        azim = np.arctan2(y, x)
        return np.array([r, incl, azim])

    def __init__(self, x, y, z, r=None, incl=None, azim=None, __system_access__=False):
        if (x == 0 and y == 0 and z == 0) or (r == 0):
            raise ZeroDivisionError("Direction must have non-zero length")
        if not __system_access__:
            r, incl, azim = self.__get_ria(x, y, z)
        self.x, self.y, self.z = x, y, z
        self.r, self.incl, self.azim = r, incl, azim

    @staticmethod
    def cart(x: float, y: float, z: float) -> "Direction":
        r, incl, azim = Direction.__get_xyz(x, y, z)
        return Direction(x, y, z, __system_access__=True)

    @staticmethod
    def pol(r: float, incl: float, azim: float) -> "Direction":
        x, y, z = Direction.__get_xyz(r, incl, azim)
        return Direction(x, y, z, r, incl, azim, __system_access__=True)

    def to_cart(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z])

    def to_pol(self) -> np.ndarray:
        return np.array([self.r, self.incl, self.azim])

    def shrink_by(self, L: float) -> "Direction":
        d = np.sqrt(self.x**2 + self.y**2 + self.z**2)
        ratio = (d - L) / d
        return Direction.cart(self.x * ratio, self.y * ratio, self.z * ratio)

    def point(self):
        return Point(self.to_cart())

    @staticmethod
    def from_points(start_point: Point, end_point: Point) -> "Direction":
        x, y, z = end_point.xyz() - start_point.xyz()
        return Direction(x, y, z)


class Vector:
    def __init__(self, direction: Direction, point: Point):
        self.direction = direction
        self.point = point

    def to_cart(self) -> np.ndarray:
        return self.direction.to_cart()

    @staticmethod
    def from_points(start_point: Point, end_point: Point) -> "Vector":
        return Vector(Direction.from_points(start_point, end_point), start_point)

    @staticmethod
    def from_zero(x, y, z) -> "Vector":
        return Vector(Direction.from_points(Point.zero(), Point.cart(x, y, z)), Point.zero())

    def shrink_by(self, length: float):
        return Vector(self.direction.shrink_by(length), self.point)

    def start(self) -> Point:
        return self.point

    def end(self) -> Point:
        return Point(self.direction.to_cart() + self.point.xyz())


class Plane:
    def __init__(self, A: float, B: float, C: float, D: float):
        self.A, self.B, self.C, self.D = A, B, C, D

    def equation(self) -> np.ndarray:
        return np.array([self.A, self.B, self.C, self.D])

    @staticmethod
    def from_intersection_with_vector_at_point(vector: Vector, point: Point):
        px, py, pz = point.xyz()
        dx, dy, dz = vector.direction.to_cart()
        magnitude = np.sqrt(dx**2 + dy**2 + dz**2)
        A, B, C = dx / magnitude, dy / magnitude, dz / magnitude
        D = A * px + B * py + C * pz
        return Plane(A, B, C, D)

    def intersect_with_vector(self, vector: Vector) -> Point:
        px, py, pz = vector.point.xyz()
        dx, dy, dz = vector.direction.to_cart()
        numerator = self.D - self.A * px - self.B * py - self.C * pz
        denominator = self.A * dx + self.B * dy + self.C * dz
        t = numerator / denominator
        return Point.cart(px + t * dx, py + t * dy, pz + t * dz)
