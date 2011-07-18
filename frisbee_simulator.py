#! /usr/bin/python


'''

The field is 64m long with two 23m endzones, 37m wide.

'''

from __future__ import division
import random
import sys




def pass_caught(distance):
    '''Returns True if a pass is caught
    The probability of success is only a function of distance of the pass.

    '''

    success_rate = distance / 100
    rand = random.random()
    return rand <= success_rate


class PossessionSimulator(object):

    def __init__(self, 
                 pass_distance_generator, 
                 pass_success_calculator):

        self.generate_pass_distance = pass_distance_generator
        self.pass_caught = pass_success_calculator

    def simulate_possession(self, disk_position):
        while True:

            pass_distance = self.generate_pass_distance()
            possession = self.pass_caught(pass_distance)

            disk_position -= pass_distance
            not_on_the_field = 87 < disk_position < -23

            if not possession or not_on_the_field:
                return False, disk_position

            if disk_position <= 0:
                return (True, False)

class Team(object):
    def __init__(self):
        self.score = 0
        self.games_won = 0

class GameSimulator(object):
    def __init__(self, simulate_point, teams):
        self.simulate_point = simulate_point
        self.teams = teams


    def simulate_game(self):

        teams = self.teams

        receiving_team, pulling_team = teams
        receiving_team.score, pulling_team.score = 0, 0
        while True:
            self.simulate_point(receiving_team, pulling_team)
            for team in teams:
                if team.score == 15:
                    team.games_won += 1
                    return
        

class PointSimulator(object):
    def __init__(self, simulate_possession, starting_disk_position=50):
        self.simulate_possession = simulate_possession
        self.starting_disk_position = starting_disk_position

    def simulate_point(self, receiving_team, pulling_team):
        '''Returns True if white scores, False if black scores.

        starting_disk_position represents where the pull is caught.

        '''

        disk_position = self.starting_disk_position
        team_on_offense, team_on_defense = receiving_team, pulling_team

        while True:
            point_scored, new_disk_position = self.simulate_possession(
                                                        disk_position
                                                                )
            if point_scored: 
                team_on_offense.score += 1
                break

            else:
                team_on_offense, team_on_defense = (team_on_defense, 
                                                    team_on_offense)
                disk_position = 64.0 - new_disk_position
        


def main():

    games_to_simulate = 1000

    possession_simulator = PossessionSimulator(
                    pass_distance_generator=lambda : random.gauss(40, 80),
                    pass_success_calculator=pass_caught
                                              )

    teams = {'white': Team(), 'black': Team()}

    point_simulator = PointSimulator(
                                possession_simulator.simulate_possession)

    game_simulator = GameSimulator(point_simulator.simulate_point, 
                                                        teams.values())


    for i in xrange(0, games_to_simulate):
        game_simulator.simulate_game()

    out_str = ( teams.items()[0][0],
                teams.items()[0][1].games_won,
                teams.items()[1][0],
                teams.items()[1][1].games_won,
              )


    print '%s team won %s games, %s team won %s games' % out_str



    return 0


if __name__ == '__main__':
    sys.exit(main())
