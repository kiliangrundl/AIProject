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
        self.position = numpy.array([float(position[0]), float(position[1])])
    
    def getPosition(self):
        return self.position
    

class Mover(Fieldobject):
    """
      Class for any Mover
    """
    def __init__(self):
        Fieldobject.__init__(self)

    def initialize(self):
        self.direction = numpy.array([0, 0])
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
        self.direction = numpy.array([1., 0])
        
    def act(self):        
        # chose a new direction
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
        self.walls = []
        self.monsters = []
        self.coins = []
        self.speed = 1
        
        self.initArena()
        self.addCoins()
        
    def getStartState(self):
        treeSearch.SearchProblem.getStartState(self)
        return tuple(self.playerstart)
    
    def getState(self):
        s = []
        s.append(self.player.getPosition()[0])
        s.append(self.player.getPosition()[1])
        for coin in self.coins:
            e = 'e'
            if not coin.exists:
                e = 'n'
            s.append(e)
        for monster in self.monsters:
            s.append(monster.getPosition()[0])
            s.append(monster.getPosition()[1])
            
        return tuple(s)
    
    def getActions(self, s):
        actions =  ['u', 'd', 'l', 'r']
        possible = []
        pos = numpy.array((s[0], s[1]))
        for a in actions:
            if self.isValid(pos, self.computeDirection(a)):
                possible.append(a)
        
        return actions

    def computeDirection(self, a):
        if a is 'u':
            return numpy.array([0, -1])
        elif a is 'd':
            return numpy.array([0, 1])
        elif a is 'l':
            return numpy.array([-1, 0])
        elif a is 'r':
            return numpy.array([1, 0])
        else:
            return numpy.array([0, 0]) 
            
    def getNewPosition(self, s, action):
        return tuple(numpy.array(s) + numpy.array(action.getMove()))
            
    def solved(self, s):
        return tuple(self.coins[0].getPosition()) == s
    
    def isGoalState(self, s):
        '''
        Check if the given state is a goal state
        '''
        if self.won or self.lost:
            return True
        else:
            return False
            
    def addWall(self, field):
        field = numpy.array(field)
        if not any((field == x).all() for x in self.walls):
            self.walls.append(field)
        
    def getField(self, position):
        return position.round()
        
    def isValid(self, position, direction):
        field = self.getField(position)
        nrm = numpy.linalg.norm(direction)
        if nrm > 1e-6:
            newField = self.getField((position) + direction / nrm * 0.51)
        else:
            newField = field
        if (newField < 0).any() or (newField >= self.fields).any():
            return False
        
        validDir = field - position
        
        if numpy.linalg.norm(validDir) < 1e-6:
            # Is in the center of the field
            if any((newField == x).all() for x in self.walls):
                return False
        else:
            if numpy.abs(numpy.dot(validDir, direction)) < 1e-6:
                return False
        return True
        
    def addPlayer(self, player):
        self.player = player        
        
    def addMonster(self, ghost):
        self.monsters.append(ghost)                    
        
    def initialize(self):
        self.won = False
        self.lost = False
        
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
                newField = numpy.array([x, y])
                if not any((newField == x).all() for x in self.walls) and \
                    not any((newField == x).all() for x in self.monsterStarts):
                    self.coins.append(Coin((x, y)))

    def takeAction(self, s, a):
        """
        play one round
        input s: the position of the player
        input a: the action the player took
        """
        R = -1 # Living reward
        
        newDirection = self.computeDirection(a)
        if self.isValid(self.player.position, newDirection):
            self.player.direction = newDirection
        
        if self.isValid(self.player.position, self.player.direction):
            self.player.setPosition(self.player.position + self.player.direction * self.speed)

        # check if a coin is taken
        for coin in self.coins:
            if (self.getField(self.player.getPosition()) == self.getField(coin.getPosition())).all():
                R += 10
                coin.exists = False
                break
        
        # check if the game is won because all coins are taken
        won = True
        for coin in self.coins:
            if coin.exists:
                won = False
                break
            
        self.won = won        
        
        if not won:
            for monster in self.monsters:
                # check if a monster was hit
                if numpy.linalg.norm(self.player.getPosition() - monster.getPosition(), 2) < 0.5:
                    self.lost = True
                    break
                
                
                monster.act()
                newDirection = self.computeDirection(monster.action)
                if self.isValid(monster.position, newDirection):
                    monster.direction = newDirection
                    
                if self.isValid(monster.position, monster.direction):
                    monster.setPosition(monster.position + monster.direction * self.speed)            
            
                # check if a monster hit the player after the move
                if numpy.linalg.norm(self.player.getPosition() - monster.getPosition(), 2) < 0.5:
                    self.lost = True
                    break

        if self.lost:
            R -= 500
        if self.won:
            R += 100
                        
        self.player.addScore(R)
        return R, self.getState()
        

