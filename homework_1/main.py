import os
from compare_sets import compare_signatures, compare_vectors, jaccard_similarity
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
    document_names = []
    for document_name in os.listdir(document_folder):
        if document_name.endswith('.txt'):
            document_names.append(document_name)
            file_path = document_folder + '/' + document_name
            shingle_obj = Shingle(k, file_path)
            shingles.append(shingle_obj)

    mini_hash = MiniHash(shingles, n)
    sig_matrix, characterisitc_matrix = mini_hash.get_hashes()
    for i in range(sig_matrix.shape[1]):
        for j in range(i, sig_matrix.shape[1]):
            if i != j:
                similarity = compare_signatures(sig_matrix.T[i], sig_matrix.T[j])
                similarity_jaccard = jaccard_similarity(set(shingles[i].shingle_set), set(shingles[j].shingle_set))
                print(f"{document_names[i]} - {document_names[j]}: Jaccard shingle vs signature similarity "
                      f"{round(similarity_jaccard, 2)} - {similarity}")


if __name__ == '__main__':
    main()
