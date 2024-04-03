import sys
import pygame
from pygame.locals import *
from traffic_light_system import TrafficLights, TrafficLightController

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

WIDTH, HEIGHT = 800, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
        pygame.draw.circle(screen, tlc.lights[tlc.lights.lanes[index]], LANE_POINTS[lane], TRAFFIC_LIGHT_RADIUS)

    tlc.run()
    pygame.display.flip()
    fpsClock.tick(fps)
