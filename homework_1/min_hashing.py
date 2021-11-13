import numpy as np
import random
import pandas as pd


class Mini_Hash:
    def __init__(self, shingles, n):
        self.shingles_hashed = [document.hashed_shingle_set for document in shingles]
        self.shingles_str = [document.shingle_set for document in shingles]
        self.n = n  # size of the signatures
        self.prime = 4385058877  # our prime number
        # using list to make sure the shingles do not get rearanged
        self.df = None
        self.shingle_universe = []
        for shingle_set in self.shingles_str:
            for shingle in shingle_set:
                if shingle not in self.shingle_universe:
                    self.shingle_universe.append(shingle)
        self.shingle_universe_hashed = []
        for shingle_set in self.shingles_hashed:
            for shingle in shingle_set:
                if shingle not in self.shingle_universe_hashed:
                    self.shingle_universe_hashed.append(shingle)
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

    def find_ones(self, arr):
        return np.where(arr == 1)[0]

    def signature(self, a, b, prime, characteristic_matrix, n):
        sig_matrix = np.full((n, len(characteristic_matrix.T)), np.inf)
        print(characteristic_matrix)
        print(self.df)
        print(f"a coeficients: {a}")
        print(f"b coeficients: {b}")
        for i in range(len(characteristic_matrix)):
            hash_values = []
            for j in range(n):
                hash_values.append((a[j]*j + b[j]) % prime)
            indeces = self.find_ones(characteristic_matrix[i])
            print(f"indeces for {i}: {indeces}")
            for k in range(len(sig_matrix)):
                for index in indeces:
                    if hash_values[k] < sig_matrix[k][index]:
                        sig_matrix[k][index] = hash_values[k]
                        print(sig_matrix)
        print(sig_matrix)
        return sig_matrix


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
        it returns a signature matrix and a characterisitc matrix where each column is a document and the rows represent
        the shingles universe of
        the documents.
        The value at row i and column j is
        1 if document j contains the shingle at row i

        Args:
            shingle_list (list): [description]

        Returns:
            sig_matrix: signature matrix n x b matrix where n is the number of hash functions applied,
            and b is the number of documents
            characteristic_matrix:
        """
        print(f"Number of hash functions: {number_of_hash_functions}")
        shingle_universe = self.shingle_universe_hashed  # using list to make sure the shingles do not get rearanged
        characteristic_matrix = np.zeros((len(shingle_universe), len(shingle_list)))
        chara_matrix_str = np.empty((len(shingle_universe), 1), dtype=object)
        for i in range(len(characteristic_matrix)):
            self.mapping[i] = shingle_universe[i]
            chara_matrix_str[i] = self.shingle_universe[i]
            for j in range(len(characteristic_matrix.T)):
                if shingle_universe[i] in shingle_list[j]:
                    characteristic_matrix[i][j] = 1

        df1 = pd.DataFrame(characteristic_matrix)
        df2 = pd.DataFrame(chara_matrix_str)
        df3 = pd.DataFrame(np.array(shingle_universe))
        self.df = pd.concat([df3, df2, df1], axis=1)
        
        #a = self.get_random_numbers(number_of_hash_functions)
        #b = self.get_random_numbers(number_of_hash_functions)
        a = [1,2]
        b = [3,4]
        #for col in characteristic_matrix.T:
            #signature = self.get_signature(col, a, b, self.prime, number_of_hash_functions)
            #sig_matrix.append(signature)
        sig_matrix = self.signature(a, b, self.prime, characteristic_matrix, number_of_hash_functions)
        return sig_matrix, characteristic_matrix
