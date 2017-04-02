import tkinter
import Arena
import Player

'''
File for playing the RAG-game
'''

                         
# define the problem
arena = Arena.Arena2()

# Define a player
player = Player.RAG(arena)
arena.addPlayer(player)

root = tkinter.Tk()
root.after(0, player.start, root)
tkinter.mainloop()


