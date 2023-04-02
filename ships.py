from random import randint
from pyinputplus import inputChoice, inputInt, inputMenu
from colorama import Fore, init
import copy


class Game():
    def __init__(self):
        init(autoreset=True)                # Auto reset color
        self.end_game = False               # If 'True" end game

        self.lvl_bot = inputInt(prompt="Choose your opponent's level [1, 2]: ", min=1, max=2)
        self.comp = Player('Bot', 'N', self.lvl_bot)

        self.name_player = input('Your name: ')
        self.how_sets = inputChoice(['Y', 'N'], prompt='Do you want to set your ships manually? [Y, N]: ')

        # The third argument determines the method of shooting. If 'player' then the player himself chooses the shooting fields.
        # There are currently 3 algorithms to choose from, but the third is not yet finish.
        self.human = Player(self.name_player, self.how_sets, 'player')

        self.human.make_sheet()           # Setting up the player's ships. Automatic or manual.
        self.comp.make_sheet()            # Setting up the comp's ships. Automatic or manual.

    def loop_game(self):
        """Game Loop"""
        self.turn = 1
        while self.end_game == False:
            print(f'\nTurn: {self.turn}')
            self.turn += 1
            # Human's turn
            #self.human.counter_turn += 1
            while self.end_game == False:

                print(f"{self.human.name} ", end='')
                if self.human.shot(self.comp) == False:         # If the player misses
                    break
                else:                                           # If human hit
                    self.human.show_2_sheets(self.comp)  # Show sheets. The second argument is the object: opponent
                    self.sum_length = 0                         # Total fields of ships yet to be hit
                    for ship in self.comp.ships:
                        self.sum_length += ship.actual_length
                    if self.sum_length == 0:                    # If human destroyed all ships
                        print(f'\n\n{self.human.name} Win !!!')
                        self.end_game = True                    # Player Win. End game

            # Bot's turn
            print()
            #self.comp.counter_turn += 1
            while self.end_game == False:
                print(f"{self.comp.name} ", end='')
                if self.comp.shot(self.human) == False:         # If comp not hit
                    break
                else:                                           # If comp hit
                    self.sum_length = 0                         # Total fields of ships yet to be hit
                    for ship in self.human.ships:
                        self.sum_length += ship.actual_length
                    if self.sum_length == 0:                    # If comp destroyed all ships
                        print(f'\n\n{self.comp.name} Win !!!')
                        self.end_game = True                    # Bot Win. End game

            if self.end_game == False:
                self.human.show_2_sheets(self.comp)  # Show sheets. The second argument is the object: opponent


        self.human.show_2_sheets(self.comp, end_game=True)      # If end game show opponent's ships


