import random
import math
import json
import csv


class Sheep:
    id = None
    x = None
    y = None

    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def get_position(self):
        return self.x, self.y


class Wolf:
    x = None
    y = None

    def __init__(self, start_position):
        self.x = start_position
        self.y = start_position

    def get_position(self):
        return self.x, self.y


class WolfSheepGame:
    __number_of_turns = None
    __number_of_sheep = None
    __init_pos_limit = None
    __sheep_move_dist = None
    __wolf_move_dist = None
    __sheep_position = list()
    __wolf_position = None
    __list_for_json = list()
    __list_for_csv = list()

    def __init__(self, number_of_turns, number_of_sheeps, init_pos_limit, sheep_move_dist, wolf_move_dist):
        self.__number_of_turns = number_of_turns
        self.__number_of_sheep = number_of_sheeps
        self.__init_pos_limit = init_pos_limit
        self.__sheep_move_dist = sheep_move_dist
        self.__wolf_move_dist = wolf_move_dist
        self.__wolf_position = Wolf(0)

        for sheep_number in range(1, number_of_sheeps + 1):
            x = random.uniform(-init_pos_limit, init_pos_limit)
            y = random.uniform(-init_pos_limit, init_pos_limit)
            self.__sheep_position.append(Sheep(sheep_number, x, y))

    def count_wolf_to_sheep_distance(self, sheep_position_x, sheep_position_y):
        x_square_distance = (sheep_position_x - self.__wolf_position.x) ** 2
        y_square_distance = (sheep_position_y - self.__wolf_position.y) ** 2
        distance = math.sqrt(x_square_distance + y_square_distance)
        return distance

    def select_closest_sheep(self):
        closest_sheep = self.__sheep_position[0]
        closest_sheep_distance = self.count_wolf_to_sheep_distance(closest_sheep.x, closest_sheep.y)
        for sheep in self.__sheep_position:
            distance = self.count_wolf_to_sheep_distance(sheep.x, sheep.y)
            if distance < closest_sheep_distance:
                closest_sheep = sheep
        return closest_sheep

    def move_sheep(self):
        for sheep in self.__sheep_position:
            x_direction = random.randint(0, 1)
            minus_or_plus = random.randint(0, 1)

            if x_direction:
                sheep.x += (-1) * minus_or_plus + self.__sheep_move_dist
            else:
                sheep.y += (-1) * minus_or_plus + self.__sheep_move_dist

    def check_if_wolf_in_range(self, sheep):
        if self.__wolf_move_dist >= self.count_wolf_to_sheep_distance(sheep.x, sheep.y):
            return True
        else:
            return False

    def eat_sheep(self, sheep):
        self.__sheep_position.remove(sheep)
        self.print_eaten_sheep(sheep)

    def move_wolf(self, sheep):
        x = sheep.x
        y = sheep.y
        distance = self.count_wolf_to_sheep_distance(x, y)
        union_vector = ((x - self.__wolf_position.x) / distance, (y - self.__wolf_position.y) / distance)
        self.__wolf_position.x += union_vector[0] * self.__wolf_move_dist
        self.__wolf_position.y += union_vector[1] * self.__wolf_move_dist

    def wolf_turn(self, sheep):
        if not self.check_if_wolf_in_range(sheep):
            self.move_wolf(sheep)
        else:
            self.eat_sheep(sheep)

    def make_turn(self):
        self.move_sheep()
        self.wolf_turn(self.select_closest_sheep())

    def start_game(self):
        for turn in range(1, self.__number_of_turns + 1):
            self.make_turn()
            self.print_current_status(turn)
            self.convert_current_status_to_list(turn)
            if len(self.__sheep_position) == 0:
                break
        self.print_end_game_status()
        self.parse_to_json_file()
        self.parse_to_csv_file()

    def convert_current_status_to_list(self, turn):
        self.__list_for_csv.append((turn, len(self.__sheep_position)))

        status_dictionary = {"round_no": turn, "wolf_pos": (self.__wolf_position.x, self.__wolf_position.y)}
        sheep_list = list()
        list_pos = 0
        for sheep_id in range(1, self.__number_of_sheep + 1):
            if list_pos < len(self.__sheep_position):
                if self.__sheep_position[list_pos].id == sheep_id:
                    sheep_list.append(self.__sheep_position[list_pos].get_position())
                    list_pos += 1
                else:
                    sheep_list.append((None, None))
            else:
                sheep_list.append((None, None))
        status_dictionary["sheep_pos"] = sheep_list

        self.__list_for_json.append(status_dictionary)

    def parse_to_csv_file(self):
        with open("alive.csv", "w", newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=" ", quoting=csv.QUOTE_NONE)
            for i in self.__list_for_csv:
                writer.writerow(i)

    def parse_to_json_file(self):
        with open("pos.json", "w") as json_file:
            json.dump(self.__list_for_json, json_file, indent=1)

    def print_eaten_sheep(self, sheep):
        print()
        print("Owca nr: " + str(sheep.id) + " zostala zjedzona!")
        print()

    def print_current_status(self, turn):
        print("Tura " + str(turn))
        print("Wilk x: " + str(self.__wolf_position.x))
        print("Wilk y: " + str(self.__wolf_position.y))
        print()

    def print_end_game_status(self):
        if len(self.__sheep_position) == 0:
            print("Koniec gry, Owce zjedzone!")
        else:
            print("Koniec gry, Owce przezyly!")


WolfSheepGame(500, 10, 10.0, 0.5, 1.0).start_game()

