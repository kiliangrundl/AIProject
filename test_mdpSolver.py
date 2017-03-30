import mdp
import mdpSolver

problem = mdp.GridWorldProblem() # mdp.RacingProblem()

vI = mdpSolver.ValueIterator(problem)
pI = mdpSolver.PolicyIterator(problem)

vI.run()
pI.run()


qLearner = mdpSolver.QLearner(problem)
qLearner.run()

mdp.printPolicy(vI.computePolicy())
mdp.printPolicy(pI.computePolicy())
mdp.printPolicy(qLearner.policy)