class Player():
    def __init__(self, name, kind_of_make_sheet, kind_of_shot):
        self.name = name                                    # Name of player
        self.kind_of_make_sheet = kind_of_make_sheet        # The way ships are set up.
        self.kind_of_shot = kind_of_shot                    # Type of shooting. Algorithm or manual
        self.directions = ('vertical', 'horizontal')        # Direction of spacing of the ship
        self.sheet = [[empty for x in range(10)] for x in range(10)]    # empty sheet
        self.length_of_ships = (4, 3, 3, 2, 2, 2, 1, 1, 1, 1)           # The lengths of each of the 10 ships
        self.first_row = [x for x in range(0, 12)]                      # Headline line for the player, index 1-10
        self.first_row[0] = ''                                          # Hide unnecessary index
        self.first_row[11] = ''                                         # Hide unnecessary index
        self.last_row = [x for x in range(-1, 11)]                      # Last line with indices 0-9
        self.last_row[0] = ''                                           # Hide unnecessary index
        self.last_row[11] = ''                                          # Hide unnecessary index
        self.alphabet = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J')      # Alphabetical index, A-J
        self.ships = []                                                 # List of objects: Ships
        self.counter_turn = 0                                           # Turn counter
        self.change_dict = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9}

    def show_sheet(self):
        """Displaying the sheet of a given player"""
        #print(self.name)
        for char in self.first_row:                         # Print the headline. Index for player (1-10)
            print(f'{Fore.YELLOW}{char}', end='\t')
        print()

        for i, row in enumerate(self.sheet):
            print(f'{Fore.YELLOW}{self.alphabet[i]}', end='\t')     # Print the left index for player (A-J)
            for char in row:                                        # Print all char in sheet with color
                if char == destroyed:
                    print(f'{Fore.GREEN}{char}', end='\t')
                elif char == hit:
                    print(f'{Fore.RED}{char}', end='\t')
                elif type(char) == int:
                    print(f'{Fore.BLUE}{char}', end='\t')
                elif char == fail:
                    print(f'{Fore.MAGENTA}{char}', end='\t')
                elif char == empty:
                    print(f'{char}', end='\t')
                else:
                    print(char, end='\t')
            print()

    def make_sheet(self):
        """Creating a sheet with ships"""

        if self.kind_of_make_sheet == 'Y':                      # If set ships manual
            self.show_sheet()
            for length in self.length_of_ships:                 # Looping through the lengths of ships. 'Adding a ship to a sheet'
                while True:
                    self.question = f'\nFirst field of ship, length of ship = {Fore.BLUE}{length}{Fore.RESET} e.g. "10C" : '    # Text input
                    self.first_field = self.check_input(self.question)              # Assigning coordinates the first field of the ship.

                    self.row = self.first_field[0]                      # Index of row
                    self.column = self.first_field[1]                   # Index of column

                    self.fields_of_ship = [[], []]                      # A list of two lists storing the row and column indexes of all the ship's fields.
                    if length > 1:
                        self.direction = inputChoice(['v', 'h'], prompt='vertical or horizontal [v, h]: ')  # Selection of ship direction. Down(v) or right(h)

                    if self.direction == 'v':       # If down
                        self.direction = 0
                    elif self.direction == 'h':     # If right
                        self.direction = 1

                    if self.directions[self.direction] == 'vertical':           # If ship vertical
                        if self.row + length - 1 <= 9:                          # Checking that the row of the last field is not out of range.
                            for field in range(length):                         # Checking that all the ship's fields are empty.
                                if self.sheet[self.row + field][self.column] == empty:      # If so, add the field coordinates to the list of ship fields.
                                    self.fields_of_ship[0].append(self.row + field)
                                    self.fields_of_ship[1].append(self.column)
                                elif self.sheet[self.row + field][self.column] != empty:    # If not then ask for another coordinate first field
                                    print(f'{Fore.RED}A minimum of one of the fields is occupied or too close to another ship.')
                                    break

                        elif self.row + length - 1 > 9:                 # If row is too large. Repeat the while loop.
                            print(f'{Fore.RED}Too large a row index.')
                            continue


                    elif self.directions[self.direction] == 'horizontal':       # If ship horizontal
                        if self.column + length - 1 <= 9:                       # Checking that the column of the last field is not out of range.
                            for field in range(length):
                                if self.sheet[self.row][self.column + field] == empty:      # If so, add the field coordinates to the list of ship fields.
                                    self.fields_of_ship[0].append(self.row)
                                    self.fields_of_ship[1].append(self.column + field)
                                elif self.sheet[self.row][self.column + field] != empty:    # If not then ask for another coordinate first field
                                    print(f'{Fore.RED}A minimum of one of the fields is occupied or too close to another ship.')
                                    break

                        elif self.column + length - 1 > 9:              # If column is too large. Repeat the while loop.
                            print(f'{Fore.RED}Too large a column index.')
                            continue

                    # If the number of fields equals the length of the ship and there are no other ships nearby. Go to next ship in loop.
                    if len(self.fields_of_ship[0]) == length and self.check_space() == True:
                        break
                    else:
                        continue        # You can't put a ship here. Provide other coordinates. Repeat the while loop.

                # Add ship on sheet. The length of the ship is the mark on the sheet e.g. '3 3 3'
                for i in range(len(self.fields_of_ship[0])):
                    self.sheet[self.fields_of_ship[0][i]][self.fields_of_ship[1][i]] = len(self.fields_of_ship[0])
                self.ships.append(Ship(self.fields_of_ship))        # Created a list with object ships

                self.show_sheet()

            # Change 'close' to 'empty'. Hide outside space of ships.
            for r in range(len(self.sheet[0])):
                for c in range(len(self.sheet[r])):
                    if self.sheet[r][c] == close:
                        self.sheet[r][c] = empty

        elif self.kind_of_make_sheet == 'N':                # If set ships automatic
            for length in self.length_of_ships:             # Looping through the lengths of ships
                while True:
                    self.direction = randint(0, 1)          # Choice vertical or horizontal
                    self.row = randint(0, 9)
                    self.column = randint(0, 9)
                    self.fields_of_ship = [[], []]

                    if self.directions[self.direction] == 'vertical':           # If ship vertical
                        if self.row + length - 1 <= 9:                          # Checking that the row of the last field is not out of range.
                            for field in range(length):                         # Checking that all the ship's fields are empty.
                                if self.sheet[self.row + field][self.column] == empty:      # If so, add the field coordinates to the list of ship fields.
                                    self.fields_of_ship[0].append(self.row + field)
                                    self.fields_of_ship[1].append(self.column)
                                elif self.sheet[self.row + field][self.column] != empty:    # If not then ask for another coordinate first field
                                    break

                        elif self.row + length - 1 > 9:                         # If row is too large. Repeat the while loop.
                            continue

                    elif self.directions[self.direction] == 'horizontal':       # If ship horizontal
                        self.fields_of_ship = self.fields_of_ship[::-1]         # TODO
                        if self.column + length - 1 <= 9:                       # Checking that the column of the last field is not out of range.
                            for field in range(length):                         # Checking that all the ship's fields are empty.
                                if self.sheet[self.row][self.column + field] == empty:      # If so, add the field coordinates to the list of ship fields.
                                    self.fields_of_ship[0].append(self.row)
                                    self.fields_of_ship[1].append(self.column + field)
                                elif self.sheet[self.row][self.column + field] != empty:    # If not then ask for another coordinate first field
                                    break

                        elif self.column + length - 1 > 9:                              # If column is too large. Repeat the while loop.
                            continue

                    # If the number of fields equals the length of the ship and there are no other ships nearby. Go to next ship in loop.
                    if len(self.fields_of_ship[0]) == length and self.check_space() == True:
                        break
                    else:
                        continue        # You can't put a ship here. Provide other coordinates. Repeat the while loop.

                # Add ship on sheet. The length of the ship is the mark on the sheet e.g. '3 3 3'
                for i in range(len(self.fields_of_ship[0])):
                    self.sheet[self.fields_of_ship[0][i]][self.fields_of_ship[1][i]] = len(self.fields_of_ship[0])
                self.ships.append(Ship(self.fields_of_ship))

            # Change 'close' to 'empty'. Hide outside space of ships.
            for r in range(len(self.sheet[0])):
                for c in range(len(self.sheet[r])):
                    if self.sheet[r][c] == close:
                        self.sheet[r][c] = empty

    def check_input(self, question):
        """
        Converts the input e.g. '3F', to indexes 0-9.
        Return List [row, kolumn]
        """

        while True:
            self.letter_cord = []
            self.digit_cord = []
            self.answer = input(question).upper()

            if len(self.answer) == 2 or len(self.answer) == 3:  # If lenght of answer is 2 or 3
                for i in self.answer:
                    if i.isupper():
                        self.letter_cord.append(i)              # ADD letter
                    elif i.isdigit():
                        self.digit_cord.append(i)               # Add digit to list

                if len(self.letter_cord) != 1:                  # If there is no letter. Repeat the while loop.
                    continue
                if len(self.digit_cord) == 1:                           # If there is one digit
                    self.digit_cord[0] = int(self.digit_cord[0]) - 1
                elif len(self.digit_cord) == 2:
                    self.digit_cord[0] = int(self.digit_cord[0] + self.digit_cord[1]) - 1       # If there is two digits then join

                if self.digit_cord[0] < 0 or self.digit_cord[0] > 9:        # If the column is out of range. Repeat the while loop.
                    continue
                elif 0 <= self.digit_cord[0] <= 9:                      # If the column index is in range then try sending coordinates.
                    try:
                        return [self.change_dict[self.letter_cord[0]], self.digit_cord[0]]
                    except:                                             # If the wrong letter is given. Repeat the while loop.
                        print('The letters must be in the range A-J')

    def check_space(self):
        """
        Checks for other ships in the vicinity
        self.fields_of_ship e.g. [[2, 3, 4], [3, 3, 3]]
        First rows, secend kolumns. Values always ascending
        """

        self.space_of_fields = [[], []]
        # Adding non-repeating elements by making a dictionary.
        self.space_of_fields[0] = list(dict.fromkeys(self.fields_of_ship[0]))
        self.space_of_fields[1] = list(dict.fromkeys(self.fields_of_ship[1]))

        # Creating a grid of fields. Adding extreme indexes, 4 corners.
        self.space_of_fields[0].append(self.fields_of_ship[0][0] - 1)
        self.space_of_fields[0].append(self.fields_of_ship[0][-1] + 1)
        self.space_of_fields[1].append(self.fields_of_ship[1][0] - 1)
        self.space_of_fields[1].append(self.fields_of_ship[1][-1] + 1)

        # Removal of indexes -1 and 10 in rows and kolumns
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

        # Adding inaccessible spaces as 'close'
        for r in self.space_of_fields[0]:
            for k in self.space_of_fields[1]:
                if self.sheet[r][k] == empty or self.sheet[r][k] == close:
                    self.sheet[r][k] = close
                else:
                    return False        # If ship is too close other ship

        return True         # If there are no other ships in the vicinity

    def hide_ships_on_sheet(self, opponent):
        """Hiding opponent ships on the sheet."""
        self.sheet_opponent = [[empty for x in range(10)] for x in range(10)]

        for r in range(10):
            for k in range(10):
                if type(opponent.sheet[r][k]) == int:       # If integer, change to 'empty'
                    self.sheet_opponent[r][k] = empty
                else:
                    self.sheet_opponent[r][k] = opponent.sheet[r][k]

        return self.sheet_opponent

    def shot(self, opponent):
        """Selects the method to generate the shot (row and column) and checks is it misses or hits."""

        if self.kind_of_shot == 'player':       # If player is shoting, get coordinates
            while True:
                self.question = f'shot: '
                self.field_of_shot = self.check_input(self.question)
                break

        elif self.kind_of_shot == 1:        # If Bot is shoting, get coordinates (lvl = 1)
            self.hide_ships_on_sheet(opponent)      # Show sheet and hide ships of opponent
            self.field_of_shot = self.shooting_algorithm_1(opponent)      # Use shooting algorithm

        elif self.kind_of_shot == 2:        # If Bot is shoting, get coordinates (lvl = 2)
            self.hide_ships_on_sheet(opponent)      # Show sheet and hide ships of opponent
            self.field_of_shot = self.shooting_algorithm_2(opponent.ships)      # Use shooting algorithm

        elif self.kind_of_shot == 3:        # If Bot is shoting, get coordinates (lvl = 3)
            self.hide_ships_on_sheet(opponent)      # Show sheet and hide ships of opponent
            self.field_of_shot = self.shooting_algorithm_3(opponent.ships)      # Use shooting algorithm

        self.display_cord = []
        self.display_cord.append(list(self.change_dict.keys())[self.field_of_shot[0]])  # Converting the row index to the letters A-J for display
        self.display_cord.append(self.field_of_shot[1] + 1)                             # Index kolumn + 1 (1-10)

        if opponent.sheet[self.field_of_shot[0]][self.field_of_shot[1]] == empty:       # If field wos 'empty'
            opponent.sheet[self.field_of_shot[0]][self.field_of_shot[1]] = fail         # Now is 'fail'
            print(f'{self.display_cord[1]}{self.display_cord[0]} = {Fore.MAGENTA}O')
            return False                # Is not hit

        elif type(opponent.sheet[self.field_of_shot[0]][self.field_of_shot[1]]) == int:     # If field is 'int'
            opponent.sheet[self.field_of_shot[0]][self.field_of_shot[1]] = hit              # Now is 'hit'
            print(f'{self.display_cord[1]}{self.display_cord[0]} = {Fore.RED}X')
            for ship in opponent.ships:
                for i in range(len(ship.fields[0])):                                        # Looking for a damaged ship
                    if ship.fields[0][i] == self.field_of_shot[0] and ship.fields[1][i] == self.field_of_shot[1]:       # If the ship's field is equal to the shot
                        ship.actual_length -= 1                                     # Reduce the current length of the ship
                        ship.actual_fields[0].remove(self.field_of_shot[0])         # Delete the row field
                        ship.actual_fields[1].remove(self.field_of_shot[1])         # Delete the column field

                        if ship.actual_length == 0:                                 # If ship is destroyed
                            print(f'{self.name} destroyed ship: {Fore.BLUE}{destroyed * ship.length_of_ship}')
                            opponent.ships.remove(ship)                             # Delete object from list of ships
                            for i in range(len(ship.fields[0])):
                                opponent.sheet[ship.fields[0][i]][ship.fields[1][i]] = destroyed  # Changing the characters on the sheet. 'hit' to 'destroyed'

            return True                 # Is hit

        elif opponent.sheet[self.field_of_shot[0]][self.field_of_shot[1]] == close:     # If shot is too close to another ship
            print('This field is too close to another ship')
            return True

        else:               # You've already shot here
            print(f"Choose another field - you've already shot here")
            return True

    def show_2_sheets(self, opponent, end_game=False):
        """Displaying the sheets"""
        self.sheets_together = copy.deepcopy(opponent.sheet)

        for char in self.first_row * 2:             # Print the headline for 2 sheets. Index for player (1-10)
            print(f'{Fore.YELLOW}{char}', end='\t')
        print()

        for r in range(10):
            print(f'{Fore.YELLOW}{self.alphabet[r]}', end='\t')         # Print the left index for player (A-J)
            for k in range(10):
                if opponent.sheet[r][k] == destroyed:
                    print(f'{Fore.BLUE}{opponent.sheet[r][k]}', end='\t')
                elif opponent.sheet[r][k] == hit:
                    print(f'{Fore.RED}{opponent.sheet[r][k]}', end='\t')
                elif type(opponent.sheet[r][k]) == int and end_game == False:   # Hide opponent's ships
                    print(f'{empty}', end='\t')
                elif type(opponent.sheet[r][k]) == int and end_game == True:    # If end game show opponent's ships
                    print(f'{Fore.GREEN}{opponent.sheet[r][k]}', end='\t')
                elif opponent.sheet[r][k] == fail:
                    print(f'{Fore.MAGENTA}{opponent.sheet[r][k]}', end='\t')
                elif opponent.sheet[r][k] == empty:
                    print(f'{opponent.sheet[r][k]}', end='\t')
                elif opponent.sheet[r][k] == close:
                    print(f'{opponent.sheet[r][k]}', end='\t')
                    opponent.sheet[r][k] = empty
                else:
                    print(opponent.sheet[r][k], end='\t')

            #print(f'{Fore.YELLOW}{range(10)[r]}', end=' - ')           # Hide index 0-9
            print(f'{Fore.YELLOW}{self.alphabet[r]} |', end='\t')       # Print the index for player (A-J)
            print(f'{Fore.YELLOW}{self.alphabet[r]}', end='\t')         # Print the index for player (A-J)
            for k in range(10):
                if self.sheet[r][k] == destroyed:
                    print(f'{Fore.GREEN}{self.sheet[r][k]}', end='\t')
                elif self.sheet[r][k] == hit:
                    print(f'{Fore.RED}{self.sheet[r][k]}', end='\t')
                elif type(self.sheet[r][k]) == int:
                    print(f'{Fore.BLUE}{self.sheet[r][k]}', end='\t')
                elif self.sheet[r][k] == fail:
                    print(f'{Fore.MAGENTA}{self.sheet[r][k]}', end='\t')
                elif self.sheet[r][k] == empty:
                    print(f'{self.sheet[r][k]}', end='\t')
                else:
                    print(self.sheet[r][k], end='\t')
            print(f'{Fore.YELLOW}{self.alphabet[r]}', end='\t')         # Print the index for player (A-J)
            #print(f'{Fore.YELLOW}{range(10)[r]}', end='\t')            # Hide index 0-9
            print()

        for char in self.first_row * 2:  # Print first row * 2          # Can change last_row (0-9) on first_row (1-10)
            print(f'{Fore.YELLOW}{char}', end='\t')
        print()

    # Algorithms:

    def shooting_algorithm_1(self, opponent):
        """ Return random index [row, column] ---  Level: easy"""
        self.shot_row = randint(0, 9)
        self.shot_kolumn = randint(0, 9)

        if type(opponent.sheet[self.shot_row][self.shot_kolumn]) == int or opponent.sheet[self.shot_row][self.shot_kolumn] == empty:
            return [self.shot_row, self.shot_kolumn]

        else:
            return self.shooting_algorithm_1(opponent)

    def shooting_algorithm_2(self, ships_opponent):
        """
        Return index [row, column] ---  Level: intermediate
        self.sheet_opponent - opponent's sheet with hide ships
        """

        self.a_ships_opponent = ships_opponent
        self.a_neighboring_fields_vertical = [[], []]
        self.a_neighboring_fields_horizontal = [[], []]
        self.a_hit_fields = [[], []]
        self.a_empty_fields = [[], []]
        self.a_counter_fields_plus_h = 0
        self.a_counter_fields_minus_h = 0
        self.a_counter_fields_plus_v = 0
        self.a_counter_fields_minus_v = 0


        for r in range(10):
            for k in range(10):
                if self.sheet_opponent[r][k] == destroyed:            # If the field is hit, the adjacent field changes to 'close'
                    if r < 9:
                        if self.sheet_opponent[r + 1][k] == empty:
                            self.sheet_opponent[r + 1][k] = close
                    if r > 0:
                        if self.sheet_opponent[r - 1][k] == empty:
                            self.sheet_opponent[r - 1][k] = close
                    if k < 9:
                        if self.sheet_opponent[r][k + 1] == empty:
                            self.sheet_opponent[r][k + 1] = close
                    if k > 0:
                        if self.sheet_opponent[r][k - 1] == empty:
                            self.sheet_opponent[r][k - 1] = close

                    if r < 9 and k < 9:
                        self.sheet_opponent[r + 1][k + 1] = close
                    if r < 9 and k > 0:
                        self.sheet_opponent[r + 1][k - 1] = close
                    if r > 0 and k < 9:
                        self.sheet_opponent[r - 1][k + 1] = close
                    if r > 0 and k > 0:
                        self.sheet_opponent[r - 1][k - 1] = close

        for r in range(10):         # Searching for a hit
            for k in range(10):
                if self.sheet_opponent[r][k] == hit:                    # If field = hit, add field to hit list
                    self.a_hit_fields[0].append(r)
                    self.a_hit_fields[1].append(k)
                elif self.sheet_opponent[r][k] == empty:                # If field = empty, add field to empty list
                    self.a_empty_fields[0].append(r)
                    self.a_empty_fields[1].append(k)


        if len(self.a_hit_fields[0]) == 0:                              # If there is no hit in the sheet
            self.a_index = randint(0, len(self.a_empty_fields[0]) - 1)
            self.a_row = self.a_empty_fields[0][self.a_index]
            self.a_kolumn = self.a_empty_fields[1][self.a_index]

        elif len(self.a_hit_fields[0]) == 1:    # If there is one hit you need to check the number of free fields in two directions
            for i in range(1, 4):  # Check 3 fields
                try:  # Right
                    if self.sheet_opponent[self.a_hit_fields[0][0]][self.a_hit_fields[1][0] + i] == empty:  # If the field is empty add to the adjacent fields
                        self.a_neighboring_fields_horizontal[0].append(self.a_hit_fields[0][0])
                        self.a_neighboring_fields_horizontal[1].append(self.a_hit_fields[1][0] + i)
                        self.a_counter_fields_plus_h += 1
                    else: break
                except: break

            for i in range(1, 4):  # Check 3 fields
                try:  # Left
                    if self.a_hit_fields[1][0] - i == -1: break
                    elif self.sheet_opponent[self.a_hit_fields[0][0]][self.a_hit_fields[1][0] - i] == empty:  # If the field is empty add to the adjacent fields
                        self.a_neighboring_fields_horizontal[0].append(self.a_hit_fields[0][0])
                        self.a_neighboring_fields_horizontal[1].append(self.a_hit_fields[1][0] - i)
                        self.a_counter_fields_minus_h += 1
                    else: break
                except: break

            for i in range(1, 4):  # Check 3 fields
                try:  # Down
                    if self.sheet_opponent[self.a_hit_fields[0][0] + i][self.a_hit_fields[1][0]] == empty:  # If the field is empty add to the adjacent fields
                        self.a_neighboring_fields_vertical[0].append(self.a_hit_fields[0][0] + i)
                        self.a_neighboring_fields_vertical[1].append(self.a_hit_fields[1][0])
                        self.a_counter_fields_plus_v += 1
                    else: break
                except: break

            for i in range(1, 4):  # Check 3 fields
                try:  # Up
                    if self.a_hit_fields[0][0] - i == -1: break
                    elif self.sheet_opponent[self.a_hit_fields[0][0] - i][self.a_hit_fields[1][0]] == empty:  # If the field is empty add to the adjacent fields
                        self.a_neighboring_fields_vertical[0].append(self.a_hit_fields[0][0] - i)
                        self.a_neighboring_fields_vertical[1].append(self.a_hit_fields[1][0])
                        self.a_counter_fields_minus_v += 1
                    else: break
                except: break


            if len(self.a_neighboring_fields_horizontal[0]) > len(self.a_neighboring_fields_vertical[0]):       # If more free fields horizontally
                if self.a_counter_fields_minus_h > self.a_counter_fields_plus_h:                                # If more free fields in left
                    if self.sheet_opponent[self.a_hit_fields[0][0]][self.a_hit_fields[1][0] - 1] == empty:      # Shoot to the left (index -) if is 'empty'
                        self.a_row = self.a_hit_fields[0][0]
                        self.a_kolumn = self.a_hit_fields[1][0] - 1
                    else:                                                   # Shoot to the right (index +)
                        self.a_row = self.a_hit_fields[0][-1]
                        self.a_kolumn = self.a_hit_fields[1][-1] + 1

                elif self.a_counter_fields_minus_h <= self.a_counter_fields_plus_h:                             # If more free fields in right or =
                    if self.sheet_opponent[self.a_hit_fields[0][0]][self.a_hit_fields[1][0] + 1] == empty:      # Shoot to the right (index +) if is 'empty'
                        self.a_row = self.a_hit_fields[0][-1]
                        self.a_kolumn = self.a_hit_fields[1][-1] + 1
                    else:                                                   # Shoot to the left (index -)
                        self.a_row = self.a_hit_fields[0][0]
                        self.a_kolumn = self.a_hit_fields[1][0] - 1

            elif len(self.a_neighboring_fields_horizontal[0]) <= len(self.a_neighboring_fields_vertical[0]):    # If more free fields vertically or =
                if self.a_counter_fields_minus_v > self.a_counter_fields_plus_v:                                # If more free fields in up
                    if self.sheet_opponent[self.a_hit_fields[0][0] - 1][self.a_hit_fields[1][0]] == empty:      # # Shoot to the up (index -)
                        self.a_row = self.a_hit_fields[0][0] - 1
                        self.a_kolumn = self.a_hit_fields[1][0]
                    else:                                                   # Shoot to the down (index +)
                        self.a_row = self.a_hit_fields[0][-1] + 1
                        self.a_kolumn = self.a_hit_fields[1][-1]


                elif self.a_counter_fields_minus_v <= self.a_counter_fields_plus_v:                             # If more free fields in down or =
                    if self.sheet_opponent[self.a_hit_fields[0][0] + 1][self.a_hit_fields[1][0]] == empty:      # Shoot to the down (index +)
                        self.a_row = self.a_hit_fields[0][-1] + 1
                        self.a_kolumn = self.a_hit_fields[1][-1]
                    else:                                                   # Shoot to the up (index -)
                        self.a_row = self.a_hit_fields[0][0] - 1
                        self.a_kolumn = self.a_hit_fields[1][0]

        elif len(self.a_hit_fields[0]) > 1:                             # If there is minimum 2 hit you need to check the number of free fields in two directions
            if self.a_hit_fields[0][0] == self.a_hit_fields[0][1]:          # The ship is horizontal. Index of the row is known.
                self.a_row = self.a_hit_fields[0][0]
                for i in range(1, 3):   # Checking 2 fields to right
                    try:
                        if self.sheet_opponent[self.a_hit_fields[0][-1]][self.a_hit_fields[1][-1] + i] == empty:  # If the field is empty add to the adjacent fields
                            self.a_neighboring_fields_horizontal[0].append(self.a_hit_fields[0][-1])
                            self.a_neighboring_fields_horizontal[1].append(self.a_hit_fields[1][-1] + i)
                            self.a_counter_fields_plus_h += 1           # Increase the counter of free fields to the right (index kolumn +)
                        else:
                            break
                    except: break
                for i in range(1, 3):  # Checking 2 fields to left
                    try:
                        if self.a_hit_fields[1][0] == 0: break
                        elif self.sheet_opponent[self.a_hit_fields[0][0]][self.a_hit_fields[1][0] - i] == empty:  # If the field is empty add to the adjacent fields
                            self.a_neighboring_fields_horizontal[0].append(self.a_hit_fields[0][0])
                            self.a_neighboring_fields_horizontal[1].append(self.a_hit_fields[1][0] - i)
                            self.a_counter_fields_minus_h += 1          # Increase the counter of free fields to the left (index kolumn -)
                        else:
                            break
                    except: break

                if self.a_counter_fields_minus_h > self.a_counter_fields_plus_h:    # If more free fields to the left then we shoot to the left
                    self.a_kolumn = self.a_hit_fields[1][0] - 1
                elif self.a_counter_fields_minus_h <= self.a_counter_fields_plus_h: # If more free fields to the right or the same amount, we shoot to the right
                    self.a_kolumn = self.a_hit_fields[1][-1] + 1


            elif self.a_hit_fields[1][0] == self.a_hit_fields[1][1]:        # The ship is vertical. Index of the kolumn is known.
                self.a_kolumn = self.a_hit_fields[1][0]

                for i in range(1, 3):  # Checking 2 fields to down
                    try:
                        if self.sheet_opponent[self.a_hit_fields[0][-1] + i][self.a_hit_fields[1][-1]] == empty:    # If the field is empty add to the adjacent fields
                            self.a_neighboring_fields_vertical[0].append(self.a_hit_fields[0][-1] + i)
                            self.a_neighboring_fields_vertical[1].append(self.a_hit_fields[1][-1])
                            self.a_counter_fields_plus_v += 1  # Increase the counter of free fields to the down (index row +)
                        else:
                            break
                    except: break
                for i in range(1, 3):  # Checking 2 fields to up
                    try:
                        if self.sheet_opponent[self.a_hit_fields[0][0] - i][self.a_hit_fields[1][0]] == empty:      # If the field is empty add to the adjacent fields
                            self.a_neighboring_fields_vertical[0].append(self.a_hit_fields[0][0] - i)
                            self.a_neighboring_fields_vertical[1].append(self.a_hit_fields[1][0])
                            self.a_counter_fields_minus_v += 1  # Increase the counter of free fields to the up (index kolumn -)
                        else:
                            break
                    except: break

                if self.a_counter_fields_minus_v > self.a_counter_fields_plus_v:        # If more free fields to the up then we shoot to the up
                    self.a_row = self.a_hit_fields[0][0] - 1
                elif self.a_counter_fields_minus_v <= self.a_counter_fields_plus_v:     # If more free fields to the down or the same amount, we shoot to the down
                    self.a_row = self.a_hit_fields[0][-1] + 1


        return [self.a_row, self.a_kolumn]

    def shooting_algorithm_3(self, ships_opponent):
        """
        Return index [row, column] ---  Level: intermediate
        self.sheet_opponent - opponent's sheet with hide ships
        """

        self.a_ships_opponent = ships_opponent
        self.a_neighboring_fields_vertical = [[], []]
        self.a_neighboring_fields_horizontal = [[], []]
        self.a_hit_fields = [[], []]
        self.a_empty_fields = [[], []]
        self.a_counter_fields_plus_h = 0
        self.a_counter_fields_minus_h = 0
        self.a_counter_fields_plus_v = 0
        self.a_counter_fields_minus_v = 0
        self.dict_ships = {1: 0, 2: 0, 3: 0, 4: 0}
        self.free_4 = [[], []]
        self.free_3 = [[], []]
        self.free_2 = [[], []]
        self.free_1 = [[], []]

        for r in range(10):
            for k in range(10):
                if self.sheet_opponent[r][k] == destroyed:            # If the field is hit, the adjacent field changes to 'close'
                    if r < 9:
                        if self.sheet_opponent[r + 1][k] == empty:
                            self.sheet_opponent[r + 1][k] = close
                    if r > 0:
                        if self.sheet_opponent[r - 1][k] == empty:
                            self.sheet_opponent[r - 1][k] = close
                    if k < 9:
                        if self.sheet_opponent[r][k + 1] == empty:
                            self.sheet_opponent[r][k + 1] = close
                    if k > 0:
                        if self.sheet_opponent[r][k - 1] == empty:
                            self.sheet_opponent[r][k - 1] = close

                    if r < 9 and k < 9:
                        self.sheet_opponent[r + 1][k + 1] = close
                    if r < 9 and k > 0:
                        self.sheet_opponent[r + 1][k - 1] = close
                    if r > 0 and k < 9:
                        self.sheet_opponent[r - 1][k + 1] = close
                    if r > 0 and k > 0:
                        self.sheet_opponent[r - 1][k - 1] = close

        for r in range(10):         # Searching for a hit
            for k in range(10):
                if self.sheet_opponent[r][k] == hit:                    # If field = hit, add field to hit list
                    self.a_hit_fields[0].append(r)
                    self.a_hit_fields[1].append(k)
                elif self.sheet_opponent[r][k] == empty:                # If field = empty, add field to empty list
                    self.a_empty_fields[0].append(r)
                    self.a_empty_fields[1].append(k)


        if len(self.a_hit_fields[0]) == 0:                              # If there is no hit in the sheet
            '''for ship in self.a_ships_opponent:
                if ship.actual_length == 1:
                    self.dict_ships[1] += 1
                elif ship.actual_length == 2:
                    self.dict_ships[2] += 1
                elif ship.actual_length == 3:
                    self.dict_ships[3] += 1
                elif ship.actual_length == 4:
                    self.dict_ships[4] += 1
            #print(f'Ships: {self.dict_ships}')'''
            print(self.a_empty_fields)
            for i in range(len(self.a_empty_fields[0])):
                try:
                    if self.sheet_opponent[self.a_empty_fields[0][i] + 1][self.a_empty_fields[1][i]] == empty:
                        self.a_counter_fields_plus_v += 1
                except: pass
                try:
                    if self.sheet_opponent[self.a_empty_fields[0][i] - 1][self.a_empty_fields[1][i]] == empty:
                        self.a_counter_fields_minus_v += 1
                except: pass
                try:
                    if self.sheet_opponent[self.a_empty_fields[0][i]][self.a_empty_fields[1][i] + 1] == empty:
                        self.a_counter_fields_plus_h += 1
                except: pass
                try:
                    if self.sheet_opponent[self.a_empty_fields[0][i]][self.a_empty_fields[1][i] - 1] == empty:
                        self.a_counter_fields_minus_h += 1
                except: pass

                if self.a_counter_fields_plus_v + self.a_counter_fields_minus_v + self.a_counter_fields_plus_h + self.a_counter_fields_minus_h == 4:
                    self.free_4[0].append(self.a_empty_fields[0][i])
                    self.free_4[1].append(self.a_empty_fields[1][i])
                    print(f'Dodaje do free_4: {self.a_empty_fields[0][i]}, {self.a_empty_fields[1][i]}')
                elif self.a_counter_fields_plus_v + self.a_counter_fields_minus_v + self.a_counter_fields_plus_h + self.a_counter_fields_minus_h == 3:
                    self.free_3[0].append(self.a_empty_fields[0][i])
                    self.free_3[1].append(self.a_empty_fields[1][i])
                    print(f'Dodaje do free_3: {self.a_empty_fields[0][i]}, {self.a_empty_fields[1][i]}')
                elif self.a_counter_fields_plus_v + self.a_counter_fields_minus_v + self.a_counter_fields_plus_h + self.a_counter_fields_minus_h == 2:
                    self.free_2[0].append(self.a_empty_fields[0][i])
                    self.free_2[1].append(self.a_empty_fields[1][i])
                    print(f'Dodaje do free_2: {self.a_empty_fields[0][i]}, {self.a_empty_fields[1][i]}')
                elif self.a_counter_fields_plus_v + self.a_counter_fields_minus_v + self.a_counter_fields_plus_h + self.a_counter_fields_minus_h == 1:
                    self.free_1[0].append(self.a_empty_fields[0][i])
                    self.free_1[1].append(self.a_empty_fields[1][i])
                    print(f'Dodaje do free_1: {self.a_empty_fields[0][i]}, {self.a_empty_fields[1][i]}')

            if len(self.free_4[0]) > 0:
                i = randint(0, len(self.free_4[0]) - 1)
                self.a_row = self.free_4[0][i]
                self.a_kolumn = self.free_4[1][i]
                print(f'W 4: {self.free_4}')

            elif len(self.free_3[0]) > 0:
                i = randint(0, len(self.free_3[0]) - 1)
                self.a_row = self.free_3[0][i]
                self.a_kolumn = self.free_3[1][i]
                print(f'W 3: {self.free_3}')

            elif len(self.free_2[0]) > 0:
                i = randint(0, len(self.free_2[0]) - 1)
                self.a_row = self.free_2[0][i]
                self.a_kolumn = self.free_2[1][i]
                print(f'W 2: {self.free_2}')

            elif len(self.free_1[0]) > 0:
                i = randint(0, len(self.free_1[0]) - 1)
                self.a_row = self.free_1[0][i]
                self.a_kolumn = self.free_1[1][i]
                print(f'W 1: {self.free_1}')

            else:
                i = randint(0, len(self.a_empty_fields[0]) - 1)
                self.a_row = self.a_empty_fields[0][i]
                self.a_kolumn = self.a_empty_fields[1][i]
                print(f'0')

            return [self.a_row, self.a_kolumn]

        elif len(self.a_hit_fields[0]) == 1:    # If there is one hit you need to check the number of free fields in two directions
            for i in range(1, 4):  # Check 3 fields
                try:  # Right
                    if self.sheet_opponent[self.a_hit_fields[0][0]][self.a_hit_fields[1][0] + i] == empty:  # If the field is empty add to the adjacent fields
                        self.a_neighboring_fields_horizontal[0].append(self.a_hit_fields[0][0])
                        self.a_neighboring_fields_horizontal[1].append(self.a_hit_fields[1][0] + i)
                        self.a_counter_fields_plus_h += 1
                    else: break
                except: break

            for i in range(1, 4):  # Check 3 fields
                try:  # Left
                    if self.a_hit_fields[1][0] - i == -1: break
                    elif self.sheet_opponent[self.a_hit_fields[0][0]][self.a_hit_fields[1][0] - i] == empty:  # If the field is empty add to the adjacent fields
                        self.a_neighboring_fields_horizontal[0].append(self.a_hit_fields[0][0])
                        self.a_neighboring_fields_horizontal[1].append(self.a_hit_fields[1][0] - i)
                        self.a_counter_fields_minus_h += 1
                    else: break
                except: break

            for i in range(1, 4):  # Check 3 fields
                try:  # Down
                    if self.sheet_opponent[self.a_hit_fields[0][0] + i][self.a_hit_fields[1][0]] == empty:  # If the field is empty add to the adjacent fields
                        self.a_neighboring_fields_vertical[0].append(self.a_hit_fields[0][0] + i)
                        self.a_neighboring_fields_vertical[1].append(self.a_hit_fields[1][0])
                        self.a_counter_fields_plus_v += 1
                    else: break
                except: break

            for i in range(1, 4):  # Check 3 fields
                try:  # Up
                    if self.a_hit_fields[0][0] - i == -1: break
                    elif self.sheet_opponent[self.a_hit_fields[0][0] - i][self.a_hit_fields[1][0]] == empty:  # If the field is empty add to the adjacent fields
                        self.a_neighboring_fields_vertical[0].append(self.a_hit_fields[0][0] - i)
                        self.a_neighboring_fields_vertical[1].append(self.a_hit_fields[1][0])
                        self.a_counter_fields_minus_v += 1
                    else: break
                except: break

            '''print(f'Ilość wolnych pól w poziomie: {len(self.a_neighboring_fields_horizontal[0])}')
            print(f'Ilość wolnych pól w pionie: {len(self.a_neighboring_fields_vertical[0])}')
            print(f'Ilość pól horizontal o index- : {self.a_counter_fields_minus_h}')
            print(f'Ilość pól horizontal o index+ : {self.a_counter_fields_plus_h}')
            print(f'Ilość pól vertical o index- : {self.a_counter_fields_minus_v}')
            print(f'Ilość pól vertical o index+ : {self.a_counter_fields_plus_v}')'''

            if len(self.a_neighboring_fields_horizontal[0]) > len(self.a_neighboring_fields_vertical[0]):       # If more free fields horizontally
                if self.a_counter_fields_minus_h > self.a_counter_fields_plus_h:                                # If more free fields in left
                    if self.sheet_opponent[self.a_hit_fields[0][0]][self.a_hit_fields[1][0] - 1] == empty:      # Shoot to the left (index -) if is 'empty'
                        self.a_row = self.a_hit_fields[0][0]
                        self.a_kolumn = self.a_hit_fields[1][0] - 1
                    else:                                                   # Shoot to the right (index +)
                        self.a_row = self.a_hit_fields[0][-1]
                        self.a_kolumn = self.a_hit_fields[1][-1] + 1

                elif self.a_counter_fields_minus_h <= self.a_counter_fields_plus_h:                             # If more free fields in right or =
                    if self.sheet_opponent[self.a_hit_fields[0][0]][self.a_hit_fields[1][0] + 1] == empty:      # Shoot to the right (index +) if is 'empty'
                        self.a_row = self.a_hit_fields[0][-1]
                        self.a_kolumn = self.a_hit_fields[1][-1] + 1
                    else:                                                   # Shoot to the left (index -)
                        self.a_row = self.a_hit_fields[0][0]
                        self.a_kolumn = self.a_hit_fields[1][0] - 1

            elif len(self.a_neighboring_fields_horizontal[0]) <= len(self.a_neighboring_fields_vertical[0]):    # If more free fields vertically or =
                if self.a_counter_fields_minus_v > self.a_counter_fields_plus_v:                                # If more free fields in up
                    if self.sheet_opponent[self.a_hit_fields[0][0] - 1][self.a_hit_fields[1][0]] == empty:      # # Shoot to the up (index -)
                        self.a_row = self.a_hit_fields[0][0] - 1
                        self.a_kolumn = self.a_hit_fields[1][0]
                    else:                                                   # Shoot to the down (index +)
                        self.a_row = self.a_hit_fields[0][-1] + 1
                        self.a_kolumn = self.a_hit_fields[1][-1]


                elif self.a_counter_fields_minus_v <= self.a_counter_fields_plus_v:                             # If more free fields in down or =
                    if self.sheet_opponent[self.a_hit_fields[0][0] + 1][self.a_hit_fields[1][0]] == empty:      # Shoot to the down (index +)
                        self.a_row = self.a_hit_fields[0][-1] + 1
                        self.a_kolumn = self.a_hit_fields[1][-1]
                    else:                                                   # Shoot to the up (index -)
                        self.a_row = self.a_hit_fields[0][0] - 1
                        self.a_kolumn = self.a_hit_fields[1][0]

        elif len(self.a_hit_fields[0]) > 1:                             # If there is minimum 2 hit you need to check the number of free fields in two directions
            if self.a_hit_fields[0][0] == self.a_hit_fields[0][1]:          # The ship is horizontal. Index of the row is known.
                self.a_row = self.a_hit_fields[0][0]
                for i in range(1, 3):   # Checking 2 fields to right
                    try:
                        if self.sheet_opponent[self.a_hit_fields[0][-1]][self.a_hit_fields[1][-1] + i] == empty:  # If the field is empty add to the adjacent fields
                            self.a_neighboring_fields_horizontal[0].append(self.a_hit_fields[0][-1])
                            self.a_neighboring_fields_horizontal[1].append(self.a_hit_fields[1][-1] + i)
                            self.a_counter_fields_plus_h += 1           # Increase the counter of free fields to the right (index kolumn +)
                        else:
                            break
                    except: break
                for i in range(1, 3):  # Checking 2 fields to left
                    try:
                        if self.a_hit_fields[1][0] == 0: break
                        elif self.sheet_opponent[self.a_hit_fields[0][0]][self.a_hit_fields[1][0] - i] == empty:  # If the field is empty add to the adjacent fields
                            self.a_neighboring_fields_horizontal[0].append(self.a_hit_fields[0][0])
                            self.a_neighboring_fields_horizontal[1].append(self.a_hit_fields[1][0] - i)
                            self.a_counter_fields_minus_h += 1          # Increase the counter of free fields to the left (index kolumn -)
                        else:
                            break
                    except: break

                if self.a_counter_fields_minus_h > self.a_counter_fields_plus_h:    # If more free fields to the left then we shoot to the left
                    self.a_kolumn = self.a_hit_fields[1][0] - 1
                elif self.a_counter_fields_minus_h <= self.a_counter_fields_plus_h: # If more free fields to the right or the same amount, we shoot to the right
                    self.a_kolumn = self.a_hit_fields[1][-1] + 1


            elif self.a_hit_fields[1][0] == self.a_hit_fields[1][1]:        # The ship is vertical. Index of the kolumn is known.
                self.a_kolumn = self.a_hit_fields[1][0]

                for i in range(1, 3):  # Checking 2 fields to down
                    try:
                        if self.sheet_opponent[self.a_hit_fields[0][-1] + i][self.a_hit_fields[1][-1]] == empty:    # If the field is empty add to the adjacent fields
                            self.a_neighboring_fields_vertical[0].append(self.a_hit_fields[0][-1] + i)
                            self.a_neighboring_fields_vertical[1].append(self.a_hit_fields[1][-1])
                            self.a_counter_fields_plus_v += 1  # Increase the counter of free fields to the down (index row +)
                        else:
                            break
                    except: break
                for i in range(1, 3):  # Checking 2 fields to up
                    try:
                        if self.sheet_opponent[self.a_hit_fields[0][0] - i][self.a_hit_fields[1][0]] == empty:      # If the field is empty add to the adjacent fields
                            self.a_neighboring_fields_vertical[0].append(self.a_hit_fields[0][0] - i)
                            self.a_neighboring_fields_vertical[1].append(self.a_hit_fields[1][0])
                            self.a_counter_fields_minus_v += 1  # Increase the counter of free fields to the up (index kolumn -)
                        else:
                            break
                    except: break

                if self.a_counter_fields_minus_v > self.a_counter_fields_plus_v:        # If more free fields to the up then we shoot to the up
                    self.a_row = self.a_hit_fields[0][0] - 1
                elif self.a_counter_fields_minus_v <= self.a_counter_fields_plus_v:     # If more free fields to the down or the same amount, we shoot to the down
                    self.a_row = self.a_hit_fields[0][-1] + 1


        return [self.a_row, self.a_kolumn]

class Ship():
    def __init__(self, fields_of_ship):
        self.fields = [[], []]
        self.actual_fields = [[], []]
        
        for i in range(len(fields_of_ship[0])):             # Adding coordinates to the ship object fields
            self.fields[0].append(fields_of_ship[0][i])
            self.fields[1].append(fields_of_ship[1][i])
            self.actual_fields[0].append(fields_of_ship[0][i])
            self.actual_fields[1].append(fields_of_ship[1][i])
                        
        self.length_of_ship = len(self.fields[0])           # Length of the ship
        self.actual_length = self.length_of_ship
        
        self.front_field = [self.fields[0][0], self.fields[1][0]]   # First field of the ship

        

# Field marks

empty = '-'
hit = 'X'
fail = 'O'
destroyed = '#'
close = '*'

game = Game()
game.loop_game()



