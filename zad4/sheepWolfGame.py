import random
import math
from tkinter import *
from tkinter import messagebox


class GUI:
    __root = Tk()
    __sheep_status_text = StringVar()
    __block_size = None
    __wolf_sheep_game = None
    __canvas = None
    __created_sheeps = list()
    __created_wolf = None
    __size = None

    def __init__(self, init_pos_limit, sheep_move_dist, wolf_move_dist, block_size):
        self.__block_size = block_size
        self.__root.title("Wilk i owce - gra")

        interface_frame = Frame(self.__root, height=30, width=300)
        interface_frame.pack_propagate(0)
        interface_frame.pack()

        self.__sheep_status_text.set("siema z podziemia!")
        label = Label(interface_frame, textvariable=self.__sheep_status_text)
        label.pack(side=RIGHT)
        reset_button = Button(interface_frame, text="reset", command=self.reset_button_action)
        step_button = Button(interface_frame, text="krok", command=self.step_button_action)
        reset_button.pack(side=LEFT)
        step_button.pack(side=LEFT)
        self.__size =  1.5 * init_pos_limit * self.__block_size
        rectangle_center = self.__size / 2
        self.__canvas = Canvas(self.__root, width=self.__size, height=self.__size, bg="green")
        wolf = self.__canvas.create_oval(rectangle_center - 3, rectangle_center + 3, rectangle_center + 3,
                                         rectangle_center - 3, fill="red")
        self.__wolf_sheep_game = WolfSheepGame(init_pos_limit, sheep_move_dist, wolf_move_dist, wolf, self.__canvas)
        self.__canvas.bind('<Button-1>', self.add_sheep_on_click)
        self.__canvas.bind('<Button-3>', self.change_wolf_position)
        self.__canvas.pack()
        self.__root.mainloop()

    def step_button_action(self):
        if len(self.__wolf_sheep_game.sheep_position) is not 0:
            self.__wolf_sheep_game.make_turn()
        else:
            messagebox.showinfo('Information', 'Nie mozna przeprowadzic kroku, za malo owiec!')

    def reset_button_action(self):
        self.__canvas.delete("all")
        self.__wolf_sheep_game.wolf = self.__canvas.create_oval((self.__size // 2) - 3, (self.__size // 2) - 3,
                                                                (self.__size // 2) + 3, (self.__size // 2) + 3,
                                                                fill='red')
        self.__wolf_sheep_game.sheep_position.clear()

    def add_sheep_on_click(self, event):
        sheep = self.__canvas.create_oval(event.x - 3, event.y + 3, event.x + 3, event.y - 3, fill="blue")
        self.__wolf_sheep_game.sheep_position.append(sheep)

    def change_wolf_position(self, event):
        self.__canvas.coords(self.__wolf_sheep_game.wolf, event.x - 3, event.y + 3, event.x + 3, event.y - 3)


class WolfSheepGame:
    __init_pos_limit = None
    __sheep_move_dist = None
    __wolf_move_dist = None
    __canvas = None
    sheep_position = list()
    wolf = None

    def __init__(self, init_pos_limit, sheep_move_dist, wolf_move_dist, wolf, canvas):
        self.__init_pos_limit = init_pos_limit
        self.__sheep_move_dist = sheep_move_dist
        self.__wolf_move_dist = wolf_move_dist
        self.__canvas = canvas
        self.wolf = wolf

    def add_sheep(self, sheep):
        self.sheep_position.append(sheep)

    def count_wolf_to_sheep_distance(self, sheep_position_x, sheep_position_y):
        wolf_coords = self.__canvas.coords(self.wolf)
        wolf_x = wolf_coords[0] + 2
        wolf_y = wolf_coords[1] - 2
        x_square_distance = (sheep_position_x - wolf_x) ** 2
        y_square_distance = (sheep_position_y - wolf_y) ** 2
        distance = math.sqrt(x_square_distance + y_square_distance)
        return distance

    def select_closest_sheep(self):
        closest_sheep = self.sheep_position[0]
        closest_sheep_coords = self.__canvas.coords(closest_sheep)
        closest_sheep_x = closest_sheep_coords[0] + 3
        closest_sheep_y = closest_sheep_coords[1] - 3
        closest_sheep_distance = self.count_wolf_to_sheep_distance(closest_sheep_x, closest_sheep_y)
        for sheep in self.sheep_position:
            sheep_coords = self.__canvas.coords(sheep)
            sheep_x = sheep_coords[0] + 3
            sheep_y = sheep_coords[1] - 3 
            distance = self.count_wolf_to_sheep_distance(sheep_x, sheep_y)
            if distance < closest_sheep_distance:
                closest_sheep = sheep
                closest_sheep_distance = distance
        return closest_sheep

    def move_sheep(self):
        for sheep in self.sheep_position:
            coords = self.__canvas.coords(sheep)
            x_direction = random.choice([True, False])
            minus_or_plus = random.choice([-1, 1])
            move = minus_or_plus * self.__sheep_move_dist
            print(coords)

            if x_direction:
                self.__canvas.coords(sheep, coords[0] + move, coords[1], coords[2] + move, coords[3])
                print(self.__canvas.coords(sheep))
            else:
                self.__canvas.coords(sheep, coords[0], coords[1] + move, coords[2], coords[3] + move)
                print(self.__canvas.coords(sheep))

    def check_if_wolf_in_range(self, sheep):
        sheep_coords = self.__canvas.coords(sheep)
        sheep_x = sheep_coords[0] + 3
        sheep_y = sheep_coords[1] - 3
        if self.__wolf_move_dist >= self.count_wolf_to_sheep_distance(sheep_x, sheep_y):
            return True
        else:
            return False

    def eat_sheep(self, sheep):
        self.sheep_position.remove(sheep)
        self.__canvas.delete(sheep)

    def move_wolf(self, sheep):
        wolf_coords = self.__canvas.coords(self.wolf)
        wolf_x = wolf_coords[0] + 3
        wolf_y = wolf_coords[1] - 3
        sheep_coords = self.__canvas.coords(sheep)
        sheep_x = sheep_coords[0] + 3
        sheep_y = sheep_coords[1] - 3
        distance = self.count_wolf_to_sheep_distance(sheep_x, sheep_y)
        union_vector = ((sheep_x - wolf_x) / distance, (sheep_y - wolf_y) / distance)
        
        wolf_x += (union_vector[0] * self.__wolf_move_dist)
        wolf_y += (union_vector[1] * self.__wolf_move_dist)
        self.__canvas.coords(sheep, wolf_coords[0] - wolf_x, wolf_coords[1] + wolf_y, wolf_coords[2] + wolf_x,
                             wolf_coords[3] - wolf_y)

    def wolf_turn(self, sheep):
        if not self.check_if_wolf_in_range(sheep):
            self.move_wolf(sheep)
        else:
            self.eat_sheep(sheep)

    def make_turn(self):
        self.move_sheep()
        self.wolf_turn(self.select_closest_sheep())


if __name__ == "__main__":
    GUI(250, 1.0, 3.0, 1)
