import random
import numpy as np
import copy

class Individuo:
    def __init__(self, sudoku_puzzle):
        self.size = 9

        self.matrix = copy.deepcopy(sudoku_puzzle)
        self.associatedMatrix = np.zeros((self.size,self.size),dtype=int)
        #self.columnsRepeated = np.zeros((self.size,self.size),dtype=int)

        self.values = [1,2,3,4,5,6,7,8,9]
        self.givenNumbersIndexes = [] #Casillas que no pueden cambiar

        self.subBlockSize = int(pow(self.size,0.5)) 
        self.subBlockIndexes = [index*self.subBlockSize for index in range(self.subBlockSize)]

    #Asigna numeros aleatorios a los espacios de la matriz
    def initMatrix(self):
        random.seed()
        for r, row in enumerate(self.matrix):
            self.setRow(row,r)
    
    #setRow
    def setRow(self, row, r):
        actualRow = set(row)
        validNumbers = set(self.values)        
        diference = list(validNumbers.difference(actualRow)) 
        for c,casilla in enumerate(row):
            if casilla == 0: 
                number = random.choice(diference)
                diference.remove(number)
                self.matrix[r][c] = number
            else:
                self.associatedMatrix[r][c] = 1
        
    #Obtiene Subblock y sus asociadas
    def getSubBlocks(self):
        subblockSize = self.subBlockSize

        subblockList = []
        associatedSubblockList = []
        repeatedValuesSubblockList = []
        numerosRepetidos =[]

        for i in range(self.size):
            subblock = []            
            associatedSubblock = []
            repeatedSubblock = np.zeros((self.subBlockSize, self.subBlockSize))
            #paraCalcularRepetidos
            numeros = []
            repetidos = []
            #coordenadas
            xInicio = self.subBlockIndexes[i%(subblockSize)]
            xFin = xInicio + subblockSize
            if i in self.subBlockIndexes:
                yInicio = i
                yFin = yInicio + subblockSize
            #Slice a la matriz
            for r,row in enumerate(self.matrix[yInicio:yFin]):
                subblock.append(row[xInicio:xFin])
                associatedSubblock.append((self.associatedMatrix[r])[xInicio:xFin])
                for c,col in enumerate(row[xInicio:xFin]):
                    if col not in numeros:
                        numeros.append(col)
                    else:
                        if col not in repetidos:
                            repetidos.append(col)
            #Actualiza repetidos
            for r,row in enumerate(subblock):
                for c,col in enumerate(row):
                    if col in repetidos:
                        repeatedSubblock[r][c] = 1
            numerosRepetidos.append(repetidos)
            repeatedValuesSubblockList.append(repeatedSubblock)
            associatedSubblockList.append(associatedSubblock)
            subblockList.append(subblock)

        return subblockList, associatedSubblockList, repeatedValuesSubblockList,numerosRepetidos
    
    def getSubBlocks_wrong(self):
        subblockSize = self.subBlockSize

        subblockList = []
        associatedSubblockList = []
        repeatedValuesSubblockList = []
        numerosRepetidos =[]

        for i in range(self.size):
            mal = False
            subblock = []            
            associatedSubblock = []
            repeatedSubblock = np.zeros((self.subBlockSize, self.subBlockSize))
            #paraCalcularRepetidos
            numeros = []
            repetidos = []
            #coordenadas
            xInicio = self.subBlockIndexes[i%(subblockSize)]
            xFin = xInicio + subblockSize
            if i in self.subBlockIndexes:
                yInicio = i
                yFin = yInicio + subblockSize
            #Slice a la matriz
            for r,row in enumerate(self.matrix[yInicio:yFin]):
                subblock.append(row[xInicio:xFin])
                associatedSubblock.append((self.associatedMatrix[r])[xInicio:xFin])
                for c,col in enumerate(row[xInicio:xFin]):
                    if col not in numeros:
                        numeros.append(col)
                    else:
                        if col not in repetidos:
                            repetidos.append(col)
            #Actualiza repetidos
            for r,row in enumerate(subblock):
                for c,col in enumerate(row):
                    if col in repetidos:
                        repeatedSubblock[r][c] = 1
                        mal = True
                    
            if mal:
                numerosRepetidos.append(repetidos)
                repeatedValuesSubblockList.append(repeatedSubblock)
                associatedSubblockList.append(associatedSubblock)
                subblockList.append(subblock)

        return subblockList, associatedSubblockList, repeatedValuesSubblockList,numerosRepetidos
    
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

    #Funcion objetivo (optimo = 0)
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

