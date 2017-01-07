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

from Tkinter import *
import numpy
from pip.utils.logging import colorama
from numpy.matlib import rand

class Fieldobject(object):
    
    def __init__(self, position, color):
        object.__init__(self)
        self.position = numpy.array([float(position[0]),float(position[1])])
        self.color = color
    
    def getPosition(self):
        return self.position
    
    def getColor(self):
        return self.color
    
    def setTkObject(self, tkobject):
        self.tkobject = tkobject
        
    def getTkObject(self):
        return self.tkobject

class Mover(Fieldobject):
    """
      Class for any Mover
    """
    def __init__(self, position, color):
        Fieldobject.__init__(self, position, color)
        self.lastDir = self.direction = numpy.array([0,0])
        self.score = 0
        self.speed = 0.2
    
    def changeDir(self):
        if self.field.isValid(self.position, self.lastDir * self.speed):
            self.direction = self.lastDir * self.speed
            self.counter = 0
        else:
            self.counter -= 1
    
    def setDir(self, direction):
        self.lastDir = direction
        self.counter = 3        
    
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
    
    
class Rag(Mover):
    
    def __init__(self, position):
        Mover.__init__(self, position, 'blue')
        self.score = 0
        
    def update(self):
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
    def __init__(self, position):
        Mover.__init__(self, position, 'red')
        
    def update(self):
        number = rand(1)
        
        if number < 0.25:
            self.up()
        elif number < 0.5:
            self.down()
        elif number < 0.75:
            self.left()
        else:
            self.right()
            
        self.changeDir()
            
class Coin(Fieldobject):
    
    def __init__(self, position):
        Fieldobject.__init__(self, position, 'yellow')
     
    
class Arena(Canvas):

    def __init__(self, master, xfields, yfields):
        Canvas.__init__(self, master)
        self.fields = numpy.array([xfields, yfields])
        self.fieldsize=50        
        self.walls = []
        self.monsters = []
   
    def neighbours(self, field1, field2):
        return numpy.linalg.norm(numpy.subtract(field1, field2)) == 1
        
    def addWall(self, field1, field2):
        if self.neighbours(field1, field2):          
            self.walls.append((numpy.array(field1), numpy.array(field2)))
        
    def getField(self, position):
        return position.round()
        
    def isValid(self, position, direction):
        field = self.getField(position)
        newField = self.getField((position) + direction/numpy.linalg.norm(direction)*0.51)
        if (newField < 0).any() or (newField >= self.fields).any():
            return False
        
        validDir = field - position
        
        if numpy.linalg.norm(validDir) < 1e-6:
            # Is in the center of the field
            for wall in self.walls:
                if ((field == wall[0]).all() and (newField == wall[1]).all())or \
                   ((field == wall[1]).all() and (newField == wall[0]).all()):
                    return False
        else:
            if numpy.abs(numpy.dot(validDir, direction)) < 1e-6:
                return False
        return True
            
        
        
    def addPlayer(self, pacman):
        self.rag = pacman
        
    def addMonster(self, ghost):
        self.monsters.append(ghost)                    
        
    def initialize(self):  
        self.coins = []
        for x in range(0,self.fields[0]):
            for y in range(0,self.fields[1]):
                self.coins.append(Coin((x,y)))
                 
        self.rag.setBattlefield(self)            
        for ghost in self.monsters:
            ghost.setBattlefield(self)
        
        # DRAWING
        self.battlefield = self.create_rectangle(0,0,self.fields[0]*self.fieldsize,self.fields[1] * self.fieldsize,fill='green')     
        for wall in self.walls:
            if wall[0][0] != wall[1][0]:
                """
                Same x-value
                """
                xmin = (1+wall[0][0])*self.fieldsize
                xmax = xmin                
                ymin = (wall[0][1]) *self.fieldsize
                ymax = ymin + self.fieldsize                
            else:
                xmin = (wall[0][0])*self.fieldsize
                xmax = xmin + self.fieldsize
                
                ymin = (1+wall[0][1]) *self.fieldsize
                ymax = ymin
            self.create_line(xmin, ymin, xmax, ymax, fill='red', width=2)
            
            
            
        x = (self.rag.getPosition()[0]+0.5)*self.fieldsize
        y = (self.rag.getPosition()[1]+0.5)*self.fieldsize
        r = self.fieldsize*0.4
        w = self.create_oval(x-r, y-r, x+r, y+r, fill=self.rag.getColor())
        self.rag.setTkObject(w)
            
        for ghost in self.monsters:
            x = (ghost.getPosition()[0]+0.5)*self.fieldsize
            y = (ghost.getPosition()[1]+0.5)*self.fieldsize
            r = self.fieldsize*0.4
            w = self.create_oval(x-r, y-r, x+r, y+r, fill=ghost.getColor())
            ghost.setTkObject(w)

        self.scorefield = self.create_text(self.fields[0]*self.fieldsize + 10, 20, text=str(self.rag.getScore()))
            
        for coin in self.coins:
            x = (coin.getPosition()[0]+0.5)*self.fieldsize
            y = (coin.getPosition()[1]+0.5)*self.fieldsize
            r = self.fieldsize*0.1
            w = self.create_oval(x-r, y-r, x+r, y+r, fill=coin.getColor())
            coin.setTkObject(w)
        
        
    def refresh(self):
        """
        update everything
        """
        
        self.rag.addScore(-1)

        self.rag.move()
        self.rag.update()
        for ghost in self.monsters:
            ghost.update()
            ghost.move()
        
        for coin in self.coins:
            if (self.getField(self.rag.getPosition()) == self.getField(coin.getPosition())).all():
                self.rag.addScore(100)
                self.coins.remove(coin) 
                # Drawing
                self.delete(coin.getTkObject())
                break


        #DRAWING        
        x = (self.rag.getPosition()[0]+0.5)*self.fieldsize
        y = (self.rag.getPosition()[1]+0.5)*self.fieldsize
        r = self.fieldsize*0.4
        self.coords(self.rag.getTkObject(),x-r, y-r, x+r, y+r)
        
        for ghost in self.monsters:        
            
            x = (ghost.getPosition()[0]+0.5)*self.fieldsize
            y = (ghost.getPosition()[1]+0.5)*self.fieldsize
            r = self.fieldsize*0.4
            self.coords(ghost.getTkObject(),x-r, y-r, x+r, y+r)
            
            
        #Drawing
        self.delete(self.scorefield)
        self.scorefield = self.create_text(self.fields[0]*self.fieldsize + 10, 20, text=str(self.rag.getScore()))
        
        lost = False
        for monster in self.monsters:
            if (self.getField(self.rag.getPosition()) == self.getField(monster.getPosition())).all():
                lost = True
        
        if self.coins == []:
            self.create_text(self.fields[0]*self.fieldsize / 2, self.fields[1]*self.fieldsize / 2 , text='You Won')
        elif lost:
            self.create_text(self.fields[0]*self.fieldsize / 2, self.fields[1]*self.fieldsize / 2 , text='You Lost')
        else:
            self.after(10, self.refresh)
   
master = Tk()

w = Arena(master, 5,5)
for x in [1,2,3]:
    for y in [0,3]:
        w.addWall((x,y), (x,y+1))
        
for x in [0,3]:
    for y in [1, 3]:
        w.addWall((x,y), (x+1,y))

w.addWall((2,1), (2,2))        
w.addWall((2,2), (2,3))  

rag = Rag((2,1))
w.addPlayer(rag)
w.addMonster(Monster((0,0)))

master.bind("<Key>", rag.keyInput)
      
w.pack()

w.initialize()
master.after(1000, w.refresh)
mainloop()    


      
