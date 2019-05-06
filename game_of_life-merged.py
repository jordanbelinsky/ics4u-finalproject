# Import #
import pygame
import random
import pygame.midi

# Rules #
rules = '''
        1. Any live cell with fewer than two live neighbours dies, as if caused by under-population.
        2. Any live cell with two or three live neighbours lives on to the next generation.
        3. Any live cell with more than three live neighbours dies, as if by overcrowding.
        4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
        '''

# General Variables #
gridSize = 100
size = 10
FPS = 100
WIDTH,HEIGHT = 1000,800
generation = 0
count = 0

# Define 2D List for Board #
board = [[False for i in range(gridSize)] for j in range(gridSize)]

# Colors #
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (211, 211, 211)
coolGrey = (130,130,130)
RED = (255,0,0)

# States #
rules = False
rules_2 = False
main_game = True

# Pygame Initialization #
pygame.init()
pygame.midi.init()

# MIDI Initialization #
player = pygame.midi.Output(0)
player.set_instrument(120)

# Pygame Display Variables #
font = pygame.font.SysFont("Ariel Black", 30)
typeFont = pygame.font.SysFont("Ariel Black", 20)
header = pygame.font.SysFont("Ariel Black", 38) 
screen = pygame.display.set_mode((WIDTH,HEIGHT))                        # define the surface for the simulation to run on
pygame.display.set_caption('Conway\'s Game of Life')
smallglider_text = font.render('Small Glider', False, (0, 0, 0))
smallexploder_text = font.render('Small Exploder', False, (0, 0, 0))
spaceship_text = font.render('Spaceship', False, (0, 0, 0))
tumbler_text = font.render('Tumbler', False, (0, 0, 0))
rules_text = font.render('Rules', False, (0, 0, 0))
screen.fill(WHITE) # Fill the screen white
pygame.display.update()
clock = pygame.time.Clock()

# Custom Shape Variables #
saveShapeText = ''
loadShapeText = ''
name = ''
saveShapeBool = False
saveTypeBox = pygame.Rect(450, 450, 100, 50)
loadShapeBool = False
loadTypeBox = pygame.Rect(450, 450, 100, 50)
typing = False
initialCoord = None                             # coordinates for drag&drop
timer=0

# Side Menu Variables # 
extendo = False                                 # side menu starts closed
currentShape = -1                               # current shape on mouse starts as nothing

# Preset Shape Preview #
def drawTempRect(row,col):
    pygame.draw.rect(screen, coolGrey, (row*10, col*10, 10, 10), 0)

# Preset Shape Class #
class Shape(object):
    def __init__(self, shapelist):
        self.shapelist = shapelist

    def rotate(self):
        list_of_tuples = zip(*self.shapelist[::-1])
        rotatedShape = [list(i) for i in list_of_tuples]
        self.shapelist = rotatedShape
    def drawtempShape(self,row,col):
        for i in range(len(self.shapelist)):
            for j in range(len(self.shapelist[0])):
                if self.shapelist[i][j]:
                    drawTempRect(row-j,col-i)
                    
    def addShape(self,row,col):
        for i in range(len(self.shapelist)):
            for j in range(len(self.shapelist[0])):
                if self.shapelist[i][j]:
                    giveLife(row-j,col-i)

# Preset Shape Tuples #
smallglider = Shape([[False,True,False],
                     [False,False,True],
                     [True,True,True]])

smallexploder = Shape([[False,True,False],
                       [True,True,True],
                       [True,False,True],
                       [False,True,False]])

spaceship = Shape([[False,True,True,True,True],
                   [True,False,False,False,True],
                   [False,False,False,False,True],
                   [True,False,False,True,False]])

tumbler = Shape([[False,True,True,False,True,True,False],
                 [False,True,True,False,True,True,False],
                 [False,False,True,False,True,False,False],
                 [True,False,True,False,True,False,True],
                 [True,False,True,False,True,False,True],
                 [True,True,False,False,False,True,True]])

# Preset Shape List #       
allShapes = [smallglider, smallexploder, spaceship, tumbler]

