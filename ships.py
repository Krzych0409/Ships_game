from random import choice, randint
from time import sleep
from pyinputplus import inputStr, inputInt

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
        self.sheet = [[entry for x in range(10)] for x in range(10)]
        self.length_of_ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

    def show_sheet(self):
        for row in self.sheet:
            for char in row:
                print(char, end='\t')
            print()

    def make_sheet(self):
        if self.name == 'Player':
            for ship in self.length_of_ships:
                print(self.name)
                self.show_sheet()
                while True:
                    self.answer = input(f'Front {ship} e.g. "5C" : ').upper()
                    self.first_field = self.check_input(self.answer)
                    if self.first_field:
                        print(f'Start field ship: {self.first_field}')
                        break




        elif self.name == 'Computer':
            self.counter_v = 0
            self.counter_h = 0
            for length in self.length_of_ships:
                while True:
                    self.direction = randint(0, 1)  # vertical
                    self.row = randint(0, 9)
                    #print(f'Row: {self.row}')
                    self.column = randint(0, 9)
                    #print(f'Column: {self.column}')
                    self.filds_of_ship = [[], []]

                    if self.directions[self.direction] == 'vertical':
                        if self.row + length <= 9:
                            for fild in range(length):
                                if self.sheet[self.row + fild][self.column] == entry:
                                    self.filds_of_ship[0].append(self.row + fild)
                                    #print(f'Dodano kolumne statku: {self.filds_of_ship[0][-1]}')
                                    self.filds_of_ship[1].append(self.column)
                                    #print(f'Dodano wiersz statku: {self.filds_of_ship[1][-1]}')

                                elif self.sheet[self.row + fild][self.column] != entry:
                                    #print('Pole zajęte')
                                    break

                        elif self.row + length > 9: continue

                        #print(self.filds_of_ship)
                        if len(self.filds_of_ship[0]) == length and self.check_space() == True:
                            if length > 1:
                                self.counter_v += 1
                            break
                        else: continue


                    elif self.directions[self.direction] == 'horizontal':
                        self.filds_of_ship = self.filds_of_ship[::-1]
                        if self.column + length <= 9:
                            for fild in range(length):
                                if self.sheet[self.row][self.column + fild] == entry:
                                    self.filds_of_ship[0].append(self.row)
                                    #print(f'Dodano kolumne statku: {self.filds_of_ship[0][-1]}')
                                    self.filds_of_ship[1].append(self.column + fild)
                                    #print(f'Dodano wiersz statku: {self.filds_of_ship[1][-1]}')

                                elif self.sheet[self.row][self.column + fild] != entry:
                                    #print('Pole zajęte')
                                    break

                        elif self.column + length > 9: continue

                        #print(self.filds_of_ship)
                        if len(self.filds_of_ship[0]) == length and self.check_space() == True:
                            if length > 1:
                                self.counter_h += 1
                            break
                        else: continue

                # Add ship on sheet
                for i in range(len(self.filds_of_ship[0])):
                    self.sheet[self.filds_of_ship[0][i]][self.filds_of_ship[1][i]] = len(self.filds_of_ship[0])
            # Change '#' to entry
            for r in range(len(self.sheet[0])):
                for c in range(len(self.sheet[r])):
                    if self.sheet[r][c] == '#':
                        self.sheet[r][c] = entry

        print(f'\n{self.name}:')
        self.show_sheet()
        print(f'Ilość Vertical: {self.counter_v}')
        print(f'Ilość Horizontal: {self.counter_h}\n')

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
        #print(f'Wiersze: {self.space_of_fields[0]}')
        #print(f'Kolumny: {self.space_of_fields[1]}')

        # Dodanie niedostępnych przestrzeni jako '#'
        for r in self.space_of_fields[0]:
            for k in self.space_of_fields[1]:
                if self.sheet[r][k] == entry or self.sheet[r][k] == '#':
                    self.sheet[r][k] = '#'
                else:
                    return False

        return True

    def check_input(self, answer):
        self.letter_cord = []
        self.digit_cord = []
        self.change_dict = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10}

        if len(answer) == 2 or len(answer) == 3:
            for i in answer:
                if i.isupper():
                    self.letter_cord.append(i)
                elif i.isdigit():
                    self.digit_cord.append(i)

            if len(self.letter_cord) != 1: return False
            if len(self.digit_cord) == 1: self.digit_cord = int(self.digit_cord[0])
            elif len(self.digit_cord) == 2: self.digit_cord = int(self.digit_cord[0] + self.digit_cord[1])
            if self.digit_cord < 1 or self.digit_cord > 10: return False
            elif 1 <= self.digit_cord <= 10: return [self.change_dict[self.letter_cord[0]], self.digit_cord]

        else: return False








entry = '()'
game = Game()
comp = Player('Computer')
comp.make_sheet()
human = Player('Player')
human.make_sheet()


