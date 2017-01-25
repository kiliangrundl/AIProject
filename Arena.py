import numpy
from numpy.matlib import rand
import random

import treeSearch

class Fieldobject(object):
    
    def __init__(self):
        object.__init__(self)        
    
    def setPosition(self, position):
        self.position = numpy.array([float(position[0]),float(position[1])])
    
    def getPosition(self):
        return self.position
    

class Mover(Fieldobject):
    """
      Class for any Mover
    """
    def __init__(self):
        Fieldobject.__init__(self)

    def initialize(self):
        self.lastDir = self.direction = numpy.array([0,0])
        self.score = 0
        self.speed = 0.1
        self.counter = 0
    
    def changeDir(self):
        if self.field.isValid(self.position, self.lastDir * self.speed):
            self.direction = self.lastDir * self.speed
            self.counter = 0
        else:
            self.counter -= 1
    
    def setDir(self, direction):
        self.lastDir = direction
        self.counter = int(5 / self.speed)
    
    def up(self):
        """
        move up
        """
        self.setDir(numpy.array([0,-1]))
        
    def down(self):
        """
        move down
        """
        self.setDir(numpy.array([0,1]))

    def left(self):
        """
        move left
        """
        self.setDir(numpy.array([-1,0]))
        
    def right(self):
        """
        move right
        """
        self.setDir(numpy.array([1,0]))           
        
    def move(self):
        if self.field.isValid(self.position, self.direction):
            self.position += self.direction
            return True
        return False
        
    def setBattlefield(self, battlefield):
        self.field = battlefield        
        
    def getDirection(self):
        return self.direction
       
class RAG(Mover):
    
    def __init__(self):
        Mover.__init__(self)
        self.score = 0
        
    def update(self):
        if self.counter > 0:
            self.changeDir()
        
    def getScore(self):
        return self.score
    
    def addScore(self, points):
        self.score += points
        
    def keyInput(self, event):
        if event.keysym == 'Right':
            self.right()
        if event.keysym == 'Left':
            self.left()
        if event.keysym == 'Up':
            self.up()
        if event.keysym == 'Down':
            self.down()            
       
class Monster(Mover):
    def __init__(self):
        Mover.__init__(self)
        
    def initialize(self):
        Mover.initialize(self)
        self.direction = numpy.array([1.,0])
        
    def update(self):        
        number = rand(1)
        
        prob = 0.1 # probability to change direction
        
        if not self.field.isValid(self.position, self.direction) or number < prob:
            #chose a new direction if the current one is not valid any more or with a certain probablity
            number = rand(1)
            if number < 0.25:
                self.up()
            elif number < 0.5:
                self.down()
            elif number < 0.75:
                self.left()
            else:
                self.right()
            
        # set new direction
        self.changeDir()
            
class Coin(Fieldobject):
    
    def __init__(self, position):
        Fieldobject.__init__(self)
        self.setPosition(position)
         
class Arena(treeSearch.SearchProblem):

    def __init__(self):
        self.fieldsize=50        
        self.walls = []
        self.monsters = []
        self.coins = []
            
    def start(self, *keys):
        del self.walls[:]
        del self.monsters[:]
        self.initArena1()
        self.initialize()        

    def initArena1(self):
                
        self.fields = numpy.array([9, 9])
        self.playerstart = numpy.array([0,0])
        self.monsterStarts = []
        self.monsterStarts.append(numpy.array([4,4]))
        self.monsterStarts.append(numpy.array([4,5]))
        
        for i in range(2):
            self.addMonster(Monster())
        
        #AROUND the monster Start
        for x in range(3,6):
            y = 3
            self.addWall((x,y))
            
        for y in range(4,6):
            for x in [3,5]:
                self.addWall((x,y))
        
        #OUTSIDE    
        for x in range(1,4):
            for y in [1,7]:
                self.addWall((x,y))
            
        for x in range(5,8):
            for y in [1,7]:
                self.addWall((x,y))
                
        for y in range(1,4):
            for x in [1,7]:
                self.addWall((x,y))
                
        for y in range(5,8):
            for x in [1,7]:
                self.addWall((x,y))
                
        self.coins = []
        for x in range(0,self.fields[0]):
            for y in range(0,self.fields[1]):
                newField = numpy.array([x,y])
                if not any((newField == x).all() for x in self.walls) and \
                    not any((newField == x).all() for x in self.monsterStarts):
                    self.coins.append(Coin((x,y)))
                
    def initArena2(self):
                
        self.fields = numpy.array([17, 8])
        self.playerstart = numpy.array([7,2])
        self.monsterStarts = []
        #self.monsterStarts.append(numpy.array([4,4]))
        #self.monsterStarts.append(numpy.array([4,5]))
        
        #for i in range(2):
        #    self.addMonster(Monster())
        
        
        self.coins.append(Coin((0,7)))
        
        self.addWall((1,0))
            
        for y in range(0,2):
            self.addWall((8,y))
            
        for y in range(0,2):
            self.addWall((8,y))
            
        for y in range(0,4):
            self.addWall((10,y))
            
        for x in range(3,7):
            self.addWall((x,1))
            
        for x in range(11,15):
            self.addWall((x,1))

        for x in range(0,4):
            self.addWall((x,2))
            
        self.addWall((3,3))           

        for x in range(5,9):
            self.addWall((x,3))
          
        self.addWall((11,3)) 
        
        for x in range(13,17):
            self.addWall((x,3))        
          
        self.addWall((5,4))  
        
        for x in range(1,4):
            self.addWall((x,4))
            
        self.addWall((13,4))
        
        self.addWall((7,5))
        self.addWall((8,5))
        self.addWall((10,5))
        self.addWall((11,5))
        self.addWall((15,5))
        
        for x in range(0,8):
            self.addWall((x,6))
            
        for x in range(11,16):
            self.addWall((x,6))            
            
        self.addWall((9,7)) 
                    
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
            newField = self.getField((position) + direction/nrm*0.51)
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
        
    def addPlayer(self, rag):
        self.rag = rag        
        
    def addMonster(self, ghost):
        self.monsters.append(ghost)                    
        
    def initialize(self):  

        self.rag.initialize()
        self.rag.setPosition(self.playerstart)
        self.rag.setBattlefield(self)
        self.lost = False         
                 
        for monster in self.monsters:
            monster.setBattlefield(self)
            monster.setPosition(random.choice(self.monsterStarts))
            monster.initialize()
        
    def refresh(self):
        """
        update everything
        """
        
        self.rag.addScore(-1)

        self.rag.update()
        self.rag.move()
        
        for monster in self.monsters:
            monster.update()
            monster.move()
        
        for coin in self.coins:
            if (self.getField(self.rag.getPosition()) == self.getField(coin.getPosition())).all():
                self.rag.addScore(100)
                self.coins.remove(coin)
                break
            
                    
        for monster in self.monsters:
            if numpy.linalg.norm(self.rag.getPosition() - monster.getPosition(),2) < 0.5:
                self.lost = True
                self.rag.addScore(-500)
                break
            
        if self.coins == []:
            self.rag.addScore(500)
        elif not self.lost:
            self.after(10, self.refresh)