# Track Mouse Position #
def mousePos():
    x, y = pygame.mouse.get_pos()
    return (x//10, y//10)

# Determine Living Neighbors #
def findNeighbors(row, column):
    alive = 0
    # Horizontally Adjacent #
    if row > 0:
        if board[row-1][column]:
            alive += 1
    if column > 0:
        if board[row][column-1]:
            alive += 1
    if row < gridSize-1:
        if board[row+1][column]:
            alive += 1
    if column < gridSize-1:
        if board[row][column+1]:
            alive += 1
    # Diagonally Adjacent #
    if row > 0 and column > 0:
        if board[row-1][column-1]:
            alive += 1
    if row < gridSize-1 and column < gridSize-1:
        if board[row+1][column+1]:
            alive += 1
    if row > 0 and column < gridSize-1:
        if board[row-1][column+1]:
            alive += 1
    if row < gridSize-1 and column > 0:
        if board[row+1][column-1]:
            alive += 1
    # Return Final Count #
    return alive

# Activate a Grid Cell #
def giveLife(row, col):
    board[row][col] = True

# Invert Tuples to Rotate Shape #
def rotateShape(shapelist):
    list_of_tuples = zip(*shapelist[::-1])
    return [list(i) for i in list_of_tuples]

# Deactivate a Grid Cell #
def killRuthlessly(row, col):
    board[row][col] = False

# Draw Current Shape Tuple #
def drawcurrentshape(row,col,currentShape):
    allShapes[currentShape].drawtempShape(row,col)
    if click[0]:
        allShapes[currentShape].addShape(row,col)
        killRuthlessly(row,col)
    if click[1]:
        allShapes[currentShape].rotate()
        pygame.time.delay(40)

# Verify Click Interaction with GUI #
def checkGui(mouseX,mouseY):
    global extendo, currentShape, rules, main_game
    # mouseX and mouseY numbers are 1/10 of actual pixel size #
    if (mouseX > 97 and mouseY > 40 and mouseY < 49):
        extendo = True
    if extendo == True:
        if (mouseX > 82 and mouseX < 98 and mouseY > 5 and mouseY < 13):
            currentShape = 0
        if (mouseX > 82 and mouseX < 98 and mouseY > 16.5 and mouseY < 24.5):
            currentShape = 1
        if (mouseX > 82 and mouseX < 98 and mouseY > 28 and mouseY < 36):
            currentShape = 2
        if (mouseX > 82 and mouseX < 98 and mouseY > 39.5 and mouseY < 47.5):
            currentShape = 3
        if (mouseX > 82 and mouseX < 98 and mouseY > 69 and mouseY < 77):
            rules = True
            run = False
        if mouseX > 77:
            killRuthlessly(mouseX,mouseY)
        if mouseX > 77 and mouseX < 80 and mouseY > 40 and mouseY < 49:
            extendo = False

# Display GUI Elements on Screen #
def drawGui():
    global extendo

    # Side Menu GUI #
    if extendo == True:
        pygame.draw.rect(screen, coolGrey, (800, 0, 200, HEIGHT), 0)
        pygame.draw.rect(screen, BLACK, (800, 1, 199, HEIGHT-2), 3)
        pygame.draw.rect(screen, WHITE, (820, 50, 160, 80), 0)                                # small glider
        pygame.draw.rect(screen, WHITE, (820, 165, 160, 80), 0)                               # small exploder
        pygame.draw.rect(screen, WHITE, (820, 280, 160, 80), 0)                               # spaceship
        pygame.draw.rect(screen, WHITE, (820, 395, 160, 80), 0)                               # tumbler
        pygame.draw.rect(screen, WHITE, (820, 690, 160, 80), 0)                               # rules
        pygame.draw.rect(screen, BLACK, (777, 402, 24, 86), 0)
        pygame.draw.rect(screen, coolGrey, (780, 405, 19, 80), 0)
        pygame.draw.polygon(screen, WHITE, [(785, 419), (785, 429), (795, 424)], 0)
        pygame.draw.polygon(screen, WHITE, [(785, 439), (785, 449), (795, 444)], 0)
        pygame.draw.polygon(screen, WHITE, [(785, 459), (785, 469), (795, 464)], 0)
        screen.blit(smallglider_text, (820, 25))                                  # small glider
        screen.blit(smallexploder_text, (820, 140))                               # small exploder
        screen.blit(spaceship_text, (820, 255))                                   # spaceship
        screen.blit(tumbler_text, (820, 370))                                     # tumblerr
        screen.blit(rules_text, (870, 720))
        
    # General GUI #
    else:
        pygame.draw.rect(screen, BLACK, (980, 405, 50, 80), 3)
        pygame.draw.rect(screen, coolGrey, (980, 405, 50, 80), 0)
        pygame.draw.polygon(screen, WHITE, [(995, 419), (995, 429), (985, 424)], 0)
        pygame.draw.polygon(screen ,WHITE, [(995, 439), (995, 449), (985, 444)], 0)
        pygame.draw.polygon(screen, WHITE, [(995, 459), (995, 469), (985, 464)], 0)

# Display Text #
def drawText(message,text_X,text_Y):
    text = font.render(message, 1, BLACK)                               # put the font and the message together
    screen.blit(text,(text_X,text_Y))

# Display First Rules Page #
def draw_rules_page_one():
    title = header.render("Conway's Game Of Life", 1, BLACK)
    description_1 = font.render('This is a game where you draw set patterns of squares on the screen,', 1, BLACK)
    description_2 = font.render('which are then animated and react to the rules below, forming a living ecosystem.', 1, BLACK) 
    rule_1 = font.render('1. Any live cell with fewer than two live neighbours dies, as if caused by under-population.', 1, BLACK)
    rule_2 = font.render('2. Any live cell with two or three live neighbours lives on to the next generation.', 1, BLACK)
    rule_3 = font.render('3. Any live cell with more than three live neighbours dies, as if by overcrowding.', 1, BLACK)
    rule_4 = font.render('4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.', 1, BLACK)
    names = font.render('By: Jordan Belinsky, Ritchie DiMaria, Alex Giannoulis, and Jeremy Weisberg', 1, BLACK)
    escape =  font.render('Press E to return to the main game', 1, BLACK)
    screen.blit(title, (350, 50))
    screen.blit(description_1, (150, 125))
    screen.blit(description_2, (95, 175))
    screen.blit(rule_1, (50, 275))
    screen.blit(rule_2, (100, 340))
    screen.blit(rule_3, (100, 415))
    screen.blit(rule_4, (50, 490))
    screen.blit(names, (105, 585))
    screen.blit(escape, (335, 700))
    pygame.draw.rect(screen, BLACK, (380,750,100,30), 0)
    pygame.draw.rect(screen, coolGrey, (530,750,100,30), 0)

# Display Second Rules Page #
def draw_rules_page_two():
    title = header.render("Conway's Game Of Life", 1, BLACK)
    description_1 = font.render('This is a game where you draw set patterns of squares on the screen,', 1, BLACK)
    description_2 = font.render('which are then animated and react to the rules below, forming a living ecosystem.', 1, BLACK)
    key_title = font.render('Keyboard Shortcuts:', 1, BLACK)
    key_space = font.render('Space: Start/Pause Game', 1, BLACK)
    key_s = font.render('S: Save Map', 1, BLACK)
    key_l = font.render('L: Load Map', 1, BLACK)
    key_f = font.render('F: Enable/Disable Drag Select', 1, BLACK)
    key_k = font.render('K: Load Shape', 1, BLACK)
    key_r = font.render('R: Random Map', 1, BLACK)
    key_c = font.render('C: Clear Map', 1, BLACK)
    key_right = font.render('Right Arrow: Fast Forward', 1, BLACK)
    escape =  font.render('Press E to return to the main game', 1, BLACK)
    screen.blit(title, (350, 50))
    screen.blit(description_1, (150, 125))
    screen.blit(description_2, (95, 175))
    screen.blit(key_title, (400, 275))
    screen.blit(key_space, (380, 320))
    screen.blit(key_s, (440, 355))
    screen.blit(key_l, (440, 390))
    screen.blit(key_f, (355, 425))
    screen.blit(key_k, (435, 460))
    screen.blit(key_r, (435, 495))
    screen.blit(key_c, (440, 530))
    screen.blit(key_right, (375, 565))
    screen.blit(escape, (335, 700))
    pygame.draw.rect(screen, coolGrey, (380,750,100,30), 0)
    pygame.draw.rect(screen, BLACK, (530,750,100,30), 0)

# Draw Background Grid #
def draw_grid():
    # Horizontal #
    for i in range(0,WIDTH,size):
        pygame.draw.line(screen,GREY,(i,0),(i,HEIGHT),1)
    # Vertical #
    for i in range(0,HEIGHT,size):
        pygame.draw.line(screen,GREY,(0,i),(WIDTH,i),1)

# Save Current Grid #
def save_grid():
    if run == False:
        #name=input("Enter the name of the file you want to save")
        file_out = open('map','w')
        for i in range(len(board)):
            for j in range(len(board[i])):
                file_out.write(str(board[i][j])+' ')
            file_out.write('\n')
        file_out.close()

# Load a Previously Saved Grid #
def load_grid():
    if run == False:
        #fname=input("Enter the filename of the map you'd like to open")
        newlst=[]
        file_in = open('map','r')
        lines = file_in.readlines()
        for line in lines:
            line = line.split()
            newlst.append([True if word == 'True' else False for word in line])
        file_in.close()
        return newlst

# Display Background for Drag & Drop #
def dragdrop(inital,x,y):
    startx,starty = inital
    pygame.draw.polygon(screen,RED,((startx*10, starty*10),(startx*10,y*10),(x*10,y*10),(x*10,starty*10)),3)

# Save Contents of Drag & Drop #
def save_shape(name,startx,starty,x,y):
    print('*'*100)
    file_out = open(name,'w')
    for i in range(len(board)):
        for j in range(len(board[i])):
            if (starty <= j <= y) and (startx <= i <= x):
                file_out.write(str(board[i][j])+' ')
        file_out.write('\n')
    file_out.close()

# Load a Previously Saved Shape #
def load_shape(name):
    newlst = []
    file_in = open(name,'r')
    lines = file_in.readlines()
    for line in lines:
        line = line.split()
        newlst.append([True if word == 'True' else False for word in line])
    file_in.close()
    list2=[x for x in newlst if x!= []]
    return list2

# Main Variables #
genCount = 0
mouse_mode = True
run = False

# Main Loop #
while main_game == True:
    mouseX,mouseY = mousePos()

    # Draw Board as Rectangles #
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col]:
                pygame.draw.rect(screen, BLACK, (row*10,col*10,size,size),0)
            if not board[row][col]:
                pygame.draw.rect(screen, WHITE, (row*10,col*10,size,size),0)
                
    # Process Events #          
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        if event.type == pygame.KEYDOWN:
                
            # When User is Typing for Saving #
            if typing == True:
                if loadShapeBool:
                    name = loadShapeText
                if saveShapeBool:
                    name = saveShapeText
                if event.unicode.isalpha() or event.unicode.isdigit():
                    name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    typing = False
                if loadShapeBool:
                    loadShapeText = name 
                if saveShapeBool:
                    saveShapeText = name
                
            # When User is Not Typing for Saving #
            if typing == False: 
                        
                # Quit #
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    break
                        
                # Play/Pause Game #
                if event.key == pygame.K_SPACE:
                    run = not run
                
                # Save Grid #
                if event.key == pygame.K_s:
                    save_grid()
                
                # Load Grid #
                if event.key == pygame.K_l:
                    newlst = load_grid()
                    board=newlst
                        
                # Toggle Drag & Drop Mode #
                if event.key == pygame.K_f:
                    mouse_mode = not mouse_mode
                
                # Load Shape #
                if event.key == pygame.K_k:
                    loadShapeBool = True
                    typing = True
                        
                # Rules Page 1 #
                if rules:
                    if event.key == pygame.K_RIGHT:
                        rules = False
                        rules_2 = True
                    if event.key == pygame.K_e:
                        rules = False
                        run = False
                        
                # Rules Page 2 #
                if rules_2:
                    if event.key == pygame.K_LEFT:
                        rules = True
                        rules_2 = False
                    if event.key == pygame.K_e:
                        rules_2 = False
                        run = False
                        
                # Fast Forward Generations #
                if event.key == pygame.K_RIGHT:
                    for x in range(1):
                            tempboard = [[False for i in range(gridSize)] for j in range(gridSize)]
                            for row in range(len(board)):
                                for col in range(len(board)):
                                    neighborcount = findNeighbors(row, col)
                                    if board[row][col]:                                 # any live cell
                                        if neighborcount < 2:
                                            tempboard[row][col] = False                 # dies
                                        if neighborcount > 3:                           # with more than three live neighbors
                                            tempboard[row][col] = False                 # dies
                                        if neighborcount == 2 or neighborcount == 3:
                                            tempboard[row][col] = True                  # lives on to the next generation 
                                    elif not board[row][col]:                           # any dead cell
                                        if neighborcount == 3:                          # with exactly three live neighbors
                                            tempboard[row][col] = True                  # becomes a live cell
                                    if board[row][col] == False and tempboard[row][col]:
                                        player.note_on(row+5, 75)
                            board = tempboard
                            generation += 1
                            run = False     
  
                # Clear Grid #
                if event.key == pygame.K_c:
                    if run == True:
                        run = not run
                    generation = 0
                    board = [[False for i in range(gridSize)] for j in range(gridSize)]
                        
                # Random Grid #
                if event.key == pygame.K_r:
                    generation = 0
                    possibilities = [False, False, True]
                    for row in range(gridSize):
                        for col in range(gridSize):
                            board[row][col] = random.choice(possibilities)
                   
    # General Rule Assignment #
    if run:
        tempboard = [[False for i in range(gridSize)] for j in range(gridSize)]
        for row in range(len(board)):
            for col in range(len(board)):
                neighborcount = findNeighbors(row, col)
                if board[row][col]:                                     # any live cell
                    if neighborcount < 2:
                        tempboard[row][col] = False                     # dies
                    if neighborcount > 3:                               # with more than three live neighbors
                        tempboard[row][col] = False                     # dies
                    if neighborcount == 2 or neighborcount == 3:
                        tempboard[row][col] = True                      # lives on to the next generation 
                elif not board[row][col]:                               # any dead cell
                    if neighborcount == 3:                              # with exactly three live neighbors
                        tempboard[row][col] = True                      # becomes a live cell
                if board[row][col] == False and tempboard[row][col] == True:
                    player.note_on(row+5, 75)
        board = tempboard
        generation += 1
        genCount = 1
    
    # Process Click for Main Game #
    click = pygame.mouse.get_pressed()
    if mouse_mode:
                
        # Left Click #
        if click[0]:
            mouseX,mouseY = mousePos()
            board[mouseX][mouseY] = True
            checkGui(mouseX,mouseY)
            if not run:
                generation = 0
                
        # Right Click #
        if click[2]:
            mouseX,mouseY = mousePos()
            board[mouseX][mouseY] = False
            currentShape = -1
            if not run:
                generation = 0
                
    # Pocess Click for Drag & Drop #
    if not mouse_mode:
                
        # Left Click #
        if click[0]:
            mouseX,mouseY = mousePos()
            if initialCoord == None:
                initialCoord = (mouseX,mouseY)
            dragdrop(initialCoord,mouseX,mouseY)
        
        # Middle or Right Click #
        else:
            if initialCoord != None:
                saveShapeBool = True
                typing = True
                run = False
                print(saveShapeBool,typing)
                initialCoord2 = initialCoord
                initialCoord = None
    
    # Process Saving Shape #
    if saveShapeBool == True and typing == False:
        run = False
        startx,starty = initialCoord2
        save_shape(saveShapeText,startx,starty,mouseX,mouseY)
        saveShapeBool = False
        run = False
    
    # Process Loading Shape #
    if loadShapeBool == True and typing == False:
        
        # If Shape Name is Valid #
        try:
            list2 = load_shape(loadShapeText)
            if mouseX<(100-(len(list2))) and mouseY<(100-(len(list2[0]))):
                for x in range(mouseX, mouseX+len(list2)):
                    for y in range(mouseY,mouseY+len(list2[0])):
                        if list2[x-mouseX][y-mouseY] == True:
                            giveLife(x,y)
                        
        # If Shape Name is Invalid #
        except:
            errorMsg = ('Name does not exist!')
            drawText(errorMsg, 400, 450)
            pygame.display.update()
            pygame.time.delay(800)
        loadShapeBool = False
        run = False
    
    # Main Game Function Calls #
    draw_grid()
    drawGui()
    if currentShape >- 1:
        drawcurrentshape(mouseX,mouseY,currentShape)
    message = ('Generation: '+str(generation))
    drawText(message, 10, 10)
        
    # Drag & Drop Mode Active #
    if not mouse_mode:
        mode = ('Selection Mode')
        drawText(mode, 10, 40)
    
    # Save Shape Mode Active #
    if saveShapeBool:
        pygame.draw.rect(screen,WHITE,saveTypeBox)
        saveType = typeFont.render(saveShapeText, False, (0, 0, 0))
        screen.blit(saveType,[450,450])
        
    # Load Shape Mode Active #
    if loadShapeBool:
        pygame.draw.rect(screen,WHITE,loadTypeBox)
        loadType = typeFont.render(loadShapeText, False, (0, 0, 0))
        screen.blit(loadType,[450,450])
    
    # Rules Page 1 Mode Active #
    if rules:
        screen.fill(WHITE)
        draw_rules_page_one()
    
    # Rules Page 2 Mode Active #
    if rules_2:
        screen.fill(WHITE)
        draw_rules_page_two()
    
    # Pygame Display Update #
    pygame.display.update()