import random
import numpy as np
import copy


#CADA POSIBLE SOLUCIÓN
class Individuo:
    def __init__(self, sudoku_puzzle):
        self.size = 9 #Tamaño del tablero

        self.matrix = copy.deepcopy(sudoku_puzzle) 
        self.associatedMatrix = np.zeros((self.size,self.size),dtype=int) #Matriz Binaria de números dados
        
        self.values = [1,2,3,4,5,6,7,8,9] #Posibles valores a tomar

        self.subBlockSize = int(pow(self.size,0.5))  #Tamaño de cada subbbloc
        self.subBlockIndexes = [index*self.subBlockSize for index in range(self.subBlockSize)] #Indices de subblock

    #INIT MATRIX: Asigna numeros aleatorios a los espacios de la matriz
    def initMatrix(self):
        random.seed()
        for r, row in enumerate(self.matrix):
            self.setRow(row,r)


    #Inicializa filas y llena matriz asociada
    def setRow(self, row, r):
        actualRow = set(row)
        validNumbers = set(self.values)        
        diference = list(validNumbers.difference(actualRow)) 

        for c,casilla in enumerate(row):
            if casilla == 0: 
                number = random.choice(diference)
                diference.remove(number)
                self.matrix[r][c] = number
            elif casilla!=0:
                self.associatedMatrix[r][c] = 1


    #Obtiene subblocks y sus subblocks asociados
    def getSubBlocks(self):
        subblockSize = self.subBlockSize

        subblockList = []
        associatedSubblockList = []
        repeatedValuesSubblockList = []
        numerosRepetidos =[]
       
        for i in range(self.size):
            subblock = []            
            repeatedSubblock = np.zeros((self.subBlockSize, self.subBlockSize))

            numeros = []
            repetidos = []
        
            xInicio = self.subBlockIndexes[i%(subblockSize)]  
            xFin = xInicio + subblockSize

            if i in self.subBlockIndexes:
                yInicio = i
                yFin = yInicio + subblockSize

            #Extrae repetidos de cada subblock
            for r,row in enumerate(self.matrix[yInicio:yFin]):
                subblock.append(row[xInicio:xFin])
                for c,col in enumerate(row[xInicio:xFin]):
                    if col not in numeros:
                        numeros.append(col)
                    else:
                        if col not in repetidos:
                            repetidos.append(col)

            #Asigna valores a la matriz de repetidos
            for r,row in enumerate(subblock):
                for c,col in enumerate(row):
                    if col in repetidos:
                        repeatedSubblock[r][c] = 1
            numerosRepetidos.append(repetidos)
            repeatedValuesSubblockList.append(repeatedSubblock)
            subblockList.append(subblock)

        #Obtiene los subblocks asociados
        associatedSubblockList = self.getAssociatedSubblock(self.associatedMatrix)

        return subblockList, associatedSubblockList, repeatedValuesSubblockList,numerosRepetidos


    #Obtiene los subblock asociados (listas binarias de posiciones que no pueden cambiar)
    def getAssociatedSubblock(self, board):
        repetedList = []
        values = []
        for row in range(3):
            r = []
            for col in range(3):
                r.append(board[row][col])
            values.append(r)
        repetedList.append(values)

        values = []
        for row in range(3):
            r = []
            for col in range(3, 6):
                r.append(board[row][col])
            values.append(r)
        repetedList.append(values)

        values = []
        for row in range(3):
            r = []
            for col in range(6, 9):
                r.append(board[row][col])
            values.append(r)
        repetedList.append(values)

        values = []
        for row in range(3, 6):
            r = []
            for col in range(3):
                r.append(board[row][col])
            values.append(r)
        repetedList.append(values)

        values = []
        for row in range(3, 6):
            r = []
            for col in range(3, 6):
                r.append(board[row][col])
            values.append(r)
        repetedList.append(values)

        values = []
        for row in range(3, 6):
            r = []
            for col in range(6, 9):
                r.append(board[row][col])
            values.append(r)
        repetedList.append(values)

        values = []
        for row in range(6, 9):
            r = []
            for col in range(3):
                r.append(board[row][col])
            values.append(r)
        repetedList.append(values)

        values = []
        for row in range(6, 9):
            r = []
            for col in range(3, 6):
                r.append(board[row][col])
            values.append(r)
        repetedList.append(values)

        values = []
        for row in range(6, 9):
            r = []
            for col in range(6, 9):
                r.append(board[row][col])
            values.append(r)
        repetedList.append(values)

        return repetedList


    #Muestra en formato sudoku la matriz
    def print_sudoku(self, board):
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("-" * 21)
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print("|", end=" ")
                print(board[i][j], end=" ")
            print()
        print("\n")


    #Funcion objetivo 
    #Función con la suma de columas - subbloques ilegales. Función a minimizar
    def fitnessFunction(self): 
        colCountRule = 0
        rowCounter = 0
        for i in range(self.size): 
            #Suma para col
            col = [fila[i] for fila in self.matrix]
            if len(col) != len(set(col)):
                colCountRule += 1
            #Suma para subblock
            subblocks,_,_,_ = self.getSubBlocks()
            for subblock in subblocks:
                for j in range(self.subBlockSize):
                    colS = [fila[j] for fila in subblock]
                    if len(colS) != len(set(colS)):
                        colCountRule += 1
        return colCountRule
    

    #Calcula la matriz repeatedColums
    def getRepeatedColumns(self):
        columnsRepeated = np.zeros((self.size,self.size),dtype=int)
        listOfRepeated = []
        for i in range(self.size):
            column = [row[i] for row in self.matrix]
            numeros = []
            repetidos = []
            for row in column:
                if row not in numeros:
                    numeros.append(row)
                else:
                    repetidos.append(row)
            for r,row in enumerate(column):
                if row in repetidos:
                    columnsRepeated[i][r] = 1
            listOfRepeated.append(repetidos)
        return columnsRepeated, listOfRepeated
    

    #Actualiza las matrices con subblocks
    def updateMatrix(self, subblocks):
        sbSize = self.subBlockSize
        for i,sub in enumerate(subblocks):
            xinicio = self.subBlockIndexes[i%(sbSize)]
            xfin = xinicio + sbSize-1
            if i in self.subBlockIndexes:
                yInicio = i
                yFin = yInicio + sbSize -1
            for r,row in enumerate(self.matrix):
                for c,col in enumerate(row):
                    if r >= yInicio and r <= yFin:
                        if c >= xinicio and c<= xfin:
                            self.matrix[r][c]=sub[r%sbSize][c%sbSize]


    #Imprime sudoku                        
    def showPuzzle(self,option):
        if option == 0:
            board = self.matrix
        elif option == 1:
            board = self.associatedMatrix
        self.print_sudoku(board)

