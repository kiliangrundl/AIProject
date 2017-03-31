import treeSearch as tS
import Arena

        
problem = tS.SailProblem([(7,3)], 8, 8)
#problem = tS.MainTestSearch()
#problem = tS.EasyTestSearchOne()

problem = Arena.Arena1()
g = [(4.0,4.0), (7.0,0.0)]
problem.setSearchGoals(g)
problem.setSearchStartState((0.0,1.0))

# Set heuristic
hC = tS.manhattenDistance2D([(7,3)])
hC = tS.manhattenDistance2D(g) # for Arena2
heuristic = hC.heuristicFun

   
print("DepthFirstSearch")
#treeSearch(problem, tS.DepthFirstSearch(problem, s))

print("BreathFirstSearch")
#treeSearch(problem, tS.BreathFirstSearch(problem, s))
    
print("UniformCostSearch")
#treeSearch(problem, tS.UniformCostSearch(problem, s))

print("GreedySearch")
#strategy = tS.GreedySearch(problem, heuristic)
#tS.treeSearch(problem, strategy)
#print('costs: ', strategy.currentFringe.getCostTotal())

print("AstarSearch")
strategy = tS.AstarSearch(problem, heuristic)
tS.treeSearch(problem, strategy)
print('costs: ', strategy.currentFringe.getCostTotal())
print('path: ', strategy.currentFringe.getPath())
