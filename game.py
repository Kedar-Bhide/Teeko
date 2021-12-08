import random
import copy


class Teeko2Player:
    """ An object representation for an AI game player for the game Teeko2.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def succ(self, state, player=None, drop_phase=None):
        successors = []
        if drop_phase:
            for i in range(len(state)):
                for j in range(len(state[i])):
                    if state[i][j] == ' ':
                        updated_state = copy.deepcopy(state)
                        updated_state[i][j] = player
                        successors.append(updated_state)
        else:
            for i in range(len(state)):
                for j in range(len(state[i])):
                    if state[i][j] == player:
                        if i - 1 >= 0 and state[i - 1][j] == ' ':
                            updated_state = copy.deepcopy(state)
                            updated_state[i - 1][j] = player
                            updated_state[i][j] = ' '
                            successors.append(updated_state)
                        if i - 1 >= 0 and j - 1 >= 0 and state[i - 1][j - 1] == ' ':
                            updated_state = copy.deepcopy(state)
                            updated_state[i - 1][j - 1] = player
                            updated_state[i][j] = ' '
                            successors.append(updated_state)
                        if i - 1 >= 0 and j + 1 < len(state) and state[i - 1][j + 1] == ' ':
                            updated_state = copy.deepcopy(state)
                            updated_state[i - 1][j + 1] = player
                            updated_state[i][j] = ' '
                            successors.append(updated_state)
                        if i + 1 < len(state) and state[i + 1][j] == ' ':
                            updated_state = copy.deepcopy(state)
                            updated_state[i + 1][j] = player
                            updated_state[i][j] = ' '
                            successors.append(updated_state)
                        if i + 1 < len(state) and j - 1 >= 0 and state[i + 1][j - 1] == ' ':
                            updated_state = copy.deepcopy(state)
                            updated_state[i + 1][j - 1] = player
                            updated_state[i][j] = ' '
                            successors.append(updated_state)
                        if i + 1 < len(state) and j + 1 < len(state[i]) and state[i + 1][j + 1] == ' ':
                            updated_state = copy.deepcopy(state)
                            updated_state[i + 1][j + 1] = player
                            updated_state[i][j] = ' '
                            successors.append(updated_state)
                        if j - 1 >= 0 and state[i][j - 1] == ' ':
                            updated_state = copy.deepcopy(state)
                            updated_state[i][j - 1] = player
                            updated_state[i][j] = ' '
                            successors.append(updated_state)
                        if j + 1 < len(state[i]) and state[i][j + 1] == ' ':
                            updated_state = copy.deepcopy(state)
                            updated_state[i][j + 1] = player
                            updated_state[i][j] = ' '
                            successors.append(updated_state)
        return successors

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this Teeko2Player object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        count = 0
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] != ' ':
                    count += 1
        if count < 8:
            drop_phase = True
        else:
            drop_phase = False

        move = []
        if not drop_phase:
            best_val = float('-inf')
            best_state = None
            for succ in self.succ(state, self.my_piece, False):
                if self.game_value(state) == -1 or self.game_value(state) == 1:
                    best_state = succ
                val = self.min_val(state, 0)
                if val > best_val:
                    best_val = val
                    best_state = succ
            for i in range(len(state)):
                for j in range(len(state[i])):
                    if state[i][j] != ' ' and best_state[i][j] == ' ':
                        move.append((i, j))
                    if state[i][j] == ' ' and best_state[i][j] != ' ':
                        move.insert(0, (i, j))
        else:
            best_val = float('-inf')
            best_state = None
            for succ in self.succ(state, self.my_piece, True):
                if self.game_value(state) == -1 or self.game_value(state) == 1:
                    best_state = succ
                val = self.min_val(state, 0)
                if val > best_val:
                    best_val = val
                    best_state = succ
            for i in range(len(state)):
                for j in range(len(state[i])):
                    if state[i][j] == ' ' and best_state[i][j] != ' ':
                        move.insert(0, (i, j))
        return move

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row is not None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row) + ": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns:
            int: 1 if this Teeko2Player wins, -1 if the opponent wins, 0 if no winner
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i + 1][col]\
                        == state[i + 2][col] == state[i + 3][col]:
                    return 1 if state[i][col] == self.my_piece else -1

        # check \ diagonal wins
        for i in range(2):
            for j in range(2):
                if state[i][j] != ' ' and state[i][j] == state[i + 1][j + 1]\
                        == state[i + 2][j + 2] == state[i + 3][j + 3]:
                    return 1 if state[i][j] == self.my_piece else -1

        # check / diagonal wins
        for i in range(3, 5):
            for j in range(2):
                if state[i][j] != ' ' and state[i][j] == state[i - 1][j + 1]\
                        == state[i - 2][j + 2] == state[i - 3][j + 3]:
                    return 1 if state[i][j] == self.my_piece else -1

        # check diamond wins
        for i in range(3):
            for j in range(1, 4):
                if state[i][j] != ' ' and state[i + 1][j] == ' ' and \
                        state[i][j] == state[i + 1][j + 1] == state[i + 2][j] == state[i + 1][j - 1]:
                    return 1 if state[i][j] == self.my_piece else -1

        return 0  # no winner yet

    def heuristic_game_value(self, state, player):
        if self.game_value(state) != 0:
            return self.game_value(state)
        else:
            horizontal = 0
            for row in state:
                if row.count(player) > horizontal:
                    horizontal = row.count(player)
            horizontal_h = horizontal / 4
            vertical = 0
            for col in list(zip(*state)):
                if col.count(player) > vertical:
                    vertical = col.count(player)
            vertical_h = vertical / 4

            # 8 possible diagonals
            diag1_h = sum(state[i][i] == player for i in range(4)) / 4
            diag2_h = sum(state[i][i] == player for i in range(1, 5)) / 4
            diag3_h = sum(state[4 - i][i] == player for i in range(4)) / 4
            diag4_h = sum(state[4 - i][i] == player for i in range(1, 5)) / 4
            diag5_h = sum(state[i][i + 1] == player for i in range(4)) / 4
            diag6_h = sum(state[i][i - 1] == player for i in range(1, 5)) / 4
            diag7_h = sum(state[3 - i][i] == player for i in range(4)) / 4
            diag8_h = sum(state[5 - i][i] == player for i in range(1, 5)) / 4

            diamond = 0
            for i in range(1, 4):
                for j in range(1, 4):
                    count = 0
                    if state[i][j] == ' ':
                        count = 0
                        if state[i][j - 1] == player:
                            count += 1
                        if state[i - 1][j] == player:
                            count += 1
                        if state[i][j + 1] == player:
                            count += 1
                        if state[i + 1][j - 1] == player:
                            count += 1
                    if count > diamond:
                        diamond = count
            diamond_h = diamond / 4

        heuristic = max(horizontal_h, vertical_h, diag1_h, diag2_h, diag3_h,
                        diag4_h, diag5_h, diag6_h, diag7_h, diag8_h, diamond_h)
        return heuristic

    def max_val(self, state, depth):
        if depth >= 5 or self.heuristic_game_value(state, self.my_piece) == -1 \
                or self.heuristic_game_value(state, self.my_piece) == 1:
            return self.heuristic_game_value(state, self.my_piece)
        else:
            alpha = float('-inf')
            for succ in self.succ(state):
                alpha = max(alpha, self.min_val(state, depth + 1))
            return alpha

    def min_val(self, state, depth):
        if depth >= 5 or self.heuristic_game_value(state, self.opp) == -1 \
                or self.heuristic_game_value(state, self.opp) == 1:
            return self.heuristic_game_value(state, self.opp)
        else:
            beta = float('inf')
            for succ in self.succ(state):
                beta = min(beta, self.max_val(state, depth + 1))
            return beta


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = Teeko2Player()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved at " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved from " + chr(move[1][1] + ord("A")) + str(move[1][0]))
            print("  to " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0]) - ord("A")),
                                      (int(move_from[1]), ord(move_from[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
