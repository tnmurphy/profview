#!/usr/bin/env python3
"""
Display a GNU Make profile as bars
"""

import pygame
import pygame.gfxdraw as draw
from random import randint
from pygame import Rect
from profile import Profile
import sys

# pygame setup
pygame.init()
screen_rect = [0, 0, 2000, 1000]
screen = pygame.display.set_mode((screen_rect[2], screen_rect[3]))
clock = pygame.time.Clock()
running = True
pr = Profile.from_file(sys.argv[1])


def draw_profile(screen, profile, start_time, end_time):
    colors = [
        pygame.Color(255, 100, 0),
        pygame.Color(0, 200, 0),
        pygame.Color(0, 200, 100),
        pygame.Color(100, 100, 0),
        pygame.Color(200, 200, 200),
    ]

    delta_t = float(screen_rect[2]) / (end_time - start_time)
    cpus = len(profile.notional_cpus)
    delta_y = screen_rect[3] / cpus

    while True:
        for cpu_idx in range(0, cpus):
            colidx = 0
            y1 = cpu_idx * delta_y + 10
            height = delta_y - 20
            targets = profile.notional_cpus[cpu_idx]
            for t_idx in range(0, len(targets)):
                t = targets[t_idx]
                if t[0] >= start_time:
                    reltime = t[0] - pr.start_time
                    x1 = reltime * delta_t
                    width = t[1] * delta_t
                    r = Rect(x1, y1, width, height)
                    pygame.draw.rect(screen, colors[colidx], r, width=3)
                    colidx = (colidx + 1) % len(colors)

        yield


lines = draw_profile(screen, pr, pr.start_time, pr.end_time)

uptodate = False
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not uptodate:
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        lines.__next__()

        # RENDER YOUR GAME HERE

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(2400)  # limits FPS to 60

        uptodate = True

pygame.quit()
