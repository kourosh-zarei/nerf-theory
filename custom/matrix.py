import typing

import numpy as np


def calculate_transformation_matrix(
    v1: typing.Tuple[float, float, float], v2: typing.Tuple[float, float, float]
):
    v1_norm = v1 / np.linalg.norm(v1)
    v2_norm = v2 / np.linalg.norm(v2)
    axis = np.cross(v1_norm, v2_norm)
    axis_norm = axis / np.linalg.norm(axis)
    cos_theta = np.dot(v1_norm, v2_norm)
    theta = np.arccos(cos_theta)

    rotation_matrix = np.array(
        [
            [
                cos_theta + (1 - cos_theta) * axis_norm[0] ** 2,
                (1 - cos_theta) * axis_norm[0] * axis_norm[1]
                - np.sin(theta) * axis_norm[2],
                (1 - cos_theta) * axis_norm[0] * axis_norm[2]
                + np.sin(theta) * axis_norm[1],
            ],
            [
                (1 - cos_theta) * axis_norm[1] * axis_norm[0]
                + np.sin(theta) * axis_norm[2],
                cos_theta + (1 - cos_theta) * axis_norm[1] ** 2,
                (1 - cos_theta) * axis_norm[1] * axis_norm[2]
                - np.sin(theta) * axis_norm[0],
            ],
            [
                (1 - cos_theta) * axis_norm[2] * axis_norm[0]
                - np.sin(theta) * axis_norm[1],
                (1 - cos_theta) * axis_norm[2] * axis_norm[1]
                + np.sin(theta) * axis_norm[0],
                cos_theta + (1 - cos_theta) * axis_norm[2] ** 2,
            ],
        ]
    )
    scaling_matrix = np.array(
        [
            [np.linalg.norm(v2) / np.linalg.norm(v1), 0, 0],
            [0, np.linalg.norm(v1) / np.linalg.norm(v2), 0],
            [0, 0, 1],
        ]
    )
    transformation_matrix = rotation_matrix.dot(scaling_matrix)
    return transformation_matrix


def find_point_on_plane(a, b, c, d, B, L):
    normal_vector = np.array([a, b, c])
    normal_vector /= np.linalg.norm(normal_vector)
    offset_vector = normal_vector * L
    closest_point = B + offset_vector
    return closest_point


if __name__ == "__main__":
    v1 = np.array([1, 0, 0])
    v2 = np.array([1, 1, 1])
    print(calculate_transformation_matrix(v1, v2))
