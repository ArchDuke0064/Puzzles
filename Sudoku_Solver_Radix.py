# Sudoku_Solver_Radix.py
# Coded in Python by Derek Radix 
# Copyright © 2018.November.12

import copy as c_o_p_y

# global variables
stop, max_depth, depth, round, guess, max_iter = False, 64, 0, 0, 0, 9999
flag = {1:'_1',2:'_2',3:'_3',4:'_4',5:'_5',6:'_6',7:'_7',8:'_8',9:'_9'}
cell_copy = {0:'_v',1:'_1',2:'_2',3:'_3',4:'_4',5:'_5',6:'_6',7:'_7',8:'_8',9:'_9',10:'_g',11:'_t'}
cell = {'_v':-1,'_g':'j','_t':9,'_1':True,'_2':True,'_3':True,'_4':True,'_5':True,'_6':True,'_7':True,'_8':True,'_9':True}
puzzle = [[[c_o_p_y.deepcopy(cell) for y in range(0,9)] for x in range(0,9)] for depth in range(0,max_depth)]
puzzle_data_01 = "0,0,0,0,0,0,2,0,0,0,3,0,0,0,7,0,1,0,6,0,2,0,0,0,5,0,0,0,7,0,0,6,0,0,0,0,0,0,0,1,0,9,0,0,0,0,0,0,0,2,0,0,4,0,0,0,5,0,0,0,6,0,8,0,1,0,4,0,0,0,7,0,0,0,6,0,0,0,0,0,0"

def print_puzzle(puzzle,depth):
	values = [['z' for y in range(0,9)] for x in range(0,9)]
	for y in range(0,9):
		for x in range(0,9):
			if(puzzle[depth][x][y]['_v'] == 0):
				values[x][y]='.' # do not display unknown cell values
			else: # display known cell values
				values[x][y] = str(puzzle[depth][x][y]['_v'])
	for y in range(0,9):
		for x in range(0,9):
			print(str(values[x][y]),end=' ')
		print('')
	print('')

def set_puzzle_groups(puzzle,depth): # Label ('a'...'i') nine 3x3 block groups in puzzle
	for y in range(0,3):
		for x in range(0,3): puzzle[depth][x][y]['_g']='a'
	for y in range(0,3):
		for x in range(3,6): puzzle[depth][x][y]['_g']='b'
	for y in range(0,3):
		for x in range(6,9): puzzle[depth][x][y]['_g']='c'
	for y in range(3,6):
		for x in range(0,3): puzzle[depth][x][y]['_g']='d'
	for y in range(3,6):
		for x in range(3,6): puzzle[depth][x][y]['_g']='e'
	for y in range(3,6):
		for x in range(6,9): puzzle[depth][x][y]['_g']='f'
	for y in range(6,9):
		for x in range(0,3): puzzle[depth][x][y]['_g']='g'
	for y in range(6,9):
		for x in range(3,6): puzzle[depth][x][y]['_g']='h'
	for y in range(6,9):
		for x in range(6,9): puzzle[depth][x][y]['_g']='i'

#puzzle_file = 'p9.csv'
def load_puzzle_file(puzzle,depth,file_name):
	try: # Sudoku puzzle file input format: string variable containing 81 comma-separated digits (0-9), read left to right and top to bottom, zero (0) indicates unknown cell
		file_open = open(file_name,'r') # read-only mode
		file_read = file_open.read()
		file_puzzle = file_read.split(',') # load Sudoku CSV file into array
		for y in range(0,9):
			for x in range(0,9):
				puzzle[depth][x][y]['_v'] = int(file_puzzle[x+9*y]) # load cell values
	except Exception as e:
		print('\nPuzzle load failure, file='+str(file_name))
	finally: file_open.close()

def load_puzzle_data(puzzle,depth,puzzle_data):
	puzzle_input = puzzle_data.split(',') # load Sudoku CSV file into array
	for y in range(0,9):
		for x in range(0,9):
			puzzle[depth][x][y]['_v'] = int(puzzle_input[x+9*y]) # load cell values

def set_flags(puzzle,depth): # set boolean flags for each cell value
	for y in range(0,9):
		for x in range(0,9):
			if(puzzle[depth][x][y]['_v'] > 0): # if cell is known
				if(puzzle[depth][x][y][flag[puzzle[depth][x][y]['_v']]] == False): # if known cell has cleared flag
					puzzle[depth][x][y][flag[puzzle[depth][x][y]['_v']]] = True # then restore flag
				if(puzzle[depth][x][y]['_t'] > 1): # clear all other flags for known cell
					for f in range(1,10):
						if(puzzle[depth][x][y]['_v'] != f): puzzle[depth][x][y][flag[f]] = False
				for yy in range(0,9):
					if(yy != y): # clear column flags
						puzzle[depth][x][yy][flag[puzzle[depth][x][y]['_v']]] = False
				for xx in range(0,9):
					if(xx != x): # clear row flags
						puzzle[depth][xx][y][flag[puzzle[depth][x][y]['_v']]] = False
				for yy in range(0,9):
					for xx in range(0,9):
						if(puzzle[depth][xx][yy]['_g'] == puzzle[depth][x][y]['_g']):
							if((xx != x) and (yy != y)): # clear group flags
								puzzle[depth][xx][yy][flag[puzzle[depth][x][y]['_v']]] = False
	for y in range(0,9):
		for x in range(0,9):
			if(puzzle[depth][x][y]['_t'] > 1):
				t = 0
				for f in range(1,10):
					if(puzzle[depth][x][y][flag[f]] == True):
						t += 1 # set flag total for each unknown cell
				puzzle[depth][x][y]['_t'] = t

