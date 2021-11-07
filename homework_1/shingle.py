import re
from min_hashing import min_hashing_signature


class Shingle():
    """Creates a set of hashed k-shingles with a signature of length n
       from a text file
    """
    def __init__(self, k: int, index_permutation: list, document_path: str) -> None:
        self.shingle_set = set()

        # Open and clean the text
        with open(document_path, encoding='latin1') as f:
            txt = f.read()
        txt = re.sub(r'\n|\t', ' ', txt)
        txt = re.sub(r'\s{2,}', ' ', txt)

        index_start = 0
        while(index_start + k < len(txt)):
            self.shingle_set.add(txt[index_start:index_start + k])
            index_start += 1
        self.signature = min_hashing_signature(list(self.shingle_set),
                                               index_permutation)


if __name__ == '__main__':
    shingle = Shingle(10, 100, 'data/sport_articles/Text0001.txt')
    print(shingle.set)
    print(shingle.signature)
