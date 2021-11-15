import numpy as np
import random
import pandas as pd


class MiniHash:
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

    def get_signature(self, a, b, prime, characteristic_matrix, n):
        """
        Given the lists a,b containing the coeficients and constants of the hash functions, a prime number,
        characteristic matrix of size y x z, return signature matrix of size n x z

        Args:
            a (list): the coeficients for the hash functions. a[0] is the coeficient for hashfunction 0
            b (list): the constants for the hash functions. b[0] is the constant for hashfunction 0
            prime (int): a prime number
            characteristic_matrix (matrix): matrix of size y x z where y is the number of unique shingles and z is the
            number of documnets
            n (int): number of hashfunctions

        Returns:
            [matrix]: signature matrix of size n x z
        """
        sig_matrix = np.full((n, len(characteristic_matrix.T)), np.inf)
        for row in range(len(characteristic_matrix)):
            hash_values = []
            for j in range(n):
                val = self.mapping[row]  # should it be the shingle value or the row number?
                hash_value = (a[j]*val + b[j]) % prime
                hash_values.append(hash_value)
            for col in range(len(characteristic_matrix.T)):
                if characteristic_matrix[row][col] == 1:
                    for m in range(n):
                        if hash_values[m] < sig_matrix[m][col]:
                            sig_matrix[m, col] = hash_values[m]
        return sig_matrix

    def get_random_numbers(self, n):
        """Generates a list of n unique numbers

        Args:
            n (int): [description]

        Returns:
            [list]: a list of n unique numbers
        """
        coeficients = []
        k = n
        max_number = max(self.shingle_universe_hashed)
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
            sig_matrix: signature matrix n x d matrix where n is the number of hash functions applied,
            and d is the number of documents
            characteristic_matrix: the characterisitc matrix of size s x d where s is the number of unique shingles
            and d is the number of documents. Each column represents a document while each row represents a shingle
        """
        # print(f"Number of hash functions: {number_of_hash_functions}")
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
        a = self.get_random_numbers(number_of_hash_functions)
        b = self.get_random_numbers(number_of_hash_functions)
        sig_matrix = self.get_signature(a, b, self.prime, characteristic_matrix, number_of_hash_functions)
        return sig_matrix, characteristic_matrix
