from wordle import Wordle
from wordle import forward_checking

def play_daily_wordle():
	wordle = Wordle ()
	wordle.file_to_words('./Wordle Answers.txt')

	#first_word = "roate"
	first_word = wordle.generate_random_word()
	wordle.update_trial(first_word)

	# instructions
	print("Type one character for current letter and enter :")
	print("0 : The letter is not in the word in any spot.")
	print("1 : The letter is in the word but in the wrong spot.")
	print("2 : The letter is in the word and in the correct spot.")
	print("Then repeat until the last letter")

	print("First word :",first_word)
	spots = []
	for i in range(wordle.n):
		print("Current letter : "+first_word[i])
		spot = int(input())
		spots.append(spot)
	wordle.update_Dn(first_word,spots)

	while True:
		print("Attempt",wordle.nb_attempts,":")
		i = str()
		nbVar = wordle.n
		print("Please wait, I am looking for a solution...")
		trial,nbNodes = forward_checking(wordle, i, nbVar)
		#print(wordle.Dn)
		print("Trial :",trial)

		print("Type as before : 0 or 1 or 2, enter and repeat until the last letter")
		spots = []
		for i in range(wordle.n):
			print("Current letter : "+trial[i])
			spot = int(input())
			spots.append(spot)  

		if wordle.check_victory_from_spots(spots):
			print("Bingo !")
			break
		elif wordle.nb_attempts >= 6:
			print("I lost... Sorry !")
			break
		else:   
			wordle.update_trial(trial)
			wordle.update_Dn(trial,spots)

	print(wordle.nb_attempts,"attempts !")

play_daily_wordle()