def check_invalid(puzzle,depth):
	r,c,g = 0,0,0 # row,column,group
	for y in range(0,9):
		for x in range(0,9):
			if(puzzle[depth][x][y]['_v'] != 0): # ignore unknown cells
				for yy in range(0,9): # same row, different column, duplicate value
						if((yy != y) and (puzzle[depth][x][yy]['_v'] == puzzle[depth][x][y]['_v'])):
							c += 1
				for xx in range(0,9): # different row, same column, duplicate value
						if((xx != x) and (puzzle[depth][xx][y]['_v'] == puzzle[depth][x][y]['_v'])):
							r += 1
				for yy in range(0,9):
					for xx in range(0,9): # duplicate value, same group, row/column not already checked
						if((puzzle[depth][xx][yy]['_v'] == puzzle[depth][x][y]['_v']) and (puzzle[depth][xx][yy]['_g'] == puzzle[depth][x][y]['_g']) and (yy != y) and (xx!=x)):
							g += 1
	return int(r+c+g) # return integer sum of invalid interactions

def count_known_cells(puzzle,depth):
	v = 0
	for y in range(0,9):
		for x in range(0,9):
			if(puzzle[depth][x][y]['_v'] != 0): v += 1
	return v

def test_flag(puzzle,depth):
	for y in range(0,9):
		for x in range(0,9):
			if(puzzle[depth][x][y]['_t'] == 0):
				return True # cell has zero options, invalid puzzle
	return False

def solve_1_iteration(puzzle,depth):
	changes = 0
	set_flags(puzzle,depth)
	if(test_flag(puzzle,depth) == True):
		depth -= 1 ; return -1 # invalid puzzle, go back one level
	if(check_invalid(puzzle,depth) > 0): return -1
	for y in range(0,9):
		for x in range(0,9): # if cell unknown & flag total = 1
			if((puzzle[depth][x][y]['_v'] == 0) and (puzzle[depth][x][y]['_t'] == 1)):
				for f in range(1,10):
					if(puzzle[depth][x][y][flag[f]] == True):
						puzzle[depth][x][y]['_v'] = f # set new cell value
						changes += 1 # increment number of changes
	return changes

def copy_guess(puzzle,depth): # copy guess into next level
	for y in range(0,9):
		for x in range(0,9):
			for c in range(0,12):
				puzzle[depth][x][y][cell_copy[c]] = puzzle[depth-1][x][y][cell_copy[c]]

# initialize
set_puzzle_groups(puzzle,depth)
#load_puzzle_file(puzzle,depth,puzzle_file) # LOAD PUZZLE @ CSV FILE
load_puzzle_data(puzzle,depth,puzzle_data_01) # LOAD PUZZLE @ STRING DATA
set_flags(puzzle,depth)
print('\nInitial puzzle:')
print_puzzle(puzzle,depth)

# solve the puzzle
while((stop == False) and (round <= max_iter)):
	round += 1
	search_done = False
	set_flags(puzzle,depth)
	if(count_known_cells(puzzle,depth) == 81):
		stop = True ; continue # puzzle solved
	changes = solve_1_iteration(puzzle,depth)
	if(changes == -1): # invalid puzzle
		depth -= 1 # go back one level before failed guess
		continue
	elif(changes >= 1): continue
	else: # elif(changes == 0): # make a guess
		guess += 1 ; depth += 1
		copy_guess(puzzle,depth)
		for t in range(2,8): # find cells with fewest options to optimize guessing
			if(search_done == True): break
			for y in range(0,9):
				if(search_done == True): break
				for x in range(0,9):
					if(search_done == True): break
					if(puzzle[depth][x][y]['_t'] == t): # find lowest flag total
						for f in range(1,10):
							if(search_done == True): break
							if(puzzle[depth][x][y][flag[f]] == True): # find first available flag
								puzzle[depth][x][y]['_v'] = f # set guess value
								puzzle[depth-1][x][y][flag[f]] = False # exclude guess in lower puzzle
								search_done = True # stop looking and re-evaluate obvious cell solutions

# display results
if(round <= max_iter): print('\nSudoku puzzle solved:\n'+str(round)+' rounds\n'+str(guess)+' guesses\n')
else: print('\nMaximal iterations exceeded.')
print_puzzle(puzzle,depth)



