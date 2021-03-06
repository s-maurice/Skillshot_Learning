import math


class Projectile(object):
    shape_image = [[1, 0, 1],
                   [0, 1, 0],
                   [1, 0, 1]]

    cooldown_max = 15
    speed_move = 5

    def __init__(self, location, board_dim):
        self.pos = list(location)
        self.rotation = 0

        self.cooldown_current = 0
        self.age = 0
        self.valid = False
        self.board_dim = board_dim
        self.shape_size = (len(self.shape_image[0]), len(self.shape_image))

    def set_position(self, location):
        # location given as tuple or list, sets the location of the projectile to the given location
        self.pos = list(location)

    def set_rotation(self, rotation):
        # sets the direction of the projectile, using gradient
        self.rotation = rotation

    def check_pos_valid(self, check_x, check_y):
        # checks if a position if within the board bounds
        if (check_x + self.shape_size[0] <= self.board_dim[0] and check_x >= 0 and
                check_y + self.shape_size[1] <= self.board_dim[1] and check_y >= 0):
            return True
        else:
            return False

    def move_forwards(self):
        # moves the projectile forwards by self.speed_move for every time its called (each tick)
        new_pos_x = int(round(self.pos[0] - math.sin(self.rotation) * self.speed_move))
        new_pos_y = int(round(self.pos[1] - math.cos(self.rotation) * self.speed_move))

        if self.valid and self.check_pos_valid(new_pos_x, new_pos_y):
            self.pos[0] = new_pos_x
            self.pos[1] = new_pos_y
        else:
            self.valid = False

    def tick(self):
        # called every game tick, ticks the whole projectile class
        self.move_forwards()
        self.cooldown_current -= 1
        self.age += 1

    def get_gradient_dir(self):
        # gets the current gradient of the projectile
        # convert rotation in radians to gradient
        gradient = math.tan(-self.rotation + math.pi / 2)
        # get the x_dir using sin, round away from 0 to 1 or -1
        x_dir = 1 if -math.sin(self.rotation) >= 0 else -1
        # calculate y-intercept
        y_intercept = self.pos[1] - gradient * self.pos[0]

        return dict(gradient=gradient, x_dir=x_dir, y_intercept=y_intercept)
