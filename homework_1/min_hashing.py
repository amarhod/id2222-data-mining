import numpy as np
import random


class Mini_Hash:
    def __init__(self, shingles, n):
        self.shingles_hashed = [s.hashed_shingle_set for s in shingles]
        self.shingles_str = [s.shingle_set for s in shingles]
        self.n = n  # size of the signatures
        self.prime = 2000000011  # our prime number
        # using list to make sure the shingles do not get rearanged
        self.shingle_universe = []
        for shingle_set in self.shingles_str:
            for shingle in shingle_set:
                if shingle not in self.shingle_universe:
                    self.shingle_universe.append(shingle)
        # list(set.union(*self.shingles_str))
        self.shingle_universe_hashed = []
        for shingle_set in self.shingles_hashed:
            for shingle in shingle_set:
                if shingle not in self.shingle_universe_hashed:
                    self.shingle_universe_hashed.append(shingle)
        # self.shingle_universe_hashed = list(set.union(*self.shingles_hashed))
        self.mapping = {}
        print("Prime is " + str(self.prime))

    def get_hashes(self):
        return self.mini_hash(self.shingles_hashed, self.n)

    def get_signature(self, shingles, a, b, prime, number_of_hash_functions):
        min_hashes = []
        for i in range(number_of_hash_functions):
            min_hash = prime + 1
            for j in range(len(shingles)):
                if shingles[j] == 1:
                    shingle_value = self.mapping[j]
                    hash = (a[i]*shingle_value + b[i]) % prime
                    if hash < min_hash:
                        min_hash = hash
            min_hashes.append(min_hash)
        return min_hashes

    def get_random_numbers(self, number_of_hash_functions):
        # random.seed(150) # adding seed gives the same output all the time, but accuracy depends on seed?
        coeficients = []
        k = number_of_hash_functions
        max_number = 2**32 - 1
        while k > 0:
            number = random.randint(0, max_number)
            while number in coeficients:
                number = random.randint(0, max_number)
            coeficients.append(number)
            k -= 1
        assert len(set(coeficients)) == len(coeficients)
        return coeficients

    def mini_hash(self, shingle_list: list, number_of_hash_functions) -> list:
        """
        Given a list, where each element is a set representing the shingles for each document we want to check,
        it returns a matrix where each column is a document and the rows represent the shingles universe of
        the documents.
        The value at row i and column j is
        1 if document j contains the shingle at row i

        Args:
            shingle_list (list): [description]

        Returns:
            sig_matrix: signature matrix
            characteristic_matrix:
        """
        print(f"Number of hash functions: {number_of_hash_functions}")
        shingle_universe = self.shingle_universe_hashed  # using list to make sure the shingles do not get rearanged
        characteristic_matrix = np.zeros((len(shingle_universe), len(shingle_list)))
        for i in range(len(characteristic_matrix)):
            self.mapping[i] = shingle_universe[i]
            for j in range(len(characteristic_matrix.T)):
                if shingle_universe[i] in shingle_list[j]:
                    characteristic_matrix[i][j] = 1

        sig_matrix = []
        # print(f"characteristic matrix: {characteristic_matrix}")
        a = self.get_random_numbers(number_of_hash_functions)
        b = self.get_random_numbers(number_of_hash_functions)
        for col in characteristic_matrix.T:
            signature = self.get_signature(col, a, b, self.prime, number_of_hash_functions)
            sig_matrix.append(signature)
        return sig_matrix, characteristic_matrix
