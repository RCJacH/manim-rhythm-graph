import numpy as np


def calculate_distance(point_a, point_b):
    return np.linalg.norm(point_a - point_b)


def shortest_distance(point_a, list_b):
    distances = [
        calculate_distance(point_a=point_a, point_b=x) for x in list_b
    ]

    if (abs(np.diff(distances)) < 0.2).all():
        return -1

    return np.argmin(distances)


def get_sector_pairs(fewer_segments, more_segments):
    fewer_segments = fewer_segments.transpose()
    more_segments = more_segments.transpose()
    result_pairs = np.zeros((len(more_segments), 2), dtype="float64")
    i = 0
    for more_segment in more_segments:
        target = shortest_distance(more_segment, fewer_segments)
        if target == -1:
            v = result_pairs[i - 1][1]
            c = fewer_segments[:, 0]
            target = (np.where(c == v)[0][0]) + 1
        pair = (more_segment[0], fewer_segments[target][0])
        result_pairs[i, :] = pair
        i += 1

    for fewer_segment in fewer_segments:
        if fewer_segment[0] not in result_pairs[:, 1]:
            target = shortest_distance(fewer_segment, more_segments)
            pair = (more_segments[target][0], fewer_segment[0])
            result_pairs[i, :] = pair
            i += 1

    result = [
        1 if x == 1 else np.where(fewer_segments[0] == x)[0][0]
        for x in result_pairs[:, 1]
    ]
    return result