class Arena1(Arena):
    def initArena(self):
                
        self.fields = numpy.array([9, 9])
        self.playerstart = numpy.array([0, 0])
        self.monsterStarts = []
        self.monsterStarts.append(numpy.array([4, 4]))
        self.monsterStarts.append(numpy.array([4, 5]))
        
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
                
        self.fields = numpy.array([17, 8])
        self.playerstart = numpy.array([0, 1])
        self.monsterStarts = []
        # self.monsterStarts.append(numpy.array([4,4]))
        # self.monsterStarts.append(numpy.array([4,5]))
        
        # for i in range(2):
        #    self.addMonster(Monster())
        
        
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
                
        self.fields = numpy.array([3, 2])
        self.playerstart = numpy.array([2, 0])
        self.monsterStarts = []
        self.monsterStarts.append(numpy.array([1, 1]))
        
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
        self.fieldsize=50        
      
    def initialize(self):
        self.TkObjects = {}
        
        # DRAWING
        self.battlefield = self.create_rectangle(0,0,self.arena.fields[0]*self.fieldsize,self.arena.fields[1] * self.fieldsize,fill='green')
        
        for mS in self.arena.monsterStarts:
            xstart = mS[0] * self.fieldsize
            ystart = mS[1] * self.fieldsize
            self.create_rectangle(xstart,ystart,xstart + self.fieldsize,ystart + self.fieldsize,fill='red')
        
        for wall in self.arena.walls:
            xstart = wall[0] * self.fieldsize
            ystart = wall[1] * self.fieldsize
            self.create_rectangle(xstart,ystart,xstart + self.fieldsize,ystart + self.fieldsize,fill='gray')


        for coin in self.arena.coins:
            x = (coin.getPosition()[0]+0.5)*self.fieldsize
            y = (coin.getPosition()[1]+0.5)*self.fieldsize
            r = self.fieldsize*0.1
            self.TkObjects[coin] = self.create_oval(x-r, y-r, x+r, y+r, fill='yellow')
            
            
            
        self.TkObjects[self.arena.player] = self.create_oval(0, 0, 0, 0, fill='blue')
        
        self.scorefield = self.create_text(self.arena.fields[0]*self.fieldsize + 30, 20, text=str(self.arena.player.getScore()))
            
        for monster in self.arena.monsters:           
            self.TkObjects[monster] = self.create_oval(0, 0, 0, 0, fill='orange')
        
        self.master.geometry('{}x{}'.format(self.arena.fields[0]*self.fieldsize, self.arena.fields[1] * self.fieldsize))     
        
    def refresh(self):
        # Drawing
        for coin in self.arena.coins:
            if not coin.exists:
                self.itemconfigure(self.TkObjects[coin], state='hidden')
            else:
                self.itemconfigure(self.TkObjects[coin], state='normal')

        #DRAWING        
        x = (self.arena.player.getPosition()[0]+0.5)*self.fieldsize
        y = (self.arena.player.getPosition()[1]+0.5)*self.fieldsize
        r = self.fieldsize*0.4
        self.coords(self.TkObjects[self.arena.player],x-r, y-r, x+r, y+r)
        
        for monster in self.arena.monsters:        
            x = (monster.getPosition()[0]+0.5)*self.fieldsize
            y = (monster.getPosition()[1]+0.5)*self.fieldsize
            r = self.fieldsize*0.4
            self.coords(self.TkObjects[monster],x-r, y-r, x+r, y+r)
            
            
        #Drawing
        self.delete(self.scorefield)
        self.scorefield = self.create_text(self.arena.fields[0]*self.fieldsize + 30, 20, text=str(self.arena.player.getScore()))
        
        #if self.arena.coins == []:
        #    self.create_text(self.arena.fields[0]*self.fieldsize / 2, self.arena.fields[1]*self.fieldsize / 2 , text='You Won, Score = ' + str(self.arena.player.getScore()), fill='white')
        #elif self.arena.lost:
        #    self.create_text(self.arena.fields[0]*self.fieldsize / 2, self.arena.fields[1]*self.fieldsize / 2 , text='You Lost, Score = ' + str(self.arena.player.getScore()), fill='white')
        
        self.master.after(10, self.refresh)
