import time
import random
import inspect


class Lane:
    def __init__(self, lane_name: str, traffic_volume: int = None) -> None:
        self.lane_name = lane_name
        self.traffic_volume = traffic_volume if traffic_volume is not None else random.randint(0, 10)

    def __repr__(self) -> str:
        return str(self.lane_name)


class TrafficLights:
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    def __init__(self, lanes: list['Lane']) -> None:
        self.lanes = lanes
        self.lights = {lane: self.RED for lane in self.lanes}
        self.last_green_times = {lane: None for lane in self.lanes}

    def __getitem__(self, item) -> str:
        for lane in self.lanes:
            if item == lane:
                return self.lights[lane]
        raise ValueError("Invalid lane")

    def __setitem__(self, key, value) -> None:
        if key not in self.lanes:
            raise ValueError("Invalid lane")
        if value == self.GREEN:
            frame = inspect.currentframe().f_back
            self.lights[key] = value
            self.last_green_times[key] = time.time()
        elif value == self.RED:
            self.lights[key] = value
            self.last_green_times[key] = None

    def __repr__(self) -> str:
        return str(self.lights)


def next_index(array: list | tuple | set, index: int, incrementer: int = 1):
    last_index = len(array) - 1
    result_index = index + incrementer
    if result_index > last_index:
        return result_index - len(array)
    else:
        return result_index


class TrafficLightController:
    MAX_GREEN_DURATION = 10
    DURATION_MULTIPLIER = 3

    def __init__(self, lanes: list['Lane'] = None) -> None:
        self.lights = TrafficLights(lanes if lanes is not None else [Lane('A'), Lane('B'), Lane('C'), Lane('D')])  # The traffic light colors for all the lanes
        self.traffic = {lane: lane.traffic_volume for lane in self.lights.lanes}
        self.green_duration = self.MAX_GREEN_DURATION
        for index, traffic in enumerate(self.traffic):
            if self.traffic[traffic] == max(self.traffic.values()):
                parallel_lane = list(self.traffic.keys())[next_index(list(self.traffic.values()), index, 2)]
                self.lights[traffic] = TrafficLights.GREEN
                self.lights[parallel_lane] = TrafficLights.GREEN
                break

    def green_light_duration(self, num_cars_waiting, car_throughput_time):
        if num_cars_waiting == 0:
            return 0
        max_cars_through = int(self.MAX_GREEN_DURATION / car_throughput_time)
        cars_to_accommodate = min(num_cars_waiting, max_cars_through)
        time_needed = cars_to_accommodate * car_throughput_time
        safety_buffer = 5
        green_light_duration = time_needed + safety_buffer

        return green_light_duration

    def run(self) -> None:
        current_time = time.time()
        last_green_times = self.lights.last_green_times  # A dictionary with the "unix epochs" of when lanes have been turned Green.
        lanes = self.lights.lanes  # List of all the lanes
        for index, lane in enumerate(lanes):
            parallel_lane = list(self.traffic.keys())[next_index(list(self.traffic.values()), index, 2)]
            if last_green_times[lane] is not None:
                # Will change the traffic light of the current lane to RED, and then change the traffic light of the next lane to GREEN
                # The duration of the green light is calculated with the `green_light_duration` function.
                traffic_volumes = sum([self.traffic[parallel_lane], self.traffic[lane]])
                self.green_duration = self.green_light_duration(traffic_volumes, 3)
                if (current_time - last_green_times[lane]) >= self.green_duration:
                    self.lights[lane] = TrafficLights.RED
                    self.lights[parallel_lane] = TrafficLights.RED
                    next_lane_index = next_index(lanes, index, 1)
                    next_lane = lanes[next_index(lanes, index, 1)]
                    next_parrallel_lane = list(self.traffic.keys())[next_index(list(self.traffic.values()), next_lane_index, 2)]
                    self.lights[next_lane] = TrafficLights.GREEN
                    self.lights[next_parrallel_lane] = TrafficLights.GREEN
            else:
                self.lights[lane] = TrafficLights.RED
