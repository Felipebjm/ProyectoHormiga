<<<<<<< HEAD
import random
from Objeto_veneno import Veneno
from Objeto_azucar import Azucar
from Objeto_Vino import Vino
import Objeto_Laberinto as lb
import time

Alelos = {"arriba": [0, -1], 
          "abajo": [0, 1],
          "derecha": [1, 0],
          "izquierda": [-1, 0],
          "comer": "comer"}

alelos_keys = list(Alelos.keys())  # Para llamar a los alelos

veneno = Veneno()
azucar = Azucar(30)
vino = Vino(10)

class Hormiga:
    def __init__(self, posicion, posicion_final, salud, alcohol_lvl, puntos, adn, laberinto):
        if posicion is None:
            raise ValueError("La posición no puede ser None")  # Lanza un error si la posición es None
        self.posicion = posicion.copy()  # Inicializa la posición de la hormiga
        self.posicion_final = posicion_final
        self.salud = salud 
        self.alcohol_lvl = alcohol_lvl
        self.puntos = puntos 
        self.laberinto = laberinto  # Matriz del laberinto
        self.adn = adn
        # Inicialización de listas para registrar iteraciones
        self.generaciones = []       # Lista para almacenar el número de iteraciones
        self.puntos_iteracion = []    # Lista para almacenar los puntos por iteración
        self.tiempos_iteracion = []   # Lista para almacenar los tiempos por iteración

    def get_info(self):
        # Obtiene información básica de la hormiga
        return [self.posicion, self.salud, self.alcohol_lvl, self.puntos, self.adn]
    
    def add_pts(self, puntos):
        # Añade puntos a la hormiga
        self.puntos += puntos

    def mover(self, alelo):
        # Calcula nueva posición basada en el alelo
        nueva_pos = [
            self.posicion[0] + Alelos[alelo][0], 
            self.posicion[1] + Alelos[alelo][1]
        ]
        
        # Verifica límites del laberinto
        if (0 <= nueva_pos[0] < len(self.laberinto[0]) and 0 <= nueva_pos[1] < len(self.laberinto)):
            # Verifica si la nueva posición es una roca
            if self.laberinto[nueva_pos[1]][nueva_pos[0]] != "R":
                self.posicion = nueva_pos

                # Verifica si ha alcanzado la posición final
                if self.posicion == self.posicion_final:
                    print("La hormiga ha llegado a la posición final.")
                    return True

                # Detecta la presencia de un objeto en la nueva posición
                self.detectar_objeto()
            else:
                print("Topó con roca (-20 pts)")
                self.puntos -= 20
        else:
            print("Intentó salir de la frontera (-20 pts)")
            self.puntos -= 20

        return False  # No ha llegado aún a la posición final
            
    def detectar_objeto(self):
        # Detecta si hay un objeto en la posición actual sin consumirlo
        objeto = self.laberinto[self.posicion[1]][self.posicion[0]]
        
        if objeto == "VN":
            print("La hormiga ha ignorado al veneno")
        elif objeto == "A":
            print("La hormiga ha ignorado al azúcar")
        elif objeto == "V":
            print("La hormiga ha ignorado al vino")

    def comer(self):
        # Consume el objeto en la posición actual y actualiza la salud o los puntos
        casilla = self.laberinto[self.posicion[1]][self.posicion[0]]
        
        if casilla == "VN":
            self.salud += veneno.consumir()
            print("La hormiga ha consumido veneno (muere)")
        elif casilla == "A":
            puntos_azucar = azucar.consumir()
            self.puntos += puntos_azucar
            print(f"La hormiga ha consumido azúcar (+{puntos_azucar} pts)")
        elif casilla == "V":
            self.alcohol_lvl += vino.consumir()
            self.salud -= 10
            print("La hormiga ha consumido vino (-10 salud)")
        
        # Limpia la casilla tras consumir el objeto
        self.laberinto[self.posicion[1]][self.posicion[0]] = None  # Vacía la posición actual
        
    def change_adn(self, pos, valor):
        # Cambia un alelo en el ADN
        print(f"Sin cambio {self.adn}")
        self.adn[pos] = valor
        print("Cambia ADN")
        print(f"Sí cambió {self.adn}")
        
    def modifica_salud(self):
        # Modifica la salud de acuerdo al objeto actual en la posición
        casilla = self.laberinto[self.posicion[1]][self.posicion[0]]
        if casilla == "VN":
            pass  # Veneno reduce salud
        if casilla == "V":
            pass  # Alcohol reduce salud

    def fitness(self):
        # Calcula el fitness de acuerdo a la cercanía a la posición final
        return abs(self.posicion_final[0] - self.posicion[0]) + abs(self.posicion_final[1] - self.posicion[1])

    def muta(self): 
        # Aplica mutación al ADN con probabilidad
        for i in range(len(self.adn)):
            muta = random.randint(0, 1)
            if muta == 1:
                new_adn = random.choice(alelos_keys)
                print(f"La hormiga ha mutado y cambió {self.adn[i]} por {new_adn}")
                self.adn[i] = new_adn
        
        # Agrega un nuevo alelo con baja probabilidad
        for alelo in range(len(self.adn)):
            muta = random.randint(0, 20)
            if muta == 20:
                print("La hormiga ha mutado y obtuvo un alelo")
                self.adn.append(random.choice(alelos_keys))

    def registrar_iteracion(self, numero_iteracion):
        # Inicio de la medición del tiempo
        inicio = time.time()
        
        # Ejemplo de una simulación de iteración del algoritmo genético
        # Aquí puedes agregar la lógica de mutación o de movimiento si es necesario
        # Para este ejemplo solo añadimos puntos de manera simulada
        puntos_actuales = self.puntos + numero_iteracion * 10  # Ejemplo de puntos generados en esta iteración
        self.puntos_iteracion.append(puntos_actuales)
        
        # Fin de la iteración y cálculo del tiempo
        tiempo_iteracion = time.time() - inicio
        self.tiempos_iteracion.append(tiempo_iteracion)
        
        # Registro de la generación actual
        self.generaciones.append(numero_iteracion)
        
        print(f"Iteración {numero_iteracion}: Puntos = {puntos_actuales}, Tiempo = {tiempo_iteracion:.4f} segundos")

    def obtener_datos(self):
        return self.generaciones, self.puntos_iteracion, self.tiempos_iteracion


