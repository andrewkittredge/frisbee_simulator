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
        possession = True
        while True:

            pass_distance = self.generate_pass_distance()
            possession = self.pass_caught(pass_distance)

            disk_position -= pass_distance
            not_on_the_field = 87 < disk_position < -23

            if not possession or not_on_the_field:
                return False, disk_position

            if disk_position <= 0:
                return (True, False)

class GameSimulator(object):
    def __init__(self, simulate_point):
        self.simulate_point = simulate_point


    def simulate_game(self):
        ''' Returns True if the white team won, False if the black team won

        '''
        white_score, black_score = 0, 0

        while white_score < 15 and black_score < 15:
            white_scored  = self.simulate_point()
            if white_scored: white_score += 1
            else: black_score += 1

        return white_score > black_score

class PointSimulator(object):
    def __init__(self, simulate_possession, starting_disk_position=50):
        self.simulate_possession = simulate_possession
        self.starting_disk_position = starting_disk_position

    def simulate_point(self):
        '''Returns True if white scores, False if black scores.

        starting_disk_position represents where the pull is caught.

        '''

        white_scored = True
        disk_position = self.starting_disk_position

        while True:
            point_scored, new_disk_position = self.simulate_possession(
                                                        disk_position
                                                                )
            if point_scored:
                return white_scored

            else:
                white_scored = not white_scored
                disk_position = 64.0 - new_disk_position
        


def main():

    games_to_simulate = 10000
    white_team_games_won = 0
    possession_simulator = PossessionSimulator(
                    pass_distance_generator=lambda : random.gauss(40, 80),
                    pass_success_calculator=pass_caught
                                              )

    point_simulator = PointSimulator(
                                possession_simulator.simulate_possession)

    game_simulator = GameSimulator(point_simulator.simulate_point)


    for i in xrange(0, games_to_simulate):
        if game_simulator.simulate_game():
            white_team_games_won += 1

    black_team_games_won = games_to_simulate - white_team_games_won
    print 'White team won %s games, back team won %s games' % (
                                                    white_team_games_won,
                                                    black_team_games_won
                                                                )

    return 0


if __name__ == '__main__':
    sys.exit(main())
