import re    
from copy import deepcopy

block_1 = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]
block_2 = [(0,3), (0,4), (0,5), (1,3), (1,4), (1,5), (2,3), (2,4), (2,5)]
block_3 = [(0,6), (0,7), (0,8), (1,6), (1,7), (1,8), (2,6), (2,7), (2,8)]
block_4 = [(3,0), (3,1), (3,2), (4,0), (4,1), (4,2), (5,0), (5,1), (5,2)]
block_5 = [(3,3), (3,4), (3,5), (4,3), (4,4), (4,5), (5,3), (5,4), (5,5)]
block_6 = [(3,6), (3,7), (3,8), (4,6), (4,7), (4,8), (5,6), (5,7), (5,8)]
block_7 = [(6,0), (6,1), (6,2), (7,0), (7,1), (7,2), (8,0), (8,1), (8,2)]
block_8 = [(6,3), (6,4), (6,5), (7,3), (7,4), (7,5), (8,3), (8,4), (8,5)]
block_9 = [(6,6), (6,7), (6,8), (7,6), (7,7), (7,8), (8,6), (8,7), (8,8)]

	
def readSudoku(filename):
	inFile=open(filename, "r")
	sudokuPuzzle = []
	for line in inFile.readlines():
		row = []
		for char in line:
			if char == '\n':
				break
			else:
				row.append(char)
		sudokuPuzzle.append(row)
	return sudokuPuzzle
	
def getDomainMap(sudokuPuzzle):
	varDomain = {}
	for x, y in enumerate(sudokuPuzzle):
		for i,j in enumerate(y):
			variable = (x,i)
			if j == '*':
				varDomain[variable] = [1,2,3,4,5,6,7,8,9]
			else:
				varDomain[variable] = [int(j)]
	return varDomain

def getBlockElements(variable):
	if variable in block_1:
		return block_1
	elif variable in block_2:
		return block_2
	elif variable in block_3:
		return block_3
	elif variable in block_4:
		return block_4
	elif variable in block_5:
		return block_5
	elif variable in block_6:
		return block_6
	elif variable in block_7:
		return block_7
	elif variable in block_8:
		return block_8
	elif variable in block_9:
		return block_9
	
def getConstraintMap(variablesList):
	varConstraint = {}
	for variable in variablesList:
		constraints = []
		row = variable[0]
		col = variable[1]
		for i in range(9):
			constraints.append((row,i))
			constraints.append((i,col))
		blockElements = getBlockElements(variable)
		for x in blockElements:
			if x not in constraints:
				constraints.append(x)
		while variable in constraints:
			constraints.remove(variable)
		varConstraint[variable] = constraints
	return varConstraint
		
def ARCqueue(constraintMap):
	variables = constraintMap.keys()
	ARC_queue = []
	for variable in variables:
		for x in constraintMap[variable]:
			ARC_queue.append([variable,x])
	return ARC_queue
	
def removeInconsistent(ARC, domainMap):
	removed = False
	if len(domainMap[ARC[1]]) == 1:
		for i in domainMap[ARC[0]]:
			if i == domainMap[ARC[1]][0]:
				domainMap[ARC[0]].remove(i)
				removed = True
	return removed
	
def AC3algorithm(arc_queue,constraintMap, domainMap):
	while len(arc_queue) > 0:
		currentARC = arc_queue.pop(0)
		if removeInconsistent(currentARC, domainMap):
			constraintMap[currentARC[0]].remove(currentARC[1])
			for x in constraintMap[currentARC[0]]:
				arc_queue.append([x,currentARC[0]])
				

	
def checkRow(variable, domainMap):
	variableSet = set(domainMap[variable])
	row = variable[0]
	unionList = []
	
	for i in range(9):
		if (row,i) != variable:
			for m,n in enumerate(domainMap[(row,i)]):
				unionList.append(n)
	unionSet = set(unionList)
	
	probableValues = variableSet - unionSet
	if len(probableValues) == 1:
		domainMap[variable] = [list(probableValues)[0]]
		return True
	else: 
		return False
		
def checkCol(variable, domainMap):
	variableSet = set(domainMap[variable])
	col = variable[1]
	unionList = []
	for i in range(9):
		if (i,col) != variable:
			for m,n in enumerate(domainMap[(i,col)]):
				unionList.append(n)
				
	unionSet = set(unionList)
	probableValues = variableSet - unionSet
	if len(probableValues) == 1:
		domainMap[variable] = [list(probableValues)[0]]
		
		return True
	else: 
		return False
		
