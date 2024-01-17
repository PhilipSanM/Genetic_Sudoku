from tkinter import *
from tkinter import ttk
import time
import random
from Solutions.BackTracking import  BackTrackSolution
from Solutions.GA_copy import GeneticAlgorithm


class Gui(Tk):
    def __init__(self):
        super().__init__()
        
        self.init_solution = [['5', '3', '.', '.', '7', '.', '.', '.', '.'],['6', '.', '.', '1', '9', '5', '.', '.', '.'],['.', '9', '8', '.', '.', '.', '.', '6', '.'],['8', '.', '.', '.', '6', '.', '.', '.', '3'],['4', '.', '.', '8', '.', '3', '.', '.', '1'],['7', '.', '.', '.', '2', '.', '.', '.', '6'],['.', '6', '.', '.', '.', '.', '2', '8', '.'],['.', '.', '.', '4', '1', '9', '.', '.', '5'],['.', '.', '.', '.', '8', '.', '.', '7', '9']]
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
        self.difficulty_box.current(0)
        self.difficulty_box.grid(row=1, column=2, pady=5, padx=5)

        self.solve_using_GA_button = Button(self, text="Solve using GA", command=self.solve_using_GA)
        self.solve_using_GA_button.grid(row=2, column=0, pady=5, padx=5)

        self.population_label = Label(self, text="Population: ")
        self.population_label.grid(row=2, column=3, pady=5, padx=5)
        self.population_entry = Entry(self)
        self.population_entry.grid(row=2, column=4, pady=5, padx=1)

        self.mutation_label_1 = Label(self, text="Mutation Rate 1: ")
        self.mutation_label_1.grid(row=2, column=7, pady=5, padx=5)
        self.mutation_entry_1 = Entry(self)
        self.mutation_entry_1.grid(row=2, column=8, pady=5, padx=1)

        self.mutation_label_2 = Label(self, text="Mutation Rate 2: ")
        self.mutation_label_2.grid(row=3, column=7, pady=5, padx=5)
        self.mutation_entry_2 = Entry(self)
        self.mutation_entry_2.grid(row=3, column=8, pady=5, padx=1)

        self.cross_label_1 = Label(self, text="Cross Rate 1: ")
        self.cross_label_1.grid(row=2, column=5, pady=5, padx=5)
        self.cross_entry_1 = Entry(self)
        self.cross_entry_1.grid(row=2, column=6, pady=5, padx=1)

        self.cross_label_2 = Label(self, text="Cross Rate 2: ")
        self.cross_label_2.grid(row=3, column=5, pady=5, padx=5)
        self.cross_entry_2 = Entry(self)
        self.cross_entry_2.grid(row=3, column=6, pady=5, padx=1)

        self.solve_button = Button(self, text="Solve using backtracking", command=self.solve_using_backtracking)
        self.solve_button.grid(row=3, column=0, pady=5, padx=5)

        self.init_board_label = Label(self, text="Initial Board: ")
        self.init_board_label.grid(row=4, column=1, pady=5, padx=5)
        self.init_board = Text(self, height=35, width=35)
        self.init_board.grid(row=5, column=0, pady=5, padx=5, columnspan=2)
        self.init_board.tag_configure("error", foreground="red")
        self.init_board.tag_configure("clean", foreground="blue")

        self.bactrack_board_label = Label(self, text="Backtracking Solution: ")
        self.bactrack_board_label.grid(row=4, column=5, pady=5, padx=5)
        self.bactrack_board = Text(self, height=35, width=35)
        self.bactrack_board.grid(row=5, column=5, pady=5, padx=5, columnspan=2)
        self.bactrack_board.tag_configure("error", foreground="red")
        self.bactrack_board.tag_configure("clean", foreground="blue")

        self.ga_board_label = Label(self, text="GA Solution: ")
        self.ga_board_label.grid(row=4, column=3, pady=5, padx=5)
        self.ga_board = Text(self, height=35, width=35)
        self.ga_board.grid(row=5, column=3, pady=5, padx=5, columnspan=2)
        self.ga_board.tag_configure("error", foreground="red")
        self.ga_board.tag_configure("clean", foreground="blue")

        self.print_board(self.init_solution, self.init_board)

    def solve_using_backtracking(self):

        start = time.time()

        self.bactrack_board.delete('1.0', END)

        backtr_solver = BackTrackSolution()

        board = list(map(list, self.init_solution))

        self.bactrack_solution = backtr_solver.solveSudoku(board)


        self.print_board(self.bactrack_solution, self.bactrack_board)

        end = time.time()

        self.bactrack_board.insert(END, "\n")
        self.bactrack_board.insert(END, f"Time taken: {round(end - start, 6)}s (Wall time)")
        
    def get_sudoku_matrix(self, cadena):
        # Convertir la matriz de caracteres a una matriz de enteros
        matriz_enteros = [[int(caracter) if caracter != '.' else 0 for caracter in fila] for fila in cadena]

        return matriz_enteros

    def solve_using_GA(self):
        #seed = int(self.seed_entry.get())
        #random.seed(seed)
        if self.population_entry.get():
            population = int(self.population_entry.get())
        else:
            population = 2
        
        if self.cross_entry_1.get():
            pc1 = float(self.cross_entry_1.get())
        else:
            pc1 = 0.2

        if self.cross_entry_2.get():
            pc2 = float(self.cross_entry_2.get())
        else:
            pc2 = 0.1
        
        if self.mutation_entry_1.get():
            pm1 = float(self.mutation_entry_1.get())
        else:
            pm1 = 0.3   
        
        if self.mutation_entry_2.get():
            pm2 = float(self.mutation_entry_2.get())
        else:
            pm2 = 0.05

        ga_solver = GeneticAlgorithm()
        start = time.time()
        self.ga_board.delete('1.0', END)


        board = list(map(list, self.init_solution))

        board = self.get_sudoku_matrix(board)

        
        #self.ga_solution = ga_solver.sudoku_ga(board, 100, 1000,  0.2, 0.1, 0.3, 0.05) 
        # self.ga_solution, iterations, solutions = ga_solver.sudoku_ga(board, population, 500,  pc1, pc2, pm1, pm2) 
        self.ga_solution, solutions, val = ga_solver.sudoku_ga(board, population, 1000,  pc1, pc2, pm1, pm2) 

        self.print_board(self.ga_solution, self.ga_board)

        end = time.time()

        self.ga_board.insert(END, "\n")
        self.ga_board.insert(END, f"Time taken: {round(end - start, 6)}s (Wall time), Total iterations: {val}")
        self.ga_board.insert(END, "\n")
        self.ga_board.insert(END, "\n")

        # self.ga_board.insert(END, f"Time taken: {round(end - start, 6)}s (Wall time), Total iterations: {10}")


        self.ga_board.insert(END, "\n")

        for i in range(len(solutions)):
            self.ga_board.insert(END, f"Solution {i + 1}: \n")
            self.print_board(solutions[i], self.ga_board)
            self.ga_board.insert(END, "\n")
        

    def map_sudoku_2_integers(self, sudoku):
        sudoku_board = []
        for row in sudoku:
            line = []
            for value in row:
                if value == '.':
                    line.append(0)
                else:
                    line.append(int(value))
            
            sudoku_board.append(line)

        return sudoku_board

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
        aux = [0,0,0, 1,1,1,2,2,2]

        for i, row in enumerate(solution):
            rows = set()
            cols = set()
            if i % 3 == 0:
                squares = {c: set() for c in range(3)}

            for j, value in enumerate(row):
                tag = "clean"


                if value in rows and value != '.':
                    tag = "error"

                if value in cols and value != '.':
                    tag = "error"
                
                if value in squares[aux[j]] and value != ".":
                    tag = "error"

                rows.add(value)
                cols.add(value)
                squares[aux[j]].add(value)

                
                board.insert(END, f" {value} ", tag)
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
