import unittest
import traffic_light_system as tls


class TestLane(unittest.TestCase):
    def test_traffic_generator(self):
        test_lane = tls.Lane("A")
        self.assertTrue(isinstance(test_lane.traffic_volume, int))


if __name__ == '__main__':
    unittest.main()
