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

import Tkinter
import Arena

class ArenaCanvas(Arena.Arena1, Tkinter.Canvas):
    '''
    Class that does all the drawing of the arenas
    '''

    def __init__(self, root):
        Arena.Arena.__init__(self)
        Tkinter.Canvas.__init__(self, root)
        self.fieldsize=50        
        self.walls = []
        self.monsters = []
        self.coins = []
        
    def start(self, *keys):
        Arena.Arena.start(self, *keys)
        self.master.after(1000, w.refresh)
      
    def initialize(self):
        Arena.Arena.initialize(self)
        self.TkObjects = {}
        
        # DRAWING
        self.battlefield = self.create_rectangle(0,0,self.fields[0]*self.fieldsize,self.fields[1] * self.fieldsize,fill='green')
        
        for mS in self.monsterStarts:
            xstart = mS[0] * self.fieldsize
            ystart = mS[1] * self.fieldsize
            self.create_rectangle(xstart,ystart,xstart + self.fieldsize,ystart + self.fieldsize,fill='red')
        
        for wall in self.walls:
            xstart = wall[0] * self.fieldsize
            ystart = wall[1] * self.fieldsize
            self.create_rectangle(xstart,ystart,xstart + self.fieldsize,ystart + self.fieldsize,fill='gray')


        for coin in self.coins:
            x = (coin.getPosition()[0]+0.5)*self.fieldsize
            y = (coin.getPosition()[1]+0.5)*self.fieldsize
            r = self.fieldsize*0.1
            self.TkObjects[coin] = self.create_oval(x-r, y-r, x+r, y+r, fill='yellow')
            
            
        x = (self.rag.getPosition()[0]+0.5)*self.fieldsize
        y = (self.rag.getPosition()[1]+0.5)*self.fieldsize
        r = self.fieldsize*0.4
        self.TkObjects[self.rag] = self.create_oval(x-r, y-r, x+r, y+r, fill='blue')
        
        self.scorefield = self.create_text(self.fields[0]*self.fieldsize + 30, 20, text=str(self.rag.getScore()))
            
        for monster in self.monsters:           
            x = (monster.getPosition()[0]+0.5)*self.fieldsize
            y = (monster.getPosition()[1]+0.5)*self.fieldsize
            r = self.fieldsize*0.4
            self.TkObjects[monster] = self.create_oval(x-r, y-r, x+r, y+r, fill='orange')
        
        self.master.geometry('{}x{}'.format(self.fields[0]*self.fieldsize, self.fields[1] * self.fieldsize))     
        
    def refresh(self):
        Arena.Arena.refresh(self)
        
        # Drawing
        delCoins = set(self.TkObjects.keys()) - set(self.coins + [self.rag] + self.monsters)
        for coin in delCoins:
            self.delete(self.TkObjects[coin])
            del self.TkObjects[coin] 

        #DRAWING        
        x = (self.rag.getPosition()[0]+0.5)*self.fieldsize
        y = (self.rag.getPosition()[1]+0.5)*self.fieldsize
        r = self.fieldsize*0.4
        self.coords(self.TkObjects[self.rag],x-r, y-r, x+r, y+r)
        
        for monster in self.monsters:        
            x = (monster.getPosition()[0]+0.5)*self.fieldsize
            y = (monster.getPosition()[1]+0.5)*self.fieldsize
            r = self.fieldsize*0.4
            self.coords(self.TkObjects[monster],x-r, y-r, x+r, y+r)
            
            
        #Drawing
        self.delete(self.scorefield)
        self.scorefield = self.create_text(self.fields[0]*self.fieldsize + 30, 20, text=str(self.rag.getScore()))
        
        if self.coins == []:
            self.create_text(self.fields[0]*self.fieldsize / 2, self.fields[1]*self.fieldsize / 2 , text='You Won, Score = ' + str(self.rag.getScore()), fill='white')
        elif self.lost:
            self.create_text(self.fields[0]*self.fieldsize / 2, self.fields[1]*self.fieldsize / 2 , text='You Lost, Score = ' + str(self.rag.getScore()), fill='white')

root = Tkinter.Tk()

w = ArenaCanvas(root)
rag = Arena.RAG()
w.addPlayer(rag)
  

root.bind("<Key>", rag.keyInput)

w.pack(fill=Tkinter.BOTH, expand=1)
root.resizable(width=False, height=False)

# create a toplevel menu
menubar = Tkinter.Menu(root)
menubar.add_command(label="Restart", command=w.start)
root.bind_all("<Control-r>", w.start)
# display the menu
root.config(menu=menubar)

root.after(10, w.start)

Tkinter.mainloop()    


      
