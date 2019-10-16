import random

class WolfSheepGame:
    __number_of_turns = None
    __number_of_sheeps = None
    __init_pos_limit = None
    __sheep_move_dist = None
    __wolf_move_dist = None
    __sheeps_position = list

    def __init__(self, number_of_turns, number_of_sheeps, init_pos_limit, sheep_move_dist, wolf_move_dist):
        self.__number_of_turns = number_of_turns
        self.__number_of_sheeps = number_of_sheeps
        self.__init_pos_limit = init_pos_limit
        self.__sheep_move_dist = sheep_move_dist
        self.__wolf_move_dist = wolf_move_dist

        for sheep in range(number_of_sheeps):
            random_x = random.uniform(-self.__init_pos_limit, self.__init_pos_limit)
            random_y = random.uniform(-self.__init_pos_limit, self.__init_pos_limit)
            list_var = [random_x, random_y]
            print(random_x, random_y)

            self.__sheeps_position.append(list_var)

        print(self.__sheeps_position)

x = WolfSheepGame(500, 15, 10.0, 0.5, 1.0)