def checkBlock(variable, domainMap):
	variableSet = set(domainMap[variable])
	unionList = []
	blockElements = getBlockElements(variable)
	for x in blockElements:
		if x != variable:
			for m,n in enumerate(domainMap[x]):
				unionList.append(n)
				
	unionSet = set(unionList)
	probableValues = variableSet - unionSet
	if len(probableValues) == 1:
		domainMap[variable] = [list(probableValues)[0]]
		return True
	else: 
		return False


def isSudokuSolved(domainMap):
	result = True
	keyVariables = domainMap.keys()
	for keyVar in keyVariables:
		if len(domainMap[keyVar]) > 1 or len(domainMap[keyVar]) == 0:
			result = False
			break
	return result
		
def sudokuSolValidate(domainMap, constraintMap):
	validate = True
	keyConstraints = constraintMap.keys()
	for keys in keyConstraints:
		currentVariableValue = domainMap[keys]
		for m in constraintMap[keys]:
			if domainMap[m] == currentVariableValue:
				validate = False
				break
		if validate == False:
			break
	return validate

def printSolution(domainMap):
	result = ''
	resultSudoku = [[0] * 9 for i in range(9)]
	keyVariables = domainMap.keys()
	for keyVar in keyVariables:
		if len(domainMap[keyVar]) > 1:
			result = 'NO SOLUTION FOUND'
			break
		else:
			#print resultSudoku
			try: 
				resultSudoku[keyVar[0]][keyVar[1]] = str(domainMap[keyVar][0])
			except:
				result = 'NO SOLUTION FOUND'	
	if result == 'NO SOLUTION FOUND':
		print 'NO SOLUTION FOUND'
	else:
		for m,n in enumerate(resultSudoku):
			result = result + ''.join(n) + '\n'
		print result
		
	
def solveSudokuAC3(domainMap, arc_queue, constraintMap):
	
	AC3algorithm(arc_queue, constraintMap, domainMap)


def solveSudokuLogical(domainMap, arc_queue, constraintMap):
	solveSudokuAC3(domainMap, arc_queue, constraintMap)
	if not(sudokuSolValidate(domainMap, constraintMap) and isSudokuSolved(domainMap)):
		keyVariables = domainMap.keys()
		while isSudokuSolved(domainMap) == False:
			local_domain_map = deepcopy(domainMap)
			for keyVar in keyVariables:
				if checkRow(keyVar, domainMap):
					arc_queue = ARCqueue(constraintMap)
					AC3algorithm(arc_queue, constraintMap, domainMap)
				if checkCol(keyVar, domainMap):
					arc_queue = ARCqueue(constraintMap)
					AC3algorithm(arc_queue, constraintMap, domainMap)
				if checkBlock(keyVar, domainMap):
					arc_queue = ARCqueue(constraintMap)
					AC3algorithm(arc_queue, constraintMap, domainMap)

			if cmp(local_domain_map,domainMap) == 0:
				break			
	
		
		
def solveSudokuGuess(domainMap, arc_queue, constraintMap):
	solveSudokuLogical(domainMap, arc_queue, constraintMap)
	if not(sudokuSolValidate(domainMap, constraintMap) and isSudokuSolved(domainMap)):
		keyVariables = domainMap.keys()
		for keyVar in keyVariables:

			if len(domainMap[keyVar]) > 1:
				domainValues = deepcopy(domainMap[keyVar])
				temp_backtrace = deepcopy(domainValues)
				for val in domainValues:

					domainMap[keyVar] = [val]
					if not(sudokuSolValidate(domainMap, constraintMap) and isSudokuSolved(domainMap)):
						solveSudokuLogical(domainMap, arc_queue, constraintMap)
						
						if sudokuSolValidate(domainMap, constraintMap) and isSudokuSolved(domainMap) :
							return
						domainMap[keyVar] = temp_backtrace
					else:
						return	
							
	
	
if __name__ == "__main__":
	filename = 'guessing_puzzle'
	sudokuPuzzle = readSudoku(filename)
	domainMap = getDomainMap(sudokuPuzzle)
	variables = domainMap.keys()
	constraintMap = getConstraintMap(variables)
	arc_queue = ARCqueue(constraintMap)
	
	# to call the guess function
	solveSudokuGuess(domainMap, arc_queue, constraintMap)
	printSolution(domainMap)
		