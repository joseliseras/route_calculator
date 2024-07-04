import heapq


class Mapa:
    def __init__(self, size): 
        self.size = size
        self.mapa = [[0 for _ in range(size)] for _ in range(size)]
        self.simbolo = {
            0: '.',  # camino
            1: 'E',  # edificio
            2: 'A',  # agua
            3: 'T'   # bloqueo temporal
        }
        self.tipos_nombres = {
            1: "EDIFICIO",
            2: "AGUA",
            3: "BLOQUEO TEMPORAL"
        }
        
    def agregar_obstaculo(self, cordenada_x, cordenada_y, tipo):
        if 0 <= cordenada_x < self.size and 0 <= cordenada_y < self.size:
            self.mapa[cordenada_x][cordenada_y] = tipo
            tipo_nombre = self.tipos_nombres.get(tipo, "desconocido")
            print(f"Ha agregado el obstáculo {tipo_nombre} en las coordenadas x:{cordenada_x} y:{cordenada_y}")
        else:
            print('No se pudo agregar obstáculo, porque está fuera del mapa')

    def agregar_obstaculo_usuario(self):
        while True:
            try:
                print("AGREGUE OBSTACULOS - Al finalizar presione la tecla 's' para salir.")
                cordenada_x = input("Ingrese la coordenada x, o presione la techa 's' para salir: ")
                if cordenada_x.lower() == "s":
                    return
                cordenada_x = int(cordenada_x)

                cordenada_y = input("Ingrese la coordenada y, o presione la techa 's' para salir: ")
                if cordenada_y.lower() == "s":
                    return
                cordenada_y = int(cordenada_y)

                tipo = input("Ingrese el tipo de obstáculo (Edificio = 1, Agua = 2, Bloqueo Temporal = 3), o presione la tecla 's' para salir): ")
                if tipo.lower() == "s":
                    return
                tipo = int(tipo)

                if tipo not in [1, 2, 3]:
                    print("Tipo de Obstáculo inválido. Intente nuevamente.")
                    continue

                self.agregar_obstaculo(cordenada_x, cordenada_y, tipo)

            except ValueError:
                print("Entrada inválida. Ingrese un número entero.")

            except IndexError:
                print("La coordenada ingresada está fuera del mapa, ingrese de nuevo.")

            self.imprimir_mapa()

    def imprimir_mapa(self, inicio=None, objetivo=None, ruta=None):
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) == inicio:
                    print('I', end=' ')
                elif (i, j) == objetivo:
                    print('O', end=' ')
                elif ruta and (i, j) in ruta:
                    print('*', end=' ')
                else:
                    print(self.simbolo[self.mapa[i][j]] if self.mapa[i][j] in self.simbolo else self.mapa[i][j], end=' ')
            print()

    def distancia_manhattan(self, a, b):
        return abs(b[0] - a[0]) + abs(b[1] - a[1])

    def obtener_vecinos(self, nodo):
        x, y = nodo
        vecinos = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Solo 4 direcciones
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                vecinos.append((nx, ny))
        return vecinos

    def costo_movimiento(self, hasta):
        tipo_celda = self.mapa[hasta[0]][hasta[1]]
        if tipo_celda in [1, 3]:  # Edificio o Bloqueo temporal
            return float('inf')
        elif tipo_celda == 2:  # Agua
            return 5
        else:  # Camino normal
            return 1

    def buscar_ruta_mas_corta(self, inicio, objetivo):
        abiertos = []
        cerrados = set()
        g_scores = {inicio: 0}
        f_scores = {inicio: self.distancia_manhattan(inicio, objetivo)}
        padres = {}

        heapq.heappush(abiertos, (f_scores[inicio], inicio))

        while abiertos:
            _, actual = heapq.heappop(abiertos)

            if actual == objetivo:
                ruta = []
                while actual in padres:
                    ruta.append(actual)
                    actual = padres[actual]
                ruta.append(inicio)
                return ruta[::-1]

            cerrados.add(actual)

            for vecino in self.obtener_vecinos(actual):
                if vecino in cerrados:
                    continue

                costo = self.costo_movimiento(vecino)
                if costo == float('inf'):
                    continue  # Saltamos los obstáculos infranqueables

                tentativo_g = g_scores[actual] + costo

                if vecino not in g_scores or tentativo_g < g_scores[vecino]:
                    padres[vecino] = actual
                    g_scores[vecino] = tentativo_g
                    f_scores[vecino] = g_scores[vecino] + self.distancia_manhattan(vecino, objetivo)
                    if vecino not in [i[1] for i in abiertos]:
                        heapq.heappush(abiertos, (f_scores[vecino], vecino))

        return None  # No se encontró ruta
    

# Uso del programa
if __name__ == "__main__":
    size = 8
    mapa = Mapa(size)

    # Agregar obstáculos desde input hasta que el usuario decida salir
    mapa.agregar_obstaculo_usuario()

    print("SU MAPA ES:")
    mapa.imprimir_mapa()

    # Definir puntos de inicio y objetivo
    while True:
        try:
            inicio_x = input("Ingrese la coordenada x del punto de inicio: ")
            inicio_y = input("Ingrese la coordenada y del punto de inicio: ")
            objetivo_x = input("Ingrese la coordenada x del punto objetivo: ")
            objetivo_y = input("Ingrese la coordenada y del punto objetivo: ")

            inicio = (int(inicio_x), int(inicio_y))
            objetivo = (int(objetivo_x), int(objetivo_y))

            if not (0 <= inicio[0] < size and 0 <= inicio[1] < size):
                print("El punto de inicio está fuera del mapa. Inténtelo de nuevo.")
                continue

            if not (0 <= objetivo[0] < size and 0 <= objetivo[1] < size):
                print("El punto objetivo está fuera del mapa. Inténtelo de nuevo.")
                continue

            break
        except ValueError:
            print("Entrada inválida. Ingrese un número entero.")

    # Buscar la ruta más corta usando A*
    ruta_mas_corta = mapa.buscar_ruta_mas_corta(inicio, objetivo)

    # Imprimir mapa con la ruta marcada
    if ruta_mas_corta:
        print("\nMAPA CON RECORRIDO FINAL:")
        mapa.imprimir_mapa(inicio, objetivo, ruta_mas_corta)
    else:
        print("No se encontró una ruta válida.")