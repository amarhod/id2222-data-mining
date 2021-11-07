import os
import random
from compare_sets import compare_signatures
from shingle import Shingle


def main(document_folder='data/sport_articles', k=10, n=100):
    shingled_documents = []
    index_permutation = list(range(n))  # Used when picking values to hash for the signature
    random.shuffle(index_permutation)

    for document_name in os.listdir(document_folder):
        if document_name.endswith('.txt'):
            file_path = document_folder + '/' + document_name
            shingled_documents.append(Shingle(k, index_permutation, file_path))

    for i in range(len(shingled_documents)):
        if i + 1 < len(shingled_documents):
            print(compare_signatures(shingled_documents[i].signature,
                                     shingled_documents[i+1].signature))


if __name__ == '__main__':
    main()
