def jaccard_similarity(set1: set, set2: set) -> float:
    intersection_size = len(set1.intersection(set2))
    union_size = len(set1.union(set2))
    if union_size == 0:
        return 0
    return intersection_size / union_size
