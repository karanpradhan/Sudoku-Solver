import numpy as np
import Queue
import sys
import copy

def init_sudoku(f):
	a = ''
	y=0
	a = f.read()
	l = a.split('\n')	
	l.pop()
	sudoku = np.zeros((9,9))
	for i,ele in enumerate(l):
		for j in range(9):
			if ele[j] == '*':
				sudoku[i][j] = 0
			else:
				sudoku[i][j] = int(ele[j])
	return sudoku		

def get_feasible_values(domains,i,j):
	feasible=set([1,2,3,4,5,6,7,8,9])
	x=[]
	x.append(sudoku[i][j])
	#feasible = feasible - set(x)
	rows = []
	for itr in range(9):
		if itr!=i:
			rows.append(domains[(itr,j)])
	rows = set(rows) 
	feasible = feasible - rows
	cols=[]
	for itr in range(9):
		if itr!=j:
			cols.append(domains[(i,itr)])
	cols = set(cols)
	feasible = feasible - cols
	x_s,y_s,x_e,y_e = get_region_limits(i,j)
	region=[]
	for x in range(x_s,x_e+1):
		for y in range(y_s,y_e+1):
			if x==i and y==j:
				pass
			else:
				region.append(domains[(x,y)])
	region = set(region)
	feasible =  feasible -region
	return feasible	
			
def get_region_limits(i,j):
	if i<=2 :
		x_start = 0
	elif i<=5 and i>2 :
		x_start = 3
	else :
		x_start = 6
	if j<=2 :
		y_start = 0
	elif j<=5 and j>2 :
		y_start = 3
	else :
		y_start = 6	
	return x_start,y_start,x_start+2,y_start+2		

def get_neighbours(sudoku,i,j):
	neigh = [] 
	for x in range(9):
		if i!=x :
			neigh.append((x,j))
	for y in range(9):
		if j!=y :
			neigh.append((i,y))		

	xs,ys,xe,ye = get_region_limits(i,j)
	for x in range(xs,xe+1):
		for y in range(ys,ye+1):
			if x!=i and y!=j :
				neigh.append((x,y))
	return list(set(neigh))			
	
def construct_queue(sudoku):
	queue = []
	for i in range(9):
		for j in range(9):
			l = get_neighbours(sudoku,i,j)	
			queue.extend((((i,j),k) for k in l))
	

	queue = list(set(queue))	
	return queue	

def construct_domains(sudoku):
	domains = {}
	for i in range(9):
		for j in range(9):
			if sudoku[i][j] == 0:
				domains[(i,j)] = {1,2,3,4,5,6,7,8,9}		
			else:
				temp = int(sudoku[i][j])
				l=[]
				l.append(temp)
				domains[(i,j)] = set(l)
	return domains			

def remove_inconsistent_values(domains,xi,xj):
	removed = False
	d1 = domains[xi]
	d2 = domains[xj]
	if len(d1) == 1:
		return False
	d1 = list(d1)
	d2 = list(d2)
	for i in d1 :
		if i in d2 and len(d2) == 1:
			d1.pop(d1.index(i))
			domains[xi] = set(d1)
			removed = True
	return removed
			

def ac3(sudoku,queue,domains):
	while len(queue) > 0:
		xi,xj = queue.pop(0)
		if remove_inconsistent_values(domains,xi,xj):
			temp = []
			temp.append(xj)
			temp=set(temp)
			neigh = set(get_neighbours(sudoku,xi[0],xi[1]))
			neigh = list(neigh)
			for xk in neigh:
				if (xk,xi) not in queue:
					queue.append((xk,xi))		
	return

def print_solution(domains):
	a = np.zeros((9,9))
	solution = True
	for i in domains.keys():
		if len(list(domains[i])) == 1:		
			a[i[0]][i[1]] = list(domains[i])[0]
		else :
			solution = False	
	if solution :
		for i in range(9):
			for j in range(9):
				sys.stdout.write(str(int(a[i][j])))
			print ""		
	else:
		print "No solution"	

def solved(domains):
	solution = True
	for i in domains.keys():
		if len(list(domains[i])) == 1:		
			solution = True
		else :
			return False
	if solution :
		return validate(domains)	

def validate(domains):
	flag = True
	test = {1,2,3,4,5,6,7,8,9}
	for x,y in domains.keys():
		rowtest = set([])
		for k in range(9):
			rowtest = rowtest|domains[(x,k)]
		if rowtest != test:
			return False
		coltest = set([])

		for k in range(9):
			coltest = coltest|domains[(k,y)]
		if coltest != test:
			return False			
		xs,ys,xe,ye = get_region_limits(x,y)
		grid = set([])
		 
		for i in range(xs,xe+1):
			for j in range(ys,ye+1):
				grid = grid | domains[(i,j)]
		if grid != test:
			return False		
	return True		



