from __future__ import annotations
import itertools


class Associator():

    def __init__(self, itemsets: dict[tuple, int], confidence):
        self.itemsets = itemsets
        self.confidence = confidence
        self.rules = self.find_associations()

    def find_associations(self):
        rules = set()
        for k, val in self.itemsets.items():
            if len(k) == 1:
                continue
            else:
                current_size = 1
                while current_size < len(k):
                    subsets = list(itertools.combinations(k, current_size))
                    for subset in subsets:
                        left_side = tuple(sorted(subset))
                        right_side = self.get_set_without_element(k, left_side)
                        support_union = val
                        support_left_side = self.itemsets[left_side]
                        confidence = support_union / support_left_side
                        if confidence >= self.confidence:
                            rule = f"{left_side} -> {right_side}"
                            rules.add(rule)
                    current_size += 1
        return rules

    def get_set_without_element(self, set_to_check, element):
        new_set = []
        for v in set_to_check:
            if v not in element:
                new_set.append(v)
        return tuple(sorted(new_set))


if __name__ == "__main__":
    frequent_itemsets = {(0,): 2, (4,): 4, (5,): 4, (1,): 2, (2,): 2, (0, 5): 2, (4, 5): 3,
                         (1, 4): 2, (2, 4): 2, (2, 5): 2, (2, 4, 5): 2}
    associator = Associator(frequent_itemsets, confidence=1)
    print(associator.rules)
    """
    correct answers for confidence 0.75
    0 -> 5
    4 -> 5
    5 -> 4
    1 -> 4
    2 -> 4
    2 -> 5
    2 -> 4,5
    2,4 -> 5
    2,5 -> 4
    """
    """
    correct answers for confidence 1
    0 -> 5
    1 -> 4
    2 -> 4
    2 -> 5
    2 -> 4,5
    2,4 -> 5
    2,5 -> 4
    """
