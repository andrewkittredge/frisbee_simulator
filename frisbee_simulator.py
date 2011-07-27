#! /usr/bin/python


'''

The field is 64m long with two 23m endzones, 37m wide.

'''

from __future__ import division
import random
import sys

DROP_CONSTANT=.94

CATCH_PROBABILITY_FUNC = lambda distance : (1 - ( distance / 110) * .5) * DROP_CONSTANT


class Catcher(object):
    '''Catches passes

    '''

    def catch(self, distance):
        success_rate = CATCH_PROBABILITY_FUNC(distance)
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

class Team(object):
    def __init__(self, decides_pass_distance, catcher):
        self._decides_pass_distance = decides_pass_distance
        self._catcher = catcher
        self.possessions = 0
        self.attempted_passes = 0
        self.total_points_scored = 0
        self._score = 0
        self.games_won = 0
        

    def pass_distance(self, distance_to_goal):
        self.attempted_passes += 1
        return self._decides_pass_distance.pass_distance(distance_to_goal)

    def catch_pass(self, pass_distance):
        return self._catcher.catch(pass_distance)

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if value != self._score + 1 and value != 0:
            raise Exception('can only increment score by 1')
        self._score = value
        self.total_points_scored += 1


    @property
    def passes_per_possession(self):
        return self.attempted_passes / self.possessions

    @property
    def possessions_per_point(self):
        return self.possessions / self.total_points_scored

def simulate_possession(team, disk_position):
    '''Returns True if the team scores.
    Returns false and the position of the disk on a turn.

    '''

    team.possessions += 1
    possession = True
    scored = False

    while possession and not scored:

        pass_distance = team.pass_distance(disk_position)
        possession = team.catch_pass(pass_distance)

        disk_position -= pass_distance

        #Threw it out the back, other team gets the disk at the top of the 
        #end-zone
        if disk_position < -23.0:
            possession = False
            disk_position = 0

        #Went out of back of end zone, not sure what the rule is. 
        if disk_position > 87:
            possession = False
            disk_position = 64

        if -23.0 < disk_position < 0.0:
            scored = True

    return scored, disk_position

class PointSimulator(object):
    def __init__(self, starting_disk_position=50):
        self.starting_disk_position = starting_disk_position

    def simulate_point(self, receiving_team, pulling_team):
        '''Simulate a point.
        
        Returns the teams that scored.

        '''

        disk_position = self.starting_disk_position
        offense = receiving_team 
        defense = pulling_team
        scored = False

        scored, new_disk_position = simulate_possession(
                                                    offense,
                                                    disk_position,
                                                        )

        while not scored:
            offense, defense = defense, offense
            disk_position = 64.0 - new_disk_position

            scored, new_disk_position = simulate_possession(
                                                    offense,
                                                    disk_position,
                                                            )

        offense.score += 1
        return offense


class GameSimulator(object):
    def __init__(self, simulate_point):
        self.simulate_point = simulate_point


    def simulate_game(self, teams):
        '''Returns the winning team.


        '''

        first_half = True
        last_score = 0

        receiving, pulling = teams
        receiving.score, pulling.score = 0, 0
        
        while last_score <= 15:

            scored = self.simulate_point(receiving, pulling)
            last_score = scored.score
            pulling, receiving = teams if teams[0] == scored else reversed(teams)

            if last_score == 8 and first_half:
                first_half = False
                receiving, pulling = pulling, receiving
        
        return scored

def simulate_games(team_1_distance, 
                   team_2_distance,
                   games_to_simulate=1000):

    '''Facade that build Teams and simulates games between them.

    team_distance arguments are the distances the teams will try
    to throw the disk.

    '''
    
    team_1_distance_chooser = DistanceChooser(team_1_distance)
    team_2_distance_chooser = DistanceChooser(team_2_distance)

    team_1_catcher = Catcher()
    team_2_catcher = Catcher()

    team_1 = Team(team_1_distance_chooser, team_1_catcher)
    team_2 = Team(team_2_distance_chooser, team_2_catcher)

    teams = (team_1, team_2)

    point_simulator = PointSimulator()
    game_simulator = GameSimulator(point_simulator.simulate_point)
       
    for i in xrange(0, games_to_simulate):
        winner = game_simulator.simulate_game(teams)
        winner.games_won += 1

    return teams

def team_results_string(team):
    str_args = (team.games_won, 
                team.passes_per_possession, 
                team.possessions_per_point)

    return 'won %s games, with %.02f passes per possession, %.02f posessions per point' % str_args

def main():
    teams = simulate_games(*map(float, sys.argv[1:3]))
    for team_name, team in  zip(('team_1', 'team_2'), teams):
        print '%s: %s' % (team_name, team_results_string(team))

    return 0


if __name__ == '__main__':
    sys.exit(main())
