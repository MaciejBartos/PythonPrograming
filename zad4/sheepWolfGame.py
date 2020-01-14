import random
import math
from tkinter import *
from tkinter import messagebox


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
    __init_pos_limit = None
    __sheep_move_dist = None
    __wolf_move_dist = None
    __sheep_position = list()
    __wolf_position = None
    __root = Tk()
    __canvas = None
    __status_sheep_text = StringVar()
    __wolf_position1 = None
    __point_size = 3
    __size = None
    __sheep_position1 = list()

    def __init__(self, init_pos_limit, sheep_move_dist, wolf_move_dist):
        self.__init_pos_limit = init_pos_limit
        self.__sheep_move_dist = sheep_move_dist
        self.__wolf_move_dist = wolf_move_dist
        self.init_gui()

    def init_gui(self):
        interface_frame = Frame(self.__root, height=30, width=300)
        interface_frame.pack_propagate(0)
        interface_frame.pack()

        self.__status_sheep_text.set("pozdrowienia z podziemia!")
        label = Label(interface_frame, textvariable=self.__status_sheep_text)
        label.pack(side=RIGHT)
        reset_button = Button(interface_frame, text="reset", command=self.reset_button_action)
        step_button = Button(interface_frame, text="krok", command=self.step_button_action)
        reset_button.pack(side=LEFT)
        step_button.pack(side=LEFT)
        self.__size = self.__init_pos_limit * 1.5

        self.__canvas = Canvas(self.__root, width=self.__size, height=self.__size, bg="green")
        self.__canvas.pack()
        self.__wolf_position1 = self.__canvas.create_oval(self.__size / 2 - self.__point_size,
                                                          self.__size / 2 + self.__point_size,
                                                          self.__size / 2 + self.__point_size,
                                                          self.__size / 2 - self.__point_size,
                                                          fill="red")
        coord = self.__canvas.coords(self.__wolf_position1)
        print("CO JEST: " + str)
        self.__canvas.bind('<Button-1>', self.add_sheep_on_click)
        self.__canvas.bind('<Button-3>', self.change_wolf_position)
        self.__root.mainloop()

    def add_sheep_on_click(self, event):
        sheep = self.__canvas.create_oval(event.x - 3, event.y + 3, event.x + 3, event.y - 3, fill="blue")
        self.__sheep_position1.append(sheep)

    def change_wolf_position(self, event):
        self.__canvas.coords(self.__wolf_position1, event.x - 3, event.y + 3, event.x + 3, event.y - 3)

    def step_button_action(self):
        if len(self.__sheep_position1) is not 0:
            self.make_turn()
        else:
            messagebox.showinfo('Information', 'Nie mozna przeprowadzic kroku, za malo owiec!')

    def reset_button_action(self):
        self.__canvas.delete("all")
        self.__wolf_position1 = self.__canvas.create_oval((self.__size // 2) - 3, (self.__size // 2) - 3,
                                                          (self.__size // 2) + 3, (self.__size // 2) + 3,
                                                          fill='red')
        self.__sheep_position1.clear()

    def count_wolf_to_sheep_distance(self, sheep_position_x, sheep_position_y):
        wolf_x, wolf_y = self.get_x_and_y_from_oval(self.__wolf_position1)
        x_square_distance = (sheep_position_x - wolf_x) ** 2
        y_square_distance = (sheep_position_y - wolf_y) ** 2
        distance = math.sqrt(x_square_distance + y_square_distance)
        return distance

    def get_x_and_y_from_oval(self, figure):
        coords = self.__canvas.coords(figure)
        x = coords[0] + self.__point_size
        y = coords[1] - self.__point_size
        return x, y

    def select_closest_sheep(self):
        closest_sheep = self.__sheep_position1[0]
        x, y = self.get_x_and_y_from_oval(closest_sheep)
        closest_sheep_distance = self.count_wolf_to_sheep_distance(x, y)
        for sheep in self.__sheep_position1:
            x, y = self.get_x_and_y_from_oval(sheep)
            distance = self.count_wolf_to_sheep_distance(x, y)
            if distance < closest_sheep_distance:
                closest_sheep = sheep
                closest_sheep_distance = distance
        return closest_sheep

    def move_sheep(self):
        for sheep in self.__sheep_position1:
            coords = self.__canvas.coords(sheep)
            x_direction = random.choice([True, False])
            minus_or_plus = random.choice([-1, 1])
            move = minus_or_plus * self.__sheep_move_dist

            if x_direction:
                self.__canvas.coords(sheep, coords[0] + move, coords[1], coords[2] + move, coords[3])
            else:
                self.__canvas.coords(sheep, coords[0], coords[1] + move, coords[2], coords[3] + move)

    def check_if_wolf_in_range(self, sheep):
        x, y = self.get_x_and_y_from_oval(sheep)
        if self.__wolf_move_dist >= self.count_wolf_to_sheep_distance(x, y):
            return True
        else:
            return False

    def eat_sheep(self, sheep):
        self.__sheep_position1.remove(sheep)
        self.__canvas.delete(sheep)

    def move_wolf(self, sheep):
        sheep_x, sheep_y = self.get_x_and_y_from_oval(sheep)
        wolf_x, wolf_y = self.get_x_and_y_from_oval(self.__wolf_position1)
        distance = self.count_wolf_to_sheep_distance(sheep_x, sheep_y)
        # print("dystans wilk-owca: " + str(distance))
        union_vector = ((sheep_x - wolf_x) / distance, (sheep_y - wolf_y) / distance)
        print ("wolf x i y: " + str(wolf_x) + " " + str(wolf_y))
        print ("sheep x i y: " + str(sheep_x) + " " + str(sheep_y))

        print("vector: " + str(union_vector))
        wolf_x += (union_vector[0] * self.__wolf_move_dist)
        wolf_y += (union_vector[1] * self.__wolf_move_dist)

        print("wolf x i y(po dodatniu vektora): " + str(wolf_x) + " " + str(wolf_y))
        # print("pozycja wilka: " + str(wolf_x) + " " + str(wolf_y))
        # print("pozycja owcy: " + str(sheep_x) + " " + str(sheep_y))
        self.__canvas.coords(self.__wolf_position1,
                             wolf_x - self.__point_size, wolf_y + self.__point_size,
                             wolf_x + self.__point_size, wolf_y - self.__point_size)
        print()
        print()


    def wolf_turn(self, sheep):
        if not self.check_if_wolf_in_range(sheep):
            self.move_wolf(sheep)
        else:
            self.eat_sheep(sheep)

    def make_turn(self):
        self.move_sheep()
        self.wolf_turn(self.select_closest_sheep())


if __name__ == "__main__":
    WolfSheepGame(250.0, 4.0, 6.0)



