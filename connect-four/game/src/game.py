# This code has been adapted from its original source code found here: https://www.askpython.com/python/examples/connect-four-game
import numpy as np
 
class Connect_Four_Game:
    def __init__(self, num_rows=6, num_cols=7):
        self.ROW_COUNT = num_rows
        self.COLUMN_COUNT = num_cols
        self.turn = 0
        self.board = np.zeros((self.ROW_COUNT, self.COLUMN_COUNT), dtype=int)
        self.game_over = False
        self.history = ["Game start"]

    def state(self):
        formatted_rows = ["".join(map(str, row)) for row in np.flipud(self.board)]
        return f"[{';'.join(formatted_rows)}]"

    def is_p1(self):
        return self.turn % 2 == 0

    def is_over(self):
        return self.game_over
    
    def move(self, col):
        self.turn += 1
        piece = 2 if self.is_p1() else 1
        row = self.get_next_open_row(col)
        self.board[row][col] = piece
        self.history.append(f"{self.turn}) P{piece}: {col} -> {self.state()}")
        if self.winning_move(piece):
            # Connect four
            self.game_over = True
            self.history.append(f"Game over, Player {piece} Wins")
        elif self.turn == self.COLUMN_COUNT * self.ROW_COUNT:
            # Draw
            self.game_over = True
            self.history.append("Game over, Draw")
    
    def is_legal(self, col):
        #if this condition is true we will let the use drop piece here.
        #if not true that means the col is not vacant
        return col < self.COLUMN_COUNT and self.board[5][col] == 0
    
    def get_next_open_row(self, col):
        for r in range(self.ROW_COUNT):
            if self.board[r][col]==0:
                return r
        
    def print_board(self):
        for row in np.flip(self.board, 0):
            print(" "+" ".join(map(str, row)))


    def winning_move(self, piece):
        # Check horizontal locations for win
        for c in range(self.COLUMN_COUNT-3):
            for r in range(self.ROW_COUNT):
                if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece:
                    return True
    
        # Check vertical locations for win
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT-3):
                if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
                    return True
    
        # Check positively sloped diaganols
        for c in range(self.COLUMN_COUNT-3):
            for r in range(self.ROW_COUNT-3):
                if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
                    return True
    
        # Check negatively sloped diaganols
        for c in range(self.COLUMN_COUNT-3):
            for r in range(3, self.ROW_COUNT):
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
                    return True

def main():
    print(" ==== Connect Four ==== ")
    tutorial = input("Would you like a tutorial? (y/n): ")
    
    if tutorial.lower() == "y":
        print("\n === Description === ")
        print("Connect Four is a two-player turn-based strategy game. Players take turns dropping pieces into a vertical grid, aiming to connect four pieces in a row, column, or diagonal before their opponent does.\n")
        
        print(" === How to Play === ")
        print("Players will take turns choosing a column (1-7) to drop their piece into. The piece will fall to the lowest available row in that column.\n")

        print(" === Moves === ")
        print("Enter a column number (1-7) to drop your piece when prompted.")
        print("Example: '3' (Drops a piece into column 3)\n")
        
        input("Press Enter to start the game...")

    game = Connect_Four_Game()
    while True:
        # Player 1
        game.print_board()
        while True:
            try:
                move = int(input(f"Player 1 Move (1-{game.COLUMN_COUNT}): ")) - 1
                if game.is_legal(move):
                    break
                print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        game.move(move)

        if game.is_over():
            game.print_board()
            print("Player 1 wins")
            print(game.history)
            break

        # Player 2
        game.print_board()
        while True:
            try:
                move = int(input(f"Player 2 Move (1-{game.COLUMN_COUNT}): ")) - 1
                if game.is_legal(move):
                    break
                print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        game.move(move)

        if game.is_over():
            game.print_board()
            print("Player 2 wins")
            break


if __name__ == "__main__":
    main()