=======
import random
from Objeto_veneno import Veneno
from Objeto_azucar import Azucar
from Objeto_Vino import Vino
import Objeto_Laberinto as lb
import time

Alelos = {"arriba": [0, -1], 
          "abajo": [0, 1],
          "derecha": [1, 0],
          "izquierda": [-1, 0],
          "comer": "comer"}

alelos_keys = list(Alelos.keys())  # Para llamar a los alelos

veneno = Veneno()
azucar = Azucar(30)
vino = Vino(10)

class Hormiga:
    def __init__(self, posicion, posicion_final, salud, alcohol_lvl, puntos, adn, laberinto):
        if posicion is None:
            raise ValueError("La posición no puede ser None")  # Lanza un error si la posición es None
        self.posicion = posicion # Inicializa la posición de la hormiga
        self.posicion_final = posicion_final
        self.salud = salud 
        self.alcohol_lvl = alcohol_lvl
        self.puntos = puntos 
        self.laberinto = laberinto  # Matriz del laberinto
        self.adn = adn
        # Inicialización de listas para registrar iteraciones
        self.generaciones = []       # Lista para almacenar el número de iteraciones
        self.puntos_iteracion = []    # Lista para almacenar los puntos por iteración
        self.tiempos_iteracion = []   # Lista para almacenar los tiempos por iteración

    def get_info(self):
        # Obtiene información básica de la hormiga
        return [self.posicion, self.salud, self.alcohol_lvl, self.puntos, self.adn]
    
    def add_pts(self, puntos):
        # Añade puntos a la hormiga
        self.puntos += puntos

    def mover(self, alelo):
        # Calcula nueva posición basada en el alelo
        nueva_pos = [
            self.posicion[0] + Alelos[alelo][0], 
            self.posicion[1] + Alelos[alelo][1]
        ]
        
        # Verifica límites del laberinto
        if (0 <= nueva_pos[0] < len(self.laberinto[0]) and 0 <= nueva_pos[1] < len(self.laberinto)):
            # Verifica si la nueva posición es una roca
            if self.laberinto[nueva_pos[1]][nueva_pos[0]] != "R":
                self.posicion = nueva_pos

                # Verifica si ha alcanzado la posición final
                if self.posicion == self.posicion_final:
                    print("La hormiga ha llegado a la posición final.")
                    return True

                # Detecta la presencia de un objeto en la nueva posición
                self.detectar_objeto()
            else:
                print("Topó con roca (-20 pts)")
                self.puntos -= 20
        else:
            print("Intentó salir de la frontera (-20 pts)")
            self.puntos -= 20

        return False  # No ha llegado aún a la posición final
            
    def detectar_objeto(self):
        # Detecta si hay un objeto en la posición actual sin consumirlo
        objeto = self.laberinto[self.posicion[1]][self.posicion[0]]
        
        if objeto == "VN":
            print("La hormiga ha ignorado al veneno")
        elif objeto == "A":
            print("La hormiga ha ignorado al azúcar")
        elif objeto == "V":
            print("La hormiga ha ignorado al vino")

    def comer(self):
        # Consume el objeto en la posición actual y actualiza la salud o los puntos
        casilla = self.laberinto[self.posicion[1]][self.posicion[0]]
        
        if casilla == "VN":
            self.salud += veneno.consumir()
            print("La hormiga ha consumido veneno (muere)")
        elif casilla == "A":
            puntos_azucar = azucar.consumir()
            self.puntos += puntos_azucar
            print(f"La hormiga ha consumido azúcar (+{puntos_azucar} pts)")
        elif casilla == "V":
            self.alcohol_lvl += vino.consumir()
            self.salud -= 10
            print("La hormiga ha consumido vino (-10 salud)")
        
        # Limpia la casilla tras consumir el objeto
        self.laberinto[self.posicion[1]][self.posicion[0]] = None  # Vacía la posición actual
        
    def change_adn(self, pos, valor):
        # Cambia un alelo en el ADN
        print(f"Sin cambio {self.adn}")
        self.adn[pos] = valor
        print("Cambia ADN")
        print(f"Sí cambió {self.adn}")
        
    def modifica_salud(self):
        # Modifica la salud de acuerdo al objeto actual en la posición
        casilla = self.laberinto[self.posicion[1]][self.posicion[0]]
        if casilla == "VN":
            pass  # Veneno reduce salud
        if casilla == "V":
            pass  # Alcohol reduce salud

    def fitness(self):
        # Calcula el fitness de acuerdo a la cercanía a la posición final
        return abs(self.posicion_final[0] - self.posicion[0]) + abs(self.posicion_final[1] - self.posicion[1])

    def muta(self): 
        # Aplica mutación al ADN con probabilidad
        for i in range(len(self.adn)):
            muta = random.randint(0, 1)
            if muta == 1:
                new_adn = random.choice(alelos_keys)
                print(f"La hormiga ha mutado y cambió {self.adn[i]} por {new_adn}")
                self.adn[i] = new_adn
        
        # Agrega un nuevo alelo con baja probabilidad
        for alelo in range(len(self.adn)):
            muta = random.randint(0, 20)
            if muta == 20:
                print("La hormiga ha mutado y obtuvo un alelo")
                self.adn.append(random.choice(alelos_keys))

    def registrar_iteracion(self, numero_iteracion):
        # Inicio de la medición del tiempo
        inicio = time.time()
        
        # Ejemplo de una simulación de iteración del algoritmo genético
        # Aquí puedes agregar la lógica de mutación o de movimiento si es necesario
        # Para este ejemplo solo añadimos puntos de manera simulada
        puntos_actuales = self.puntos + numero_iteracion * 10  # Ejemplo de puntos generados en esta iteración
        self.puntos_iteracion.append(puntos_actuales)
        
        # Fin de la iteración y cálculo del tiempo
        tiempo_iteracion = time.time() - inicio
        self.tiempos_iteracion.append(tiempo_iteracion)
        
        # Registro de la generación actual
        self.generaciones.append(numero_iteracion)
        
        print(f"Iteración {numero_iteracion}: Puntos = {puntos_actuales}, Tiempo = {tiempo_iteracion:.4f} segundos")

    def obtener_datos(self):
        return self.generaciones, self.puntos_iteracion, self.tiempos_iteracion


>>>>>>> 9d1494c (Actualizacion 12:27)
