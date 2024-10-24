import numpy as np  

# Cargar la matriz de distancias desde el archivo gr17.csv
def cargar_matriz_distancias(archivo):
    return np.loadtxt(archivo, delimiter=',', dtype=int)


# Parámetros del problema
n_hormigas = 100  # Número de hormigas
archivo_distancias = 'gr17.csv' 
matriz_distancias = cargar_matriz_distancias(archivo_distancias)  # Cargar la matriz de distancias

n_ciudades = matriz_distancias.shape[0]  # Obtener el número de ciudades desde la matriz de distancias

# Parámetros del algoritmo de optimización
alpha = 1.0  # Parámetro de control: atención a la fermona
beta =  1.5   # Parámetro de control: atención a la distancia

tasa_evaporacion = 0.5  # Tasa de evaporación de fermona
Q = 10  # Cantidad de feromona máxima a depositar en cada conexión
fermonas = np.random.uniform(0, Q, size=(n_ciudades, n_ciudades))  # Inicializar la matriz de feromonas

# Inicializar el array de hormigas, donde están la cantidad de hormigas y la ciudad que visitó
hormigas = np.full((n_hormigas, n_ciudades), -1)  # Crear un array donde cada hormiga puede visitar todas las ciudades
longitudes = np.full(n_hormigas,-1)


# # Inicializar cada hormiga en la ciudad de origen, ciudad 0 o hormiguero
# for k in range(n_hormigas):
#     hormigas[k, 0] = 0  # Todas las hormigas comienzan en la ciudad 0

mejor_recorrido = None  # Variable para almacenar el mejor recorrido encontrado
mejor_longitud = float('inf')  # Inicializa la mejor longitud como infinito

iteracion = 0  # Contador para las iteraciones del bucle
max_iteraciones=1000 # Establecer un número máximo de iteraciones 
condicion=True


while condicion:
    print(f"Iteración {iteracion + 1}")  # Imprimir el número de la iteración actual
    iteracion += 1  # Incrementar el contador de iteraciones

    # Iterar sobre todas las hormigas
    for k in range(n_hormigas):
        # Inicializar la trayectoria de la hormiga k
        recorrido = [0]  # Lista para almacenar las ciudades visitadas (comienza en la ciudad 0)
        ciudad_actual = 0  # Comenzamos en la ciudad de origen

        # Repetir hasta que todas las ciudades hayan sido visitadas
        while len(recorrido) < n_ciudades:
            # Calcular las probabilidades para las ciudades vecinas
            probabilidades = np.zeros(n_ciudades)  # Vector para almacenar las probabilidades

            # Identificar los nodos vecinos (ciudades no visitadas)
           # Inicializar una lista vacía para los nodos vecinos
            nodos_vecinos = []
            # Recorrer todas las ciudades para identificar cuáles no han sido visitadas
            for i in range(n_ciudades):
                if i not in recorrido:  # Si la ciudad no fue visitada, se agrega a nodos_vecinos
                    nodos_vecinos.append(i)
            
            #J me da el valor de la ciudad, y se calcula las probabilidades para moverse a las ciudades vecinas
            for j in nodos_vecinos:
                probabilidad_ij = (fermonas[ciudad_actual, j] ** alpha) * ((1 / matriz_distancias[ciudad_actual, j]) ** beta)
                probabilidades[j] = probabilidad_ij
            
            # Sumar todas las probabilidades de los nodos vecinos
            suma_probabilidades = np.sum(probabilidades[nodos_vecinos])
            
            # L = me da el valor de la ciudad
            for l in nodos_vecinos:  # Iterar sobre los nodos vecinos
                probabilidades[l] /= suma_probabilidades  # Normalizar la probabilidad de cada nodo
            
           
            siguiente_ciudad = np.random.choice(nodos_vecinos, p=probabilidades[nodos_vecinos]) 
        
            recorrido.append(siguiente_ciudad)  # Agregar la ciudad seleccionada al recorrido
            ciudad_actual = siguiente_ciudad  # Actualizar la ciudad actual

        # Almacenar el recorrido final de la hormiga k
        hormigas[k] = recorrido

        # Calcular la longitud del camino
      # Calcular la longitud del camino usando un bucle for
        longitud_camino = 0  # Inicializar la longitud del camino
        for i in range(len(recorrido) - 1):
            ciudad_actual = recorrido[i]
            siguiente_ciudad = recorrido[i + 1]
            longitud_camino += matriz_distancias[ciudad_actual, siguiente_ciudad]  # Sumar la distancia entre ciudades
            
        # Agregar la distancia de regreso al origen
        longitud_camino += matriz_distancias[recorrido[-1], recorrido[0]]  # Sumar la distancia de regreso a la ciudad inicial
        
        longitudes[k]=longitud_camino

        # Comparar y actualizar el mejor recorrido
        if longitud_camino < mejor_longitud:  
            mejor_longitud = longitud_camino  # Actualizar la mejor longitud
            mejor_recorrido = recorrido.copy()  # Hacer una copia del recorrido para guardar el mejor

    # Evaporación de Feromonas
    fermonas =fermonas* (1 - tasa_evaporacion)  # Aplicar la evaporación de feromonas

    # Inicializar la matriz de cambio de feromonas
    cambio_fermonas = np.zeros((n_ciudades, n_ciudades))  
        
    # Depositar feromona en el recorrido de cada hormiga
    for k in range(n_hormigas):
        recorrido = hormigas[k]
        
        for i in range(len(recorrido) - 1):
            ciudad_actual = recorrido[i]
            siguiente_ciudad = recorrido[i + 1]
            #cambio_fermonas[ciudad_actual, siguiente_ciudad] += Q / longitudes[k] # Global
            #cambio_fermonas[ciudad_actual, siguiente_ciudad] += Q  # Uniforme
            cambio_fermonas[ciudad_actual, siguiente_ciudad] += Q / matriz_distancias[ciudad_actual, siguiente_ciudad]  # Local

    # Actualización de Feromonas
    fermonas += cambio_fermonas  # Actualizar la matriz de feromonas con el depósito acumulado
   
   
   
    # Verificar condiciones de salida, es decir hasta que todos los vectores sean todos iguales o sea que todas las hormigas siguen el mismo camino o hasta max iteraciones
    if (len(np.unique(hormigas, axis=0)) <= 1) or (iteracion >= max_iteraciones):
        condicion=False
    
    print("Mejor recorrido encontrado:", mejor_recorrido)  # Imprimir el mejor recorrido encontrado
    print("Longitud del mejor recorrido:", mejor_longitud)  # Imprimir la longitud del mejor recorrido

# Mostrar el mejor recorrido encontrado
print(" ")
print(" ------------------------ ")
print("Cantidad de hormigas: ", n_hormigas)
print("Cambio feromona tipo:", "LOCAL")
print("Mejor recorrido encontrado:", mejor_recorrido)  # Imprimir el mejor recorrido encontrado
print("Longitud del mejor recorrido:", mejor_longitud)  # Imprimir la longitud del mejor recorrido
print("Alpha:", alpha)
print("Beta:", beta)
print("Tasa de evaporación:", tasa_evaporacion)
