#prueba del algoritmo genético únicamente:

import Objeto_Laberinto as lb
import Hormiga as h
import random
import tkinter as tk
import time

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
                move = hormiga.mover(alelo)
                post_fitness = hormiga.fitness()
                fitness_impact = 20 if post_fitness < pre_fitness else -30
                hormiga.add_pts(fitness_impact)
                if move == True:
                    return True

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


def validar_y_comenzar(laberinto_obj):
    global Poblacion, start, exit, laberinto
    
    matriz_laberinto = laberinto
    start = encontrar_pos(matriz_laberinto, "H")
    exit = encontrar_pos(matriz_laberinto, "F")

    if start is None or exit is None:
        print("Defina las posiciones de inicio y fin en el laberinto.")
        return
    else:
        print("Posiciones de inicio y fin definidas. Comenzando el algoritmo...")

        adn_i_1 = [random.choice(h.alelos_keys)]
        adn_i_2 = [random.choice(h.alelos_keys)]

        if not Poblacion:
            Poblacion.extend([
                h.Hormiga(start, exit, 100, 0, 0, adn_i_1, laberinto_obj),
                h.Hormiga(start, exit, 100, 0, 0, adn_i_2, laberinto_obj)
            ])

        ejecutar_algoritmo_genetico(laberinto_obj)

def ejecutar_algoritmo_genetico(laberinto_obj):
    global Poblacion, gen
    
    
    laberinto_obj.restaurar_laberinto()
    a = algoritmo_genetico(Poblacion, laberinto_obj)
    if a == True:
        print("LLEGÓ AL FINAL YEI")
        return
    se_cruzan(laberinto_obj)
    gen += 1

    # Programar la siguiente generación después de un breve retraso
    laberinto_obj.root.after(300, lambda: ejecutar_algoritmo_genetico(laberinto_obj))
    

# Función para el cruce de ADN entre dos hormigas

def cruce(adn1, adn2, laberinto_obj):
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

    return h.Hormiga(start, exit, 100, 0, 0, adn_hijo, laberinto_obj)

def se_cruzan(laberinto_obj):
    global Poblacion

    with open("puntajes-hormiga.txt", "r") as text:
        lines = text.readlines()

    if not lines:
        print("No hay hormigas, vamos a agregar dos más")
        Poblacion = [
            h.Hormiga(start, exit, 100, 0, 0, [random.choice(h.alelos_keys)], laberinto_obj),
            h.Hormiga(start, exit, 100, 0, 0, [random.choice(h.alelos_keys)], laberinto_obj)
        ]
    elif len(lines) == 1:
        print("Solo queda una hormiga, vamos a agregar una más")
        Poblacion = [
            h.Hormiga(start, exit, 100, 0, 0, [random.choice(h.alelos_keys)], laberinto_obj)
        ]
    else:
        adnh1 = encuentre_datos(lines[0], "ADN:")
        adnh2 = encuentre_datos(lines[1], "ADN:")

        hormiga_hija = cruce(adnh1, adnh2, laberinto_obj)
        hormiga_hija.muta()
        print("Hormiga Hija:", hormiga_hija.get_info())

        Poblacion = [hormiga_hija]

def iniciar_algoritmo_genetico(matriz_laberinto, laberinto_obj):
    global Poblacion, start, exit, laberinto, gen
    laberinto = matriz_laberinto
    gen = 1
    Poblacion = []

    with open("puntajes-hormiga.txt", "w") as text:
        pass
    laberinto_obj.restaurar_laberinto()
    validar_y_comenzar(laberinto_obj)
    


if __name__ == "__main__":
    import tkinter as tk
    from Objeto_Laberinto import Laberinto

    # Crear la ventana principal de Tkinter
    root = tk.Tk()

    # Crear una instancia del laberinto
    laberinto_obj = Laberinto(root)

    # Iniciar el loop de Tkinter
    root.mainloop()

    


