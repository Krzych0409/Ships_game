from random import choice, randint
from time import sleep
from pyinputplus import inputStr, inputInt, inputChoice
from colorama import Fore, init
import copy


class Game():
    def __init__(self):
        init(autoreset=True)              # auto reset color
        self.end_game = False
        self.human = Player('Human', 'c', 'bot2')
        self.human.make_sheet()
        self.human.show_sheet()
        print()
        self.comp = Player('Bot', 'c', 'bot')
        self.comp.make_sheet()
        self.comp.show_sheet()
        print('\n' * 50)

    def loop_game(self):
        while self.end_game == False:
            # Human
            while self.end_game == False:
                if self.human.counter_turn > 200:
                    print('Za dużo tur')
                    break
                self.human.counter_turn += 1
                print(f'\nSHOT {self.human.name} Turn = {self.human.counter_turn}')
                if self.human.shot(self.comp) == False:         # If human not hit
                    self.human.show_2_sheets(self.comp)
                    break
                else:                                           # If human hit
                    self.human.show_2_sheets(self.comp)
                    self.sum_length = 0
                    for ship in self.comp.ships:                # If human destroyed all ships
                        self.sum_length += ship.actual_length
                    #print(f"Sum of length all opponent's ships = {self.sum_length}")
                    if self.sum_length == 0:
                        print(f'{self.human.name} Win !!!')
                        self.end_game = True

                if self.human.counter_turn > 200:
                    print('Za dużo tur')
                    break

            # Bot
            while self.end_game == False:
                if self.comp.counter_turn > 200:
                    print('Za dużo tur')
                    break
                self.comp.counter_turn += 1
                print(f'\nSHOT {self.comp.name} Turn = {self.comp.counter_turn}')
                if self.comp.shot(self.human) == False:         # If comp not hit
                    break
                else:                                           # If comp hit
                    self.sum_length = 0
                    for ship in self.human.ships:
                        self.sum_length += ship.actual_length     # If comp destroyed all ships
                    #print(f"Sum of length all opponent's ships = {self.sum_length}")
                    if self.sum_length == 0:
                        print(f'{self.comp.name} Win !!!')
                        self.end_game = True

                if self.comp.counter_turn > 200:
                    print('Za dużo tur')
                    break


