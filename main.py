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

class mover(object):
    """
      Class for any mover
    """
    def __init__(self, position):
        object.__init__(self)
        self.position = numpy.array(position)
        self.direction = numpy.array([0,0])
        self.color = 'yellow'
    
    def up(self):
        """
        move up
        """
        self.direction = numpy.array([0,-1])
        
    def down(self):
        """
        move down
        """
        self.direction = numpy.array([0,1])
        
    def left(self):
        """
        move left
        """
        self.direction = numpy.array([-1,0])
        
    def right(self):
        """
        move right
        """
        self.direction = numpy.array([1,0])
        
    def move(self):
        if not self.field.isWall(self.position, self.direction):
            self.position += self.direction
            return True
        return False
        
    def setBattlefield(self, battlefield):
        self.field = battlefield        
        
    def getDirection(self):
        return self.direction
    
    def getPosition(self):
        return self.position
    
    def getNextPosition(self):
        return self.position + self.direction
    
    def getColor(self):
        return self.color
    
    def setObject(self, tkobject):
        self.tkobject = tkobject
        
    def getObject(self):
        return self.tkobject
    
class pacman(mover):
    
    def keyInput(self, event):
        if event.keysym == 'Right':
            self.right()
        if event.keysym == 'Left':
            self.left()
        if event.keysym == 'Up':
            self.up()
        if event.keysym == 'Down':
            self.down()            
            
    
class arena(Canvas):

    def __init__(self, master, xfields, yfields):
        Canvas.__init__(self, master)
        self.fields = numpy.array([xfields, yfields])
        self.fieldsize=50        
        self.walls = []
        self.movers = []
   
    def neighbours(self, field1, field2):
        return numpy.linalg.norm(numpy.subtract(field1, field2)) == 1
        
    def addWall(self, field1, field2):
        if self.neighbours(field1, field2):          
            self.walls.append((numpy.array(field1), numpy.array(field2)))
        
    def isWall(self, position, direction):
        if (position+direction < 0).any() or (position+direction >= self.fields).any():
            return True
        for wall in self.walls:
            if ((position == wall[0]).all() and (position+direction == wall[1]).all()) or \
               ((position == wall[1]).all() and (position+direction == wall[0]).all()):
                return True
        return False
        
    def addMover(self, mover):
        self.movers.append(mover)                    
        
    def initialize(self):                       
        for mover in self.movers:
            mover.setBattlefield(self)
        
        # DRAWING
        self.create_rectangle(0,0,self.fields[0]*self.fieldsize,self.fields[1] * self.fieldsize,fill='green')     
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
            
        for mover in self.movers:
            x = (mover.getPosition()[0]+0.5)*self.fieldsize
            y = (mover.getPosition()[1]+0.5)*self.fieldsize
            r = self.fieldsize*0.4
            w = self.create_oval(x-r, y-r, x+r, y+r, fill=mover.getColor())
            mover.setObject(w)
        
        
    def refresh(self):
        """
        update everything
        """
        for mover in self.movers:
            if mover.move():
                #DRAWING
                self.move(mover.getObject(),mover.getDirection()[0]*self.fieldsize,mover.getDirection()[1]*self.fieldsize)
            
        self.after(200, self.refresh)
   
master = Tk()

w = arena(master, 5,5)
for x in [1,2,3]:
    for y in [0,3]:
        w.addWall((x,y), (x,y+1))
        
for x in [0,3]:
    for y in [1, 3]:
        w.addWall((x,y), (x+1,y))

w.addWall((2,1), (2,2))        
w.addWall((2,2), (2,3))  

paxman = pacman((2,1))
w.addMover(paxman)

master.bind("<Key>", paxman.keyInput)
      
w.pack()

w.initialize()
master.after(1000, w.refresh)
mainloop()    


      
