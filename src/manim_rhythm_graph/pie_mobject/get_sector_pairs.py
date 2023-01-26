import math
import numpy as np


def calculate_distance(point_a, point_b):
    return np.linalg.norm(point_a - point_b)
    # return math.dist(point_a, point_b)


def shortest_distance(point_a, list_b):
    distances = [
        calculate_distance(point_a=point_a, point_b=x) for x in list_b
    ]

    return np.argmin(distances)


def get_sector_pairs(fewer_segments, more_segments):
    real_fewer_segments = fewer_segments.transpose()
    cap = real_fewer_segments[-1, 1]
    fewer_segments = np.concatenate((real_fewer_segments, ((cap, cap),)))
    more_segments = more_segments.transpose()
    result_pairs = np.zeros((len(more_segments), 2), dtype="float64")
    i = 0
    for more_segment in more_segments:
        target = shortest_distance(more_segment, real_fewer_segments)
        if fewer_segments[target][0] not in result_pairs[:, 1] or not i:
            pair = (more_segment[0], fewer_segments[target][0])
            result_pairs[i, :] = pair
            i += 1

    for fewer_segment in real_fewer_segments:
        if fewer_segment[0] not in result_pairs[:, 1]:
            target = shortest_distance(fewer_segment, more_segments)
            pair = (more_segments[target][0], fewer_segment[0])
            result_pairs[i, :] = pair
            i += 1

    fewer_edges = np.stack(
        (fewer_segments[:, 0], fewer_segments[:, 0])
    ).transpose()
    for more_segment in more_segments:
        if more_segment[0] not in result_pairs[:, 0]:
            target = shortest_distance(more_segment, fewer_edges)
            pair = (more_segment[0], fewer_segments[target][0])
            result_pairs[i, :] = pair
            i += 1

    result_pairs = np.sort(result_pairs[:, 1])

    result = [
        -1 if x == cap else np.where(real_fewer_segments[0] == x)[0][0]
        for x in result_pairs
    ]
    return result
