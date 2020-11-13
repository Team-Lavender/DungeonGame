from game import *
import pygame
from player import *

vector = pygame.math.Vector2
MAX_SPEED = 10
RADIUS = 200


# make step
# add dialogue
# add audio
# try to control other characters

class CutSceneManager:
    def __init__(self, game, actors, waypoints, i):
        self.game = game
        self.i = i
        self.actors = actors
        self.acc = vector(0, 0)
        self.vel = vector(MAX_SPEED, 0)
        self.waypoints = waypoints
        self.waypoint_index = 0
        self.target = self.waypoints[self.waypoint_index]
        self.distance_from_target = 999999

    def insert_black_borders(self):

        pygame.draw.rect(self.game.window, [0, 0, 0], [0, 0, 1280, 120], 0)
        pygame.draw.rect(self.game.window, [0, 0, 0], [0, 600, 1280, 120], 0)
        pygame.display.update()

    def update(self, pos):

        pos = vector(pos)
        if self.game.cutscene_trigger:
            self.acc = (self.target - pos).normalize() * 0.5
            self.insert_black_borders()

            # Update the distance from the target and find the length of the vector
            self.distance_from_target = self.target - pos
            test = self.distance_from_target.length()
            if test < 20 and self.waypoint_index < len(self.waypoints) - 1:
                self.waypoint_index += 1
                self.target = self.waypoints[self.waypoint_index]



            # remove the wobbling
            if test < RADIUS:
                # If we're approaching the target, we slow down.
                self.vel = self.distance_from_target * (test / RADIUS * MAX_SPEED * 4)
            else:  # Otherwise move with max_speed.
                self.vel = self.distance_from_target * MAX_SPEED

            self.vel += self.acc
            if self.vel.length() > MAX_SPEED:
                self.vel.scale_to_length(MAX_SPEED)
            pos += self.vel
            self.game.curr_actors[self.i].pos_x = pos[0]
            self.game.curr_actors[self.i].pos_y = pos[1]

            #print(self.waypoint_index,len(self.waypoints) )
            if self.waypoint_index + 1 == len(self.waypoints) :
                self.game.cutscene_trigger = False
