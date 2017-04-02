import numpy
from numpy.matlib import rand
import random
import tkinter

import treeSearch
import mdp

class Fieldobject(object):
    
    def __init__(self):
        object.__init__(self)        
    
    def setPosition(self, position):
        self.position = position
    
    def getPosition(self):
        return self.position
    

class Mover(Fieldobject):
    """
      Class for any Mover
    """
    def __init__(self):
        Fieldobject.__init__(self)

    def initialize(self):
        self.action = numpy.array([0, 0], dtype=int)
        self.action = 's'
    
    def up(self):
        """
        chose up
        """
        self.action = 'u'
        
    def down(self):
        """
        chose down
        """
        self.action = 'd'

    def left(self):
        """
        chose left
        """
        self.action = 'l'
        
    def right(self):
        """
        chose right
        """
        self.action = 'r'                      
       
class Monster(Mover):
    def __init__(self):
        Mover.__init__(self)
        
    def initialize(self):
        Mover.initialize(self)
        self.action = numpy.array([1., 0], dtype=int)
        
    def act(self):        
        # chose a new action
        number = rand(1)
        if number < 0.25:
            self.up()
        elif number < 0.5:
            self.down()
        elif number < 0.75:
            self.left()
        else:
            self.right()
            
class Coin(Fieldobject):
    
    def __init__(self, position):
        Fieldobject.__init__(self)
        self.exists = False
        self.setPosition(position)

