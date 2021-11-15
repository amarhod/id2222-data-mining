def jaccard_similarity(set1: set, set2: set) -> float:
    intersection_size = len(set1.intersection(set2))
    union_size = len(set1.union(set2))
    if union_size == 0:
        return 0.0
    return intersection_size / union_size


def compare_signatures(signature1: list, signature2: list) -> float:
    if len(signature1) != len(signature2):
        raise ValueError
    if len(signature1) == 0:
        return 0.0

    n = len(signature1)
    matching_values = 0
    for i in range(n):
        if signature1[i] == signature2[i]:
            matching_values += 1
    return matching_values / n


def compare_vectors(v1, v2):
    if len(v1) != len(v1):
        raise ValueError
    if len(v1) == 0:
        return 0.0

    n = len(v1)
    matching_values = 0
    union_counter = 0
    for i in range(n):
        if v1[i] == 1 or v2[1] == 1:
            union_counter += 1
        if v1[i] == 1 and v2[i] == 1:
            matching_values += 1
    return matching_values / union_counter
