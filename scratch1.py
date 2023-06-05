import numpy as np
import plotly.graph_objects as go
from typing import List
from custom.types import Point, Vector, Plane


def plot(
    points: List[Point] = [],
    vectors: List[Vector] = [],
    planes: List[Plane] = [],
    point_size: float = 5,
    plane_size: float = 3,
    plane_opacity: float = 0.5,
):
    fig = go.Figure()
    for _point in points:
        x, y, z = _point.xyz()
        fig.add_trace(
            go.Scatter3d(
                x=[x], y=[y], z=[z], mode="markers", marker=dict(size=point_size)
            )
        )
    for _vector in vectors:
        px, py, pz = _vector.point.xyz()
        dx, dy, dz = _vector.direction.to_cart()
        fig.add_trace(go.Scatter3d(x=[px, dx], y=[py, dy], z=[pz, dz], mode="lines"))
    for _plane in planes:
        A, B, C, D = _plane.np()
        x_range = y_range = z_range = [-plane_size, plane_size]
        x, y, z = np.meshgrid(x_range, y_range, z_range)
        z_plane = (-A * x - B * y - D) / C
        fig.add_trace(go.Surface(x=x[0], y=y[:, 0], z=z_plane, opacity=plane_opacity))
    fig.update_layout(
        scene=dict(xaxis=dict(title="X"), yaxis=dict(title="Y"), zaxis=dict(title="Z"))
    )
    fig.show()


if __name__ == "__main__":
    FOCAL_LENGTH = 0.5

    vector_pinhole = Vector.from_zero(1, 1, 1)
    vector_center = vector_pinhole.shrink_by(FOCAL_LENGTH)

    plane = Plane.from_intersection_with_vector_at_point(vector_pinhole, vector_center.end())

    point_up = plane.intersect_with_vector(Vector.from_zero(0, 0, 1))
    point_down = point_up.reflect_on(vector_center.end())

    points = [Point.zero(), vector_pinhole.end(), vector_center.end(), point_up, point_down]
    planes = [plane]
    
    # plot(points=points, planes=planes)
