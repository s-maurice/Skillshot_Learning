import math

import numpy as np

from Player import Player


class SkillshotGame(object):

    def __init__(self):
        self.board_size = (250, 250)
        self.board = np.zeros(self.board_size, dtype=int)

        self.player1 = Player([50, 50], self.board_size, 1)
        self.player2 = Player([200, 200], self.board_size, 2)

        self.ticks = 0
        self.game_live = True

    def get_board(self):
        board = self.board.copy()
        # append players and projectiles
        for player, player_colour_index, pointer_colour_index in zip((self.player1, self.player2), [1, 2], [3, 4]):
            # player and direction indicator
            for index_y, row in enumerate(player.shape_image):
                for index_x, item in enumerate(row):
                    # append player
                    if item is not 0:
                        board[index_x + player.pos[0], index_y + player.pos[1]] = player_colour_index
                    # append direction indicator
                    if (index_x == math.floor(-math.sin(player.rotation) * player.shape_size[0] / 2 + player.shape_size[0] / 2) and
                            index_y == math.floor(-math.cos(player.rotation) * player.shape_size[1] / 2 + player.shape_size[1] / 2)):
                        board[index_x + player.pos[0], index_y + player.pos[1]] = pointer_colour_index
            # projectile - if valid
            if player.projectile.valid:
                for index_y, row in enumerate(player.projectile.shape_image):
                    for index_x, item in enumerate(row):
                        if item is not 0:
                            board[index_x + player.projectile.pos[0], index_y + player.projectile.pos[1]] = pointer_colour_index
        return board

    def check_collision(self):
        # check for player touching projectile 
        for player, enemy_projectile in (self.player1, self.player2.projectile), (self.player2, self.player1.projectile):
            # check only if the enemy projectile if valid
            if enemy_projectile.valid:
                # player
                player_left = player.pos[0]  # left side
                player_right = player.pos[0] + player.shape_size[0]  # right side
                player_top = player.pos[1]  # top side
                player_bottom = player.pos[1] + player.shape_size[1]  # bottom side
                # projectile
                projectile_left = enemy_projectile.pos[0]  # left side
                projectile_right = enemy_projectile.pos[0] + enemy_projectile.shape_size[0]  # right side
                projectile_top = enemy_projectile.pos[1]  # top side
                projectile_bottom = enemy_projectile.pos[1] - enemy_projectile.shape_size[1]  # bottom side
        
                # manually go through the 4 combinations
                if player_left <= projectile_right <= player_right and player_top <= projectile_top <= player_bottom:
                    print("Player", player.id, "loss")
                    self.game_live = False
                    break
                elif player_left <= projectile_right <= player_right and player_top <= projectile_bottom <= player_bottom:
                    print("Player", player.id, "loss")
                    self.game_live = False
                    break
                elif player_left <= projectile_left <= player_right and player_top <= projectile_top <= player_bottom:
                    print("Player", player.id, "loss")
                    self.game_live = False
                    break
                elif player_left <= projectile_left <= player_right and player_top <= projectile_bottom <= player_bottom:
                    print("Player", player.id, "loss")
                    self.game_live = False
                    break

    def game_tick(self):
        # check if game if live
        if self.game_live:
            # ticks the game by one, moving projectiles, etc
            self.ticks += 1
            for player in [self.player1, self.player2]:
                player.projectile.move_forwards()
                player.projectile_cooldown_current -= 1
            self.check_collision()

    @staticmethod
    def get_dist_line_point(line_gradient, line_point, comparison_point):
        # returns the minimum distance between a line and a point
        # first convert the line to ax+by+c=0 form
        c = (line_point[1] - line_gradient * line_point[0])
        # c=c, b=-1, a=line_gradient
        return abs(line_gradient * comparison_point[0] - comparison_point[1] + c) / math.sqrt(line_gradient**2 + 1)

    @staticmethod
    def get_dist_point_point(point1, point2):
        return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5

    def get_state(self):
        # collects the game state and returns 2 dicts (one for each player) with all the features for model use
        for player, opponent_player in (self.player1, self.player2), (self.player2, self.player1):
            # player features
            player_grad_dir_dict = player.get_gradient_dir()
            self.get_dist_line_point(player_grad_dir_dict.get("gradient"), player.pos, opponent_player.pos)  # min distance from a point on this line to opponent
            player.pos[0]
            player.pos[1]
            player.rotation

            # player's projectile features
            player.projectile_cooldown_current
            projectile_grad_dir_dict = player.projectile.get_gradient_dir()
            self.get_dist_line_point(projectile_grad_dir_dict.get("gradient"), player.projectile.pos, opponent_player.pos)  # min distance from a point on this line to opponent
            player.projectile.pos[0]
            player.projectile.pos[1]
            player.projectile.rotation
            self.get_dist_point_point(player.projectile.pos, opponent_player.pos)  # distance between projectile and opponent
            # is projectile going to hit opponent

    def game_reset(self):
        self.__init__()
