import os
import random
from compare_sets import compare_signatures, compare_vectors
from shingle import Shingle
from min_hashing import Mini_Hash


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


def start(document_folder='./data/sport_articles', k=10, n=100):
    shingles = []
    for document_name in os.listdir(document_folder):
        if document_name.endswith('.txt'):
            file_path = document_folder + '/' + document_name
            shingle = Shingle(k, file_path)
            shingles.append(shingle)

    mini_hash = Mini_Hash(shingles, n)
    sig_matrix, characterisitc_matrix = mini_hash.get_hashes()
    # print(f"Mapping: {mini_hash.mapping}")
    print(f"Signature matrix: {sig_matrix}")
    # print(f"len of sig matrix: {len(sig_matrix)}")
    similarity = compare_signatures(sig_matrix[0], sig_matrix[1])
    similarity_from_char_matrix = compare_vectors(characterisitc_matrix.T[0], characterisitc_matrix.T[1])
    # print("Characteristic matrix: ")
    # print(characterisitc_matrix)
    print(f"Similarity from signatures: {similarity}")
    print(f"Similarity from characteristic matrix: {similarity_from_char_matrix}")


if __name__ == '__main__':
    start(document_folder="./tests/data", k=10, n=100)
    #start(document_folder="./tests/", k=5, n=3)
