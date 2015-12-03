import copy, math, string
def parseFile(fileName):
	valueDict = {}
	inFile = open(fileName, "r")
	fileLines = inFile.readlines()
	inFile.close()
	for line in fileLines:
		splitList = line.split(" ")
		if not splitList[0] in valueDict:
			valueDict[splitList[0]] = {}
		valueDict[splitList[0]][splitList[1]] = float(splitList[2])
	return valueDict

def parseSequences(fileName, tags=True):
	inFile = open(fileName, "r")
	fileLines = inFile.readlines()
	inFile.close()
	valueList = []
	newSequence = []
	for line in fileLines:
		if tags:
			line = line.split(" ")[0]
		line = line.strip()
		if len(line) > 0:
			newSequence.append(line)
		elif len(line) == 0:
			valueList.append(newSequence)
			newSequence = []
	return valueList

class ViterbiSequence:
	def __init__(self, lastTag):
		self.sequence = [lastTag]
		self.logProbability = 0.0
	def probTransmission(self, nextTag, nextEmission):
		lastTag = self.sequence[-1]
		try:
			if self.logProbability == None:
				return None
			if nextEmission == None:
				return self.logProbability + logTransmissions[lastTag][nextTag]	
			return self.logProbability + logTransmissions[lastTag][nextTag] + logEmissions[nextTag][nextEmission]
		except KeyError:
			return None
	def transit(self, nextTag, nextEmission):
		nextStep = copy.deepcopy(self)
		nextStep.logProbability = nextStep.probTransmission(nextTag, nextEmission)
		nextStep.sequence.append(nextTag)
		return nextStep

if __name__ == "__main__":
	START = "START"
	# model parameters
	transmissions = parseFile("transition.txt")
	emissions = parseFile("emission_training.txt")

	# list of all tags
	allTags = emissions.keys()

	# list of sequences
	# each sequence is a Python list containing the words in the sequence
	sequences = parseSequences("train")
	logTransmissions = {}
	for key1 in transmissions:
		logTransmissions[key1] = {}
		for key2 in transmissions[key1]:
			logTransmissions[key1][key2] = math.log(transmissions[key1][key2])
	logEmissions = {}
	for key1 in emissions:
		logEmissions[key1] = {}
		for key2 in emissions[key1]:
			logEmissions[key1][key2] = math.log(emissions[key1][key2])

	# output sequences corresponding to input sequences
	outputs = []

	for sequence in sequences:
		dpTable = [ViterbiSequence("__START")]
		for i in range(-1, len(sequence) -1):
			newDpTable= []
			for tag in allTags:
				positionMax = None
				maxChoice = None
				for dpEntry in dpTable:
					piValue = dpEntry.probTransmission(tag, sequence[i +1])
					if piValue >= positionMax:
						positionMax = piValue
						maxChoice = dpEntry
				newDpTable.append(maxChoice.transit(tag,sequence[i +1]))
			dpTable = newDpTable
		endingMax = None
		endMaxChoice = None
		for dpEntry in dpTable:
			piValue = dpEntry.probTransmission("__END", None)
			if piValue >= endingMax:
				endingMax = piValue
				endMaxChoice = dpEntry
		endingState = endMaxChoice.transit("__END", None)
		outputs.append(endingState)

	for i in outputs:
		print math.exp(i.logProbability) if not i.logProbability is None else 0