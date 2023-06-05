import typing

from custom.types import Direction


class Points:
    @staticmethod
    def generate_points_at_inclination(
        n_samples: int, incl: float, r: float = 1
    ) -> typing.List[Direction]:
        if 180 - incl < 5:
            points = [Direction.pol(r, 0, 0)]
        elif 175 < 180 - incl:
            points = [Direction.pol(r, 180, 0)]
        else:
            n_azimuth_samples = [i * 360 / n_samples for i in range(n_samples + 1)]
            points = [Direction.pol(r, incl, azim) for azim in n_azimuth_samples]
        return points

    @staticmethod
    def generate_points_at_inclinations(
        n_samples, inclinations: typing.List[float]
    ) -> typing.List[Direction]:
        points = [
            point
            for incl in inclinations
            for point in Points.generate_points_at_inclination(n_samples, incl)
        ]
        return points

    @staticmethod
    def to_cart(points: typing.List[Direction]):
        return [point.to_cart() for point in points]

    @staticmethod
    def to_pol(points: typing.List[Direction]):
        return [point.to_pol() for point in points]

    @staticmethod
    def split_points(
        points: typing.List[typing.Tuple[float, float, float]],
    ) -> typing.Tuple[typing.List, ...]:
        x, y, z = [], [], []
        for p in points:
            _x, _y, _z = p
            x.append(_x)
            y.append(_y)
            z.append(_z)
        return x, y, z