class Arena(treeSearch.SearchProblem, mdp.MDP):
    """
    gernerally the directions are
    
      0 1 2 3 4 5
      _ _ _ _ _ _ _> x
    0|
    1|
    2|
    3|
    4|
     y 
    """

    def __init__(self):
        self.walls = set()
        self.monsters = set()
        self.coins = set()
        
        self.initArena()
        self.addCoins()
        
    def setSearchStartState(self, pos):
        self.searchStart = pos
        
    def getSearchStartState(self):
        treeSearch.SearchProblem.getSearchStartState(self)
        return self.searchStart
    
    def getState(self):
        s = []
        s.append(self.player.getPosition())
        for coin in self.coins:
            e = 'e'
            if not coin.exists:
                e = 'n'
            s.append((coin.getPosition(), e))
        for monster in self.monsters:
            s.append(monster.getPosition())
            
        return tuple(s)
    
    def getSearchActions(self, pos):
        '''
        Return actions with a certain cost for a search
        Remark: the search state (pos) is different from the arena-state!
        '''
        actions = []
        for a in self.getStateActions([pos]):
            actions.append(treeSearch.Action(a, 1))
        return actions
    
    def getStateActions(self, s):
        actions = ['u', 'd', 'l', 'r']
        possible = []
        pos = s[0]
        for a in actions:
            if self.isValid(self.getNewPosition(pos, a)):
                possible.append(a)
        
        return possible
    
    def computeLinkPositions(self):
        '''
        compute all positions which are a link (3 choices or more)
        '''
        lP = []
        for x in range(self.fields[0]):
            for y in range(self.fields[1]):
                pos = [(x,y)]
                if len(self.getStateActions(pos)) > 2 and not pos[0] in self.walls:
                    lP.append(pos[0])
        return lP

    def computeDirection(self, a):
        if a is 'u':
            return (0, -1)
        elif a is 'd':
            return (0, 1)
        elif a is 'l':
            return (-1, 0)
        elif a is 'r':
            return (1, 0)
        else:
            return (0, 0) 
    
    def computeActualDistance(self, p1, goals):
        '''
        Compute/search the actual distance between two positions on the field
        p1: the position of the first object
        goals: the position of the search objects (the goal)
        '''
        self.setSearchStartState(p1)
        self.setSearchGoals(goals)
        heuristic = treeSearch.manhattenDistance2D(goals)
        strategy = treeSearch.AstarSearch(self, heuristic.heuristicFun)
        treeSearch.treeSearch(self, strategy)
        
        return strategy.getCurrentFringe().getCostTotal()
       
    def getNewPosition(self, s, action):
        nD = self.computeDirection(action)
        return (s[0] + nD[0], s[1] + nD[1])
    
    def setSearchGoals(self, g):
        '''
        Set a goal for the search
        '''
        self.searchGoals = g
         
    def solvedSearch(self, searchState):
        return searchState in self.searchGoals
    
    def isGoalState(self, s):
        '''
        Check if the given state is a goal state
        '''
        won = True
        for i in range(1, len(self.coins)):
            if s[i][1] == 'e':
                won = False
                break
        
        lost = False
        pos = s[0]
        for i in range(1 + len(self.coins), 1 + len(self.coins) + len(self.monsters)):
            if pos == s[i]:
                lost = True
                break
            
        if won or lost:
            return True
        else:
            return False
            
    def addWall(self, field):
        field = field
        if not field in self.walls:
            self.walls.add(field)
        
    def isValid(self, position):
        newField = position
        if newField[0] < 0 or newField[1] < 0 or newField[0] >= self.fields[0] or newField[1] >= self.fields[1]:
            return False
        
        # Is in the center of the field
        if newField in self.walls:
            return False
        
        return True
    
    def areEqual(self, field1, field2):
        return field1[0] == field2[0] and field1[1] == field2[1]
        
    def addPlayer(self, player):
        self.player = player        
        
    def addMonster(self, ghost):
        self.monsters.add(ghost)                    
        
    def initialize(self):
        # initilaize all the monsters
        for monster in self.monsters:
            monster.setPosition(random.choice(self.monsterStarts))
            monster.initialize()
            
        for coin in self.coins:
            coin.exists = True
            
        # initialize the player
        self.player.setPosition(self.playerstart)
        self.player.initialize()
        
        # the state is here simpliefied to be everything on the field (which is actually a little more than just the state)
        return self

    def addCoins(self):
        self.coins = []
        for x in range(0, self.fields[0]):
            for y in range(0, self.fields[1]):
                newField = numpy.array([x, y], dtype=int)
                if not any((newField == x).all() for x in self.walls) and \
                    not any((newField == x).all() for x in self.monsterStarts) and \
                    not any((newField == x).all() for x in self.playerstart):
                    self.coins.append(Coin((x, y)))

    def takeAction(self, s, a):
        """
        play one round
        input s: the position of the player
        input a: the action the player took
        """
        R = -1  # Living reward
        
        if self.isValid(self.getNewPosition(self.player.position, a)):
            self.player.action = a
        
        nP = self.getNewPosition(self.player.position, self.player.action)
        if self.isValid(nP):
            self.player.setPosition(nP)

        # check if a coin is taken
        for coin in self.coins:
            if coin.exists:
                if self.player.getPosition() == coin.getPosition():
                    R += 10
                    coin.exists = False
                    break
        
        # check if the game is won because all coins are taken
        won = True
        for coin in self.coins:
            if coin.exists:
                won = False
                break
        if won:
            R += 100
        
        if not won:
            lost = False
            for monster in self.monsters:
                # check if a monster was hit
                if self.areEqual(self.player.getPosition(), monster.getPosition()):
                    lost = True
                    break
                
                
                monster.act()
                
                nP = self.getNewPosition(monster.position, monster.action)
                if self.isValid(nP):
                    monster.setPosition(nP)            
            
                # check if a monster hit the player after the move
                if self.areEqual(self.player.getPosition(), monster.getPosition()):
                    lost = True
                    break
                
            if lost:
                R -= 500

        self.player.addScore(R)
        return R, self.getState()
        

class Arena1(Arena):
    def initArena(self):
                
        self.fields = (9, 9)
        self.playerstart = (0, 0)
        self.monsterStarts = []
        self.monsterStarts.append((4, 4))
        self.monsterStarts.append((4, 5))
        
        for i in range(2):
            self.addMonster(Monster())
        
        # AROUND the monster Start
        for x in range(3, 6):
            y = 3
            self.addWall((x, y))
            
        for y in range(4, 6):
            for x in [3, 5]:
                self.addWall((x, y))
        
        # OUTSIDE    
        for x in range(1, 4):
            for y in [1, 7]:
                self.addWall((x, y))
            
        for x in range(5, 8):
            for y in [1, 7]:
                self.addWall((x, y))
                
        for y in range(1, 4):
            for x in [1, 7]:
                self.addWall((x, y))
                
        for y in range(5, 8):
            for x in [1, 7]:
                self.addWall((x, y))
                
