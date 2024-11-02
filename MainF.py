import Objeto_Laberinto as lb
import Hormiga as h
import random

# Función para encontrar la posición de un elemento en la matriz del laberinto
def encontrar_pos(matriz, elemento):
    for fila in range(len(matriz)):
        for columna in range(len(matriz[fila])):
            if matriz[fila][columna] == elemento:
                return [columna, fila]  # posición del elemento en formato [x, y]

# Condiciones de inicio y configuración del laberinto y la población de hormigas
if __name__ == "__main__":
    # Crear la ventana principal y el laberinto
    root = lb.tk.Tk()
    laberinto = lb.Laberinto(root)

    # Obtener la matriz del laberinto para buscar posiciones
    matriz_laberinto = laberinto.obtener_matriz()  #Llama un meto del objeto laberinto

    # Encontrar posiciones de inicio y salida
    start = encontrar_pos(matriz_laberinto, "s")
    exit = encontrar_pos(matriz_laberinto, "e")

    # Crear el ADN inicial para las hormigas
    adn_i_1 = [random.choice(h.alelos_keys)]
    adn_i_2 = [random.choice(h.alelos_keys)]
    end_position = (10, 10)  # O cualquier posición final deseada

    # Crear la población inicial de hormigas
    Poblacion = [h.Hormiga(start,end_position, 100, 0, 0, adn_i_1, laberinto), 
                 h.Hormiga(start,end_position, 100, 0, 0, adn_i_2, laberinto)]

    # Ejecutar la ventana principal del laberinto
    root.after(1000, lambda: algoritmo_genetico(Poblacion))  # Ejecuta el algoritmo después de 1 segundo
    root.mainloop()

# Función para el cruce de ADN entre dos hormigas
def cruce(adn1, adn2):
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

    return h.Hormiga(start, 100, 0, 0, adn_hijo, laberinto)

# Algoritmo genético para evolucionar la población
def algoritmo_genetico(Poblacion):
    for hormiga in Poblacion:
        adn = hormiga.get_info()[4]
        for alelo in adn:
            if alelo != "comer":
                pre_fitness = hormiga.fitness()
                hormiga.mover(alelo)
                post_fitness = hormiga.fitness()
                fitness_impact = 20 if post_fitness <= pre_fitness else -30
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

# Función para guardar los puntajes en un archivo de texto
def guardar_puntajes(Poblacion):
    with open("puntajes-hormiga.txt", "a") as text:
        for hormiga in Poblacion:
            text.write(f"HORMIGA_SALUD:{hormiga.get_info()[1]}_ALCOHOL:{hormiga.get_info()[2]}_PUNTOS:{hormiga.get_info()[3]}_ADN:{hormiga.get_info()[4]}\n")



    


