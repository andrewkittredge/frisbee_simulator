#! /usr/bin/python


'''

The field is 64m long with two 23m endzones, 37m wide.

'''

from __future__ import division
import random
import sys


class Catcher(object):
    '''Catches passes

    '''

    def catch(self, distance):
        success_rate = 1 - (distance / 110)
        rand = random.random()
        return rand <= success_rate

class DistanceChooser(object):
    '''How far will the team try to throw the disk?

    '''

    def __init__(self, 
                constant_distance=0.0, 
                percentage_of_distance_to_goal=0.0):

        self._constant_distance = constant_distance
        self._percentage_of_distance_to_goal= percentage_of_distance_to_goal

    def pass_distance(self, distance_from_goal):
        distance = self._constant_distance
        try:
            distance += (self._percentage_of_distance_to_goal /
                        distance_from_goal)
        except ZeroDivisionError:
            pass

        return distance


def simulate_possession(team, disk_position):
    '''Returns True if the team scores.
    Returns false and the position of the disk on a turn

    '''

    while True:

        pass_distance = team.pass_distance(disk_position)
        possession = team.catch_pass(pass_distance)

        disk_position -= pass_distance
        not_on_the_field = 87 < disk_position < -23

        if not possession or not_on_the_field:
            return False, disk_position

        if disk_position <= 0:
            return True, 0

class PointSimulator(object):
    def __init__(self, starting_disk_position=50):
        self.starting_disk_position = starting_disk_position

    def simulate_point(self, receiving_team, pulling_team):

        disk_position = self.starting_disk_position
        team_on_offense, team_on_defense = receiving_team, pulling_team

        while True:
            team_on_offense.possessions += 1
            point_scored, new_disk_position = simulate_possession(
                                                        team_on_offense,
                                                        disk_position,
                                                                )
            if point_scored: 
                team_on_offense.score += 1
                break

            else:
                team_on_offense, team_on_defense = (team_on_defense, 
                                                    team_on_offense)
                disk_position = 64.0 - new_disk_position


class GameSimulator(object):
    def __init__(self, simulate_point, teams):
        self.simulate_point = simulate_point
        self.teams = teams


    def simulate_game(self):

        teams = self.teams
        first_half = True

        receiving_team, pulling_team = teams
        receiving_team.score, pulling_team.score = 0, 0
        while True:
            self.simulate_point(receiving_team, pulling_team)
            for team in teams:
                if team.score == 15:
                    team.games_won += 1
                    return
                if team.score == 8 and first_half: #halftime
                    first_half = False
                    receiving_team, pulling_team = (pulling_team, 
                                                    receiving_team)

class Team(object):
    def __init__(self, decides_pass_distance, catcher):
        self.score = 0
        self.games_won = 0
        self._decides_pass_distance = decides_pass_distance
        self._catcher = catcher
        self.possessions = 0
        self.attempted_passes = 0
        

    def pass_distance(self, distance_to_goal):
        self.attempted_passes += 1
        return self._decides_pass_distance.pass_distance(distance_to_goal)

    def catch_pass(self, pass_distance):
        return self._catcher.catch(pass_distance)

def build_team(constant_distance, distance_to_goal):
    distance_chooser = DistanceChooser(constant_distance, distance_to_goal)
    return Team(distance_chooser, Catcher())
    
       


def main():

    games_to_simulate = 100

    teams = {'white': build_team(20, 0), 'black': build_team(10, 0)}

    point_simulator = PointSimulator()

    game_simulator = GameSimulator(point_simulator.simulate_point, 
                                                        teams.values())


    for i in xrange(0, games_to_simulate):
        game_simulator.simulate_game()

    for team_name, team in  teams.items():
        passes_per_possessions = team.attempted_passes / team.possessions
        str_args = (team_name, team.games_won, passes_per_possessions)
        print '%s won %s games, with %.02f passes per possession' % str_args



    return 0


if __name__ == '__main__':
    sys.exit(main())
