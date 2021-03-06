def tag_extractor(filename):
	alist = []
	with open(filename, "r") as file:
		data = file.readlines()
		for line in data:
			words = line.rstrip("\n").split(" ")
			if len(words) != 1:
				alist.append(words[1])
	return alist

def accuracy(original_file, predicted_file):
	count = 0
	originals = tag_extractor(original_file)
	predicted = tag_extractor(predicted_file)
	for tag in xrange(len(originals)):
		if originals[tag] == predicted[tag]:
			count += 1
	return (count *1.0)/ len(predicted)

print accuracy("POS/Part 4/p4_viterbi_0.txt","POS/dev.out")
