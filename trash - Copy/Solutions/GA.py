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

    def indexAvailableToSwap(self, rowAsociada):    
        index = []
        for c,col in enumerate(rowAsociada):
            if col != 1:
                index.append(c)
        if len(index) >= 2:
            index1,index2 = random.sample(index, 2)
            return index1,index2
        else: return None, None
    
    def mutation(self, pm1, pm2, population):
        for individuo in population:
            matrix = individuo.matrix
            matrixAsociada = individuo.associatedMatrix

            for r,row in enumerate(matrix):
                rowAsociada = matrixAsociada[r]
                rand1 = random.uniform(0,1)
                rand2 = random.uniform(0,1)
                if rand1 < pm1:
                    idx1,idx2 = self.indexAvailableToSwap(rowAsociada)
                    if idx1!=None and idx2!=None:
                        temp = matrix[r][idx1]
                        matrix[r][idx1] = matrix[r][idx2]
                        matrix[r][idx2] = temp
                if rand2 < pm2:
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
                self.actualiza_columna(matrizCopia, col, c)
            #print("\n")

            #print("DESPEUS")
            individuo.matrix = matrizCopia
            #individuo.showPuzzle(0)


            #print("\n\n\n")

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
        subblock_mal = []

        for individuo in population:
            subblockList, associatedSubblockList, repeatedValuesSubblockList,valoresRepetidos = copy.deepcopy(individuo.getSubBlocks_wrong())
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
                                        if self.checkNumbersInBothSubblocksNowFast(num1, num2, subblock, subblockAlterno, individuo.subBlockSize):
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
             
    def elitePopulationLearning(self, population, elitePopulation):
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
        val = 1000

        for _ in range(populationSize):
            instance = Individuo.Individuo(board)
            instance.initMatrix()
            population.append(instance)

        for i in range(generaciones):
            # print(f"===GENERACION {i}===")

            population=self.sortPopulation(population)

            #mostrarAptitudPoblacion(elitePopulation,"ELITES")

            #mostrarAptitudPoblacion(population,"Inicio generacion")

            self.crossOver(pc1,pc2,population)

            #mostrarAptitudPoblacion(population,"despues de cross")

            self.mutation(pm1,pm2,population)
            population = self.sortPopulation(population)


            #mostrarAptitudPoblacion(population,"despues de mutation")

            self.columnLocalSarch(population)

            self.subblockLocalSearch(population)

            population = self.sortPopulation(population)


            best = copy.deepcopy(population[0])
            self.updateElitePopulation(elitePopulation,best)

            #mostrarAptitudPoblacion(population,"Despues de actualizar elite")
            population = self.sortPopulation(population)
            #elitePopulationLearning(population,copy.deepcopy(elitePopulation))
            
            #mostrarAptitudPoblacion(population,"Despues de actualizar learning")

            Gbest = elitePopulation[-1]
            # print(f"Best {Gbest.fitnessFunction()}")
            if Gbest.fitnessFunction() == 0: 
                val = i
                break
            #elitePopulationLearning(population,copy.deepcopy(elitePopulation))
            
        Gbest.showPuzzle(0)

            
        #return elitePopulation[-1].fitnessFunction(), val 
        return Gbest.matrix

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


