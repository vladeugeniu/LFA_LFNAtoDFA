def getLambdaStar(state):
	""" return the last col of the table ( lambda* )
	"""

	if (state, '.') in transitions:
		tempoList = transitions[(state, '.')]
		if state not in tempoList:
			tempoList = tempoList + [state]
		return tempoList
	else:
		return [state]


def getTable1():
	""" return the first table
	"""

	table1 = transitions
	for state in states:
		table1[state, '.'] = getLambdaStar(state)
	return table1



def getDfaState(state, symbol, table1):
	""" return a new state based on
	NFA state and symbol
	"""

	dfaState = []
	for st in state:	
		if (st, symbol) in table1:
			for s in table1[ (st, symbol) ]:
				dfaState.extend(table1[(s, '.')])	
	return tuple(set(dfaState))



def createDfa():
	""" create the DFA based on input
	"""

	table1 = getTable1()
	stateList = [(initState,)]
	table2 = {}
	for state in stateList:	
		for symbol in symbols:
			tempState = getDfaState(state, symbol, table1)
			if tempState is not ():
				table2[(state, symbol)] = getDfaState(state, symbol, table1)
				if table2[(state, symbol)] not in stateList:
					stateList.append(table2[(state, symbol)])	
	dfaInit = initState
	dfaFinalState = [x[0] for x in table2 if (set(finalStates)&set(x[0]))]	
	g = open('dfa','w')
	toWrite = "init " + str(dfaInit) + '\n'
	g.write(toWrite)
	toWrite = "final states: " + str(list(set(dfaFinalState))) + '\n'
	g.write(toWrite)
	g.write("transitions:\n")
	for key,info in table2.iteritems():
		toWrite = str(key) + " = " + str(info) + '\n'
		g.write(toWrite)

f = open("nfa", "r")
nrStates = int(f.readline())
states = f.readline().rstrip('\n').split()
nrSymbls = int(f.readline())
symbols = f.readline().rstrip('\n').split()
initState = f.readline().rstrip('\n')
nrFinalStates = int(f.readline())
finalStates = f.readline().rstrip('\n').split()
nrTransitions = int(f.readline())
transitions = {}
for line in f:
	trans = line.strip('\n').split()
	if (trans[0],trans[1]) in transitions:
		transitions[(trans[0],trans[1])].append(trans[2])
	else:
		transitions[(trans[0],trans[1])]=[trans[2]] 
createDfa()
