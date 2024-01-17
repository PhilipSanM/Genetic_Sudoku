import random
import numpy as np
import copy
import Solutions.Individuo as Individuo

class GeneticAlgorithm:
    def __init__(self):
        self.population = []
        self.elitePopulation = []
        # # ... other attributes

    def crossOver(self, pc1,pc2,population):
        # Iteramos sobre cada individuo de la poblacion
        for index, individuo in enumerate(population):

            p1 = individuo # El padre 1 es el individuo sobre el cual iteramos
            restantes = [sub for sub in population if sub != individuo] # Lista de individuos restantes
            rand1 = random.uniform(0,1) # Variable random de 0 a 1 

            if rand1 < pc1: #Se realiza la cruza
                p2 = random.choice(restantes) # Seleccionamos padre 2 aleatoriamente 
                
                for r,row in enumerate(p1.matrix): # Iteramos sobre cada fila del padre 1
                    rand2 = random.uniform(0,1) # Variable random de 0 a 1 

                    if rand2 < pc2: #Se realiza el intercambio de genes entre filas

                        actualAssociatedRow1 = p1.associatedMatrix[r] # Vector binario de posiciones
                        indices_of_zeros = [i for i, val in enumerate(actualAssociatedRow1) if val == 0] # Indices de posiciones a cambiar
                        
                        for idx0 in indices_of_zeros:

                                aux1 = p1.matrix[r][idx0]
                                aux2 = p2.matrix[r][idx0]

                                p1.matrix[r][idx0] = aux2
                                p2.matrix[r][idx0] = aux1

    def mutation(self, pm1, pm2, population):
        for individuo in population:
            matrix = individuo.matrix

            for r,row in enumerate(matrix):
                rowAsociada = individuo.associatedMatrix[r] # Vector binario de posiciones
                rand1 = random.uniform(0,1) # Variable random de 0 a 1
                rand2 = random.uniform(0,1) # Variable random de 0 a 1

                if rand1 < pm1:
                    indices_of_zeros = [i for i, val in enumerate(rowAsociada) if val == 0] # Indices de posiciones en 0

                    if len(indices_of_zeros) >= 2: # swap of two positions
                        random_idx= random.sample(indices_of_zeros, 2)

                        idx1 = random_idx[0]
                        idx2 = random_idx[1]
                        aux1 = matrix[r][idx1]
                        aux2 = matrix[r][idx2]
                        matrix[r][idx1] = aux2
                        matrix[r][idx2] = aux1 

                if rand2 < pm2: # reinitializing the distribution of the rows
                    for c,col in enumerate(rowAsociada):
                        if col == 0:
                            matrix[r][c] = 0
                    individuo.setRow(matrix[r],r)
                             
    def actualiza_columna(self, matriz, nueva_columna, indice_columna):
        for i in range(len(matriz)):
            matriz[i][indice_columna] = nueva_columna[i]
        return matriz

    def columnLocalSarch(self, population):
        for individuo in population:
            columnasAsociadas = []
            columnas = []
            repetidos, repetidosPorCol = copy.deepcopy(individuo.getRepeatedColumns())
            nuevasColumnas = []
            matrizCopia = copy.deepcopy(individuo.matrix)
            matrizCopiaAsociada = copy.deepcopy(individuo.associatedMatrix)

            for i in range(individuo.size):
                columnas.append( [row[i] for row in matrizCopia])
                associatedColumn = [row[i] for row in matrizCopiaAsociada]
                columnasAsociadas.append(associatedColumn)

            for c,columna in enumerate(columnas):
                columnas_disponibles = [col for col in columnas if col != columna]
                indiceCol1 = columnas.index(columna)

                for repetido in repetidosPorCol[indiceCol1]:
                    #Obtenemos su col de repetidos para este numero
                    colNumRepetido = [0] * individuo.size
                    for r,num in enumerate(columna):
                        if num == repetido:
                            colNumRepetido[r] = 1

                    flag = False
                    random.shuffle(columnas_disponibles)
                    for columnaAlternativa in columnas_disponibles:
                        if flag ==True:
                            break

                        indiceColAltern = columnas.index(columnaAlternativa)
                        repetidoColAlternativa = list(repetidos[indiceColAltern])
                        prohibidosColAlternativa = columnasAsociadas[indiceColAltern]

                        if repetido not in columnaAlternativa:
                            for r,row in enumerate(columna):
                                if colNumRepetido[r] == 1 and repetidoColAlternativa[r] == 1:
                                    #print(f"ambos tienen repetidos {r}")
                                    if columnasAsociadas[indiceCol1][r]==0 and prohibidosColAlternativa[r]==0:
                                        #print(f"No son prohibidos")
                                        if columnaAlternativa[r] not in columna:
                                            #print(f"otro {indiceCol1}:{indiceColAltern}:{r}")
                                            aux1 = columna[r] 
                                            aux2 = columnaAlternativa[r]
                                            columna[r] = aux2
                                            columnaAlternativa[r] = aux1
                                            #Se hizo un cambio
                                            flag = True

                        
                                            
                nuevasColumnas.append(columna) 

            for c,col in enumerate(nuevasColumnas):
                self.actualiza_columna(matrizCopia, col, c)
            individuo.matrix = matrizCopia

    #Checa si los numeros existen en ambos subblocks
    def checkNumbersInBothSubblocksNowFast(self, n1, n2, sub1, sub2, size):
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

    def subblockLocalSearch(self, population):
        for individuo in population:
            subblockList, associatedSubblockList, repeatedValuesSubblockList,valoresRepetidos = copy.deepcopy(individuo.getSubBlocks_wrong())

            newSubblocks = []
            for index,subblock in enumerate(subblockList):
                subblocksRestantes = [sub for sub in subblockList if sub != subblock]
                random.shuffle(subblocksRestantes)
                change = False

                for subblockAlterno in subblocksRestantes:
                    if change == True:
                            break
                    
                    indiceSBA = subblockList.index(subblockAlterno)
                    valorRepSubAlterno = valoresRepetidos[indiceSBA]

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
                                    if self.checkNumbersInBothSubblocksNowFast(num1, num2, subblock, subblockAlterno, individuo.subBlockSize):
                                        #print(f"===============SUBBLOCK EXCHANGE============")
                                        aux1 = actualRow[toChange]
                                        aux2 = actualRowAlterno[toChangeA] 
                                        actualRow[toChange] =  aux2 
                                        actualRowAlterno[toChangeA]  = aux1
                            
                                        change = True
                newSubblocks.append(subblock)
        
            individuo.updateMatrix(newSubblocks)
             
    def elitePopulationLearning(self, population, elitePopulation, board):
        elites = copy.deepcopy(elitePopulation)
        xrandom = random.choice(elites)
        xrandomFitness = xrandom.fitnessFunction()

        xworst = population[-1]
        maxfx = xworst.fitnessFunction()
        Pb = (maxfx-xrandomFitness)/maxfx
        rand = random.uniform(0,1)

        if rand < Pb:
            population[-1] = xrandom
            #print("reemplazado")
        else:
            nuevoIndividuo = Individuo.Individuo(board)
            nuevoIndividuo.initMatrix()
            population[-1] = nuevoIndividuo
            #print("nuevoIndividuo")

    def sortPopulation(self, population):
        fitnessEv = []
        for individuo in population:
            fitness = individuo.fitnessFunction()
            fitnessEv.append([individuo, fitness])
        fitnessEv.sort(key=lambda x: x[1], reverse=False)
        return [individuo for individuo, _ in fitnessEv]
    
    def sudoku_ga(self, board, populationSize, generaciones, pc1, pc2, pm1, pm2):
        population = self.population
        elitePopulation = self.elitePopulation
        val = generaciones
        iteraciones = []
        aptitud = []

        for _ in range(populationSize):
            instance = Individuo.Individuo(board)
            instance.initMatrix()
            population.append(instance)

        for i in range(generaciones):
            print(f"===GENERACION {i}===")

            population=self.sortPopulation(population)
            # CROSS OVER
            self.crossOver(pc1,pc2,population)
            # MUTACION
            self.mutation(pm1,pm2,population)
            population = self.sortPopulation(population)

            self.columnLocalSarch(population)

            self.subblockLocalSearch(population)

            population = self.sortPopulation(population)

            best = copy.deepcopy(population[0])
            self.updateElitePopulation(elitePopulation,best)

            #mostrarAptitudPoblacion(population,"Despues de actualizar elite")
            population = self.sortPopulation(population)
            #mostrarAptitudPoblacion(population,"Despues de actualizar learning")

            Gbest = elitePopulation[-1]

            #Graficas
            iteraciones.append(i)
            aptitud.append(copy.deepcopy(Gbest.fitnessFunction()))
            
            print(f"Best {Gbest.fitnessFunction()}")
            Gbest.showPuzzle(0)

            if Gbest.fitnessFunction() == 0: 
                val = i
                break

            self.elitePopulationLearning(population,elitePopulation, board)
            
        Gbest.showPuzzle(0)

            
        #return elitePopulation[-1].fitnessFunction(), val 
        return Gbest.matrix, elitePopulation[-1].fitnessFunction(), val

    def updateElitePopulation(self,elitePopulation, indvElite):
        if all(indvElite.fitnessFunction() < elite.fitnessFunction() for elite in elitePopulation):
            elitePopulation.append(indvElite)
            if len(elitePopulation)>=50:
                elitePopulation.pop(0)

    def mostrarPuzzles(self,population,str=''):
        print(f"Fitness poblacion {str}")
        for p in population:
            p.showPuzzle(0)
        print("\n")

    def mostrarAptitudPoblacion(self,population,str=''):
        print(f"Fitness poblacion {str}")
        for p in population:
            print(f"{p.fitnessFunction()}", end='  ')
        print("\n")

    def mostrarDirecciones(self,population,str=''):
        print(f"Direccion {str}")
        for p in population:
            print(f"{id(p)}", end='  ')
        print("\n")


