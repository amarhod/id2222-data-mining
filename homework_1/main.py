import os
from compare_sets import compare_signatures, compare_vectors
from shingle import Shingle
from min_hashing import MiniHash
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", nargs="?", default="./tests/data/", type=str)
    parser.add_argument("--shingle_size", nargs="?", default=10, type=int)
    parser.add_argument("--signature_size", nargs="?", default=100, type=int)
    return parser.parse_args()


def main():
    args = get_args()
    document_folder = args.folder
    n, k = args.signature_size, args.shingle_size
    shingles = []
    for document_name in os.listdir(document_folder):
        if document_name.endswith('.txt'):
            file_path = document_folder + '/' + document_name
            shingle_obj = Shingle(k, file_path)
            shingles.append(shingle_obj)

    mini_hash = MiniHash(shingles, n)
    sig_matrix, characterisitc_matrix = mini_hash.get_hashes()
    similarity = compare_signatures(sig_matrix.T[0], sig_matrix.T[1])
    similarity_from_char_matrix = compare_vectors(characterisitc_matrix.T[0], characterisitc_matrix.T[1])
    print(f"Similarity from signatures: {similarity}")
    print(f"Similarity from characteristic matrix: {similarity_from_char_matrix}")


if __name__ == '__main__':
    main()
