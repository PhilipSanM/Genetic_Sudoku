import random
import numpy as np
import copy
import matplotlib.pyplot as plt

import get_sudoku

cadena = "5...........8....23.....1...7..6......6...8......9..5...1.....94....7......3....6"

sudoku_puzzle = get_sudoku.get_sudoku_matrix(cadena)

def print_sudoku(board):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(board[i][j], end=" ")
        print()
    print("\n")

class Individuo:
    def __init__(self):
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

        print_sudoku(board)


def crossOver(pc1,pc2,population):
    #nuevaPoblacion = []
    for _ in range(len(population)//2):
        p1,p2 = random.sample(population,2)
        rand1 = random.uniform(0,1)
        if rand1 < pc1: #Se realiza la cruza
            for r,row in enumerate(p1.matrix):
                rand2 = random.uniform(0,1)
                if rand2 < pc2: #Se realiza el intercambio de genes entre filas
                    for c,col in enumerate(row):
                        actualAssociatedRow1 = p1.associatedMatrix[r]
                        actualAssociatedRow2 = p2.associatedMatrix[r]
                        if actualAssociatedRow1[c] != 1 and actualAssociatedRow2[c] != 1:
                            temp = p1.matrix[r][c]
                            p1.matrix[r][c] = p2.matrix[r][c]
                            p2.matrix[r][c] = temp
            #offspring1 = p1
            #offspring2 = p2
        #else:
            #offspring1 = p1
            #offspring2 = p2
        
        #nuevaPoblacion.append(offspring1)
        #nuevaPoblacion.append(offspring2)
                
    #return nuevaPoblacion
def indexAvailableToSwap(rowAsociada):
    
    index = []
    for c,col in enumerate(rowAsociada):
        if col != 1:
            index.append(c)
    index1,index2 = random.sample(index, 2)
    return index1,index2
def mutation(pm1, pm2,population):
    for individuo in population:
        matrix = individuo.matrix
        matrixAsociada = individuo.associatedMatrix
        #print(matrixAsociada)
        for r,row in enumerate(matrix):
            rowAsociada = matrixAsociada[r]
            rand1 = random.uniform(0,1)
            rand2 = random.uniform(0,1)
            if rand1 < pm1:
                idx1,idx2 = indexAvailableToSwap(rowAsociada)
                temp = matrix[r][idx1]
                matrix[r][idx1] = matrix[r][idx2]
                matrix[r][idx2] = temp
            if rand2 < pm2:
                for c,col in enumerate(rowAsociada):
                    if col == 0:
                        matrix[r][c] = 0          
                individuo.setRow(matrix[r],r)
def actualiza_columna(matriz, nueva_columna, indice_columna):
    for i in range(len(matriz)):
        matriz[i][indice_columna] = nueva_columna[i]
    return matriz



def columnLocalSarch(population):
    for individuo in population:
        #print(f"COLUMNEANDO INDIVIDUO")
        #individuo.showPuzzle(0)
        columnasAsociadas = []
        columnas = []
        repetidos, repetidosPorCol = copy.deepcopy(individuo.getRepeatedColumns())

        #print(repetidosPorCol)
        #print(repetidos)

        nuevasColumnas = []

        #print("\n")

        matrizCopia = copy.deepcopy(individuo.matrix)
        matrizCopiaAsociada = copy.deepcopy(individuo.associatedMatrix)

      
      
        for i in range(individuo.size):
            columnas.append( [row[i] for row in matrizCopia])
            associatedColumn = [row[i] for row in matrizCopiaAsociada]
            columnasAsociadas.append(associatedColumn)
        #print(columnasAsociadas)

        for c,columna in enumerate(columnas):
            columnas_disponibles = [col for col in columnas if col != columna]
            randomColumna = random.choice(columnas_disponibles)
            
            indiceCol1 = columnas.index(columna)
            indiceCol2 = columnas.index(randomColumna)

            colRep1 = repetidos[indiceCol1]
            colRep2 = repetidos[indiceCol2]

            #Vamos repetido por repetido
            for repetido in repetidosPorCol[indiceCol1]:
                #print(f"For repetido {repetido}")
                flag = False
                #Obtenemos su col de repetidos para este numero
                colNumRepetido = [0] * individuo.size
                for r,num in enumerate(columna):
                    if num == repetido:
                        colNumRepetido[r] = 1
                #print(f"Para numero repetido {repetido} y num {repetido} se obtuvo {colNumRepetido}")
                #Buscamos una columna en n-1 que no contenga el repetido actuial
                #print(f"Repetido {repetido} para columna {indiceCol1}")
                columnas_disponibles = [col for col in columnas if col != columna]
                random.shuffle(columnas_disponibles)
                for columnaAlternativa in columnas_disponibles:
                    #print(f"Se evalua con todas las demas columnas")
                    if flag ==True:
                        #print(f"Ya se hizo un cambio, breakeando")
                        break

                    indiceColAltern = columnas.index(columnaAlternativa)
                    repetidoColAlternativa = repetidos[indiceColAltern]
                    prohibidosColAlternativa = columnasAsociadas[indiceColAltern]
                    if repetido not in columnaAlternativa:
                        #print(f"Evaluando {repetido}: \nC{columna} <-> R{colNumRepetido} <-> A{columnasAsociadas[indiceCol1]} \nC{columnaAlternativa} <-> R{repetidoColAlternativa} <-> A{prohibidosColAlternativa} ")
                        
                        for r,row in enumerate(columna):
                            if colNumRepetido[r] == 1 and repetidoColAlternativa[r] == 1:
                                #print(f"ambos tienen repetidos {r}")
                                if columnasAsociadas[indiceCol1][r]==0 and prohibidosColAlternativa[r]==0:
                                    #print(f"No son prohibidos")
                                    if columnaAlternativa[r] not in columna:
                                        #print(f"otro")
                                        temp = columna[r]    
                                        columna[r] = columnaAlternativa[r]
                                        columnaAlternativa[r] = temp
                                        #Se hizo un cambio
                                        flag = True
                                        #print(columna)
                    
                                        
            nuevasColumnas.append(columna) 
        
        #print("ANTESSSS")
        #individuo.showPuzzle(0)

        for c,col in enumerate(nuevasColumnas):
            actualiza_columna(matrizCopia, col, c)
        #print("\n")

        #print("DESPEUS")
        individuo.matrix = matrizCopia
        #individuo.showPuzzle(0)


        #print("\n\n\n")

#Checa si los numeros existen en ambos subblocks
def checkNumbersInBothSubblocksNowFast(n1,n2,sub1,sub2,size):

    f1 = False
    f2 = False
    for r in range(size):
        for c in range(size):
            if n1 == sub2[r][c]:
                f1 = True
            if n2 == sub1[r][c]:
                f2 = True
    if f1 == True or f2==True:
 
        return False
    else:
        return True


def subblockLocalSearch(population):
    for individuo in population:
        subblockList, associatedSubblockList, repeatedValuesSubblockList,valoresRepetidos = copy.deepcopy(individuo.getSubBlocks())
        #print(f"Individuo antes:")
        #individuo.showPuzzle(0)
        newSubblocks = []

        for index,subblock in enumerate(subblockList):
           
            subblocksRestantes = [sub for sub in subblockList if sub != subblock]
            random.shuffle(subblocksRestantes)


            change = False
            for subblockAlterno in subblocksRestantes:
                if change == False:
                    indiceSBA = subblockList.index(subblockAlterno)
                    valorRepSubAlterno = valoresRepetidos[indiceSBA]
                    #print(f"\nSUBBLOCK <{index}>    SUBALTERNO {indiceSBA}")
                    for r,row in enumerate(subblock):
                        actualRow = subblock[r]
                        actualRowAlterno = subblockAlterno[r]
                        prohibidos = associatedSubblockList[index][r]
                        prohibidosAlterno = associatedSubblockList[indiceSBA][r]
                        repetidos = repeatedValuesSubblockList[index][r]
                        repetidosAlterno = repeatedValuesSubblockList[indiceSBA][r]
                        #print(f"comparando {actualRow} con {actualRowAlterno}")
                        if (1 in repetidos and 1 in repetidosAlterno):
                            #print(f"Hay repetidos en esta fila\n{actualRow} <-> R{repetidos} <-> P{prohibidos}\n{actualRowAlterno} <-> R{repetidosAlterno} <-> P{prohibidosAlterno}")
                            #print(f"Aqui hay repetidos numeros {valorRepSub} y {valorRepSubAlterno}")
                            indicesRepetidos = [idx for idx,value in enumerate(repetidos) if value==1]
                            indicesRepetidosA = [idx for idx,value in enumerate(repetidosAlterno) if value==1]
                            for toChange, toChangeA in zip(indicesRepetidos, indicesRepetidosA):
                                #print(f"En esta ejecucion cambiaremos {toChange} y {toChangeA}")
                                if prohibidos[toChange]==0 and prohibidosAlterno[toChangeA]==0:
                                    #print(f"Estos intercambis son permitidos")
                                    num1 = actualRow[toChange]
                                    num2 = actualRowAlterno[toChangeA]
                                    #print(f"Cambiando {num1} y {num2}")
                                    if checkNumbersInBothSubblocksNowFast(num1, num2, subblock, subblockAlterno, individuo.subBlockSize):
                                        #print(f"===============SUBBLOCK EXCHANGE============")
                                        temp = actualRow[toChange]
                                        actualRow[toChange] =actualRowAlterno[toChangeA]    
                                        actualRowAlterno[toChangeA]  = temp
                                        change = True
                                        break
            newSubblocks.append(subblock)
       
        individuo.updateMatrix(newSubblocks)
        #print(f"Individuo despues:")
        #individuo.showPuzzle(0)
        #print(f"\n\n")

def elitePopulationLearning(population, elitePopulation):
    elites = copy.deepcopy(elitePopulation)
    xrandom = random.choice(elites)
    xrandomFitness = xrandom.fitnessFunction()

    xworst = copy.deepcopy(population[0])
    maxfx = xworst.fitnessFunction()
    Pb = (maxfx-xrandomFitness)/maxfx
    rand = random.uniform(0,1)

    if rand < Pb:
        population[-1] = xrandom
        #print("reemplazado")
    else:
        nuevoIndividuo = Individuo()
        nuevoIndividuo.initMatrix()
        population[-1] = nuevoIndividuo
        #print("nuevoIndividuo")


def sortPopulation(population):
    fitnessEv = []
    for individuo in population:
        fitness = individuo.fitnessFunction()
        fitnessEv.append([individuo, fitness])
    fitnessEv.sort(key=lambda x: x[1], reverse=False)
    return [individuo for individuo, _ in fitnessEv]

def sudoku_ga(populationSize, generaciones, pc1, pc2, pm1, pm2):
    population = []
    for _ in range(populationSize):
        instance = Individuo()
        instance.initMatrix()
        population.append(instance)

    elitePopulation = []
    val = 1000
    for i in range(generaciones):
        #print(f"===GENERACION {i}===")

        population=sortPopulation(population)

        #mostrarAptitudPoblacion(elitePopulation,"ELITES")

        #mostrarAptitudPoblacion(population,"Inicio generacion")

        crossOver(pc1,pc2,population)

        #mostrarAptitudPoblacion(population,"despues de cross")

        mutation(pm1,pm2,population)
        population = sortPopulation(population)


        #mostrarAptitudPoblacion(population,"despues de mutation")

        columnLocalSarch(population)

        subblockLocalSearch(population)
        

        population = sortPopulation(population)


        best = copy.deepcopy(population[0])
        updateElitePopulation(elitePopulation,best)

        #mostrarAptitudPoblacion(population,"Despues de actualizar elite")
        population = sortPopulation(population)
        #elitePopulationLearning(population,copy.deepcopy(elitePopulation))
        
        #mostrarAptitudPoblacion(population,"Despues de actualizar learning")

        Gbest = elitePopulation[-1]
        #print(f"Best {Gbest.fitnessFunction()}")
        if Gbest.fitnessFunction() == 0: 
            val = i
            break
        #elitePopulationLearning(population,copy.deepcopy(elitePopulation))
        
    Gbest.showPuzzle(0)

        
    return elitePopulation[-1].fitnessFunction(), val

    

def updateElitePopulation(elitePopulation, indvElite):
    if all(indvElite.fitnessFunction() < elite.fitnessFunction() for elite in elitePopulation):
        elitePopulation.append(indvElite)
        if len(elitePopulation)>=50:
            elitePopulation.pop(0)

def mostrarPuzzles(population,str=''):
    print(f"Fitness poblacion {str}")
    for p in population:
        p.showPuzzle(0)
    print("\n")

def mostrarAptitudPoblacion(population,str=''):
    print(f"Fitness poblacion {str}")
    for p in population:
        print(f"{p.fitnessFunction()}", end='  ')
    print("\n")
def mostrarDirecciones(population,str=''):
    print(f"Direccion {str}")
    for p in population:
        print(f"{id(p)}", end='  ')
    print("\n")


#Parametros
populationSize = 20#población par
generaciones = 1000

# Inicializar los mejores parámetros y el mejor resultado
mejores_parametros = None
mejor_resultado = float('inf')
parametros = None
resultado = float('inf')

import numpy as np

# Rangos para cada variable con decimales
rango_var1 = np.arange(.1, 1, 0.1)  # Por ejemplo, del 1 al 5 en pasos de 0.5
rango_var2 = np.arange(.1, 1, 0.1)  # Por ejemplo, del 5 al 8 en pasos de 0.5
rango_var3 = np.arange(.1, 1, 0.1)   # Por ejemplo, de -2 a 2 en pasos de 0.5
rango_var4 = np.arange(0.01, .1, 0.01)  # Por ejemplo, del 0 al 3 en pasos de 0.5
file_path = "C:/Users/diego/OneDrive/Escritorio/ESCOM/5SEM/BIO/Genetic_Sudoku-main/params.txt"
file_path2 = "C:/Users/diego/OneDrive/Escritorio/ESCOM/5SEM/BIO/Genetic_Sudoku-main/wrong_params.txt"

# Generar todas las combinaciones
for var4 in rango_var4:
    for var3 in rango_var3:
        for var2 in rango_var2:
            for var1 in rango_var1:
                combinacion = (var1, var2, var3, var4)

                resultado_actual, i = sudoku_ga(populationSize, generaciones, var1, var2, var3, var4)

                if resultado_actual == 0:
                    mejores_parametros = (var1, var2, var3, var4)
                    mejor_resultado = resultado_actual
                    with open(file_path, "a") as file:
                        # Write the data to the file
                        file.write(str(mejores_parametros))
                        file.write(f"{i}\n")
                else:
                    parametros = (var1, var2, var3, var4)
                    resultado = resultado_actual
                    with open(file_path2, "a") as file:
                        # Write the data to the file
                        file.write(str(parametros))
                        file.write(str(resultado))
                        file.write(f"\t{i}\n")


