# ToDo

# create highlighting animation over the boxes
# ability to open boxes individually (done!)
# sliding animation for boxes closing and opening (done!)
# after two boxes are open, both close, if they are different, if they are same, they stay open (done!)
# boxes stay open for 10 seconds at the start of the game, so player can memorize (done!)
# win condition (done! maybe, haven't checked, should work in theory)


import pygame 
import random
import sys
import time



# ^^^^^^^^^^
# CONSTANTS
# ^^^^^^^^^^


	#           R    G    B
GRAY  =       (100, 100, 100)
NAVYBLUE = 	  ( 60,  60, 100)
WHITE =    	  (255, 255, 255)
RED =      	  (255,  0,    0)
GREEN =    	  (  0, 255,   0)
BLUE =     	  (  0,   0, 255)
YELLOW =   	  (255, 255,   0)
ORANGE =   	  (255, 128,   0)
PURPLE =   	  (255,   0, 255)
CYAN =     	  ( 0,  255, 255)
HIGHLIGHTER = (255, 255, 100)
SIENNA      = (160,  82,  45)
STEELBLUE   = (119, 136, 153)
TEAL        = (  0, 128, 128)
GREENYELLOW = (173, 255,  47)

BGCOLOR  = STEELBLUE
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = HIGHLIGHTER

DONUT    = "donut"
SQUARE   = "square"
CIRCLE   = "circle"
OVAL     = "oval"
TRIANGLE = "triangle"
DIAMOND  = "diamond"

ALLSHAPECOLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, CYAN, ORANGE, SIENNA]
ALLSHAPES = [DONUT, SQUARE, CIRCLE, OVAL, TRIANGLE, DIAMOND]

FPS = 30
BOXSIZE = 40 # dimensions of a square box that has the icons underneath
GAPSIZE = 10 
WINDOWX = 640 # lenght of window on x axis 
WINDOWY = 480 # length of window on y axis 
BOXCOLUMNS = 7 # no. of boxes that are there vertically
BOXROWS = 10 # no. of boxes that are there horizontally
COVERSPEED = 10 # pixels that the box is covered by per frame

YMARGIN = (WINDOWY - ((BOXSIZE + GAPSIZE)* BOXCOLUMNS)) // 2  # x coords of margin 
XMARGIN = (WINDOWX - ((BOXSIZE + GAPSIZE)* BOXROWS)) // 2     # y coords of margin

# OTHER

fpsClock = pygame.time.Clock()
pygame.init()

# BOOLS & BOOL "STRINGS"

BOARD_REVEAL = True
BOARD_DRAWN = False
GAME_START = False



# ^^^^^^^^^^^
# MAIN LOOP
# ^^^^^^^^^^



def main():
	global DISPLAYSURF, BOARD_REVEAL, GAME_START
	DISPLAYSURF = pygame.display.set_mode((WINDOWX, WINDOWY))
	pygame.display.set_caption('Memory Card')
	
	firstX, firstY = None, None

	while True:
		
		mouseX = 0 # used to store x coordinate of mouse event
		mouseY = 0 # used to store y coordinate of mouse event
		
		if not GAME_START: # starting sequence
			
			DISPLAYSURF.fill(BGCOLOR)
			board = createBoardData()
			drawRevealedBoard(board, BOARD_REVEAL)
			
			fpsClock.tick(FPS)			
			pygame.display.update()
			
			BOARD_REVEAL = False

			pygame.time.wait(3000)
			drawBoard(board, BOARD_REVEAL)

			fpsClock.tick(FPS)
			pygame.display.update()
			
			GAME_START = True
		

		for event in pygame.event.get():
			
			if event.type == 256: # 256 = QUIT
			    pygame.quit()
			    sys.exit()
			
			if event.type == 1025 and event.button == 1: # 1025 = MOUSEBUTTONDOWN
				mouseX, mouseY = event.pos
				
				if getCellFromCoords(mouseX, mouseY, board) != None:
					
					if (firstX , firstY) != (None, None): # if a first box has already been selected
						secondCell = getCellFromCoords(mouseX, mouseY, board)
						firstCell = getCellFromCoords(firstX , firstY, board)
						
						if secondCell == firstCell: # if ur pressing on the same box as the first box pressed out of the two boxes, then we cover the box up again
							getCellFromCoords(mouseX, mouseY, board)[4] = False
							coverBoxesAnimation(firstCell, board)
							(firstX , firstY) = (None, None)
							continue

						else: # the two boxes are not the exact same....as in the box no. is not the exact same though the color and shape might still be the same
							
							if secondCell[0] == firstCell[0] and secondCell[1] == firstCell[1]: # if shape and color are same
								print("same shapes")
								secondCell[4] = True
								uncoverBoxesAnimation(secondCell, board)
								firstCell[5] = "matched"
								secondCell[5] = "matched"
								(firstX , firstY) = (None, None)
								continue
							
							elif secondCell[0] != firstCell[0] or secondCell[1] != firstCell[1]:
								print("different shapes")
								secondCell[4] = True
								uncoverBoxesAnimation(secondCell, board)
								pygame.time.wait(1000)
								firstCell[4] = False
								secondCell[4] = False
								coverBoxesAnimation(firstCell, board)
								coverBoxesAnimation(secondCell, board)								
								(firstX , firstY) = (None, None)
								continue
					
					elif (firstX , firstY) == (None, None):
						
						firstX, firstY = mouseX, mouseY
						getCellFromCoords(mouseX, mouseY, board)[4] = True
						uncoverBoxesAnimation(getCellFromCoords(mouseX, mouseY, board), board)

			if winGame(board):
				GAME_START = True

		fpsClock.tick(FPS)
		pygame.display.update()




