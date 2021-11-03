import re


class Shingle():
    def __init__(self, k, document_path) -> None:
        self.set = set()

        with open(document_path) as f:
            txt = f.read()
        txt = re.sub(r'\n|\t', ' ', txt)
        txt = re.sub(r'\s{2,}', ' ', txt)

        index_start = 0
        while(index_start + k < len(txt)):
            self.set.add(txt[index_start:index_start + k])
            index_start += 1


if __name__ == '__main__':
    shingle = Shingle(10, 'data/sport_articles/Text0001.txt')
    shingles_sorted_list = sorted(list(shingle.set))
    print(shingles_sorted_list)
