import unittest
import treeSearch

class DepthFirstSearchTests(unittest.TestCase):

    def testSearchMainTestSearch(self):
        result = ['S', 'd', 'e', 'r', 'f', 'G']

        problem = treeSearch.MainTestSearch()
        strategy = treeSearch.DepthFirstSearch(problem)
        treeSearch.treeSearch(problem, strategy)
        self.assertTrue(strategy.getCurrentFringe().getPath() == result)
        
    def testEasyTestSearchOne(self):
        result = ['S', 'A', 'G']

        problem = treeSearch.EasyTestSearchOne()
        strategy = treeSearch.DepthFirstSearch(problem)
        treeSearch.treeSearch(problem, strategy)
        self.assertTrue(strategy.getCurrentFringe().getPath() == result)        

    def testSearchSailProblem(self):
        result = [(4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (8, 3), (7, 3)]

        problem = treeSearch.SailProblem([(7,3)], 8, 8)
        strategy = treeSearch.DepthFirstSearch(problem)
        treeSearch.treeSearch(problem, strategy)
        self.assertTrue(strategy.getCurrentFringe().getPath() == result)
        
class BreathFirstSearchTests(unittest.TestCase):

    def testSearchMainTestSearch(self):
        result = ['S', 'e', 'r', 'f', 'G']

        problem = treeSearch.MainTestSearch()
        strategy = treeSearch.BreathFirstSearch(problem)
        treeSearch.treeSearch(problem, strategy)
        self.assertTrue(strategy.getCurrentFringe().getPath() == result)
        
    def testEasyTestSearchOne(self):
        result = ['S', 'G']

        problem = treeSearch.EasyTestSearchOne()
        strategy = treeSearch.BreathFirstSearch(problem)
        treeSearch.treeSearch(problem, strategy)
        self.assertTrue(strategy.getCurrentFringe().getPath() == result)        

    def testSearchSailProblem(self):
        result = [(4, 4), (5, 4), (6, 4), (7, 4), (7, 3)]

        problem = treeSearch.SailProblem([(7,3)], 8, 8)
        strategy = treeSearch.BreathFirstSearch(problem)
        treeSearch.treeSearch(problem, strategy)
        self.assertTrue(strategy.getCurrentFringe().getPath() == result) 
        
class UniformCostSearchTest(unittest.TestCase):

    def testSearchMainTestSearch(self):
        result = ['S', 'd', 'e', 'r', 'f', 'G']

        problem = treeSearch.MainTestSearch()
        strategy = treeSearch.UniformCostSearch(problem)
        treeSearch.treeSearch(problem, strategy)
        self.assertTrue(strategy.getCurrentFringe().getPath() == result)
        
    def testEasyTestSearchOne(self):
        result = ['S', 'A', 'G']

        problem = treeSearch.EasyTestSearchOne()
        strategy = treeSearch.UniformCostSearch(problem)
        treeSearch.treeSearch(problem, strategy)
        self.assertTrue(strategy.getCurrentFringe().getPath() == result)        

    def testSearchSailProblem(self):
        result = [(4, 4), (5, 4), (6, 4), (7, 4), (7, 3)]

        problem = treeSearch.SailProblem([(7,3)], 8, 8)
        strategy = treeSearch.UniformCostSearch(problem)
        treeSearch.treeSearch(problem, strategy)
        self.assertTrue(strategy.getCurrentFringe().getPath() == result)    
        
def main():
    unittest.main()

if __name__ == '__main__':
    main()