from tkinter import *
from functools import partial
from tkinter import messagebox
import random, sys
import art

class Game(Tk):
    def __init__(self, is_user_first):
        super().__init__()
        self.title("Undefeatable Tic Tac Toe")
        self.geometry("400x400")
        self.resizable(False, False)

        self.is_user_first = is_user_first
        self.button_list = []
        self.board = [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' ']
        ]
        self.current_character = 'X'
        self.corner_pieces = [
            (0,0),(0,2),(2,0),(2,2)
        ]
        if self.is_user_first:
            self.player = 'O'
            self.opponent = 'X'
        else:
            self.player = 'X'
            self.opponent = 'O'

        # Loop to create buttons and configure them
        for i in range(3):
            rowlist = []
            for j in range(3):
                button = Button(self, text=' ')
                button.configure(width=100, height=100, font=("Helvetica", 30), command=partial(self.place, i, j))
                button.grid(row=i, column=j)
                rowlist.append(button)
            self.button_list.append(rowlist)
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)

        if not self.is_user_first:
            self.computer_move()

    def display_win(self, char):
        if self.is_user_first:
            if char == 'X':
                messagebox.showinfo("Win", "You did the impossible !!! Did you cheat ?")
                exit(0)
            elif char == 'O':
                messagebox.showinfo("Win", "Computer Won")
                exit(0)
        else:
            if char == 'X':
                messagebox.showinfo("Win", "Computer Won")
                exit(0)
            elif char == 'O':
                messagebox.showinfo("Win", "You did the impossible !!! Did you cheat ?")
                exit(0)

    def check_draw(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    return True
        return False

    def place(self, i, j):
        if self.board[i][j] == ' ':
            self.board[i][j] = self.current_character
            self.button_list[i][j].configure(text=self.current_character)
        else:
            messagebox.showerror("Error", "Place already occupied")
            return 0

        # Check win
        output = self.check_win()
        if output[0] == 1:
            self.display_win(output[1])

        # Check draw
        if not self.check_draw():
            messagebox.showinfo("Draw", "Well played! The match ended with a draw")
            exit(0)

        # Change character and give computer turn
        if self.current_character == 'X':
            self.current_character = 'O'
        else:
            self.current_character = 'X'
            self.computer_move()

    def get_characters_on_board(self):
        count = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != ' ':
                    count += 1
        return count

    def check_win(self):
        for i in range(3):
            if (self.board[i][0] == self.board[i][1]) and (self.board[i][1] == self.board[i][2]) and self.board[i][1] != ' ':
                return (1, self.board[i][0])
            if(self.board[0][i] == self.board[1][i]) and (self.board[1][i] == self.board[2][i]) and self.board[2][i] != ' ':
                return (1, self.board[1][i])
        if (self.board[0][0] == self.board[1][1]) and (self.board[1][1] == self.board[2][2]) and self.board[1][1] != ' ':
            return (1, self.board[1][1])
        if (self.board[0][2] == self.board[1][1]) and (self.board[1][1] == self.board[2][0]) and self.board[1][1] != ' ':
            return (1, self.board[1][1])
        return (0, 0)

    def computer_move(self):
        try:
            if self.get_characters_on_board() == 0 and not self.is_user_first:
                self.button_list[0][0].invoke()
            elif self.get_characters_on_board() == 2:
                pos = self.find_O()
                if pos == (0,1) or pos == (1, 2):
                    self.button_list[2][0].invoke()
                elif pos == (1, 0) or pos == (2, 1):
                    self.button_list[0][2].invoke()
                elif pos == (2, 2):
                    self.button_list[2][0].invoke()
                elif pos == (0,2):
                    self.button_list[2][0].invoke()
                elif pos == (2, 0):
                    self.button_list[0][2].invoke()
                elif pos == (1, 1):
                    move = self.compute_best_move()
                    self.button_list[move[0]][move[1]].invoke()
            else:
                move = self.compute_best_move()
                self.button_list[move[0]][move[1]].invoke()
        except Exception as ex:
            exit(0)

    def find_O(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 'O':
                    return (i, j)

    def check_draw_minimax(self):
        # Check if move is left
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    return True
        return False

    def check_win_minimax(self):
        for i in range(3):
            if (self.board[i][0] == self.board[i][1]) and (self.board[i][1] == self.board[i][2]) and self.board[i][1] != ' ':
                if self.board[1][0] == self.player:
                    return 10
                else:
                    return -10
            if(self.board[0][i] == self.board[1][i]) and (self.board[1][i] == self.board[2][i]) and self.board[2][i] != ' ':
                if self.board[1][i] == self.player:
                    return 10
                else:
                    return -10
        if (self.board[0][0] == self.board[1][1]) and (self.board[1][1] == self.board[2][2]) and self.board[1][1] != ' ':
            if self.board[1][1] == self.player:
                return 10
            else:
                return -10
        if (self.board[0][2] == self.board[1][1]) and (self.board[1][1] == self.board[2][0]) and self.board[1][1] != ' ':
            if self.board[1][1] == self.player:
                return 10
            else:
                return -10
        return 0


    def minimax_recursive_function(self, depth, isPlayer):
        score = self.check_win_minimax()
        if (score == 10) :
            return score - depth
        if (score == -10) :
            return score + depth
        if (self.check_draw_minimax() == False) :
            return 0
        if (isPlayer) :	
            best = -1000
            for i in range(3) :		
                for j in range(3) :
                    if (self.board[i][j]==' ') :
                        self.board[i][j] = self.player

                        # Call minimax recursively and choose
                        # the maximum value
                        best = max( best, self.minimax_recursive_function(depth + 1,not isPlayer) )

                        # Undo the move
                        self.board[i][j] = ' '
            return best

        # If this minimizer's move
        else :
            best = 1000

            # Traverse all cells
            for i in range(3) :		
                for j in range(3) :
                
                    # Check if cell is empty
                    if (self.board[i][j] == ' ') :
                    
                        # Make the move
                        self.board[i][j] = self.opponent

                        # Call minimax recursively and choose
                        # the minimum value
                        best = min(best, self.minimax_recursive_function(depth + 1, not isPlayer))

                        # Undo the move
                        self.board[i][j] = ' '
            return best

    def compute_best_move(self):
        bestVal = -1000
        bestMove = (-1, -1)

        for i in range(3) :	
            for j in range(3) :
                if (self.board[i][j] == ' ') :
                    self.board[i][j] = self.player
                    moveVal = self.minimax_recursive_function(0, self.is_user_first)
                    self.board[i][j] = ' '
                    if (moveVal > bestVal) :			
                        bestMove = (i, j)
                        bestVal = moveVal

        return bestMove

if __name__ == '__main__':
    is_user_first = False

    # ASCII art
    print(art.text2art("Undefeatable", "small"))
    print(art.text2art("Tic Tac Toe", "small"))

    game = Game(is_user_first=is_user_first)
    game.mainloop()