# ^^^^^^^^^^^
# DRAWING
# ^^^^^^^^^^



def drawBoard(board, boardRevealed): # function that draws covered boards
	
	global BOXSIZE, DISPLAYSURF, BOXCOLOR

	if not boardRevealed:
		for row in board:
			for cell in row:
				cell[4] = False
				coverBoxesAnimation(cell, board)
	

def drawRevealedBoard(board ,boardRevealed): # function that shows all the pieces
	global DISPLAYSURF
	if boardRevealed:
		for row in board:
			for cell in row:
				cell[4] = True

				drawRevealedPiece(cell, board)
	

def drawRevealedPiece(cell, board): # function that reveals piece that was clicked on
	global DISPLAYSURF
	
	if cell == None:
		return None
	
	coordDict = cell[3]
	color = cell[0]
	shape = cell[1]
	cell[4] = True
	drawShape(shape, color, coordDict, DISPLAYSURF)	


def drawShape(shape, color, coordDict, surface): # function that shows a variety of shapes
	
	quarter = int(BOXSIZE * 0.25)
	half = int(BOXSIZE * 0.5)

	pygame.draw.rect(DISPLAYSURF, BGCOLOR, (coordDict["TL"][0],  coordDict["TL"][1], BOXSIZE, BOXSIZE))

	if shape == SQUARE:
		pygame.draw.rect(surface, color, (coordDict["TL"][0] + quarter,  coordDict["TL"][1] + quarter, half, half))
	if shape == TRIANGLE:
		pygame.draw.polygon( surface, color, ((coordDict["TC"][0], coordDict["TC"][1] + quarter), (coordDict["CL"][0] + quarter, coordDict["CL"][1]),  (coordDict["BC"][0], coordDict["BC"][1] - quarter)))
	if shape == CIRCLE:
		pygame.draw.circle(surface, color, (coordDict["CC"][0], coordDict["CC"][1]), 10)
	if shape == DONUT:
		pygame.draw.circle(surface, color, (coordDict["CC"][0], coordDict["CC"][1]), 10, 5)
	if shape == OVAL:
		ellipseRect = pygame.Rect(coordDict["TL"][0] + quarter,  coordDict["TL"][1], half, BOXSIZE)
		pygame.draw.ellipse(surface, color, ellipseRect)
	if shape == DIAMOND:
		pygame.draw.polygon(surface, color, ((coordDict["TC"][0], coordDict["TC"][1] + quarter), (coordDict["CL"][0] + quarter, coordDict["CL"][1]),  (coordDict["BC"][0], coordDict["BC"][1] - quarter), (coordDict["CR"][0] - quarter, coordDict["CR"][1])))



# ^^^^^^^^^^
# ANIMATIONS
# ^^^^^^^^^^



