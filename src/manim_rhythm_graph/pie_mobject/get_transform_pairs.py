import math
import manim as mn
import numpy as np


def get_transform_pairs(pie, pie2):
    new_division = len(pie2.weights)
    old_division = len(pie.weights)
    pie.background.set_opacity(opacity=0)
    pie2.background.set_opacity(opacity=0)
    if old_division == new_division:
        return ((pie2.background, pie.background), *zip(pie2, pie))
    elif old_division < new_division:
        return [(y, x) for (x, y) in get_unequal_pairs(pie, pie2)]
    elif old_division > new_division:
        return get_unequal_pairs(pie2, pie)


def get_unequal_pairs(fewer, more):
    pairs = [(fewer.background, more.background)]
    more_array = -(more.angles[:, 0] - mn.PI / 2)
    more_array = np.stack((more_array, (*more_array[1:], mn.TAU)))
    fewer_array = -(fewer.angles[:, 0] - mn.PI / 2)
    fewer_array = np.stack((fewer_array, (*fewer_array[1:], mn.TAU)))
    indice = get_sector_pairs(fewer_array, more_array)

    for i in range(len(indice)):
        cur_pos = indice[i]
        try:
            next_pos = indice[i + 1]
        except IndexError:
            next_pos = -1

        if cur_pos == next_pos or cur_pos == -1:
            start_item = fewer.radii[cur_pos].copy()
            # avoid weird artifact when transforming
            start_item["stroke"].set_stroke(width=start_item.stroke_width / 4)
        else:
            start_item = fewer[cur_pos]
        pairs.append((start_item, more[i]))
    return pairs


def get_sector_pairs(fewer_segments, more_segments):
    real_fewer_segments = fewer_segments.transpose()
    start = real_fewer_segments[0, 0]
    cap = real_fewer_segments[-1, 1]
    fewer_segments = np.concatenate((real_fewer_segments, ((cap, cap),)))
    more_segments = more_segments.transpose()
    result_pairs = np.full((len(more_segments), 2), start, dtype="float64")
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
        -1 if x == cap else np.where(real_fewer_segments[:, 0] == x)[0][0]
        for x in result_pairs
    ]
    return result


def shortest_distance(point_a, list_b):
    distances = [
        calculate_distance(point_a=point_a, point_b=x) for x in list_b
    ]

    return np.argmin(distances)


def calculate_distance(point_a, point_b):
    return np.linalg.norm(point_a - point_b)
