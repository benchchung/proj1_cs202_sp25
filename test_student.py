import unittest
from proj1 import *
#proj1.py should contain your data class and function definitions
#these do not contribute positivly to your grade. 
#but your grade will be lowered if they are missing

class TestRegionFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_holder(self):
        pass

    def test_tokyo_emissionpercapita(self):
        self.assertAlmostEqual(emissions_per_capita(tokyo), 60000000/14000000, places=3)




if __name__ == '__main__':
    unittest.main()
