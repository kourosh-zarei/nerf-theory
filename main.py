# pinhole = Direction.cart(1, 1, 1)
# focal_length = 0.5
# center = pinhole.shrink_by(focal_length)
# plane = Plane.from_intersection_with_vector(center)
# up = plane.intersect_with_vector(Direction.cart(0, 0, 1))
# down = up.reflect_on(center)
# # vector_from_center_to_left
# points = [Point, pinhole, center, up, down]
# plot_plane_and_points(points, plane)
