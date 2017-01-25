import treeSearch as tS
from Arena import Arena

        
problem = tS.SailProblem([(14,18)], 20, 20)
#problem = tS.MainTestSearch()
#problem = tS.EasyTestSearchOne()

problem = Arena()
problem.initArena2()

# Set heuristic
hC = tS.manhattenDistance2D([(14,18)])
hC = tS.manhattenDistance2D([(0,7)]) # for Arena2
heuristic = hC.heuristicFun

   
print("DepthFirstSearch")
#treeSearch(problem, tS.DepthFirstSearch(problem, s))

print("BreathFirstSearch")
#treeSearch(problem, tS.BreathFirstSearch(problem, s))
    
print("UniformCostSearch")
#treeSearch(problem, tS.UniformCostSearch(problem, s))

print("GreedySearch")
tS.treeSearch(problem, tS.GreedySearch(problem, heuristic))

print("AstarSearch")
tS.treeSearch(problem, tS.AstarSearch(problem, heuristic))