#Structure of the count_word = {tag: {word: count, word: count}, tag:{word, count}}

from output_printer import output_to_file, tagger

def gen_bjos(state_count, filetest, emission_count):
	states = {}
	dict = {}
	predicts = {} #list of tag to unique words
	# Read state count from file
	with open(state_count, "r") as file:
		data = file.readlines()
		for line in data:
			words = line.strip().split(" ")
			states[words[0]] = float(words[1])
	for i in states.keys(): dict[i] = {}
	all_state_count = sum([states[tags] for tags in states])
	for words in filetest:
		prob_list = check(emission_count, words)
		if prob_list != {}: # word exist
			for tags in states.keys():
				if tags in prob_list.keys():
					prob_list[tags] = (prob_list[tags]*1.0)/(states[tags] + 1)
					dict[tags][words] = prob_list[tags]
				else:
					dict[tags][words] = 0.0
			predicted_tag = argmax(prob_list)
			predicts[words] = predicted_tag
		else: # word does not exist
			temp = 0
			argtemp = ""
			for tags in states.keys():
				dict[tags][words] = 1.0 / 43 #states[tags] / all_state_count 
				if dict[tags][words] > temp:
					temp = dict[tags][words]
					argtemp = tags
			predicts[words] = argtemp
	return dict, predicts

def testing_splitter(filename, mode):
	if mode == "ALL":
		one_dataset, total_dataset = [], []
		with open(filename) as file:
			data = file.readlines()
			for line in data:
				words = line.strip()
				if len(words) != 0:
					one_dataset.append(words)
				else:
					total_dataset.append(one_dataset)
					one_dataset = []
		return total_dataset
	elif mode == "unique": # finds all unique word, saves time
		data_set = []
		with open(filename) as file:
			data = file.readlines()
			for line in data:
				words = line.strip()
				if words != " " and words not in data_set:
					data_set.append(words)
		return data_set

def check(filename, word):
	dict = {}
	with open(filename) as file:
		data = file.readlines()
		for line in data:
			words = line.strip().split(" ")
			if word == words[1]:
				dict[words[0]] = float(words[2])
	return dict

def argmax(alist):
	for key in alist.keys():
		if alist[key] == min(alist.values()):
			return key

testing = "../dev.in"
emission_count = "../Part 3/emission_train_count.txt"
state_count = "../Part 3/emission_count.txt"
filetest = testing_splitter(testing, mode="unique")
bjos, predicts = gen_bjos(state_count, filetest, emission_count)
output_to_file(bjos, "part5_emission_testing.txt")
