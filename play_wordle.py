from wordle import Wordle
from wordle import forward_checking

def play_wordle():
	wordle = Wordle ()
	wordle.file_to_words('./Wordle Answers.txt')

	wordle.generate_random_word_to_guess()

	while True:
		print("Attempt",wordle.nb_attempts+1,":")
		print("Type a word with",wordle.n,"letters")
		trial = input()
		while(len(trial) != wordle.n):
			print("Retype the word with",wordle.n,"letters :")
			trial = input()
		#print(wordle.Dn)
		print("Trial :",trial)
		wordle.update_trial(trial)

		spots = wordle.update_spots_Dn()
		print("Spots :",spots)

		if wordle.check_victory():
			print("Bingo !")
			break
		elif wordle.nb_attempts >= 6:
			print("You lost... Sorry !")
			print("The answer was "+wordle.word_to_guess+" !")
			break

	print(wordle.nb_attempts,"attempts !")

play_wordle()