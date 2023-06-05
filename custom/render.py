import typing
import numpy as np
import plotly.graph_objects as go
from custom.static_classes import Points
from custom.types import Direction, Plane, Point


def plot_point_3d(points: typing.List[Direction], axis_size: int = 1):
    points = Points.to_cart(points)
    x, y, z = Points.split_points(points)
    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=x,
                y=y,
                z=z,
                mode="markers",
                marker=dict(size=5, color="red"),
            )
        ]
    )

    fig.update_layout(
        scene=dict(
            xaxis=dict(
                title="X",
                nticks=4,
                range=[-axis_size, axis_size],
                backgroundcolor="rgb(255, 255, 255)",
                gridcolor="gray",
                showbackground=True,
                zerolinecolor="gray",
            ),
            yaxis=dict(
                title="Y",
                nticks=4,
                range=[-axis_size, axis_size],
                backgroundcolor="rgb(255, 255, 255)",
                gridcolor="gray",
                showbackground=True,
                zerolinecolor="gray",
            ),
            zaxis=dict(
                title="Z",
                nticks=4,
                range=[-axis_size, axis_size],
                backgroundcolor="rgb(255, 255, 255)",
                gridcolor="gray",
                showbackground=True,
                zerolinecolor="gray",
            ),
            aspectratio=dict(x=1, y=1, z=1),
            camera=dict(eye=dict(x=1.2, y=1.2, z=0.8)),
        )
    )

    fig.show()


def plot_plane_and_points(
    points: typing.List[typing.Union[Direction, Point]], plane: Plane
):
    # Generate coordinates for points on the plane
    x = np.linspace(-10, 10, 100)
    y = np.linspace(-10, 10, 100)
    x, y = np.meshgrid(x, y)
    z = (plane.D - plane.A * x - plane.B * y) / plane.C

    # Create 3D scatter plot
    fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, opacity=0.5)])

    # Plot points
    for point in points:
        fig.add_trace(
            go.Scatter3d(
                x=[point.x],
                y=[point.y],
                z=[point.z],
                mode="markers",
                marker=dict(size=5, color="red"),
            )
        )

    # Set plot title and labels
    fig.update_layout(
        title=f"Plane: {plane.A}x + {plane.B}y + {plane.C}z = {plane.D}",
        scene=dict(xaxis_title="X", yaxis_title="Y", zaxis_title="Z"),
    )

    # Show plot
    fig.show()