class Player():
    def __init__(self, name, kind_of_make_sheet, kind_of_shot):
        self.name = name
        self.kind_of_make_sheet = kind_of_make_sheet
        self.kind_of_shot = kind_of_shot
        self.directions = ('vertical', 'horizontal')
        self.sheet = [[entry for x in range(10)] for x in range(10)]
        self.length_of_ships = (4, 3, 3, 2, 2, 2, 1, 1, 1, 1)
        self.first_row = [x for x in range(0, 12)]
        self.first_row[0] = ''
        self.first_row[11] = ''
        self.last_row = [x for x in range(-1, 11)]
        self.last_row[0] = ''
        self.last_row[11] = ''
        self.alphabet = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J')
        self.ships = []
        self.counter_turn = 0

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

    def hide_ships_on_sheet(self, opponent):
        self.sheet_opponent = [[entry for x in range(10)] for x in range(10)]

        for r in range(10):
            for k in range(10):
                if type(opponent.sheet[r][k]) == int:
                    self.sheet_opponent[r][k] = entry
                else:
                    self.sheet_opponent[r][k] = opponent.sheet[r][k]

        return self.sheet_opponent

    def show_2_sheets(self, opponent):
        self.sheets_together = copy.deepcopy(opponent.sheet)

        for char in self.first_row * 2:                                      # Print first row * 2  Change index COLUMN
            print(f'{Fore.YELLOW}{char}', end='\t')
        print()

        for r in range(10):
            print(f'{Fore.YELLOW}{self.alphabet[r]}', end='\t')
            for k in range(10):
                if opponent.sheet[r][k] == destroyed:
                    print(f'{Fore.GREEN}{opponent.sheet[r][k]}', end='\t')
                elif opponent.sheet[r][k] == hit:
                    print(f'{Fore.RED}{opponent.sheet[r][k]}', end='\t')
                elif type(opponent.sheet[r][k]) == int:
                    print(f'{entry}', end='\t')
                elif opponent.sheet[r][k] == fail:
                    print(f'{Fore.MAGENTA}{opponent.sheet[r][k]}', end='\t')
                elif opponent.sheet[r][k] == entry:
                    print(f'{opponent.sheet[r][k]}', end='\t')
                else:
                    print(opponent.sheet[r][k], end='\t')

            print(f'{Fore.YELLOW}{range(10)[r]}', end=' - ')
            print(f'{Fore.YELLOW}{self.alphabet[r]}', end='\t')
            for k in range(10):
                if self.sheet[r][k] == destroyed:
                    print(f'{Fore.GREEN}{self.sheet[r][k]}', end='\t')
                elif self.sheet[r][k] == hit:
                    print(f'{Fore.RED}{self.sheet[r][k]}', end='\t')
                elif type(self.sheet[r][k]) == int:
                    print(f'{Fore.BLUE}{self.sheet[r][k]}', end='\t')
                elif self.sheet[r][k] == fail:
                    print(f'{Fore.MAGENTA}{self.sheet[r][k]}', end='\t')
                elif self.sheet[r][k] == entry:
                    print(f'{self.sheet[r][k]}', end='\t')
                else:
                    print(self.sheet[r][k], end='\t')
            print(f'{Fore.YELLOW}{range(10)[r]}', end='\t')
            print()

        for char in self.last_row * 2:  # Print first row * 2
            print(f'{Fore.YELLOW}{char}', end='\t')
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
            self.field_of_shot = self.random_cord_of_shot(opponent)
            print(f'{self.kind_of_shot} shot: {self.field_of_shot}')

        elif self.kind_of_shot == 'bot2':
            self.hide_ships_on_sheet(opponent)      # Tworzenie zmiennej przechowującą arkusz przeciwnika z ukrytymi statkami
            self.field_of_shot = self.shooting_algorithm_1(opponent.ships)
            print(f'{self.kind_of_shot} shot: {self.field_of_shot}')


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
                        #print(f'opponent.ships.actual_fields = {ship.actual_fields}')
                        #print(f'opponent.ships.length_of_ship: {ship.actual_length}')
                        if ship.actual_length == 0:     # Zatopiony
                            print(f'{self.name} destroyed  --> {ship.fields}')
                            self.if_ship_destroyed(opponent, ship)
            return True     # Is hit

        else:      # Trafienie w coś co już było
            print(f"Choose another field - you've already shot here")
            return True

    def random_cord_of_shot(self, opponent):  # Return List [Y, X]
        self.shot_row = randint(0, 9)
        self.shot_kolumn = randint(0, 9)

        if type(opponent.sheet[self.shot_row][self.shot_kolumn]) == int or opponent.sheet[self.shot_row][self.shot_kolumn] == entry:
            return [self.shot_row, self.shot_kolumn]

        else:
            #print(f'Już było {[self.shot_row, self.shot_kolumn]}')
            #print(f'Wybieram jeszcze raz dla {self.name}')
            return  self.random_cord_of_shot(opponent)

    def if_ship_destroyed(self, opponent, ship):
        if len(ship.actual_fields[0]) == 0 and len(ship.actual_fields[1]) == 0: # dodatkowe sprawdzenie czy aktualne pola są puste
            print('Warunek spełniony do zatopienia statku')
            for i in range(len(ship.fields[0])):
                opponent.sheet[ship.fields[0][i]][ship.fields[1][i]] = destroyed

    def shooting_algorithm_1(self, ships_opponent):
        # self.sheet_opponent
        self.a_ships_opponent = ships_opponent
        self.a_counter_shots = 0
        self.a_neighboring_fields_vertical = [[], []]
        self.a_neighboring_fields_horizontal = [[], []]
        self.a_hit_fields = [[], []]
        self.a_entry_fields = [[], []]
        self.a_counter_fields_plus_h = 0
        self.a_counter_fields_minus_h = 0
        self.a_counter_fields_plus_v = 0
        self.a_counter_fields_minus_v = 0


        for r in range(10):
            for k in range(10):
                if self.sheet_opponent[r][k] == destroyed:            # Jeśli pole zatopione to sąsiednie zamień na 'close'
                    if r < 9:
                        if self.sheet_opponent[r + 1][k] == entry:
                            self.sheet_opponent[r + 1][k] = close
                    if r > 0:
                        if self.sheet_opponent[r - 1][k] == entry:
                            self.sheet_opponent[r - 1][k] = close
                    if k < 9:
                        if self.sheet_opponent[r][k + 1] == entry:
                            self.sheet_opponent[r][k + 1] = close
                    if k > 0:
                        if self.sheet_opponent[r][k - 1] == entry:
                            self.sheet_opponent[r][k - 1] = close

                    if r < 9 and k < 9:
                        self.sheet_opponent[r + 1][k + 1] = close
                    if r < 9 and k > 0:
                        self.sheet_opponent[r + 1][k - 1] = close
                    if r > 0 and k < 9:
                        self.sheet_opponent[r - 1][k + 1] = close
                    if r > 0 and k > 0:
                        self.sheet_opponent[r - 1][k - 1] = close

        for r in range(10):         # Szuka trafienia 'X'
            for k in range(10):
                if self.sheet_opponent[r][k] == hit:                    # If field = hit
                    #print(f'trafienie: {self.sheet_opponent[r][k]}')
                    self.a_hit_fields[0].append(r)
                    self.a_hit_fields[1].append(k)
                elif self.sheet_opponent[r][k] == entry:                # If field = entry
                    #print(f'puste: {self.sheet_opponent[r][k]}')
                    self.a_entry_fields[0].append(r)
                    self.a_entry_fields[1].append(k)

        print(f'Ilość pustych pól: {len(self.a_entry_fields[0])}')

        if len(self.a_hit_fields[0]) == 0:  # Jeśli nie ma trafienia w arkuszu
            self.a_index = randint(0, len(self.a_entry_fields[0]) - 1)
            self.a_row = self.a_entry_fields[0][self.a_index]
            self.a_kolumn = self.a_entry_fields[1][self.a_index]

        elif len(self.a_hit_fields[0]) == 1:  # Jeśli jest jedno trafienie trzeba sprawdzić ilość wolnych pól w dwóch kierunkach
            for i in range(1, 4):  # Sprawdzenie 3 pól
                try:  # W prawo
                    if self.sheet_opponent[self.a_hit_fields[0][0]][self.a_hit_fields[1][0] + i] == entry:  # Jeśli pole jest puste dodaj do sąsiednich pól
                        self.a_neighboring_fields_horizontal[0].append(self.a_hit_fields[0][0])
                        self.a_neighboring_fields_horizontal[1].append(self.a_hit_fields[1][0] + i)
                        self.a_counter_fields_plus_h += 1
                    else: break
                except: break

            for i in range(1, 4):  # Sprawdzenie 3 pól
                try:  # W lewo
                    if self.a_hit_fields[1][0] - i == -1: break
                    elif self.sheet_opponent[self.a_hit_fields[0][0]][self.a_hit_fields[1][0] - i] == entry:  # Jeśli pole jest puste dodaj do sąsiednich pól
                        self.a_neighboring_fields_horizontal[0].append(self.a_hit_fields[0][0])
                        self.a_neighboring_fields_horizontal[1].append(self.a_hit_fields[1][0] - i)
                        self.a_counter_fields_minus_h += 1
                    else: break
                except: break

            for i in range(1, 4):  # Sprawdzenie 3 pól
                try:  # W dół
                    if self.sheet_opponent[self.a_hit_fields[0][0] + i][self.a_hit_fields[1][0]] == entry:  # Jeśli pole jest puste dodaj do sąsiednich pól
                        self.a_neighboring_fields_vertical[0].append(self.a_hit_fields[0][0] + i)
                        self.a_neighboring_fields_vertical[1].append(self.a_hit_fields[1][0])
                        self.a_counter_fields_plus_v += 1
                    else: break
                except: break

            for i in range(1, 4):  # Sprawdzenie 3 pól
                try:  # W góre
                    if self.a_hit_fields[0][0] - i == 0: break
                    elif self.sheet_opponent[self.a_hit_fields[0][0] - i][self.a_hit_fields[1][0]] == entry:  # Jeśli pole jest puste dodaj do sąsiednich pól
                        self.a_neighboring_fields_vertical[0].append(self.a_hit_fields[0][0] - i)
                        self.a_neighboring_fields_vertical[1].append(self.a_hit_fields[1][0])
                        self.a_counter_fields_minus_v += 1
                    else: break
                except: break

            print(f'Ilość wolnych pól w poziomie: {len(self.a_neighboring_fields_horizontal[0])}')
            print(f'Ilość wolnych pól w pionie: {len(self.a_neighboring_fields_vertical[0])}')
            print(f'Ilość pól horizontal o index- : {self.a_counter_fields_minus_h}')
            print(f'Ilość pól horizontal o index+ : {self.a_counter_fields_plus_h}')
            print(f'Ilość pól vertical o index- : {self.a_counter_fields_minus_v}')
            print(f'Ilość pól vertical o index+ : {self.a_counter_fields_plus_v}')

            if len(self.a_neighboring_fields_horizontal[0]) > len(self.a_neighboring_fields_vertical[0]):   # Jeśli więcej wolnych pól w poziomie
                # Gdzie więcej wolnych pól, jeśli remis to w prawo
                if self.a_counter_fields_minus_h > self.a_counter_fields_plus_h:
                    if self.sheet_opponent[self.a_hit_fields[0][0]][self.a_hit_fields[1][0] - 1] == entry:      # Strzelamy w lewo (index -)
                        self.a_row = self.a_hit_fields[0][0]
                        self.a_kolumn = self.a_hit_fields[1][0] - 1
                    else:                                                       # Strzelamy w prawo (index +)
                        self.a_row = self.a_hit_fields[0][-1]
                        self.a_kolumn = self.a_hit_fields[1][-1] + 1

                elif self.a_counter_fields_minus_h <= self.a_counter_fields_plus_h:                                 # Strzelamy w prawo (index +)
                    if self.sheet_opponent[self.a_hit_fields[0][0]][self.a_hit_fields[1][0] + 1] == entry:
                        self.a_row = self.a_hit_fields[0][0]
                        self.a_kolumn = self.a_hit_fields[1][0] + 1
                    else:                                                       # Strzelamy w lewo (index -)
                        self.a_row = self.a_hit_fields[0][-1]
                        self.a_kolumn = self.a_hit_fields[1][-1] - 1

            elif len(self.a_neighboring_fields_horizontal[0]) <= len(self.a_neighboring_fields_vertical[0]): # Jeśli więcej wolnych pól w pionie lub remis
                # Gdzie więcej wolnych pól, jeśli remis to w dół
                if self.a_counter_fields_minus_v > self.a_counter_fields_plus_v:
                    if self.sheet_opponent[self.a_hit_fields[0][0] - 1][self.a_hit_fields[1][0]] == entry:      # Strzelamy w góre (index -)
                        self.a_row = self.a_hit_fields[0][0] - 1
                        self.a_kolumn = self.a_hit_fields[1][0]
                    else:                                               # Strzelamy w dół (index +)
                        self.a_row = self.a_hit_fields[0][-1] + 1
                        self.a_kolumn = self.a_hit_fields[1][-1]


                elif self.a_counter_fields_minus_v <= self.a_counter_fields_plus_v:  # Strzelamy w dół (index +)
                    if self.sheet_opponent[self.a_hit_fields[0][0] + 1][self.a_hit_fields[1][0]] == entry:      # Strzelamy w dół (index +)
                        self.a_row = self.a_hit_fields[0][-1] + 1
                        self.a_kolumn = self.a_hit_fields[1][-1]
                    else:                                               # Strzelamy w góre (index -)
                        self.a_row = self.a_hit_fields[0][0] - 1
                        self.a_kolumn = self.a_hit_fields[1][0]

        elif len(self.a_hit_fields[0]) > 1:  # Jeśli są minimum 2 trafienia
            if self.a_hit_fields[0][0] == self.a_hit_fields[0][1]:      # Statek jest w poziomie
                self.a_row = self.a_hit_fields[0][0]                        # Wiersz przyszłego strzału jest znany
                print(f'Będzie w poziome:  --')
                for i in range(1, 3):  # Sprawdzenie 2 pól w poziomie
                    try:  # W prawo
                        if self.sheet_opponent[self.a_hit_fields[0][-1]][self.a_hit_fields[1][-1] + i] == entry:  # Jeśli pole jest puste dodaj do sąsiednich pól
                            self.a_neighboring_fields_horizontal[0].append(self.a_hit_fields[0][-1])
                            self.a_neighboring_fields_horizontal[1].append(self.a_hit_fields[1][-1] + i)
                            self.a_counter_fields_plus_h += 1  # dodanie pola index +
                        else:
                            break
                    except: break
                for i in range(1, 3):  # Sprawdzenie 2 pól w poziomie
                    try:  # W lewo
                        if self.a_hit_fields[1][0] == 0: break
                        elif self.sheet_opponent[self.a_hit_fields[0][0]][self.a_hit_fields[1][0] - i] == entry:  # Jeśli pole jest puste dodaj do sąsiednich pól
                            self.a_neighboring_fields_horizontal[0].append(self.a_hit_fields[0][0])
                            self.a_neighboring_fields_horizontal[1].append(self.a_hit_fields[1][0] - i)
                            self.a_counter_fields_minus_h += 1  # dodanie pola index -
                        else:
                            break
                    except: break

                # Gdzie więcej wolnych pól, jeśli remis to w prawo
                if self.a_counter_fields_minus_h > self.a_counter_fields_plus_h:  # Strzelamy w lewo (index -)
                    self.a_kolumn = self.a_hit_fields[1][0] - 1
                elif self.a_counter_fields_minus_h <= self.a_counter_fields_plus_h:  # Strzelamy w prawo (index +)
                    self.a_kolumn = self.a_hit_fields[1][-1] + 1


            elif self.a_hit_fields[1][0] == self.a_hit_fields[1][1]:    # Statek jest w pionie
                self.a_kolumn = self.a_hit_fields[1][0]                     # Kolumna przyszłego strzału jest znana
                print(f'Będzie w pionie:  |')

                for i in range(1, 3):  # Sprawdzenie 2 pól w pionie
                    try:  # W dół
                        if self.sheet_opponent[self.a_hit_fields[0][-1] + i][self.a_hit_fields[1][-1]] == entry:  # Jeśli pole jest puste dodaj do sąsiednich pól
                            self.a_neighboring_fields_vertical[0].append(self.a_hit_fields[0][-1] + i)
                            self.a_neighboring_fields_vertical[1].append(self.a_hit_fields[1][-1])
                            self.a_counter_fields_plus_v += 1  # dodanie pola index +
                        else:
                            break
                    except: break
                for i in range(1, 3):  # Sprawdzenie 2 pól w pionie
                    try:  # W góre
                        if self.sheet_opponent[self.a_hit_fields[0][0] - i][self.a_hit_fields[1][0]] == entry:  # Jeśli pole jest puste dodaj do sąsiednich pól
                            self.a_neighboring_fields_vertical[0].append(self.a_hit_fields[0][0] - i)
                            self.a_neighboring_fields_vertical[1].append(self.a_hit_fields[1][0])
                            self.a_counter_fields_minus_v += 1  # dodanie pola index -
                        else:
                            break
                    except: break

                # Gdzie więcej wolnych pól, jeśli remis to w dół
                if self.a_counter_fields_minus_v > self.a_counter_fields_plus_v:  # Strzelamy w góre (index -)
                    self.a_row = self.a_hit_fields[0][0] - 1
                elif self.a_counter_fields_minus_v <= self.a_counter_fields_plus_v:  # Strzelamy w dół (index +)
                    self.a_row = self.a_hit_fields[0][-1] + 1


        self.a_counter_shots += 1
        print(f'self.a_row = {self.a_row}   self.a_kolumn = {self.a_kolumn}')

        return [self.a_row, self.a_kolumn]


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
close = '*'

game = Game()
game.loop_game()



