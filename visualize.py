import sys
import time
import pygame
from pygame.locals import *
from traffic_light_system import TrafficLights, TrafficLightController

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

WIDTH, HEIGHT = 800, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Automatic Traffic Controller")
background_image = "images/background.png"
background = pygame.image.load(background_image)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
LANE_POINTS = \
    {
        "A": (399, 102),
        "B": (660, 346),
        "C": (400, 573),
        "D": (121, 343)
    }
lane_colors = {lane: TrafficLights.RED for lane in LANE_POINTS}
font = pygame.font.SysFont("JetBrains Mono", 30)
TRAFFIC_LIGHT_RADIUS = 30
tlc = TrafficLightController()

while True:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())

    for index, lane in enumerate(LANE_POINTS):
        current_lane = tlc.lights.lanes[index]
        light_color = tlc.lights[current_lane]
        if light_color == TrafficLights.GREEN:
            duration_difference = tlc.green_duration - (int(time.time() - tlc.lights.last_green_times[current_lane]))
            text = font.render(str(duration_difference), 1, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (LANE_POINTS[lane][0], LANE_POINTS[lane][1]+45)
            screen.blit(text, textRect)
        traffic_volume = tlc.traffic[current_lane]
        text = font.render(str(traffic_volume), 1, (0, 0, 255))
        textRect = text.get_rect()
        textRect.center = (LANE_POINTS[lane][0]+45, LANE_POINTS[lane][1]+45)
        screen.blit(text, textRect)
        pygame.draw.circle(screen, tlc.lights[tlc.lights.lanes[index]], LANE_POINTS[lane], TRAFFIC_LIGHT_RADIUS)

    tlc.run()
    pygame.display.flip()
    fpsClock.tick(fps)
