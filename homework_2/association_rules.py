from __future__ import annotations
import itertools


def find_associations(itemsets: dict[tuple, int], c: int):
    rules = {}
    for k, val in itemsets.items():
        if len(k) == 1:
            continue
        else:
            current_size = 1
            while current_size < len(k):
                subsets = list(itertools.combinations(k, current_size))
                print(f"Subsets {subsets}")
                for subset in subsets:
                    left_side = tuple(sorted(subset))
                    right_side = get_set_without_element(k, left_side)
                    print(f"{left_side=}, {right_side=}")
                    union = tuple(sorted(left_side + right_side))
                    support_union = itemsets[union]
                    support_left_side = itemsets[left_side]
                    confidence = support_union / support_left_side
                    if confidence >= c:
                        rules[left_side] = right_side
                current_size += 1
    print(rules)


def get_set_without_element(set_to_check, element):
    new_set = []
    for v in set_to_check:
        if v not in element:
            new_set.append(v)
    return tuple(sorted(new_set))


if __name__ == "__main__":
    frequent_itemsets = {(0,): 2, (4,): 4, (5,): 4, (1,): 2, (2,): 2, (0, 5): 2, (4, 5): 3, (1, 4): 2, (2, 4): 2, (2, 5): 2, (2, 4, 5): 2}
    find_associations(frequent_itemsets, 0.5)
