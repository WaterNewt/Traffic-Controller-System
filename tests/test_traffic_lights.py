import unittest
import traffic_light_system as tls


class TestRaises(unittest.TestCase):
    def setUp(self):
        self.lanes = [tls.Lane('A'), tls.Lane('B'), tls.Lane('C'), tls.Lane('D')]
        self.traffic_lights = tls.TrafficLights(self.lanes)

    def test_get_item(self):
        with self.assertRaisesRegex(ValueError, "Invalid lane"):
            _ = self.traffic_lights[None]

    def test_set_item(self):
        with self.assertRaisesRegex(ValueError, "Invalid lane"):
            self.traffic_lights['Test'] = None


class TestTrafficLights(unittest.TestCase):
    def setUp(self):
        self.lanes = [tls.Lane('A'), tls.Lane('B'), tls.Lane('C'), tls.Lane('D')]
        self.traffic_lights = tls.TrafficLights(self.lanes)

    def test_greent_times(self):
        self.traffic_lights[self.lanes[0]] = self.traffic_lights.GREEN
        self.assertFalse(self.traffic_lights.last_green_times[self.lanes[0]] is None)
        self.traffic_lights[self.lanes[1]] = self.traffic_lights.RED
        self.assertTrue(self.traffic_lights.last_green_times[self.lanes[1]] is None)


if __name__ == '__main__':
    unittest.main()
