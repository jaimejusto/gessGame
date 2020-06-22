# Author: Jaime Justo
# Date: 5/23/2020
""" Description:
    A board game for two players that is a combination of Chess and Go.
"""


class GessGame:
    """
    A board game for two players.
    """
    def __init__(self):
        """
        Initializes private data members for Gess Game.
        """
        self._player = 1        # current player

        self._white_stone = "\u2616" + "\u2007"
        self._black_stone = "\u2617" + "\u2007"
        self._blank_space = "  "
        self._board = [[]]

        self._new_game = True
        self._game_winner = None
        self._black_has_ring = False
        self._white_has_ring = False

        self._starting_sqr_row = None
        self._starting_sqr_col = None
        self._starting_sqr_footprint = [[]]

        # stone placements on footprint
        self._north_west = None
        self._north = None
        self._north_east = None
        self._west = None
        self._center = None
        self._east = None
        self._south_west = None
        self._south = None
        self._south_east = None

        self._ending_sqr_row = None
        self._ending_sqr_col = None

    def display_board(self):
        """
        Displays the board.\n
        """
        column_letters = ("\t", "a  ", "b  ", "c  ", "d  ", "e  ", "f  ", "g  ", "h  ", "i  ", "j  ", "k  ", "l  ",
                          "m  ", "n  ", "o  ", "p  ", "q  ", "r  ", "s  ", "t  ")

        # top line of board
        upper_separator = (("\u2500", "\u252C") * 19)
        # lines between rows
        middle_separator = (("\u2500", "\u253C") * 19)
        # bottom line of board
        lower_separator = (("\u2500", "\u2534") * 19)

        # prints column label
        print(" ".join(column_letters))

        # prints top line of board
        print("  ", "\u250C", " ".join(upper_separator), "\u2500", "\u2510")

        # prints each row with corresponding row number
        for j in range(20, 0, -1):
            if j > 9:
                print(j, end=" ")
            # add space before single digit
            else:
                print("", j, end=" ")
            # prints column separator
            for k in range(20):
                print("\u2502", self._board[j][k], end="")
            print("\u2502")

            # prints lower line
            if j == 1:
                print("  ", "\u2514", " ".join(lower_separator), "\u2500", "\u2518")
                print(" ".join(column_letters))
            # prints middle lines between rows
            else:
                print("  ", "\u251C", " ".join(middle_separator), "\u2500", "\u2524")

        print("\n")

    def new_board(self):
        """
        Places the stones back to their starting positions when a new game starts.
        """
        # creates a blank board
        self._board = [[self._blank_space for i in range(21)] for j in range(21)]

        # places black and white stones in original positions
        for i in range(2, 18, 3):
            self._board[7][i] = self._black_stone
            self._board[14][i] = self._white_stone

        for i in range(2, 13, 2):
            self._board[4][i] = self._black_stone
            self._board[17][i] = self._white_stone

        for i in range(7, 18, 2):
            if i == 17:
                self._board[3][i] = self._black_stone
                self._board[18][i] = self._white_stone
            self._board[2][i] = self._black_stone
            self._board[4][i] = self._black_stone
            self._board[17][i] = self._white_stone
            self._board[19][i] = self._white_stone

        for i in range(1, 10, 2):
            self._board[3][i] = self._black_stone
            self._board[18][i] = self._white_stone

        for i in range(8, 19, 2):
            self._board[3][i] = self._black_stone
            self._board[18][i] = self._white_stone

        for i in range(2, 13, 2):
            if i == 2:
                self._board[3][i] = self._black_stone
                self._board[18][i] = self._white_stone
            self._board[2][i] = self._black_stone
            self._board[19][i] = self._white_stone

    def update_board(self):
        """
        Updates the board after a move.\n
        """

        # removes pieces from starting position
        for r in range(-1, 2):
            for c in range(-1, 2):
                self._board[self._starting_sqr_row + r][self._starting_sqr_col + c] = self._blank_space

        # places pieces at ending position
        for r in range(-1, 2):
            for c in range(-1, 2):
                if c == -1:
                    j = 0
                elif c == 0:
                    j = 1
                elif c == 1:
                    j = 2

                if r == -1:
                    i = 2
                elif r == 0:
                    i = 1
                elif r == 1:
                    i = 0

                # places pieces on the board
                self._board[self._ending_sqr_row + r][self._ending_sqr_col + c] = self._starting_sqr_footprint[i][j]

                # removes pieces that went off the board
                if (self._ending_sqr_col + c) < 1 or (self._ending_sqr_col + c) > 18:
                    self._board[self._ending_sqr_row + r][self._ending_sqr_col + c] = self._blank_space
                elif (self._ending_sqr_row + r) < 2 or (self._ending_sqr_row + r) > 19:
                    self._board[self._ending_sqr_row + r][self._ending_sqr_col + c] = self._blank_space

    def get_game_state(self):
        """
        Checks if a winner has been declared.\n
        :return: 'UNFINISHED' if game_status == None, 'BLACK_WON' if game_status == B, or
        'WHITE_WON' if game_status == W
        :rtype: str
        """
        if self._game_winner == "W":
            return "WHITE_WON"

        elif self._game_winner == "B":
            return "BLACK_WON"

        else:
            return "UNFINISHED"

    def resign_game(self):
        """
        Current player uses their turn to forfeit the game. \n
        """
        # current player forfeits and declares the other player the winner
        self._game_winner = "W" if (self._player == 1) else "B"

    def make_move(self, center_sqr_selected, center_sqr_destination):
        """
        Makes a move specified by the current player if the move is allowed. \n
        :param str center_sqr_selected: center square of piece to be moved
        :param str center_sqr_destination: center square of where to move the piece
        :return: True if legal move or False if illegal move.
        :rtype: bool
        """
        # new game started
        if self._new_game is True:
            self.new_board()        # board is reset
            self.display_board()    # board is displayed
            self._new_game = False
            self.check_for_rings()

        # winner has been declared and game has ended
        if self._game_winner is not None:
            return False

        # current player's turn
        self._player = 1 if (self._player % 2) else 2

        # gets the center squares from the player's input
        self.get_center_squares(center_sqr_selected, center_sqr_destination)

        # the move is legal
        if self.is_move_valid(center_sqr_selected, center_sqr_destination) is True:

            # board is updated
            self.update_board()

            # board is scanned for rings
            self.check_for_rings()

            # Black no longer has a ring but White does
            if self._black_has_ring is False and self._white_has_ring is True:
                # declares White the winner
                self._game_winner = "W"

            # White no longer has a ring but Black does
            elif self._black_has_ring is True and self._white_has_ring is False:
                # declares Black the winner
                self._game_winner = "B"

            # next player's turn
            self._player += 1

            # "clear" the console screen
            print("\n"*20)

            # display the board
            self.display_board()

            return True

        # the move is illegal
        else:
            return False

    def get_center_squares(self, center_sqr_selected, center_sqr_destination):
        """
        Uses the player's input to retrieve the rows and columns on the board. \n
        :param str center_sqr_selected: center square of piece to be moved.
        :param str center_sqr_destination: center square of where to move the piece.
        """

        # gets the column and row of the center square from the starting piece
        self._starting_sqr_col = center_sqr_selected[0:1]
        self._starting_sqr_row = center_sqr_selected[1:]

        # converts the starting column and row into integers
        self._starting_sqr_col = ord(self._starting_sqr_col) - 97
        self._starting_sqr_row = int(self._starting_sqr_row)

        # gets the column and row of the center square of where to move the piece
        self._ending_sqr_col = center_sqr_destination[0:1]
        self._ending_sqr_row = center_sqr_destination[1:]

        # converts the ending column and row into integers
        self._ending_sqr_col = ord(self._ending_sqr_col) - 97
        self._ending_sqr_row = int(self._ending_sqr_row)

    def is_move_valid(self, center_sqr_selected, center_sqr_destination):
        """
        Checks if a potential move is legal or not according to the rules.\n
        :param str center_sqr_selected: center square of piece to be moved.
        :param str center_sqr_destination: center square of where to move the piece.
        :return: True if move is legal, otherwise, returns False.
        :rtype: bool
        """

        # piece didn't move
        if center_sqr_selected == center_sqr_destination:
            return False

        # starting piece is out of bounds
        if self._starting_sqr_col < 1 or self._starting_sqr_col > 18:
            return False
        if self._starting_sqr_row < 2 or self._starting_sqr_row > 19:
            return False

        # square to move to is out of bounds
        if self._ending_sqr_col < 1 or self._ending_sqr_col > 18:
            return False
        if self._ending_sqr_row < 2 or self._starting_sqr_row > 19:
            return False

        # retrieve the piece's footprint
        self.get_footprint()

        # check if the footprint is valid
        if self.is_footprint_valid() is False:
            return False

        # check if the footprint is allowed to move in that manner
        if self.is_footprint_move_valid() is False:
            return False

        # check if Black player broke their own ring
        if self._black_has_ring is False and self._player == 1:
            return False

        # check if White player broke their own ring
        elif self._white_has_ring is False and self._player == 2:
            return False

        # piece is allowed to move
        else:
            return True

    def get_footprint(self):
        """
        Gets the stones surrounding a piece's center square. \n
        """

        # initializes the piece's footprint
        self._starting_sqr_footprint = [[self._blank_space for i in range(3)] for j in range(3)]

        for row in range(0, 3):
            for col in range(0, 3):
                if row == 0:
                    i = 1
                elif row == 1:
                    i = 0
                elif row == 2:
                    i = -1

                if col == 0:
                    j = -1
                elif col == 1:
                    j = 0
                elif col == 2:
                    j = 1

                # assigns the stones on the board to the piece's footprint
                self._starting_sqr_footprint[row][col] = \
                    self._board[self._starting_sqr_row + i][self._starting_sqr_col + j]

        # check where stones are placed in footprint
        self._north_west = False if (self._starting_sqr_footprint[0][0] == self._blank_space) else True
        self._north = False if (self._starting_sqr_footprint[0][1] == self._blank_space) else True
        self._north_east = False if (self._starting_sqr_footprint[0][2] == self._blank_space) else True
        self._west = False if (self._starting_sqr_footprint[1][0] == self._blank_space) else True
        self._center = False if (self._starting_sqr_footprint[1][1] == self._blank_space) else True
        self._east = False if (self._starting_sqr_footprint[1][2] == self._blank_space) else True
        self._south_west = False if (self._starting_sqr_footprint[2][0] == self._blank_space) else True
        self._south = False if (self._starting_sqr_footprint[2][1] == self._blank_space) else True
        self._south_east = False if (self._starting_sqr_footprint[2][2] == self._blank_space) else True

    def check_for_rings(self):
        """
        Searches the board for rings. \n
        """

        # assume there are no rings on the board
        self._black_has_ring = False
        self._white_has_ring = False

        # check for rings on the board
        for row in range(2, 20):
            for col in range(1, 20):
                # check for Black rings
                if (self._board[row][col] == self._black_stone and self._board[row + 1][col] == self._black_stone and
                        self._board[row+2][col] == self._black_stone and
                        self._board[row + 2][col + 1] == self._black_stone and
                        self._board[row+2][col+2] == self._black_stone and
                        self._board[row + 1][col + 2] == self._black_stone and
                        self._board[row][col+2] == self._black_stone and
                        self._board[row][col + 1] == self._black_stone and
                        self._board[row+1][col+1] == self._blank_space):
                    # Black ring was found
                    self._black_has_ring = True

                # check for White rings
                elif (self._board[row][col] == self._white_stone and self._board[row + 1][col] == self._white_stone and
                        self._board[row+2][col] == self._white_stone and
                        self._board[row + 2][col + 1] == self._white_stone and
                        self._board[row+2][col+2] == self._white_stone and
                        self._board[row + 1][col + 2] == self._white_stone and
                        self._board[row][col+2] == self._white_stone and
                        self._board[row][col + 1] == self._white_stone and
                        self._board[row+1][col+1] == self._blank_space):
                    # White ring was found
                    self._white_has_ring = True

    def is_footprint_valid(self):
        """
        Determines if the piece selected has a legal footprint.\n
        :return: True if the footprint is valid, otherwise returns False.
        :rtype: bool
        """

        # assume there are no stones surrounding the piece
        footprint_is_empty = True

        # assume the stones in the footprint all belong to the current player
        footprint_is_one_color = True

        # check the stones within the selected piece
        for row in range(0, 3):
            for col in range(0, 3):
                # ignore the center piece
                if row == 1 and col == 1:
                    continue

                # the center square is not occupied by a stone
                if self._starting_sqr_footprint[1][1] == self._blank_space:
                    # check if the surrounding squares are occupied
                    if self._starting_sqr_footprint[row][col] != self._blank_space:
                        # the footprint has stones
                        footprint_is_empty = False

                # the center square is occupied by a stone
                elif self._starting_sqr_footprint[1][1] != self._blank_space:
                    # check if the surrounding squares are occupied
                    if self._starting_sqr_footprint[row][col] != self._blank_space:
                        # the footprint has stones
                        footprint_is_empty = False

                # Black player chose a piece with white stones in the footprint
                if self._player == 1 and self._starting_sqr_footprint[row][col] == self._white_stone:
                    # the footprint contains white stones
                    footprint_is_one_color = False

                # White player chose a piece with black stones in the footprint
                elif self._player == 2 and self._starting_sqr_footprint[row][col] == self._black_stone:
                    # the footprint contains black stones
                    footprint_is_one_color = False

        # the footprint is not empty and all the stones belong to the current player
        if footprint_is_empty is False and footprint_is_one_color is True:
            return True

        # the footprint was either empty or had stones belonging to the other player
        else:
            return False

    def is_footprint_move_valid(self):
        """
        Determines if the piece is allowed to move in the specified direction and distance. \n
        :return: True if the piece movement obeys the rules, otherwise returns False.
        :rtype: bool
        """

        # vertical distance to be travelled
        rise = self._ending_sqr_row - self._starting_sqr_row
        # horizontal distance to be travelled
        run = self._ending_sqr_col - self._starting_sqr_col

        # checks if there is a stone in the center of the footprint
        if self._center is False:
            # checks if the piece has moved too far
            if abs(rise) > 3 or abs(run) > 3:
                return False

        # piece is moving horizontally
        if run != 0 and rise == 0:

            # piece is moving west
            if run < 0:

                # piece is not allowed to move west
                if self._west is False:
                    return False

                # piece is allowed to move west
                else:
                    # checks if the piece encounters any stones before reaching the destination
                    start_col = self._starting_sqr_col - 2     # column to start checking
                    end_col = self._ending_sqr_col - 2         # column to stop checking
                    start_row = self._starting_sqr_row          # row to start checking

                    for col in range(start_col, end_col, -1):
                        # piece ran into a stone
                        if (self._board[start_row + 1][col] != self._blank_space or
                                self._board[start_row][col] != self._blank_space or
                                self._board[start_row - 1][col] != self._blank_space) and \
                                col + 1 != self._ending_sqr_col:
                            return False

            # piece is moving east
            elif run > 0:

                # piece is not allowed to move east
                if self._east is False:
                    return False

                # piece is allowed to move east
                else:
                    # checks if the piece encounters any stones before reaching the destination
                    start_col = self._starting_sqr_col + 2       # column to start checking
                    end_col = self._ending_sqr_col + 2          # column to stop checking
                    start_row = self._starting_sqr_row          # row to start checking

                    for col in range(start_col, end_col):
                        # piece ran into a stone
                        if (self._board[start_row + 1][col] != self._blank_space or
                                self._board[start_row][col] != self._blank_space or
                                self._board[start_row - 1][col] != self._blank_space) and \
                                col - 1 != self._ending_sqr_col:
                            return False

        # piece is moving vertically
        elif run == 0 and rise != 0:

            # piece is moving north
            if rise > 0:

                # piece is not allowed to move north
                if self._north is False:
                    return False

                # piece is allowed to move north
                else:
                    # checks if the piece encounters any stones before reaching the destination
                    start_row = self._starting_sqr_row + 2      # row to start checking
                    end_row = self._ending_sqr_row + 2          # row to stop checking
                    start_col = self._starting_sqr_col          # column to start checking

                    for row in range(start_row, end_row):
                        # piece ran into a stone
                        if (self._board[row][start_col - 1] != self._blank_space or
                                self._board[row][start_col] != self._blank_space or
                                self._board[row][start_col + 1] != self._blank_space) and \
                                row - 1 != self._ending_sqr_row:
                            return False

            # piece is moving south
            elif rise < 0:

                # piece is not allowed to move south
                if self._south is False:
                    return False

                # piece is allowed to move south
                else:
                    # check if the piece encounters any stones before reaching the destination
                    start_row = self._starting_sqr_row - 2         # row to start checking
                    end_row = self._ending_sqr_row - 2             # row to stop checking
                    start_col = self._starting_sqr_col             # column to stop checking

                    for row in range(start_row, end_row, -1):
                        # piece ran into a stone
                        if (self._board[row][start_col - 1] != self._blank_space or
                                self._board[row][start_col] != self._blank_space or
                                self._board[row][start_col + 1] != self._blank_space) and \
                                row + 1 != self._ending_sqr_row:
                            return False

        # piece is moving diagonally
        elif rise % run == 0:

            # piece is moving diagonally north
            if rise > 0:

                # piece is moving in northwest direction
                if run < 0:

                    # piece is not allowed to move in the northwest direction
                    if self._north_west is False:
                        return False

                    # piece is allowed to move in the northwest direction
                    else:
                        # check if the piece encounters any stones before reaching the destination
                        start_row = self._starting_sqr_row + 2
                        end_row = self._ending_sqr_row + 2
                        start_col = self._starting_sqr_col - 2
                        end_col = self._ending_sqr_col - 2

                        for row in range(start_row, end_row):
                            for col in range(start_col, end_col, -1):
                                # piece ran into a stone
                                if (self._board[row][col] != self._blank_space or
                                    self._board[row][col + 1] != self._blank_space or
                                    self._board[row][col] != self._blank_space or
                                    self._board[row - 1][col] != self._blank_space or
                                    self._board[row][col] != self._blank_space) and \
                                        (row - 1 != self._ending_sqr_row and col + 1 != self._ending_sqr_col):
                                    return False

                # piece is moving in northeast direction
                elif run > 0:

                    # piece is not allowed to move in the northeast direction
                    if self._north_east is False:
                        return False

                    # piece is allowed to move in the northeast direction
                    else:
                        # check if the piece encounters any stones before reaching the destination
                        start_row = self._starting_sqr_row + 2
                        end_row = self._ending_sqr_row + 2
                        start_col = self._starting_sqr_col + 2
                        end_col = self._ending_sqr_col + 2

                        for row in range(start_row, end_row):
                            for col in range(start_col, end_col):
                                # piece ran into a stone
                                if (self._board[row][col] != self._blank_space or
                                    self._board[row][col - 1] != self._blank_space or
                                    self._board[row][col] != self._blank_space or
                                    self._board[row - 1][col] != self._blank_space or
                                    self._board[row][col] != self._blank_space) and \
                                        (row - 1 != self._ending_sqr_row and col - 1 != self._ending_sqr_col):
                                    return False

            # piece is moving diagonally south
            if rise < 0:

                # piece is moving in southwest direction
                if run < 0:

                    # piece is not allowed to move in the southwest direction
                    if self._south_west is False:
                        return False

                    # piece is allowed to move in the southwest direction
                    else:
                        # check if the piece encounters any stones before reaching the destination
                        start_row = self._starting_sqr_row - 2
                        end_row = self._ending_sqr_row - 2
                        start_col = self._starting_sqr_col - 2
                        end_col = self._ending_sqr_col - 2

                        for row in range(start_row, end_row, -1):
                            for col in range(start_col, end_col, -1):
                                # piece ran into a stone
                                if (self._board[row][col] != self._blank_space or
                                    self._board[row][col + 1] != self._blank_space or
                                    self._board[row][col] != self._blank_space or
                                    self._board[row + 1][col] != self._blank_space or
                                    self._board[row][col] != self._blank_space) and \
                                        (row + 1 != self._ending_sqr_row and col + 1 != self._ending_sqr_col):
                                    return False

                # piece is moving southeast
                elif run > 0:

                    # piece is not allowed to move in the southeast direction
                    if self._south_east is False:
                        return False

                    # piece is allowed to move in the southeast direction
                    else:
                        # check if the piece encounters any stones before reaching the destination
                        start_row = self._starting_sqr_row - 2
                        end_row = self._ending_sqr_row - 2
                        start_col = self._starting_sqr_col + 2
                        end_col = self._ending_sqr_col + 2

                        for row in range(start_row, end_row, -1):
                            for col in range(start_col, end_col):
                                # piece ran into a stone
                                if (self._board[row][col] != self._blank_space or
                                    self._board[row][col - 1] != self._blank_space or
                                    self._board[row][col] != self._blank_space or
                                    self._board[row + 1][col] != self._blank_space or
                                    self._board[row][col] != self._blank_space) and \
                                        (row + 1 != self._ending_sqr_row and col - 1 != self._ending_sqr_col):
                                    return False

        # piece is moving in a way that it shouldn't
        elif rise % run != 0:
            return False

        # piece direction and distance is allowed
        else:
            return True


game = GessGame()
game.make_move("c3", "c5")
game.make_move("d15", "d13")