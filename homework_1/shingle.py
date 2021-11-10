import re
from min_hashing import min_hashing_signature

class Shingle():
		"""Creates a set of hashed k-shingles with a signature of length n
			 from a text file
		"""
		def __init__(self, k: int, document_path: str) -> None:
				self.shingle_set = set()
				self.mapping = {} #this is just in case we want to get the text from the shingle hash 
				self.hashed_shingle_set = set()  

				# Open and clean the text
				with open(document_path, encoding='latin1') as f:
						txt = f.read()
				txt = re.sub(r'\n|\t', ' ', txt)
				txt = re.sub(r'\s{2,}', ' ', txt)

				index_start = 0
				shingle_hash = 0
				while(index_start + k <= len(txt)):
						shingle = txt[index_start:index_start + k]
						if shingle not in self.shingle_set:
							self.shingle_set.add(shingle)
							self.hashed_shingle_set.add(shingle_hash)
							self.mapping[shingle_hash] = shingle
							shingle_hash += 1
						index_start += 1


if __name__ == '__main__':
		shingle = Shingle(5, 100, './tests/text_1.txt')
		print(shingle.shingle_set)
		print(shingle.hashed_shingle_set)
		print(shingle.mapping)
		assert len(shingle.shingle_set) == len(shingle.hashed_shingle_set)
		#print(shingle.signature)
