import random
import numpy as np
import copy
import Solutions.Individuo as Individuo
import matplotlib.pylab as plt

class GeneticAlgorithm:
    def __init__(self):
        self.population = [] #Vulgo
        self.elitePopulation = [] #Burguesía

    #Realiza el intercambio genético entre mismas filas de individuos sin alterar las posiciones dadas
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
    #Realiza la mutación a las filas del individuo (intercambio o reinicialización)
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

    #Recibe columnas para colocarlas en la matriz
    def actualiza_columna(self, matriz, nueva_columna, indice_columna):
        for i in range(len(matriz)):
            matriz[i][indice_columna] = nueva_columna[i]
        return matriz

    #Progresivamente convierte las columnas ilegales en legales mediante intercambio con columnas
    #que también son ilegales
    def columnLocalSarch(self, population):
        for individuo in population:
            columnasAsociadas = []
            columnas = []
            repetidos, repetidosPorCol = copy.deepcopy(individuo.getRepeatedColumns())
            nuevasColumnas = []
            matrizCopia = copy.deepcopy(individuo.matrix)
            matrizCopiaAsociada = copy.deepcopy(individuo.associatedMatrix)

            #Extrae las columnas del individuo
            for i in range(individuo.size):
                columnas.append( [row[i] for row in matrizCopia])
                associatedColumn = [row[i] for row in matrizCopiaAsociada]
                columnasAsociadas.append(associatedColumn)

            #itera sobre las columas del individuo
            for c,columna in enumerate(columnas):
                columnas_disponibles = [col for col in columnas if col != columna] #Las demás columnas
                indiceCol1 = columnas.index(columna)

                for repetido in repetidosPorCol[indiceCol1]:
                    colNumRepetido = [0] * individuo.size
                    for r,num in enumerate(columna):
                        if num == repetido:
                            colNumRepetido[r] = 1
                    flag = False
                    random.shuffle(columnas_disponibles)
                    #Itera sobre las demás columnas hasta hacer un cambio que haga legal a la columna actual vs col alterna
                    for columnaAlternativa in columnas_disponibles:
                        if flag ==True:
                            break
                        indiceColAltern = columnas.index(columnaAlternativa)
                        repetidoColAlternativa = list(repetidos[indiceColAltern])
                        prohibidosColAlternativa = columnasAsociadas[indiceColAltern]
                        if repetido not in columnaAlternativa: #Para evitar calculo redundante
                            for r,row in enumerate(columna):    
                                if colNumRepetido[r] == 1 and repetidoColAlternativa[r] == 1:#Hay repetidos en la misma col
                                    if columnasAsociadas[indiceCol1][r]==0 and prohibidosColAlternativa[r]==0:#NO son prohibidos
                                        if columnaAlternativa[r] not in columna: #Para evitar calculo redundante
                                            aux1 = columna[r] 
                                            aux2 = columnaAlternativa[r]
                                            columna[r] = aux2
                                            columnaAlternativa[r] = aux1
                                            flag = True
                #Agrega cambios
                nuevasColumnas.append(columna) 
            #Actualiza cambios sobre el individuo
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

    #Realiza emparejamiento con otros subbloques para hacer que los subbloques del individuo
    #para progresivamente hacer los subbloques validos y legales
    def subblockLocalSearch(self, population):
        for individuo in population:
            subblockList, associatedSubblockList, repeatedValuesSubblockList,_ = copy.deepcopy(individuo.getSubBlocks())
           
            newSubblocks = []
            for index,subblock in enumerate(subblockList):
                subblocksRestantes = [sub for sub in subblockList if sub != subblock]
                random.shuffle(subblocksRestantes)
                change = False
                if change == True:
                    break

                for subblockAlterno in subblocksRestantes:                   
                    indiceSBA = subblockList.index(subblockAlterno)
                    for r,row in enumerate(subblock):                     
                        if change == True:
                            break
                        actualRow = subblock[r]
                        actualRowAlterno = subblockAlterno[r]

                        prohibidos = copy.deepcopy(associatedSubblockList[index][r])
                        prohibidosAlterno = copy.deepcopy(associatedSubblockList[indiceSBA][r])

                        repetidos = repeatedValuesSubblockList[index][r]
                        repetidosAlterno = repeatedValuesSubblockList[indiceSBA][r]

                        if (1 in repetidos and 1 in repetidosAlterno):
                            indicesRepetidos = [idx for idx,value in enumerate(repetidos) if value==1]
                            indicesRepetidosA = [idx for idx,value in enumerate(repetidosAlterno) if value==1]

                            for toChange, toChangeA in zip(indicesRepetidos, indicesRepetidosA):
                                if prohibidos[toChange]==0 and prohibidosAlterno[toChangeA]==0:
                                    num1 = actualRow[toChange]
                                    num2 = actualRowAlterno[toChangeA]
                            
                                    if self.checkNumbersInBothSubblocksNowFast(num1, num2, subblock, subblockAlterno, individuo.subBlockSize):
                                        aux1 = actualRow[toChange]
                                        aux2 = actualRowAlterno[toChangeA] 
                                        actualRow[toChange] =  aux2 
                                        actualRowAlterno[toChangeA]  = aux1
                            
                                        change = True
                newSubblocks.append(subblock)
        
            individuo.updateMatrix(newSubblocks)
    
    #Selecciona el peor individuo de cada generación y se toma la decisión de sustituirlo por un elite
    #o crear un nuevo individuo para introducir diversidad
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
            #reemplazado por elite
        else:
            nuevoIndividuo = Individuo.Individuo(board)
            nuevoIndividuo.initMatrix()
            population[-1] = nuevoIndividuo
            #nuevoIndividuo

    #Ordena a la población de menor a mayor en aptitud
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

        #Inicialización de la población
        for _ in range(populationSize):
            instance = Individuo.Individuo(board)
            instance.initMatrix()
            population.append(instance)

        #La vida comienza a reproducirse sobre la computadora...
        #Proximamente la evolución hará que tengamos individuos peleando guerras...
        #Inician generaciones
        mejores = []
        peores = []
        promedios = []
        for i in range(generaciones):
            print(f"===GENERACION {i}===")
            #Se ordena la población
            population=self.sortPopulation(population)
            
            #Crossover
            self.crossOver(pc1,pc2,population)
            #self.mostrarPuzzles(population, "Despues de crossover")
            
            #Mutación
            self.mutation(pm1,pm2,population)
            #self.mostrarPuzzles(population, "Despues de mutacion")
            
            population = self.sortPopulation(population)

            #Busqueda local por columnas
            self.columnLocalSarch(population)
            #self.mostrarPuzzles(population, "Despues de column")

            #Busqueda local por subbloques
            self.subblockLocalSearch(population)
            #self.mostrarPuzzles(population, "Despues de subblock")

            population = self.sortPopulation(population)

            best = copy.deepcopy(population[0])
            self.updateElitePopulation(elitePopulation,best)
            #mostrarAptitudPoblacion(population,"Despues de actualizar elite")


            population = self.sortPopulation(population)
            

            Gbest = elitePopulation[-1]

            Lbest = population[0].fitnessFunction()
            mejores.append(Lbest)
            Lworst = population[-1].fitnessFunction()
            peores.append(Lworst)
            averange = self.sumAptitudes(population)/len(population)
            promedios.append(averange)

            print(f"Localbest {Lbest}")

            #Graficas
            iteraciones.append(i)
            aptitud.append(copy.deepcopy(Gbest.fitnessFunction()))
            
            print(f"Best {Gbest.fitnessFunction()}")

            if Gbest.fitnessFunction() == 0: 
                val = i
                break

  

            self.elitePopulationLearning(population,elitePopulation, board)
            
        Gbest.showPuzzle(0)
        #print(mejores)
        #print(peores)
        #print(promedios)

        self.grafica(mejores, peores, promedios, len(mejores))
        return Gbest.matrix, elitePopulation[-1].fitnessFunction(), val



    #FUNTIONES "UTILIDADES"

    def grafica(self, mejores, peores, promedio, generaciones):
        x = list(range(1, generaciones+1))

        plt.scatter(x, mejores, color='green', label='mejor')
        plt.plot(x, mejores, color='green')
        plt.scatter(x, peores, color='red', label='peor')
        plt.plot(x, peores, color='red')
        plt.scatter(x, promedio, color='blue', label='promedio')
        plt.plot(x, promedio, color='blue')
        plt.legend()
        plt.xlabel('Generaciones')
        plt.ylabel('Aptitud')
        plt.title("Grafica de convergencia")
        plt.show()

    #Actualiza el mejor de cada generacion si es que hay alguno mejor, con limite de 50 individuos elite
    def updateElitePopulation(self,elitePopulation, indvElite):
        if all(indvElite.fitnessFunction() < elite.fitnessFunction() for elite in elitePopulation):
            elitePopulation.append(indvElite)
            if len(elitePopulation)>=50:
                elitePopulation.pop(0)

    #muestra puzzles de la poblacion
    def mostrarPuzzles(self,population,str=''):
        print(f"Fitness poblacion {str}")
        for p in population:
            p.showPuzzle(0)
        print("\n")

    def sumAptitudes(self, population):
        sum = 0
        for indv in population:
            sum += indv.fitnessFunction()
        return sum

    #Muestra aptitud de la poblacion
    def mostrarAptitudPoblacion(self,population,str=''):
        print(f"Fitness poblacion {str}")
        for p in population:
            print(f"{p.fitnessFunction()}", end='  ')
        print("\n")

    #Muestra dicciones de memoria para checar individuos duplicados
    def mostrarDirecciones(self,population,str=''):
        print(f"Direccion {str}")
        for p in population:
            print(f"{id(p)}", end='  ')
        print("\n")