class Arena2(Arena):
    def initArena(self):
                
        self.fields = (20, 5)
        self.playerstart = (0, 0)
        self.monsterStarts = []
        self.monsterStarts.append((10,2))
        #self.monsterStarts.append(numpy.array([2,11]))
        
        for _ in range(3):
            self.addMonster(Monster())
            
        self.addWall((0, 2))
        self.addWall((2, 2))
        self.addWall((2, 3))
        self.addWall((3, 3))
        self.addWall((4, 3))
        self.addWall((5, 3))
        self.addWall((5, 2))
        self.addWall((5, 1))
        self.addWall((4, 1))
        self.addWall((6, 1))
        self.addWall((6, 3))
        self.addWall((8, 3))
        self.addWall((9, 3))
        self.addWall((9, 2))
        self.addWall((10, 3))
        self.addWall((11, 3))
        self.addWall((11, 2))
        self.addWall((12, 3))
        self.addWall((14, 3))
        self.addWall((15, 3))
        self.addWall((15, 2))
        self.addWall((15, 1))
        self.addWall((14, 1))
        self.addWall((16, 1))
        self.addWall((16, 3))
        self.addWall((17, 3))
        self.addWall((18, 3))       
            
            
                
class Test_Arena1(Arena):
    def initArena(self):
                
        self.fields = (17, 8)
        self.playerstart = (0, 1)
        self.monsterStarts = []
        
        
        self.addWall((1, 0))
            
        for y in range(0, 2):
            self.addWall((8, y))
            
        for y in range(0, 2):
            self.addWall((8, y))
            
        for y in range(0, 4):
            self.addWall((10, y))
            
        for x in range(3, 7):
            self.addWall((x, 1))
            
        for x in range(11, 15):
            self.addWall((x, 1))

        for x in range(0, 4):
            self.addWall((x, 2))
            
        self.addWall((3, 3))           

        for x in range(5, 9):
            self.addWall((x, 3))
          
        self.addWall((11, 3)) 
        
        for x in range(13, 17):
            self.addWall((x, 3))        
          
        self.addWall((5, 4))  
        
        for x in range(1, 4):
            self.addWall((x, 4))
            
        self.addWall((13, 4))
        
        self.addWall((7, 5))
        self.addWall((8, 5))
        self.addWall((10, 5))
        self.addWall((11, 5))
        self.addWall((15, 5))
        
        for x in range(0, 8):
            self.addWall((x, 6))
            
        for x in range(11, 16):
            self.addWall((x, 6))            
            
        self.addWall((9, 7))
         
    def addCoins(self):
        self.coins.append(Coin((0, 7)))
        
class SimpleArena1(Arena):
    def initArena(self):
                
        self.fields = (3, 2)
        self.playerstart = (2, 0)
        self.monsterStarts = []
        self.monsterStarts.append((1, 1))
        
        for _ in range(1):
            self.addMonster(Monster())
        
    def addCoins(self):
        self.coins.append(Coin((0, 1)))
        
        # self.addWall((1,0))
