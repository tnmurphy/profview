#!/usr/bin/env python3
"""
Display a GNU Make profile as bars on a timeline

"""

import pygame
import pygame.gfxdraw as draw
from random import randint
from pygame import Rect
from profile import Profile
import sys
import pygame.locals
import pygame.colordict
import re


class TargetType:
    index = 0
    cache = {}
    classes = []

    def __init__(self, pattern: re.Pattern, description: str, colour: str):
        self.pattern = re.compile(pattern)
        self.description = description
        self.colour = pygame.colordict.THECOLORS[colour]

    @classmethod
    def lookup(cls, target: str):
        if target in cls.cache:
            return cls.cache[target]
        print(f"looking up {target=}")
        for t in cls.classes:
            print(f"trying {t.description}")
            if t.pattern.match(target) is not None:
                print(f"match {t.description}")
                cls.cache[target] = t
                return t


TargetType.classes = [
    TargetType(r".*\.h$", "generated C header", "yellow"),
    TargetType(r".*\.c$", "generated C source", "slateblue"),
    TargetType(r".*\.o$", "compiled object file", "tomato"),
    TargetType(r"^make$", "make", "wheat"),
    TargetType(r".*", "unknown", "green"),
]


def draw_profile(screen, profile):

    cpus = len(profile.notional_cpus)

    start_time, end_time = yield
    delta_t = float(screen_rect[2]) / (end_time - start_time)
    delta_y = screen_rect[3] / cpus

    while True:
        for cpu_idx in range(0, cpus):
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
                    target_type = TargetType.lookup(t[2])
                    pygame.draw.rect(screen, target_type.colour, r, width=3)
        start_time, end_time = yield
        delta_t = float(screen_rect[2]) / (end_time - start_time)
        delta_y = screen_rect[3] / cpus


def log_key(event):
    key = pygame.key.name(event.key)
    print(f"{event.key=}  {key=}  down")


def viewer_loop(pr: Profile, screen, screen_rect):
    running = True
    uptodate = False
    # Define the "viewport"
    start_time, end_time = pr.start_time, pr.end_time
    zoom = 0.0
    delta_t = 0.0

    lines = draw_profile(screen, pr)

    next(lines)  # start the generator

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.locals.K_UP:
                    zoom = 0.01
                elif event.key == pygame.locals.K_DOWN:
                    zoom = -0.01
                elif event.key == pygame.locals.K_LEFT:
                    delta_t = -0.01
                elif event.key == pygame.locals.K_RIGHT:
                    delta_t = 0.01
            elif event.type == pygame.KEYUP:
                if event.key == pygame.locals.K_UP:
                    zoom = 0.0
                elif event.key == pygame.locals.K_DOWN:
                    zoom = 0.0
                elif event.key == pygame.locals.K_LEFT:
                    delta_t = 0.0
                elif event.key == pygame.locals.K_RIGHT:
                    delta_t = 0.0

        if zoom != 0.0:
            print(f"{zoom=} {start_time=} {end_time=} ")
            uptodate = False
            start_time += zoom
            end_time -= zoom
            print(f"postzoom {start_time=} {end_time=} ")

        if delta_t != 0.0:
            uptodate = False
            start_time += delta_t
            end_time += delta_t

        if not uptodate:
            # fill the screen with a color to wipe away anything from last frame
            screen.fill("black")

            lines.send((start_time, end_time))

            # RENDER YOUR GAME HERE

            # flip() the display to put your work on screen
            pygame.display.flip()

            clock.tick(2400)  # limits FPS to 60

            uptodate = True


if __name__ == "__main__":
    # pygame setup
    pygame.init()
    screen_rect = [0, 0, 2000, 1000]
    screen = pygame.display.set_mode((screen_rect[2], screen_rect[3]))
    clock = pygame.time.Clock()
    pr = Profile.from_file(sys.argv[1])

    viewer_loop(pr, screen, screen_rect)

    pygame.quit()
