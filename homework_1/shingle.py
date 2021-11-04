import re


class Shingle():
    """Creates a set of hashed k-shingles from a text file for a given
       file path and k
    """
    def __init__(self, k: int, document_path: str) -> None:
        shingle_set = set()

        with open(document_path, encoding='latin1') as f:
            txt = f.read()
        txt = re.sub(r'\n|\t', ' ', txt)
        txt = re.sub(r'\s{2,}', ' ', txt)

        index_start = 0
        while(index_start + k < len(txt)):
            shingle_set.add(txt[index_start:index_start + k])
            index_start += 1
        self.set = set(sorted(map(hash, shingle_set)))


if __name__ == '__main__':
    shingle = Shingle(10, 'data/sport_articles/Text0001.txt')
    print(shingle.set)
