import Objeto_Laberinto as lb
import Hormiga as h
import random

if __name__ == "__main__":
    root = lb.tk.Tk()
    laberinto = lb.Laberinto(root)
    root.mainloop()


###

def encontrar_pos(matriz, elemento):

    for fila in range(len(matriz)):
        for columna in range(len(matriz[fila])):
            if matriz[fila][columna] == elemento:
                return [columna, fila] #posición del elemento en la fila, es basicamente para el inicio  [x,y]
            
### Condiciones de inicio
            
start = encontrar_pos(laberinto, "s")
exit = encontrar_pos(laberinto, "e")

adn_i_1 = [random.choice(h.alelos_keys)]
adn_i_2 = [random.choice(h.alelos_keys)]

Poblacion = [h.Hormiga(start, 100, 0, 0, adn_i_1, laberinto), h.Hormiga(start, 100, 0, 0, adn_i_2, laberinto)]

#Cruce de los adn 

def cruce(adn1, adn2):

    print(f"Inicio de cruce: {start}")
    if not adn1 or not adn2:
        return []
    adn_hijo = []
    
    for i in range(max(len(adn1), len(adn2))):
        mutacion = random.randint(0,3)
        if mutacion == 1: #si es 1 toma el alelo de padre 1
            if i < len(adn1):
                adn_hijo.append(adn1[i])

                if random.choice([True, False]): #si es true también toma el alelo de padre 2
                    if i < len(adn2):
                        adn_hijo.append(adn2[i])

        elif mutacion==2: #si es dos toma el alelo de padre 2
            if i < len(adn2):
                adn_hijo.append(adn2[i])

                if random.choice([True, False]): #si es True también toma el alelo de padre 1
                    if i < len(adn1):
                        adn_hijo.append(adn1[i])
        
        #si es 3, nada pasa, o sea no toma ningún alelo


    
    

    print(type(adn_hijo))
    hormiga_hija = h.Hormiga(start, 100, 0, 0, adn_hijo, laberinto) 
    return hormiga_hija #Retorna a la hormiga hija

### Encuentra los datos de una linea en un TXT (si la linea es "ADN:" retorna una lista con los alelos)

def encuentre_datos(linea, etiqueta):
    
    inicio = linea.find(etiqueta)
    inicio += len(etiqueta) 

    final = linea.find("_", inicio)

    if etiqueta == "ADN:": #Esto porque ADN siempre es una lista y para efectos de este código ponerlo aparte es muy útil
        dato = linea[inicio:final].strip()  # Eliminar espacios en blanco

        if dato.startswith("[") and dato.endswith("]"): # Si el dato está en formato de lista, convertirlo en una lista
            
            dato = dato[1:-1].replace("'", "").strip()
            return [d.strip() for d in dato.split(",")]  # Devolver una lista de alelos
        else:
            return [dato]  # Retornar como lista de un solo elemento
    

    return linea[inicio:final]  #si no es ADN, retorna string, pues lo que se escribe es str            


#Algoritmo genético 


