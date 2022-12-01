from random import choice, randint
from time import sleep


class Game():
    def __init__(self):
        pass

    def turn_of_human(self):
        pass

    def turn_of_comp(self):
        pass

class Player():
    def __init__(self, name):
        self.name = name
        self.directions = ('vertical', 'horizontal')
        self.sheet = [[puste for x in range(10)] for x in range(10)]
        self.length_of_ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        self.show_sheet()

    def show_sheet(self):
        for row in self.sheet:
            for char in row:
                print(char, end='\t')
            print()

    def make_sheet(self):
        if self.name == 'Player':
            pass

        elif self.name == 'Computer':
            for length in self.length_of_ships:
                while True:
                    sleep(0.01)
                    self.direction = 0  # vertical
                    self.row = randint(0, 9)
                    self.column = randint(0, 9)
                    self.filds_of_ship = [[], []]

                    if self.directions[self.direction] == 'vertical':
                        if self.column + length <= 9:
                            for fild in range(length):
                                if self.sheet[self.column + fild][self.row] == puste:
                                    self.filds_of_ship[0].append(self.column + fild)
                                    print(f'Dodano kolumne statku: {self.filds_of_ship[0][-1]}')
                                    self.filds_of_ship[1].append(self.row)
                                    print(f'Dodano wiersz statku: {self.filds_of_ship[1][-1]}')

                                elif self.sheet[self.column + fild][self.row] != puste:
                                    print('Pole zajęte')
                                    break


                        elif self.column + length > 9:
                            continue

                        print(self.filds_of_ship)
                        if len(self.filds_of_ship[0]) == length and self.check_space() == True: break
                        else: continue


                    elif self.directions[self.direction] == 'horizontal':
                        if self.column + length <= 9:
                            for fild in range(length):
                                if self.sheet[self.column + fild][self.row] == puste:
                                    self.filds_of_ship[0].append(self.column + fild)
                                    print(f'Dodano kolumne statku: {self.filds_of_ship[0][-1]}')
                                    self.filds_of_ship[1].append(self.row)
                                    print(f'Dodano wiersz statku: {self.filds_of_ship[1][-1]}')

                                elif self.sheet[self.column + fild][self.row] != puste:
                                    print('Pole zajęte')
                                    break


                        elif self.column + length > 9:
                            continue

                        print(self.filds_of_ship)
                        if len(self.filds_of_ship[0]) == length and self.check_space() == True:
                            break
                        else:
                            continue





                for i in range(len(self.filds_of_ship[0])):
                    self.sheet[self.filds_of_ship[0][i]][self.filds_of_ship[1][i]] = len(self.filds_of_ship[0])
                self.show_sheet()
        print()
        for row in self.sheet:
            for char in row:
                if char == '#':
                    char = puste
                print(char, end='\t')
            print()


    def check_space(self):
        # self.filds_of_ship = [[2, 3, 4], [3, 3, 3]]
        self.space_of_fields = [[], []]
        # Dodanie niepowtarzających się elemetów przez zrobienie słownika
        self.space_of_fields[0] = list(dict.fromkeys(self.filds_of_ship[0]))
        self.space_of_fields[1] = list(dict.fromkeys(self.filds_of_ship[1]))
        # dodanie skrajnych indeksów
        self.space_of_fields[0].append(self.filds_of_ship[0][0] - 1)
        self.space_of_fields[0].append(self.filds_of_ship[0][-1] + 1)
        self.space_of_fields[1].append(self.filds_of_ship[1][0] - 1)
        self.space_of_fields[1].append(self.filds_of_ship[1][-1] + 1)
        # Usunięcie indeksów -1 i 10
        if -1 in self.space_of_fields[0]:
            self.space_of_fields[0].remove(-1)
        if 10 in self.space_of_fields[0]:
            self.space_of_fields[0].remove(10)
        if -1 in self.space_of_fields[1]:
            self.space_of_fields[1].remove(-1)
        if 10 in self.space_of_fields[1]:
            self.space_of_fields[1].remove(10)

        self.space_of_fields[0].sort()
        self.space_of_fields[1].sort()
        print(f'Wiersze: {self.space_of_fields[0]}')
        print(f'Kolumny: {self.space_of_fields[1]}')

        # Dodanie niedostępnych przestrzeni jako '#'
        for r in self.space_of_fields[0]:
            for k in self.space_of_fields[1]:
                if self.sheet[r][k] == puste or self.sheet[r][k] == '#':
                    self.sheet[r][k] = '#'
                else:
                    return False


        return True


'''if -1 not in self.space_of_fields[0] and 10 not in self.space_of_fields[1]:
    break
else:
    return False'''




class Ship():
    def __init__(self):
        self.ships = []




puste = '()'
game = Game()
comp = Player('Computer')
comp.make_sheet()
#human = Player('Player')
#human.make_sheet()


