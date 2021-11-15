
class LHS():

    def __init__(self, threashold, sig_matrix, band=20, row=5):
        self.threashold = threashold
        self.sig_matrix = sig_matrix
        self.num_buckets = 4385058877  # prime number
        self.bands = 20
        self.rows = 5

    def hash_vector(self, vector):
        assert len(vector) == self.rows
        vector = [str(v) for v in vector]
        for v in vector:
            print(v)

    def find_candidates(self):
        print(self.sig_matrix)
        for row in range(0, len(self.sig_matrix), self.rows):
            start_row = row
            end_row = row + self.rows
            hashed_vals = []
            for col in range(len(self.sig_matrix.T)):
                current_col_vector = self.sig_matrix[start_row:end_row][:]
                current_col_vector = current_col_vector.T[col]
                hashed_vals.append(self.hash_vector(current_col_vector))
