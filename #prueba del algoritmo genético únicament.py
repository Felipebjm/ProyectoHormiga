#prueba del algoritmo genético únicamente:

import Objeto_Laberinto as lb
import Hormiga as h
import random
import tkinter as tk

"""root = tk.Tk()
# Suponiendo que Laberinto también necesita ser inicializado
laberinto = lb.Laberinto(root)  # Inicializa el laberinto de acuerdo a tu implementación""" #aquí lo estás llamando dos veces
#una en if main y otra aquí, esta no funciona porque el mainloop es una función aparte

start = []  # define la variable global del incio
exit = [] #define la variab le global de la salida


# ADN de ejemplo
adn_i_1 = [random.choice(h.alelos_keys)]
adn_i_2 = [random.choice(h.alelos_keys)]

Poblacion = []

# Función para encontrar la posición de un elemento en la matriz del laberinto
def encontrar_pos(matriz, elemento):
    for fila in range(len(matriz)):
        for columna in range(len(matriz[fila])):
            if matriz[fila][columna] == elemento:
                return [columna, fila]  # posición del elemento en formato [x, y]


# Algoritmo genético para evolucionar la población
def algoritmo_genetico(Poblacion, laberinto):
    for hormiga in Poblacion:
        adn = hormiga.get_info()[4]
        for alelo in adn:
            if alelo != "comer":
                pre_fitness = hormiga.fitness()
                hormiga.mover(alelo)
                post_fitness = hormiga.fitness()
                fitness_impact = 20 if post_fitness < pre_fitness else -30
                hormiga.add_pts(fitness_impact)
            else:
                hormiga.comer()
                if hormiga.get_info()[1] <= 0:
                    print("La hormiga ha muerto :(")
                    Poblacion.remove(hormiga)
                    break

        if hormiga.get_info()[1] > 0:
            fitness = hormiga.fitness()
            points = 100 if fitness == 0 else -5 * fitness
            hormiga.add_pts(points)
            print("Hormiga resultados:", hormiga.get_info())

    # Guardar resultados de la población actual en el archivo de puntajes
    guardar_puntajes(Poblacion)
    

#Función para encontrar los datos de un txt
#Para este algoritmo en específico, si es ADN, entonces lo convierte en matriz
def encuentre_datos(linea, etiqueta):
    
    inicio = linea.find(etiqueta)
    inicio += len(etiqueta) 

    final = linea.find("_", inicio)

    if etiqueta == "ADN:": 
        dato = linea[inicio:final].strip()  # Eliminar espacios en blanco

        if dato.startswith("[") and dato.endswith("]"): # Si el dato está en formato de lista, convertirlo en una lista
            
            dato = dato[1:-1].replace("'", "").strip()
            return [d.strip() for d in dato.split(",")]  # Devolver una lista de alelos
        else:
            return [dato]  # Retornar como lista de un solo elemento
    

    return linea[inicio:final]  #si no es ADN, retorna string, pues lo que se escribe es str           

# Función para guardar los puntajes en un archivo de texto
def guardar_puntajes(Poblacion):
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

def validar_y_comenzar(laberinto):
    global Poblacion, start, exit
    
    matriz_laberinto = laberinto
    start = encontrar_pos(matriz_laberinto, "H")
    exit = encontrar_pos(matriz_laberinto, "F")

    if start is None or exit is None:
        # If start or exit is undefined, check again after a short delay
        validar_y_comenzar(laberinto)
    else:
        # Both start and end positions are defined, so we can initialize the population
        print("Posiciones de inicio y fin definidas. Comenzando el algoritmo...")
        
        # Create initial DNA for ants
        adn_i_1 = [random.choice(h.alelos_keys)]
        adn_i_2 = [random.choice(h.alelos_keys)]

        # Initialize the population with ants
        if not Poblacion: 
            Poblacion = [
                h.Hormiga(start, exit, 100, 0, 0, adn_i_1, laberinto),
                h.Hormiga(start, exit, 100, 0, 0, adn_i_2, laberinto)
            ]

        # Start the genetic algorithm after 1 second
        algoritmo_genetico(Poblacion, laberinto)
        se_cruzan()

# Función para el cruce de ADN entre dos hormigas
def cruce(adn1, adn2):
    global start, exit
    adn_hijo = []
    for i in range(max(len(adn1), len(adn2))):
        mutacion = random.randint(0, 3)
        if mutacion == 1 and i < len(adn1):
            adn_hijo.append(adn1[i])
            if random.choice([True, False]) and i < len(adn2):
                adn_hijo.append(adn2[i])
        elif mutacion == 2 and i < len(adn2):
            adn_hijo.append(adn2[i])
            if random.choice([True, False]) and i < len(adn1):
                adn_hijo.append(adn1[i])

    return h.Hormiga(start, exit, 100, 0, 0, adn_hijo, laberinto)

def se_cruzan (): 

    global Poblacion

    with open("puntajes-hormiga.txt", "r") as text:
        lines = text.readlines()
        #Selección

    ### Aquí evalua si se pueden cruzar

    if not lines: #Si las líneas son nulas, no hay hormigas
        print("no hay hormigas, vamos a meter dos más")
        Poblacion = [h.Hormiga(start, exit, 100, 0, 0, [random.choice(h.alelos_keys)], laberinto), h.Hormiga(start, exit, 100, 0, 0, [random.choice(h.alelos_keys)], laberinto)]

    elif len(lines) == 1: # Si las líenas son una, significa solo hay una hormiga
        print("solo queda una hormiga, vamos a meter una más")
        Poblacion = [h.Hormiga(start, exit, 100, 0, 0, [random.choice(h.alelos_keys)], laberinto)] #modifica la población para que
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

# Condiciones de inicio y configuración del laberinto y la población de hormigas
laberinto = [["H","",""],["","",""],["","","F"]]
def comienza():
    global laberinto
    with open("puntajes-hormiga.txt", "w") as text: #borra todo para comenzar
        pass
    
    while True:
        laberinto = [["H","",""],["","",""],["","","F"]]
        validar_y_comenzar(laberinto)
        option= input("input: ")
        if option == "s":
            break
        
    

comienza()


    


