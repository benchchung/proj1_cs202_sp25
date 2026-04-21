import unittest
import math
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

    def test_seattle_area(self):
        self.assertAlmostEqual(area(seattle.region.rect), (6378.1**2) * abs((-122.224 * (math.pi/180)) - (-122.459 * (math.pi/180))) * abs(math.sin(47.734 * math.pi/180) - math.sin(47.495 * math.pi/180)),
        places=5)

    def test_maldives_emissionperkm(self):
        maldives_area = area(maldives.region.rect)
        self.assertAlmostEqual(emissions_per_square_km(maldives), 2500000/maldives_area, places = 5)

    def test_densest_of_the_four(self):
        self.assertEqual(densest(region_conditions), "Tokyo")


if __name__ == '__main__':
    unittest.main()
