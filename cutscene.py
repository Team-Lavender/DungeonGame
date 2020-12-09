from game import *
import pygame
from player import *
from cutscene_lookup import *
from config import *
from dialogue import *
vector = pygame.math.Vector2
RADIUS = 200

#TODO: Do not allow player to shoot in cutscene
#      Fix enemy targeting in index
#      Fix player positioning (facing the right way)
#      Add audio



class CutSceneManager:
    def __init__(self, game):
        self.game = game
        self.MAX_SPEED = 2.5
        self.acc = vector(0, 0)
        self.vel = vector(self.MAX_SPEED, 0)
        self.waypoint_index = 0
        self.dialogue_index = 0
        self.scenario_index = 0
        self.distance_from_target = 999999
        self.triggered_cutscene = []
        self.last_iteration = 0
        self.completed_cutscenes = []

    def insert_black_borders(self):

        # TODO: add transition
        pygame.draw.rect(self.game.window, [0, 0, 0], [0, 0, 1280, 65], 0)
        pygame.draw.rect(self.game.window, [0, 0, 0], [0, 600, 1280, 120], 0)


    def update(self, cutscene_number):
        # Check if the current cutscene is not 0 and the cutscene number is not completed
        if self.game.current_cutscene != 0 and cutscene_number not in self.completed_cutscenes:
            self.cutscene_checks(cutscene_number)
            # Perform cutscene operations
            if self.game.cutscene_trigger:
                cutscene = cutscene_lookup_dict[cutscene_number]  # from here we get the first subdict
                #actors = self.game.curr_actors[cutscene[self.scenario_index][0][0]]
                actors = self.game.curr_actors[self.game.get_npc_index()]
                pos = (actors.pos_x, actors.pos_y)
                waypoints = cutscene[self.scenario_index][1]

                #i = cutscene[self.scenario_index][0][0]
                i = self.game.get_npc_index()
                # if i == ncp_index:
                # i = npc_index
                # else
                dialogue = cutscene[self.scenario_index][2]
                target = waypoints[self.waypoint_index]
                #print(target)
                current_dialogue = dialogue[self.dialogue_index]
                #print(current_dialogue)
                pos = vector(pos)
                self.acc = (target - pos).normalize() * 0.5
                self.insert_black_borders()

                # Update the distance from the target and find the length of the vector
                self.distance_from_target = target - pos
                distance_vector_length = self.distance_from_target.length()


                # When we are close to the target slow down to display dialogue
                if distance_vector_length < 100 : #and self.waypoint_index < len(waypoints) - 1:
                    if current_dialogue != '':
                        self.MAX_SPEED = 0.8
                        text = StaticText(self.game, WHITE)
                        text.display_text_dialogue(actors, current_dialogue)
                        pygame.display.update()

                    # When we have reached the waypoint increment the index to go to the next waypoint
                    if distance_vector_length < 20:
                        self.MAX_SPEED = 2.5
                        self.waypoint_index += 1
                        self.dialogue_index += 1
                        target = waypoints[self.waypoint_index]

                # remove the wobbling
                # TODO: to refactor
                if distance_vector_length < RADIUS:
                    # If we're approaching the target, we slow down.
                    self.vel = self.distance_from_target * (distance_vector_length / RADIUS * self.MAX_SPEED * 4)
                else:  # Otherwise move with max_speed.
                    self.vel = self.distance_from_target * self.MAX_SPEED

                # set the new position
                self.vel += self.acc
                if self.vel.length() > self.MAX_SPEED:
                    self.vel.scale_to_length(self.MAX_SPEED)
                pos += self.vel
                self.game.curr_actors[i].pos_x = pos[0]
                self.game.curr_actors[i].pos_y = pos[1]



    def reset(self):
        self.MAX_SPEED = 2.5
        self.acc = vector(0, 0)
        self.vel = vector(self.MAX_SPEED, 0)
        self.waypoint_index = 0
        self.dialogue_index = 0
        self.distance_from_target = 999999
        self.last_iteration = 0
        self.game.current_cutscene = 0
        self.game.cutscene_trigger = False
        self.scenario_index = 0

    def cutscene_checks(self, cutscene_number):
        # Check if we have finished going through all the cutscene waypoints
        if self.waypoint_index == len(cutscene_lookup_dict[cutscene_number][self.scenario_index][1])-1:

            # Reset the waypoint and dialogue index for the next scenario
            self.waypoint_index = 0
            self.dialogue_index = 0

            # If we are not at the last scenario, increment the scenario
            if self.scenario_index < len(cutscene_lookup_dict[cutscene_number]) - 1:
                self.scenario_index += 1

            # Else add the cutscene to completed cutscenes and reset fields
            else:
                # Once finished add the current cutscene to completed cutscenes
                self.completed_cutscenes.append(cutscene_number)
                self.reset()
