import random
import time
from GA import GeneticAlgorithm


def get_sudoku_matrix(cadena):
    # Convertir la matriz de caracteres a una matriz de enteros
    matriz_enteros = [[int(caracter) if caracter != '.' else 0 for caracter in fila] for fila in cadena]

    return matriz_enteros

init_solution= [["5","8","9","7","6",".",".","4","3"],["4","7",".","5","0","0","1","9","6"],[".",".","3","4","9","2",".","8","7"],[".","9","4","6","8",".",".","5","1"],[".","3","6","1","5",".","4","2","8"],["1","5","8","3",".","4","6","7","."],["8",".","5","9","4",".","7",".","."],["3","2","7",".",".","5","9","6","4"],["9","4",".",".",".","6","8",".","5"]]

start = time.time()
ga_solver = GeneticAlgorithm()
board = get_sudoku_matrix(init_solution)

ga_solution, it = ga_solver.sudoku_ga(board, 100, 1000,  0.2, 0.1, 0.3, 0.05)


end = time.time()
print(f"Valor funcion = {ga_solution} en iteracion {it}")
print(f"Time taken: {round(end - start, 6)}s (Wall time)")
