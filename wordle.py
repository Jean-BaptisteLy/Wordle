import random
import copy
import csv

class Wordle:

	#def __init__(self, n=5, words):
	def __init__(self):
		self.n = 5
		self.words = []
		#self.current_words = words
		self.D = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		self.p = len(self.D)
		self.Dn = []
		for i in range(self.n):
			self.Dn.append(self.D.copy())

		self.trial = str()
		self.word_to_guess = str()

		self.nb_attempts = 0
		self.victory = False
		

	# to guess
	#############################################################
	def generate_random_word_to_guess(self):
		self.word_to_guess = random.choice(self.words)
		return self.word_to_guess

	def generate_my_word_to_guess(self, word):
		if word not in self.words:
			print("This word does not exist in the dictionary !")
			print("Game cancelled !")
			return None
		else:
			self.word_to_guess = word
		return word
	#############################################################

	# for trials
	#############################################################
	def generate_random_word(self):
		return random.choice(self.words)
	#############################################################

	def update_trial(self, trial):
		if trial not in self.words:
			print("This word does not exist in the dictionary !")
			return None
		self.nb_attempts += 1
		self.trial = trial
		return trial

	def update_spots(self):
		"""
		spots : vector list []
		0 : The letter is not in the word in any spot.
		1 : The letter is in the word but in the wrong spot.
		2 : The letter is in the word and in the correct spot.
		compare trial and word to guess
		"""
		spots = []
		for i in range(len(self.trial)):
			if self.trial[i] != self.word_to_guess[i]:
				if self.trial[i] not in self.word_to_guess:
					spots.append(0)
				else:
					spots.append(1)
			elif self.trial[i] == self.word_to_guess[i]:
				spots.append(2)
		#print("spots :",spots)
		return spots

	def check_last_wrong_spot(self,spots,letter):
		"""
		check if the letter is only in one Dn
		useful when a letter has just been classified "wrong spot" (see below update_Dn(word,spots))
		"""
		count = 0
		for D in self.Dn:
			if letter not in D:
				count += 1
		if count == len(spots) - 1:
			return True
		return False


	def update_Dn(self, word, spots):
		"""
		spots : vector list []
		0 : The letter is not in the word in any spot.
			We remove the letter in all Dn
		1 : The letter is in the word but in the wrong spot.
			Dn has his letter removed, then we check if there is one other only Dn has this letter,
			if yes, this other only Dn has must have only this letter
		2 : The letter is in the word and in the correct spot.
			Dn has finally one letter
		"""
		for i in range(len(word)):
			if spots[i] == 0:
				for j in range(len(self.Dn)):
					if word[i] in self.Dn[j] and len(self.Dn[j]) > 1:
						self.Dn[j].remove(word[i])
			elif spots[i] == 1:
				if word[i] in self.Dn[i]:
					self.Dn[i].remove(word[i])
					if self.check_last_wrong_spot(spots,word[i]):
						for j in range(len(self.Dn)):
							if word[i] in self.Dn[j]:
								self.Dn[j].clear()
								self.Dn[j].append(word[i])
			elif spots[i] == 2:
				self.Dn[i].clear()
				self.Dn[i].append(word[i])
			else:
				print("Error : update")
		#print(self.Dn)
		return self.Dn


	def update_spots_Dn(self):
		spots = self.update_spots()
		self.update_Dn(self.trial,spots)
		return spots

	def check_word_exists(self, word):
		if word in self.words:
			return True
		return False

	def check_victory(self):
		if self.trial == self.word_to_guess:
			self.victory = True
			return True

	def check_victory_from_spots(self, spots):
		spots = list(set(spots))
		if spots == [2]:
			self.victory = True
			return True
		self.victory = False
		return False

	# for reading files :
	def file_to_words(self, file):
		self.words = []
		with open(file, 'r') as f:
			reader = csv.reader(f, dialect='excel', delimiter='\t')
			for row in reader:
				self.words.append(row[2])
		del self.words[0]
		return self.words

def forward_checking(w, i, nbVar):
	nb_nodes = 0
	if nbVar == 0:
		return i,nb_nodes
	else:
		nbVar -= 1
		number = w.n - nbVar - 1
		for lv in range(len(w.Dn[number])):
			v = random.choice(w.Dn[number])
			node = i + v
			#print("node :",node)
			nb_nodes += 1
			if len(node) == w.n:
				if w.check_word_exists(node):
					return node,nb_nodes
			else:
				i_bis,nb_nodes_bis = forward_checking(w, node, nbVar)
				nb_nodes += nb_nodes_bis
				if len(i_bis) == w.n and w.check_word_exists(i_bis):
					i = i_bis
					break
	return i,nb_nodes


