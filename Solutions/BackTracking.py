# ===================================================================
# ===================== Genetic Sudoku Solver =======================
# ===================================================================
# repository: https://github.com/PhilipSanM/Genetic_Sudoku


class BackTrackSolution(object):
    def solveSudoku(self, board):
        """
        :type board: List[List[str]]
        :rtype: None Do not return anything, modify board in-place instead.
        """

        
        
        def isValid(x, y, value):
            '''
            Esta funcion verifica si el valor que se quiere poner en la posicion x, y es valido, dentro de la fila, columna y cuadrado

            '''
            return value not in rows[x] and value not in columns[y] and value not in squares[(auxiliar[x], auxiliar[y])]


        # Backtracking approach
        def backtracking(row = 0, column = 0):
            ''''
            Esta solucion es recursiva buscando la solucion del sudoku, se va a la siguiente columna si la actual esta llena, y a la siguiente fila si la columna actual esta llena
            y determinista
            '''
            if row >= 9:
                return True
            elif column == 9:
                return backtracking(row + 1, 0)
            elif board[row][column] != '.':
                return backtracking( row, column + 1)
            else:
                for value in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    if isValid(row, column, value):
                        board[row][column] = value
                        
                        # Adding those columns
                        rows[row].add(value)
                        columns[column].add(value)
                        squares[(auxiliar[row], auxiliar[column])].add(value)
                    
                

                        # backtracking until finding solution
                        if backtracking(row, column + 1):
                            return True


            
                        board[row][column] = '.'
                        rows[row].remove(value)
                        columns[column].remove(value)
                        squares[(auxiliar[row], auxiliar[column])].remove(value)


                return False

        auxiliar = [0,0,0,1,1,1,2,2,2]
        rows = {row: set() for row in range(9)}
        columns = {column: set() for column in range(9)}
        squares = {(x, y): set() for x in range(3) for y in range(3)}


        for row in range(9):
            for column in range(9):
                if board[row][column] == '.':
                    continue
            
                rows[row].add(board[row][column])
                columns[column].add(board[row][column])
                squares[(auxiliar[row], auxiliar[column])].add(board[row][column])



        

        backtracking()

        return board