def coverBoxesAnimation(cell, board):
	print("CLOSING", cell)
	for cover in range(0, BOXSIZE + 1, COVERSPEED):
		if not cell[4] and cell[5] == "unmatched":
			coordDict = cell[3]
			color = cell[0]
			shape = cell[1]
			pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (coordDict["TL"][0],  coordDict["TL"][1], BOXSIZE, cover))				


			fpsClock.tick(FPS)
			pygame.display.update()
			

def uncoverBoxesAnimation(cell, board):
	for cover in range(BOXSIZE, -COVERSPEED, -COVERSPEED):
		if cell[4] and cell[5] == "unmatched":
			drawRevealedPiece(cell, board)
			coordDict = cell[3]
			color = cell[0]
			shape = cell[1]
			pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (coordDict["TL"][0],  coordDict["TL"][1], BOXSIZE, cover))				
		
			fpsClock.tick(FPS)
			pygame.display.update()
	

# ^^^^^^^^^^
# DATA
# ^^^^^^^^^^



def createBoardData(): # creates necessary data for the cell in each row that looks like
					   #      color         shape   boxcoords                                                important coords                                                                                       Reveal  if the box has been matched correctly
  					   # [(119, 136, 153), 'lines',  (0, 0), {'TL': (70, 65), 'TR': (110, 65), 'TC': (90, 65), 'CL': (70, 90), 'CC': (70, 90), 'CR': (70, 90), 'BL': (70, 110), 'BC': (90, 110), 'BR': (110, 110)}, True,   "matched" / "unmatched"]
	global ALLSHAPECOLORS, ALLSHAPES, BOARD_DRAWN

	if not BOARD_DRAWN:
		board = [["" for x in range(0, BOXROWS)] for y in range(0, BOXCOLUMNS)] # creating the 7*10 board
		
		icons = [] # list of (color, shape) tuple 
		
		random.shuffle(ALLSHAPECOLORS)
		random.shuffle(ALLSHAPES)	
		
		for color in ALLSHAPECOLORS[0:7]: # 7 colors for 5 shapes leading to 70 cells filled total with one icon shared for two cells
			for shape in ALLSHAPES[0:5]:
				for i in range(0, 2): # duplicates the icon, so that there are two of them in the list, that can be matched
					icons.append([color, shape])
		
		random.shuffle(icons) # to ensure that the icons are random.
	
		row = 0
		cell = 0
	
		for icon in icons:
			if cell == 10:
				cell = 0
				row += 1
			icon.append((cell, row))
			icon.append(getCoordsFromBox(cell, row))
			icon.append(True)
			icon.append("unmatched")
			
			board[row][cell] = icon
			cell += 1
		
		BOARD_DRAWN = True

		return board
	

def getCoordsFromBox(BOXROW, BOXCOLUMN): # finds all the necessary coords from the box coords

			# (x, y)
	tl = ( XMARGIN + (BOXROW * (BOXSIZE + GAPSIZE)), YMARGIN + (BOXCOLUMN * (BOXSIZE + GAPSIZE)))
	tr = (tl[0] + BOXSIZE, tl[1])
	tc = ((tl[0] + tr[0]) // 2, tl[1])

	bl = (tl[0], tl[1] + BOXSIZE)
	br = (tl[0] + BOXSIZE, tl[1] + BOXSIZE)
	bc = ((bl[0] + br[0]) // 2, tl[1] + BOXSIZE)

	cl = (tc[0], tc[1] + (BOXSIZE // 2))
	cr = (tc[0], tc[1] + (BOXSIZE // 2))
	cc = (tc[0], tc[1] + (BOXSIZE // 2))	
	

		   # T = top, C = center, B = bottom, R = right, L = left 
	return {"TL" : tl , "TR" : tr, "TC" : tc, 
			"CL" : cl,  "CC" : cc, "CR" : cr, 
			"BL" : bl,  "BC" : bc, "BR": br}


def getCellFromCoords(x, y, board): # finds the boxrow and boxcolumn from the coordinates of mouse click
	row = 0
	cell = 0

	boxList = []

	for row in board:
		for cell in row:
			coordDict = cell[3]
			if x in range(coordDict["TL"][0],  coordDict["TL"][0] + BOXSIZE) and y in range(coordDict["TL"][1],  coordDict["TL"][1] + BOXSIZE):
				return cell
	
	return None

def winGame(board):
	for row in board:
		for cell in board:
			if cell[5] == "unmatched":
				return False # no win 
	return True # win 


main()