def row_check(domains,coord):
	value_set = domains[coord]
	#print "value set"
	#print value_set
	myset = set()
	for i,j in domains.keys():
		if i == coord[0] and j!=coord[1]:
			myset = myset | domains[(i,j)]
	temp = value_set - myset
	#print temp
	if len(temp) == 1:
		domains[coord] = temp
		return True
	else:
		return False

def column_check(domains,coord):
	value_set = domains[coord]
	#print "value set"
	#print value_set
	myset = set()
	for i,j in domains.keys():
		if j == coord[1] and i!=coord[0]:
			myset = myset | domains[(i,j)]
	temp = value_set - myset
	#print temp
	if len(temp) == 1:
		domains[coord] = temp
		return True
	else:
		return False

def grid_check(domains,coord):
	value_set = domains[coord]
	xs,ys,xe,ye = get_region_limits(coord[0],coord[1])
	myset = set()
	for i in range(xs,xe+1):
		for j in range(ys,ye+1):
			if i == coord[0] and j == coord[1] :
				continue
			else :
				#print i,j
				myset = myset |	domains[(i,j)]
	temp = value_set - myset
	if len(temp) == 1:
		domains[coord]= temp
		return True
	else:
		return False

def logical_sudoku(sudoku,queue,domains):
	ac3(sudoku,queue,domains)
	while not(solved(domains)):
		prev = copy.deepcopy(domains)
		for i in range(9):
			for j in range(9):
				if len(domains[(i,j)]) > 1:
					if row_check(domains,(i,j)):
						queue = construct_queue(sudoku)
						ac3(sudoku,queue,domains)	
					if column_check(domains,(i,j)):
						queue = construct_queue(sudoku)
						ac3(sudoku,queue,domains)
					if grid_check(domains,(i,j)):
						queue = construct_queue(sudoku)
						ac3(sudoku,queue,domains)
		if prev == domains :
			return						
	return 	

def compare_domains(domain1,domain2):
	for x,y in zip(domain1.iteritems(),domain2.iteritems()):
		if x == y :
			pass
		else:
			return False
	return True			


def diabolical_sudoku(sudoku,queue,domains):
	if not(solved(domains)):
		logical_sudoku(sudoku,queue,domains)
	if not(solved(domains)):
		for i in range(9):
			for j in range(9):
				if len(domains[(i,j)]) > 1:
					feasible = copy.deepcopy(domains[(i,j)])
					temp = copy.deepcopy(feasible)
					for f in feasible:
						domains[(i,j)] = set([f])
						if not(solved(domains)):
							
							logical_sudoku(sudoku,queue,domains)
							if(solved(domains)):
								return
							domains[(i,j)] = temp	
						else: 
							return	


	return

if __name__ == "__main__":
	f = open('dp_puzzle')
	a=init_sudoku(f)
	#print a
	#print get_neighbours(a,0,0)
	domains = construct_domains(a)
	#print domains
	#print domains[(5,0)]
	#print grid_check(domains,(5,0))
	#print domains[(0,0)]
	#print remove_inconsistent_values(domains,(1,0),(0,0))
	#print domains[(1,0)]
	#print domains[(0,0)]	
	queue = construct_queue(a)
	#print "..."
	#print queue
	#print domains[(1,0)]
	#print queue
	#ac3(a,queue,domains)
	#ac3(a,queue,domains)
	#print_solution(domains)
	#print solved(domains)
	#print domains
	#print get_region_limits(4,1)
	print "dp puzzle"
	logical_sudoku(a,queue,domains)
	#a = {1:3,2:4}
	#b = a
	#b[1] = 4
	#print compare_domains(a,b)
	print_solution(domains)

	print "guessing puzzle"

	f = open('diabolical_sudoku')
	a=init_sudoku(f)
	#print a
	#print get_neighbours(a,0,0)
	domains = construct_domains(a)
	#print domains
	#print domains[(5,0)]
	#print grid_check(domains,(5,0))
	#print domains[(0,0)]
	#print remove_inconsistent_values(domains,(1,0),(0,0))
	#print domains[(1,0)]
	#print domains[(0,0)]	
	queue = construct_queue(a)
	#print "..."
	#print queue
	#print domains[(1,0)]
	#print queue
	#ac3(a,queue,domains)
	#ac3(a,queue,domains)
	#print_solution(domains)
	#print solved(domains)
	#print domains
	diabolical_sudoku(a,queue,domains)
	print_solution(domains)
	