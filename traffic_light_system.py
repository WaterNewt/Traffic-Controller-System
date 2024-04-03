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
            line_number = frame.f_lineno
            self.lights[key] = value
            self.last_green_times[key] = time.time()
        elif value == self.RED:
            self.lights[key] = value
            self.last_green_times[key] = None

    def __repr__(self) -> str:
        return str(self.lights)


class TrafficLightController:
    MAX_GREEN_DURATION = 10
    MIN_GREEN_DURATION = 5

    def __init__(self, lanes: list['Lane'] = None) -> None:
        self.lights = TrafficLights(lanes if lanes is not None else [Lane('A'), Lane('B'), Lane('C'), Lane('D')])
        self.traffic = {lane: lane.traffic_volume for lane in self.lights.lanes}
        for traffic in self.traffic:
            if self.traffic[traffic] == max(self.traffic.values()):
                self.lights[traffic] = TrafficLights.GREEN
                break

    def run(self) -> None:
        current_time = time.time()
        last_green_times = self.lights.last_green_times
        for index, lane in enumerate(self.lights.lanes):
            if last_green_times[lane] is not None:
                if (current_time - last_green_times[lane]) >= self.MAX_GREEN_DURATION:
                    self.lights[lane] = TrafficLights.RED
                    try:
                        next_lane = self.lights.lanes[index+1]
                    except IndexError:
                        next_lane = self.lights.lanes[0]
                    self.lights[next_lane] = TrafficLights.GREEN
                elif self.traffic[lane] != max(self.traffic.values()) and (last_green_times[lane] - current_time) >= self.MIN_GREEN_DURATION:
                    self.lights[lane] = TrafficLights.RED
                    for traffic in self.traffic:
                        if self.traffic[traffic] == max(self.traffic.values()):
                            self.lights[traffic] = TrafficLights.GREEN
                            break
            else:
                self.lights[lane] = TrafficLights.RED
