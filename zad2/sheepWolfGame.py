import random
import math


class Sheep:
    id = None
    x = None
    y = None

    def __init__(self, init_pos_limit, id):
        self.x = random.uniform(-init_pos_limit, init_pos_limit)
        self.y = random.uniform(-init_pos_limit, init_pos_limit)
        self.id = id


class Wolf:
    x = None
    y = None

    def __init__(self, start_position):
        self.x = start_position
        self.y = start_position


class WolfSheepGame:
    __number_of_turns = None
    __number_of_sheeps = None
    __init_pos_limit = None
    __sheep_move_dist = None
    __wolf_move_dist = None
    __sheeps_position = list()
    __wolf_position = list()

    def __init__(self, number_of_turns, number_of_sheeps, init_pos_limit, sheep_move_dist, wolf_move_dist):
        self.__number_of_turns = number_of_turns
        self.__number_of_sheeps = number_of_sheeps
        self.__init_pos_limit = init_pos_limit
        self.__sheep_move_dist = sheep_move_dist
        self.__wolf_move_dist = wolf_move_dist
        self.__wolf_position = Wolf(0)

        for sheep_numer in range(1, number_of_sheeps + 1):
            self.__sheeps_position.append(Sheep(self.__init_pos_limit, sheep_numer))

    def count_wolf_to_sheep_distance(self, sheep_position_x, sheep_position_y):
        x_square_distance = (sheep_position_x - self.__wolf_position.x) ** 2
        y_square_distance = (sheep_position_y - self.__wolf_position.y) ** 2
        distance = math.sqrt(x_square_distance + y_square_distance)
        return distance

    def select_closest_sheep(self):
        closest_sheep = self.__sheeps_position[0]
        closest_sheep_distance = self.count_wolf_to_sheep_distance(closest_sheep.x, closest_sheep.y)
        for sheep in self.__sheeps_position:
            distance = self.count_wolf_to_sheep_distance(sheep.x, sheep.y)
            if distance < closest_sheep_distance:
                closest_sheep = sheep
        return closest_sheep

    def move_sheeps(self):
        for sheep in self.__sheeps_position:
            random_position = random.randint(0, 3)
            # move to east
            if random_position == 0:
                sheep.x += self.__sheep_move_dist

            # move to west
            elif random_position == 1:
                sheep.x -= self.__sheep_move_dist

            # move to north
            elif random_position == 2:
                sheep.y += self.__sheep_move_dist

            # move to south
            elif random_position == 3:
                sheep.y -= self.__sheep_move_dist

    def check_if_wolf_in_range(self, sheep):
        if self.__wolf_move_dist >= self.count_wolf_to_sheep_distance(sheep.x, sheep.y):
            self.__sheeps_position.remove(sheep)
            print()
            print("Owca nr: " + str(sheep.id) + " zostala zjedzona!")
            print()
            return True
        else:
            return False

    def select_wolf_direction(self, sheep):
        x = sheep.x
        y = sheep.y
        distance = self.count_wolf_to_sheep_distance(x, y)
        if distance > self.count_wolf_to_sheep_distance(x + self.__wolf_move_dist, y):
            self.__wolf_position.x -= self.__wolf_move_dist
        elif distance > self.count_wolf_to_sheep_distance(x - self.__wolf_move_dist, y):
            self.__wolf_position.x += self.__wolf_move_dist
        elif distance > self.count_wolf_to_sheep_distance(x, y + self.__wolf_move_dist):
            self.__wolf_position.y -= self.__wolf_move_dist
        elif distance > self.count_wolf_to_sheep_distance(x, y - self.__wolf_move_dist):
            self.__wolf_position.y += self.__wolf_move_dist

    def print_current_status(self, turn):
        print("Tura " + str(turn))
        print("Wilk x: " + str(self.__wolf_position.x))
        print("Wilk y: " + str(self.__wolf_position.y))
        print()

    def print_end_game_status(self):
        if len(self.__sheeps_position) == 0:
            print("Koniec gry, Owce zjedzone!")
        else:
            print("Koniec gry, Owce przezyly!")

    def move_wolf(self, sheep):
        if not self.check_if_wolf_in_range(sheep):
            self.select_wolf_direction(sheep)

    def make_turn(self):
        for turn in range(1, self.__number_of_turns + 1):
            self.print_current_status(turn)
            self.move_sheeps()
            self.move_wolf(self.select_closest_sheep())
            if len(self.__sheeps_position) == 0:
                break
        self.print_end_game_status()


WolfSheepGame(500, 10, 10.0, 0.5, 0.25).make_turn()