def algoritmo_genetico(): #corre el algoritmo genetico

    global Poblacion    
        
    for hormiga in Poblacion: #Para cada hormiga en la población
        
        adn = hormiga.get_info()[4] 
        

        for alelo in adn: #Para cada alelo que esté en el adn de las hormigas de la población

            
            if alelo != "comer":
                
                pre_fitness = hormiga.fitness()

                hormiga.mover(alelo) #cambia los atributos del objeto

                #### Aquí creo que ponemos la unión

                post_fitness = hormiga.fitness()

                if post_fitness <= pre_fitness:
                    print("La hormiga hizo un movimiento óptimo (+20 pts)")
                    hormiga.add_pts(20)
                else:
                    print("La hormiga hizo un movimiento NO óptimo (-30 pts)")
                    hormiga.add_pts(-30)
            else:

                hormiga.comer()

                ###Aquí ponemos la otra unión

                salud = hormiga.get_info()[1]

                if salud <= 0:
                    print("La hormiga ha muerto :(")
                    break

       
                    
        salud = hormiga.get_info()[1] 

        if salud > 0: #Evalua si la hormiga está muerta
            fitness = hormiga.fitness()

            

            if fitness == 0:
                hormiga.add_pts(100)
                print("la hormiga ha llegado a la meta")
                
            else:
                hormiga.add_pts(-5*fitness)
                print(f"la hormiga quedó a una distancia relativa de {fitness} ({-5*fitness}pts)")
                
            print("Hormiga resultados:", hormiga.get_info())

        else:

            Poblacion.remove(hormiga) #si está muerta la quita de la población

    if Poblacion: #evalua si hay hormiga en la población
        for hormiga in Poblacion: #para meterlas despues de modificarlas (evalua su puntaje)

            with open("puntajes-hormiga.txt", "r") as text:

                lines = text.readlines()
                
                if not lines: #si no hay nada
                    lines = []
                    
                        
                    lines.append(f"HORMIGA:1_SALUD:{hormiga.get_info()[1]}_ALCOHOL:{hormiga.get_info()[2]}_PUNTOS:{hormiga.get_info()[3]}_ADN:{hormiga.get_info()[4]}_" + "\n")
                    
                
                elif len(lines) == 1:
                    puntos = int(encuentre_datos(lines[0], "PUNTOS:"))
                    if hormiga.get_info()[3] > puntos:
                        lines.append(f"HORMIGA:2_SALUD:{encuentre_datos(lines[0], "SALUD:")}_ALCOHOL:{encuentre_datos(lines[0], "ALCOHOL:")}_PUNTOS:{encuentre_datos(lines[0], "PUNTOS:")}_ADN:{encuentre_datos(lines[0], "ADN:")}_" + "\n")
                        lines[0] = f"HORMIGA:1_SALUD:{hormiga.get_info()[1]}_ALCOHOL:{hormiga.get_info()[2]}_PUNTOS:{hormiga.get_info()[3]}_ADN:{hormiga.get_info()[4]}_" + "\n"
                    else:
                        lines.append(f"HORMIGA:2_SALUD:{hormiga.get_info()[1]}_ALCOHOL:{hormiga.get_info()[2]}_PUNTOS:{hormiga.get_info()[3]}_ADN:{hormiga.get_info()[4]}_" + "\n")

                elif len(lines) == 2:
                    puntos_hormiga = hormiga.get_info()[3]
                    puntos_linea_1 = int(encuentre_datos(lines[0], "PUNTOS:"))
                    puntos_linea_2 = int(encuentre_datos(lines[1], "PUNTOS:"))

                    if puntos_hormiga > puntos_linea_1:
                        linea1 = lines[0]
                        linea2 = lines[1]
                        
                        lines[0] = lines[0].replace(f"{linea1.split('HORMIGA:1_')[1]}", f"SALUD:{hormiga.get_info()[1]}_ALCOHOL:{hormiga.get_info()[2]}_PUNTOS:{hormiga.get_info()[3]}_ADN:{hormiga.get_info()[4]}_" + "\n")
                        lines[1] = lines[1].replace(f"{linea2.split('HORMIGA:2_')[1]}", f"SALUD:{encuentre_datos(linea1, "SALUD:")}_ALCOHOL:{encuentre_datos(linea1, "ALCOHOL:")}_PUNTOS:{encuentre_datos(linea1, "PUNTOS:")}_ADN:{encuentre_datos(linea1, "ADN:")}_" + "\n")
                        lines.append(f"HORMIGA:3_SALUD:{encuentre_datos(linea2, "SALUD:")}_ALCOHOL:{encuentre_datos(linea2, "ALCOHOL:")}_PUNTOS:{encuentre_datos(linea2, "PUNTOS:")}_ADN:{encuentre_datos(linea2, "ADN:")}_" + "\n")
                    elif puntos_hormiga > puntos_linea_2:
                        linea2 = lines[1]
        
                        lines[1] = lines[1].replace(f"{linea2.split('HORMIGA:2_')[1]}", f"SALUD:{hormiga.get_info()[1]}_ALCOHOL:{hormiga.get_info()[2]}_PUNTOS:{hormiga.get_info()[3]}_ADN:{hormiga.get_info()[4]}_" + "\n")
                        lines.append(f"HORMIGA:3_SALUD:{encuentre_datos(linea2, "SALUD:")}_ALCOHOL:{encuentre_datos(linea2, "ALCOHOL:")}_PUNTOS:{encuentre_datos(linea2, "PUNTOS:")}_ADN:{encuentre_datos(linea2, "ADN:")}_" + "\n")

                    else:
                        lines.append(f"HORMIGA:3_SALUD:{hormiga.get_info()[1]}_ALCOHOL:{hormiga.get_info()[2]}_PUNTOS:{hormiga.get_info()[3]}_ADN:{hormiga.get_info()[4]}_" + "\n")
                else:

                    puntos_hormiga = hormiga.get_info()[3]
                    puntos_linea_1 = int(encuentre_datos(lines[0], "PUNTOS:"))
                    puntos_linea_2 = int(encuentre_datos(lines[1], "PUNTOS:"))
                    puntos_linea_3 = int(encuentre_datos(lines[2], "PUNTOS:"))

                    if puntos_hormiga > puntos_linea_1:
                        linea1 = lines[0]
                        linea2 = lines[1]
                        linea3 = lines[2]

                        lines[0] = lines[0].replace(f"{linea1.split('HORMIGA:1_')[1]}", f"SALUD:{hormiga.get_info()[1]}_ALCOHOL:{hormiga.get_info()[2]}_PUNTOS:{hormiga.get_info()[3]}_ADN:{hormiga.get_info()[4]}_" + "\n")
                        lines[1] = lines[1].replace(f"{linea2.split('HORMIGA:2_')[1]}", f"SALUD:{encuentre_datos(linea1, "SALUD:")}_ALCOHOL:{encuentre_datos(linea1, "ALCOHOL:")}_PUNTOS:{encuentre_datos(linea1, "PUNTOS:")}_ADN:{encuentre_datos(linea1, "ADN:")}_" + "\n")
                        lines[2] = lines[2].replace(f"{linea3.split('HORMIGA:3_')[1]}", 
                                            f"SALUD:{encuentre_datos(linea2, "SALUD:")}_ALCOHOL:{encuentre_datos(linea2, "ALCOHOL:")}_PUNTOS:{encuentre_datos(linea2, "PUNTOS:")}_ADN:{encuentre_datos(linea2, "ADN:")}_" + "\n")
                    elif puntos_hormiga > puntos_linea_2:
                        linea2 = lines[1]
                        linea3 = lines[2]
        
                    
                        lines[1] = lines[1].replace(f"{linea2.split('HORMIGA:2_')[1]}", f"SALUD:{hormiga.get_info()[1]}_ALCOHOL:{hormiga.get_info()[2]}_PUNTOS:{hormiga.get_info()[3]}_ADN:{hormiga.get_info()[4]}_" + "\n")
                        lines[2] = lines[2].replace(f"{linea3.split('HORMIGA:3_')[1]}", 
                                            f"SALUD:{encuentre_datos(linea2, "SALUD:")}_ALCOHOL:{encuentre_datos(linea2, "ALCOHOL:")}_PUNTOS:{encuentre_datos(linea2, "PUNTOS:")}_ADN:{encuentre_datos(linea2, "ADN:")}_" + "\n")
                    elif puntos_hormiga > puntos_linea_3:
                        linea3 = lines[2]
                        lines[2] = lines[2].replace(f"{linea3.split('HORMIGA:3_')[1]}", 
                                            f"SALUD:{hormiga.get_info()[1]}_ALCOHOL:{hormiga.get_info()[2]}_PUNTOS:{hormiga.get_info()[3]}_ADN:{hormiga.get_info()[4]}_" + "\n")     

                    else:
                        print("la hormiga no entra en el top 3")

        with open("puntajes-hormiga.txt", "w") as text: 
            text.writelines(lines)  


