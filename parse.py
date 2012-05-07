import jsonrpc
import json
import sys
from simplejson import loads
server = jsonrpc.ServerProxy(jsonrpc.JsonRpc20(),
        jsonrpc.TransportTcpIp(addr=('127.0.0.1', 8080)))

# Print Error message and quit
def error(message):
	print 'Error:', message
	sys.exit()

# Find the word entry corresponding to a given word
def findWord(word):
	for i in result[s]['words']:
		if i[0] == word:
			return i
	return None

# Find the first instance of a dependency relation of a given type
def findFirstRel(relType):
	for i in result[s]['tuples']:
		if i[0] == relType:
			return i
	return None

# Find the dependent in first instance of a dependency relation of a given type and all modifiers
def findFirstRelGovAndMods(relType):
	rel = findFirstRel(relType)
	if rel is not None:
		dep = findWord(rel[2])
		dep.append(findAllRelDeps('amod', dep[0]))
		return dep
	return None

# Find all instances of a dependency relation of a given type
def findAllRels(relType):
	rels = []
	for i in result[s]['tuples']:
		if i[0] == relType:
			rels.append(i)
	return rels

# Finds the dependents in all instances of a given dependency relation with a given governer
def findAllRelDeps(relType, gov):
	rels = findAllRels(relType, gov)
	if rels is not None:
		for idx, val in enumerate(rels):
			rels[idx] = findWord(val[2])[1]['Lemma']
	return rels

# Find all instances of a dependency relation of a given type with a given govener
def findAllRels(relType, gov):
	rels = []
	for i in result[s]['tuples']:
		if i[0] == relType and i[1] == gov:
			rels.append(i)
	return rels

# Find all the prepositions
def findPreps():
	preps = {}
	for i in result[s]['tuples']:
		if 'prep' in i[0]:
			preps[i[0][5:]] = findWord(i[2])
			preps[i[0][5:]].append(findAllRelDeps('amod', i[2]))
	return preps
	
# Order the adjectives from global to non-global
def orderAdjectives(adj):	
	adjDict = {}
	for a in adj:
		(before, sep, after) = a.partition('-')
		if after != '':
			if before in adjDict:
				error('Multiple adjectives of the same type')
			adjDict[before] = after
		#else:
		#	print 'ignoring adjective - ', before

	adjList = []
	if 'c' in adjDict:
		if adjDict['c'] == 'bad':
			error('I don\'t understand that color')
		adjList.append(adjDict['c'])
	if 's' in adjDict:
		adjList.append(adjDict['s'])
	if 'f' in adjDict:
		adjList.append(adjDict['f'])

	return adjList
			
# Print a filter command
def printFilter(command):
	print 'filter', command


# Load the json data
result = json.loads(server.parse(sys.argv[1]));

# Enumerate through all of the sentences.
for s, val in enumerate(result):
	# Find the Root of the sentence
	root = findWord(findFirstRel('root')[2])
	if root is None:
		error("No root.")

	# find the Direct Object and its modifiers
	dobj = findFirstRelGovAndMods('dobj')

	# find the Prepositions and their modifiers
	preps = findPreps()

	# Print Prepositions and their modifiers
	# To add more sentence types simply add the prepositions associated below
	if 'to' in preps and 'of' in preps:
		printFilter(preps['of'][1]['Lemma'])
		for adj in orderAdjectives(preps['of'][2]):
			printFilter(adj)
		print 'remember'
		printFilter(preps['to'][1]['Lemma'])
	elif 'to' in preps:
		printFilter(preps['to'][1]['Lemma'])
		for adj in orderAdjectives(preps['to'][2]):
			printFilter(adj)

	if 'at' in preps:
		printFilter(preps['at'][1]['Lemma'])
		for adj in orderAdjectives(preps['at'][2]):
			printFilter(adj)

	# Print the Direct Object and its modifiers if it exists
	if dobj is not None:
		printFilter(dobj[1]['Lemma'])
		for adj in orderAdjectives(dobj[2]):
			printFilter(adj)

	# If the root is 'go' print out the first 'to' clause
	if root[1]['Lemma'] == 'go':
		prep_to = findFirstRelGovAndMods('prep_to')
		if prep_to is not None and prep_to[0] != preps['to'][0]:
			printFilter(prep_to[1]['Lemma'])
			for adj in orderAdjectives(prep_to[2]):
				printFilter(adj)

	# Print the root of the sentence (the verb)
	print root[1]['Lemma']

