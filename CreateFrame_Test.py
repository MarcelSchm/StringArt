import unittest
import math
from CreateFrame import calc_point_distance

class TestCalcDistance(unittest.TestCase):

    def test_calc_point_distance(self):
        x1,y1 = point1 = (0, 0)
        x2,y2 = point2 = (3, 4)
        expected_distance = 5.0
        calc_distance = calc_point_distance(x1,y1,x2,y2)
        self.assertEqual(expected_distance, calc_distance)

    def test_calc_point_distance_negative(self):
        x1,y1 = point1 = (1, 1)
        x2,y2 = point2 = (4, 5)
        expected_distance = 5.0
        calc_distance = calc_point_distance(x1,y1,x2,y2)
        self.assertEqual(expected_distance, calc_distance)
            
    def test_calc_point_distance_negative_points(self):
        x1,y1 = point1 = (-1, -1)
        x2,y2 = point2 = (4, 2)
        expected_distance = 5.830951894845301
        calc_distance = calc_point_distance(x1,y1,x2,y2)
        self.assertEqual(expected_distance, calc_distance)
    
    def test_calc_point_distance_NaN(self):
        x1,y1 = point1 = ('f', -1)
        x2,y2 = point2 = (4, 2)
        expected_distance = float('NaN')
        calc_distance = calc_point_distance(x1,y1,x2,y2)
        self.assertTrue(math.isnan(calc_distance))

if __name__ == '__main__':
    unittest.main()