class ArenaCanvas(tkinter.Canvas):
    '''
    Class that does all the drawing of the arenas
    '''

    def __init__(self, root, arena):
        self.arena = arena
        tkinter.Canvas.__init__(self, root)
        self.fieldsize = 50        
      
    def mouseClick(self, event):
        fieldx = int(event.x / 50)
        fieldy = int(event.y / 50)
        print('(',fieldx, ',' , fieldy,')', sep='')
      
    def initialize(self):
        self.TkObjects = {}
        
        self.bind("<Button-1>", self.mouseClick)
        
        # DRAWING
        self.battlefield = self.create_rectangle(0, 0, self.arena.fields[0] * self.fieldsize, self.arena.fields[1] * self.fieldsize, fill='green')
        
        for mS in self.arena.monsterStarts:
            xstart = mS[0] * self.fieldsize
            ystart = mS[1] * self.fieldsize
            self.create_rectangle(xstart, ystart, xstart + self.fieldsize, ystart + self.fieldsize, fill='red')
        
        for wall in self.arena.walls:
            xstart = wall[0] * self.fieldsize
            ystart = wall[1] * self.fieldsize
            self.create_rectangle(xstart, ystart, xstart + self.fieldsize, ystart + self.fieldsize, fill='gray')


        for coin in self.arena.coins:
            x = (coin.getPosition()[0] + 0.5) * self.fieldsize
            y = (coin.getPosition()[1] + 0.5) * self.fieldsize
            r = self.fieldsize * 0.1
            self.TkObjects[coin] = self.create_oval(x - r, y - r, x + r, y + r, fill='yellow')
            
            
            
        self.TkObjects[self.arena.player] = self.create_oval(0, 0, 0, 0, fill='blue')
        
        self.scorefield = self.create_text(self.arena.fields[0] * self.fieldsize + 30, 20, text=str(self.arena.player.getScore()))
            
        for monster in self.arena.monsters:           
            self.TkObjects[monster] = self.create_oval(0, 0, 0, 0, fill='orange')
        
        self.master.geometry('{}x{}'.format(self.arena.fields[0] * self.fieldsize, self.arena.fields[1] * self.fieldsize))     
        
    def refresh(self):
        # Drawing
        for coin in self.arena.coins:
            if not coin.exists:
                self.itemconfigure(self.TkObjects[coin], state='hidden')
            else:
                self.itemconfigure(self.TkObjects[coin], state='normal')

        # DRAWING        
        x = (self.arena.player.getPosition()[0] + 0.5) * self.fieldsize
        y = (self.arena.player.getPosition()[1] + 0.5) * self.fieldsize
        r = self.fieldsize * 0.4
        self.coords(self.TkObjects[self.arena.player], x - r, y - r, x + r, y + r)
        
        for monster in self.arena.monsters:        
            x = (monster.getPosition()[0] + 0.5) * self.fieldsize
            y = (monster.getPosition()[1] + 0.5) * self.fieldsize
            r = self.fieldsize * 0.4
            self.coords(self.TkObjects[monster], x - r, y - r, x + r, y + r)
            
            
        # Drawing
        self.delete(self.scorefield)
        self.scorefield = self.create_text(self.arena.fields[0] * self.fieldsize + 30, 20, text=str(self.arena.player.getScore()))
        
        # if self.arena.coins == []:
        #    self.create_text(self.arena.fields[0]*self.fieldsize / 2, self.arena.fields[1]*self.fieldsize / 2 , text='You Won, Score = ' + str(self.arena.player.getScore()), fill='white')
        # elif self.arena.lost:
        #    self.create_text(self.arena.fields[0]*self.fieldsize / 2, self.arena.fields[1]*self.fieldsize / 2 , text='You Lost, Score = ' + str(self.arena.player.getScore()), fill='white')
        
        self.master.after(40, self.refresh) # 10 fps
        
def initializeCanvas(player, root):
    '''
    Routine uch that the arena can be painted or not in a different thread
    '''
    paint = True
    if paint:
        
        # TODO: solve this more nicely
        try:
            root.bind("<Key>", player.keyInput)
        except:
            pass
        
        canvas = ArenaCanvas(root, player.problem)
        canvas.initialize()
        # canvas.pack()
        canvas.pack(fill=tkinter.BOTH, expand=1)
        # root.resizable(width=False, height=False)
    
        # create a toplevel menu
        menubar = tkinter.Menu(root)
        # menubar.add_command(label="Restart", command=self.start)
        # root.bind_all("<Control-r>", self.start)
        # display the menu
        root.config(menu=menubar)
    
        root.after(100, canvas.refresh)
    
        # tkinter.mainloop()
