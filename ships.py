from random import choice, randint
from time import sleep
from pyinputplus import inputStr, inputInt, inputChoice
from colorama import Fore, init
from time import sleep

class Game():
    def __init__(self):
        init(autoreset=True)              # auto reset color
        self.end_game = False
        self.comp = Player('Bot', 'c', 'bot')
        self.comp.make_sheet()
        self.comp.show_sheet()
        print()
        self.human = Player('Human', 'c', 'bot')
        self.human.make_sheet()
        self.human.show_sheet()

    def loop_game(self):
        while self.end_game == False:
            while self.end_game == False:
                print(f'\nSHOT {self.human.name}')
                if self.human.shot(self.comp) == False:         # If human not hit
                    self.comp.show_sheet()
                    break
                else:                                           # If human hit
                    self.comp.show_sheet()
                    self.sum_length = 0
                    for ship in self.comp.ships:                # If human destroyed all ships
                        self.sum_length += ship.actual_length
                    print(f"Sum of length all opponent's ships = {self.sum_length}")
                    if self.sum_length == 0:
                        print(f'Human Win  -  {self.human.name}')
                        self.end_game = True

            while self.end_game == False:
                print(f'\nSHOT {self.comp.name}')
                if self.comp.shot(self.human) == False:         # If comp not hit
                    self.human.show_sheet()
                    break
                else:                                           # If comp hit
                    self.human.show_sheet()
                    self.sum_length = 0
                    for ship in self.human.ships:
                        self.sum_length += ship.actual_length     # If comp destroyed all ships
                    print(f"Sum of length all opponent's ships = {self.sum_length}")
                    if self.sum_length == 0:
                        print(f'Comp Win  -  {self.comp.name}')
                        self.end_game = True

    def turn_of_human(self):
        pass

    def turn_of_comp(self):
        pass


