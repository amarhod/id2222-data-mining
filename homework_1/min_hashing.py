

def min_hashing_signature(shingle_list: list, index_permutation: list) -> list:
    """Generates a signature of length n by hashing the first value in the
    shuffled (permutated) list n times

    Args:
        shingle_list (list): A list of shingles
        index_permutation (list): A list of indexes

    Returns:
        list: A signature of n hashed values
    """
    signature = []
    for i in index_permutation:
        signature.append(hash(shingle_list[i]))
    return signature
