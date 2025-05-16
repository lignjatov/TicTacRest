class tictactoe:
    
    def __init__(self, board):
        """constructor immedaitely creates 2 fields based on the "---------" board input and turns it into"""
        self.board = board
        self.playable_board = self.transform_board_to_playable()
            
    def transform_board_to_playable(self):
        """Method for transforming the board from --------- into array based 3x3 grid"""
        string_line_board = self.board
        play_board = []
        for i in range(0, 9, 3):
            red = list(string_line_board[i:i+3])
            play_board.append(red)
        return play_board
    
    def transform_board_to_line(self):
        """Method for transforming the board from the 3x3 grid into a line based output for saving into the database
        """
        line_board = ""
        for row in self.playable_board:
            for col in row:
                line_board += col
        
        return line_board
    
    def make_move(self, sign, row, column):
        """Method for making a move on the board. It checks first for legality of the move and whether or not the correct signs were given. If None is returned, the moves was passed correctly
        """
        board = self.playable_board
        allowed_moves = ['x','o']

        if row < 0 or row > 3:
            return "Invalid move: row value can be between 0 and 3"
        if column < 0 or column > 3:
            return "Invalid move: column value can be between 0 and 3"
        if sign not in allowed_moves:
            return "Invalid move: sign can only be 'x' or 'o'"
        #check for whether or not a spot was taken. The '-' sign is default for an empty space on the board
        if board[row][column] != '-':
            return "Invalid move: position already taken"
        
        board[row][column] = sign
        self.playable_board = board
        return None
        
    def is_finished(self):
        """Method for checking if game is finished. If it returns False, then game is not yet finished"""
        board = self.playable_board
        #check for first column
        for row in board:
            if row[0] == row[1] == row[2] and row[0] != "-":
                return row[0]
        #check all rows
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] and board[0][col] != "-":
                return board[0][col]
        #check diagonal
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "-":
            return board[0][0]

        #check other diagonal
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "-":
            return board[0][2]

        return False
