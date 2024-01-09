from tkinter import *
from tkinter import ttk

from GUI.Solutions.BackTracking import  BackTrackSolution


import random
import time


class Gui(Tk):
    def __init__(self):
        super().__init__()
        

        self.init_solution= [["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]
        self.bactrack_solution = []
        self.ga_solution = []
    
        self.title("Genetic Sudoku ;)")
        self.geometry("1500x500")

        self.welcome_label = Label(self, text="This a Genetic Sudoku Solver, using GA or a Backtracking approach")
        self.welcome_label.grid(row=0, column=3, pady=5, padx=5)


        self.generate_sudoku_button = Button(self, text="Generate Sudoku", command=self.generate_sudoku)
        self.generate_sudoku_button.grid(row=1, column=0, pady=5, padx=5)

        self.select_label = Label(self, text="Select difficulty: ")
        self.select_label.grid(row=1, column=1, pady=5, padx=5)

        self.difficulty_box = ttk.Combobox(self, values=["Easy", "Medium", "Advanced"])
        self.difficulty_box.current(2)
        self.difficulty_box.grid(row=1, column=2, pady=5, padx=5)

        self.solve_using_GA_button = Button(self, text="Solve using GA", command=self.solve_using_GA)
        self.solve_using_GA_button.grid(row=2, column=0, pady=5, padx=5)

        self.seed_label = Label(self, text="Seed: ")
        self.seed_label.grid(row=2, column=1, pady=5, padx=5)

        self.seed_entry = Entry(self)
        self.seed_entry.grid(row=2, column=2, pady=5, padx=1)

        self.population_label = Label(self, text="Population: ")
        self.population_label.grid(row=2, column=3, pady=5, padx=5)

        self.population_entry = Entry(self)
        self.population_entry.grid(row=2, column=4, pady=5, padx=1)

        self.mutation_label = Label(self, text="Mutation Rate: ")
        self.mutation_label.grid(row=2, column=5, pady=5, padx=5)

        self.mutation_entry = Entry(self)
        self.mutation_entry.grid(row=2, column=6, pady=5, padx=1)

        self.cross_label = Label(self, text="Cross Rate: ")
        self.cross_label.grid(row=2, column=7, pady=5, padx=5)

        self.cross_entry = Entry(self)
        self.cross_entry.grid(row=2, column=8, pady=5, padx=1)


        self.solve_button = Button(self, text="Solve using backtracking", command=self.solve_using_backtracking)
        self.solve_button.grid(row=3, column=0, pady=5, padx=5)


        self.init_board_label = Label(self, text="Initial Board: ")
        self.init_board_label.grid(row=4, column=1, pady=5, padx=5)

        self.init_board = Text(self, height=35, width=35)
        self.init_board.grid(row=5, column=0, pady=5, padx=5, columnspan=2)

        self.bactrack_board_label = Label(self, text="Backtracking Solution: ")
        self.bactrack_board_label.grid(row=4, column=5, pady=5, padx=5)

        self.bactrack_board = Text(self, height=35, width=35)
        self.bactrack_board.grid(row=5, column=5, pady=5, padx=5, columnspan=2)

        self.ga_board_label = Label(self, text="GA Solution: ")
        self.ga_board_label.grid(row=4, column=3, pady=5, padx=5)

        self.ga_board = Text(self, height=35, width=35)
        self.ga_board.grid(row=5, column=3, pady=5, padx=5, columnspan=2)


        self.print_board(self.init_solution, self.init_board)



    def solve_using_backtracking(self):

        start = time.time()

        self.bactrack_board.delete('1.0', END)

        backtr_solver = BackTrackSolution()

        board = self.init_solution.copy()

        self.bactrack_solution = backtr_solver.solveSudoku(board)


        self.print_board(self.bactrack_solution, self.bactrack_board)

        end = time.time()

        self.bactrack_board.insert(END, "\n")
        self.bactrack_board.insert(END, f"Time taken: {round(end - start, 6)}s (Wall time)")
        


    def solve_using_GA(self):
        seed = int(self.seed_entry.get())
        population = int(self.population_entry.get())
        mutation_rate = float(self.mutation_entry.get())
        cross_rate = float(self.cross_entry.get())
        
        # TODO CAMARA EMI >;(
        pass

    def generate_sudoku(self):
        self.init_board.delete('1.0', END)

        difficulty_level = self.difficulty_box.get()

        if difficulty_level == 'Easy':
            num_empty_cells = round(81 - 81 * 0.6)
        elif difficulty_level == 'Medium':
            num_empty_cells = round(81 - 81 * 0.48)
        elif difficulty_level == 'Advanced':
            num_empty_cells = round(81 - 81 * 0.3)

        self.init_solution = self.generate_sudoku_board(num_empty_cells)
            


        self.print_board(self.init_solution, self.init_board)


    

    def print_board(self, solution, board):
        for i, row in enumerate(solution):
            for j, value in enumerate(row):
                board.insert(END, f" {value} ")
                if (j + 1) % 3 == 0 and j < 8:
                    board.insert(END, "|")
            board.insert(END, "\n")
            if (i + 1) % 3 == 0 and i < 8:
                board.insert(END, "-----------------------------\n")


    def generate_sudoku_board(self, num_empty_cells):
        def is_valid_move(board, row, col, num):
            # Verificar si es válido colocar 'num' en la posición (row, col) del tablero
            for i in range(9):
                if board[row][i] == num or board[i][col] == num or board[3 * (row // 3) + i // 3][3 * (col // 3) + i % 3] == num:
                    return False
            return True

        def fill_board(board):
            # Backtracking approach to fill the board
            for i in range(81):
                row, col = divmod(i, 9)
                if board[row][col] == '.':
                    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
                    random.shuffle(numbers)
                    for num in numbers:
                        if is_valid_move(board, row, col, num):
                            board[row][col] = num
                            if fill_board(board):
                                return True
                            board[row][col] = '.'  # Backtrack if no valid number is found


                    return False
            return True

        # Inicializar un tablero vacío
        sudoku_board = [['.' for _ in range(9)] for _ in range(9)]

        # Llenar el tablero usando backtracking
        fill_board(sudoku_board)

        # Quitar aleatoriamente algunas celdas para hacerlas vacías
        for _ in range(num_empty_cells):
            row, col = random.randint(0, 8), random.randint(0, 8)
            while sudoku_board[row][col] == '.':
                row, col = random.randint(0, 8), random.randint(0, 8)
            sudoku_board[row][col] = '.'

        return sudoku_board