class Player():
    def __init__(self, name, kind_of_make_sheet, kind_of_shot):
        self.name = name
        self.kind_of_make_sheet = kind_of_make_sheet
        self.kind_of_shot = kind_of_shot
        self.directions = ('vertical', 'horizontal')
        self.sheet = [[entry for x in range(10)] for x in range(10)]
        self.length_of_ships = (4, 3, 3, 2, 2, 2, 1, 1, 1, 1)
        self.first_row = [x for x in range(-1, 10)]
        self.first_row[0] = ''
        self.alphabet = ('A-0', 'B-1', 'C-2', 'D-3', 'E-4', 'F-5', 'G-6', 'H-7', 'I-8', 'J-9')
        self.ships = []

    def show_sheet(self):
        print(self.name)
        for char in self.first_row:
            print(f'{Fore.YELLOW}{char}', end='\t')
        print()

        for i, row in enumerate(self.sheet):
            print(f'{Fore.YELLOW}{self.alphabet[i]}', end='\t')
            for char in row:
                if char == destroyed:
                    print(f'{Fore.GREEN}{char}', end='\t')
                elif char == hit:
                    print(f'{Fore.RED}{char}', end='\t')
                elif type(char) == int:
                    print(f'{Fore.BLUE}{char}', end='\t')
                elif char == fail:
                    print(f'{Fore.MAGENTA}{char}', end='\t')
                elif char == entry:
                    print(f'{char}', end='\t')
                else:
                    print(char, end='\t')
            print()

    def make_sheet(self):
        if self.kind_of_make_sheet == 'p':
            self.counter_v = 0
            self.counter_h = 0
            for length in self.length_of_ships:
                while True:
                    self.question = f'First field of ship {length} e.g. "5C" : '
                    self.first_field = self.check_input(self.question)

                    self.row = self.first_field[0]
                    self.column = self.first_field[1]
                    print(f'Row: {self.row}   Kolumn: {self.column}')
                    self.fields_of_ship = [[], []]
                    self.direction = inputChoice(['v', 'h'], prompt='vertical or horizontal [v, h]: ')

                    if self.direction == 'v': self.direction = 0
                    elif self.direction == 'h': self.direction = 1
                    print(f'Direction : {self.direction}')

                    if self.directions[self.direction] == 'vertical':
                        if self.row + length - 1 <= 9:
                            for field in range(length):
                                if self.sheet[self.row + field][self.column] == entry:
                                    self.fields_of_ship[0].append(self.row + field)
                                    # print(f'Dodano kolumne statku: {self.fields_of_ship[0][-1]}')
                                    self.fields_of_ship[1].append(self.column)
                                    # print(f'Dodano wiersz statku: {self.fields_of_ship[1][-1]}')

                                elif self.sheet[self.row + field][self.column] != entry:
                                    print('Pole zajęte')
                                    break

                        elif self.row + length - 1 > 9:
                            print('to big row')
                            continue

                        # print(self.fields_of_ship)
                        if len(self.fields_of_ship[0]) == length and self.check_space() == True:
                            if length > 1:
                                self.counter_v += 1
                            break
                        else:
                            continue

                    elif self.directions[self.direction] == 'horizontal':
                        self.fields_of_ship = self.fields_of_ship[::-1]
                        if self.column + length - 1 <= 9:
                            for field in range(length):
                                if self.sheet[self.row][self.column + field] == entry:
                                    self.fields_of_ship[0].append(self.row)
                                    #print(f'Dodano kolumne statku: {self.fields_of_ship[0][-1]}')
                                    self.fields_of_ship[1].append(self.column + field)
                                    #print(f'Dodano wiersz statku: {self.fields_of_ship[1][-1]}')

                                elif self.sheet[self.row][self.column + field] != entry:
                                    print('Pole zajęte')
                                    break

                        elif self.column + length - 1 > 9:
                            print('to big kolumn')
                            continue

                    #print(self.fields_of_ship)
                    if len(self.fields_of_ship[0]) == length and self.check_space() == True:
                        if length > 1:
                            self.counter_h += 1
                        break
                    else: continue


                # Add ship on sheet
                for i in range(len(self.fields_of_ship[0])):
                    self.sheet[self.fields_of_ship[0][i]][self.fields_of_ship[1][i]] = len(self.fields_of_ship[0])
                self.ships.append(Ship(self.fields_of_ship))

            # Change '#' to entry
            for r in range(len(self.sheet[0])):
                for c in range(len(self.sheet[r])):
                    if self.sheet[r][c] == '#':
                        self.sheet[r][c] = entry

        elif self.kind_of_make_sheet == 'c':
            self.counter_v = 0
            self.counter_h = 0
            for length in self.length_of_ships:
                while True:
                    self.direction = randint(0, 1)  # vertical
                    self.row = randint(0, 9)
                    #print(f'Row: {self.row}')
                    self.column = randint(0, 9)
                    #print(f'Column: {self.column}')
                    self.fields_of_ship = [[], []]

                    if self.directions[self.direction] == 'vertical':
                        if self.row + length - 1 <= 9:
                            for field in range(length):
                                if self.sheet[self.row + field][self.column] == entry:
                                    self.fields_of_ship[0].append(self.row + field)
                                    #print(f'Dodano kolumne statku: {self.fields_of_ship[0][-1]}')
                                    self.fields_of_ship[1].append(self.column)
                                    #print(f'Dodano wiersz statku: {self.fields_of_ship[1][-1]}')

                                elif self.sheet[self.row + field][self.column] != entry:
                                    #print('Pole zajęte')
                                    break

                        elif self.row + length - 1 > 9: continue

                        #print(self.fields_of_ship)
                        if len(self.fields_of_ship[0]) == length and self.check_space() == True:
                            if length > 1:
                                self.counter_v += 1
                            break
                        else: continue

                    elif self.directions[self.direction] == 'horizontal':
                        self.fields_of_ship = self.fields_of_ship[::-1]
                        if self.column + length - 1 <= 9:
                            for field in range(length):
                                if self.sheet[self.row][self.column + field] == entry:
                                    self.fields_of_ship[0].append(self.row)
                                    #print(f'Dodano kolumne statku: {self.fields_of_ship[0][-1]}')
                                    self.fields_of_ship[1].append(self.column + field)
                                    #print(f'Dodano wiersz statku: {self.fields_of_ship[1][-1]}')

                                elif self.sheet[self.row][self.column + field] != entry:
                                    #print('Pole zajęte')
                                    break

                        elif self.column + length - 1 > 9: continue

                        #print(self.fields_of_ship)
                        if len(self.fields_of_ship[0]) == length and self.check_space() == True:
                            if length > 1:
                                self.counter_h += 1
                            break
                        else: continue

                # Add ship on sheet
                for i in range(len(self.fields_of_ship[0])):
                    self.sheet[self.fields_of_ship[0][i]][self.fields_of_ship[1][i]] = len(self.fields_of_ship[0])
                self.ships.append(Ship(self.fields_of_ship))
                
            # Change '#' to entry
            for r in range(len(self.sheet[0])):
                for c in range(len(self.sheet[r])):
                    if self.sheet[r][c] == '#':
                        self.sheet[r][c] = entry

        #self.show_sheet()
        #print(f'Ilość Vertical: {self.counter_v}')
        #print(f'Ilość Horizontal: {self.counter_h}\n')

    def check_space(self):
        # self.fields_of_ship = [[2, 3, 4], [3, 3, 3]]
        self.space_of_fields = [[], []]
        # Dodanie niepowtarzających się elemetów przez zrobienie słownika
        self.space_of_fields[0] = list(dict.fromkeys(self.fields_of_ship[0]))
        self.space_of_fields[1] = list(dict.fromkeys(self.fields_of_ship[1]))
        # dodanie skrajnych indeksów
        self.space_of_fields[0].append(self.fields_of_ship[0][0] - 1)
        self.space_of_fields[0].append(self.fields_of_ship[0][-1] + 1)
        self.space_of_fields[1].append(self.fields_of_ship[1][0] - 1)
        self.space_of_fields[1].append(self.fields_of_ship[1][-1] + 1)
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

    def check_input(self, question):  # Return List [Y, X]
        self.change_dict = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9}

        while True:
            self.letter_cord = []
            self.digit_cord = []
            self.answer = input(question).upper()
            if len(self.answer) == 2 or len(self.answer) == 3:
                for i in self.answer:
                    if i.isupper():
                        self.letter_cord.append(i)
                    elif i.isdigit():
                        self.digit_cord.append(i)

                if len(self.letter_cord) != 1:
                    #print('if len(self.letter_cord) != 1:')
                    continue
                if len(self.digit_cord) == 1:
                    self.digit_cord[0] = int(self.digit_cord[0]) - 1                            # If cord of field is range (1-9)
                elif len(self.digit_cord) == 2:
                    self.digit_cord[0] = int(self.digit_cord[0] + self.digit_cord[1]) - 1       # If cord of field = 10
                # od tej chwili index jest od 0
                #print(f'self.digit_cord: {self.digit_cord[0]}')
                #print(f'self.letter_cord (index): {self.change_dict[self.letter_cord[0]]}')

                if self.digit_cord[0] < 0 or self.digit_cord[0] > 9:
                    #print('if self.digit_cord[0] < 1 or self.digit_cord[0] > 9:')
                    continue
                elif 0 <= self.digit_cord[0] <= 9:
                    try:
                        #print(f'check_input: return {self.change_dict[self.letter_cord[0]]}, {self.digit_cord[0]}')    # Add self.input
                        return [self.change_dict[self.letter_cord[0]], self.digit_cord[0]]

                    except: print('Wyjątek')

    def shot(self, opponent):
        if self.kind_of_shot == 'player':
            while True:
                self.question = f'Give me cord of shot: '
                self.field_of_shot = self.check_input(self.question)
                print(f'Player answer shot: {self.field_of_shot}')
                break


        elif self.kind_of_shot == 'bot':
            self.field_of_shot = self.random_cord_of_shot()
            print(f'Computer answer shot: {self.field_of_shot}')

        if opponent.sheet[self.field_of_shot[0]][self.field_of_shot[1]] == entry:           # Pudło
            opponent.sheet[self.field_of_shot[0]][self.field_of_shot[1]] = fail
            print(f'Fail {self.name}')
            return False  # Is entry

        elif type(opponent.sheet[self.field_of_shot[0]][self.field_of_shot[1]]) == int:     # Trafiony
            opponent.sheet[self.field_of_shot[0]][self.field_of_shot[1]] = hit
            print(f'Hit {self.name}')
            for ship in opponent.ships:
                for i in range(len(ship.fields[0])):
                    if ship.fields[0][i] == self.field_of_shot[0] and ship.fields[1][i] == self.field_of_shot[1]:       # Serch hit's ship
                        ship.actual_length -= 1
                        ship.actual_fields[0].remove(self.field_of_shot[0])
                        ship.actual_fields[1].remove(self.field_of_shot[1])
                        print(f'opponent.ships.actual_fields = {ship.actual_fields}')
                        print(f'opponent.ships.length_of_ship: {ship.actual_length}')
                        if ship.actual_length == 0:     # Zatopiony
                            print(f'{self.name} destroyed  --> {ship.fields}')
                            self.if_ship_destroyed(opponent, ship)
            return True     # Is hit

        else:      # Trafienie w coś co już było
            print(f"Choose another field - you've already shot here")
            return True

    def random_cord_of_shot(self):  # Return List [Y, X]
        self.shot_row = randint(0, 9)
        self.shot_kolumn = randint(0, 9)

        return [self.shot_kolumn, self.shot_row]

    def if_ship_destroyed(self, opponent, ship):
        if len(ship.actual_fields[0]) == 0 and len(ship.actual_fields[1]) == 0: # dodatkowe sprawdzenie czy aktualne pola są puste
            print('Warunek spełniony do zatopienia statku')
            for i in range(len(ship.fields[0])):
                opponent.sheet[ship.fields[0][i]][ship.fields[1][i]] = destroyed


class Ship():
    def __init__(self, fields_of_ship):
        self.fields = [[], []]
        self.actual_fields = [[], []]
        
        for i in range(len(fields_of_ship[0])):
            self.fields[0].append(fields_of_ship[0][i])
            self.fields[1].append(fields_of_ship[1][i])
            self.actual_fields[0].append(fields_of_ship[0][i])
            self.actual_fields[1].append(fields_of_ship[1][i])
                        
        self.length_of_ship = len(self.fields[0])
        self.actual_length = self.length_of_ship
        
        self.front_field = [self.fields[0][0], self.fields[1][0]]
        
        #print(f'self.length_of_ship: {self.length_of_ship}')
        #print(f'self.front_field: {self.front_field}')
        #print(f'self.fields: {self.fields}')
        
        
            


entry = '-'
hit = 'X'
fail = 'O'
destroyed = '#'

game = Game()
game.loop_game()