### Cruza a las dos mejores (encuentra los datos en el txt y llama a cruze)

def se_cruzan (): 

    global Poblacion

    with open("puntajes-hormiga.txt", "r") as text:
        lines = text.readlines()
        #Selección

    ### Aquí evalua si se pueden cruzar

    if not lines: #Si las líneas son nulas, no hay hormigas
        print("no hay hormigas, vamos a meter dos más")
        Poblacion = [h.Hormiga(start, 100, 0, 0, [random.choice(h.alelos_keys)]), h.Hormiga(start, 100, 0, 0, [random.choice(h.alelos_keys)])]

    elif len(lines) == 1: # Si las líenas son una, significa solo hay una hormiga
        print("solo queda una hormiga, vamos a meter una más")
        Poblacion = [h.Hormiga(start, 100, 0, 0, [random.choice(h.alelos_keys)])] #modifica la población para que
                                                                                # El while corra a las nuevas hormigas
                                                                                # y las viejas se quedan en el txt
    
    else:
        
        adnh1 = encuentre_datos(lines[0], "ADN:")
        adnh2 = encuentre_datos(lines[1], "ADN:")

        #cruzamiento            
        hormiga_hija = cruce(adnh1, adnh2)

        hormiga_hija.muta()

        print("Hormiga Hija:", hormiga_hija.get_info())

        Poblacion = [hormiga_hija] #esta lista se modifica para que tenga sentido en el código, pues evalua las hormigas in Poblacion

def intento():

    global Poblacion

    with open("puntajes-hormiga.txt", "w") as text: #borra todo para comenzar
        pass

    gen = 1

    while True:


        gen+=1
        if Poblacion: #Esto es solo para evitar errores de que la lista de población esté vacía

            algoritmo_genetico()
            se_cruzan() #si hay población, se cruzan

        else:

            print("no hay hormigas, vamos a meter dos más")
            Poblacion = [h.Hormiga(start, 100, 0, 0, [random.choice(h.alelos_keys)]), h.Hormiga(start, 100, 0, 0, [random.choice(h.alelos_keys)])]
            #Si no, agrega dos hormigas

        with open("puntajes-hormiga.txt", "r") as text:
            lines = text.readlines()
            if lines:
                if int(encuentre_datos(lines[0], "PUNTOS:")) >= 180:
                    break
        #option = input("<s> para salir, <any oter key> para la siguiente simulación")
        #esto for debbug, pero ya después lo quitamos
        #if option == "s":
            #break

    print(f"Numero de generaciones: {gen}")


    


