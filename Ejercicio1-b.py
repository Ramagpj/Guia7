import numpy as np
import matplotlib.pyplot as plt
import time

# Iniciar el cronómetro
inicio = time.time()

# Definir la función objetivo
def funcion_objetivo(x, y):
    return (x**2 + y**2)**0.25 * np.sin(np.square(np.sqrt(x**2 + y**2)))

# Parámetros -----------ENJAMBRE MEJOR GLOBAL
num_particulas = 1000
dim = 2  # Dimensiones (x, y)
limite_inf = -100
limite_sup = 100
num_iteraciones = 1000
 
c1 = 1.5   #Influencia personal
c2 = 1.5  #Influencia grupo

# Inicializar posiciones y velocidades aleatorias dentro del rango dado
posiciones = np.random.uniform(limite_inf, limite_sup, (num_particulas, dim))

#No se entre cuanto y cuanto tiene que ir las velocidades, probe varios valores y siempre andaba. Supongo que inicia en cero
velocidades = np.random.uniform(0,0, (num_particulas, dim))

# Inicializar las mejores posiciones personales y globales
mejor_pos_personal = np.copy(posiciones)
mejor_valor_personal = funcion_objetivo(posiciones[:, 0], posiciones[:, 1])

# Inicializar el mejor valor global
mejor_valor_global = np.min(mejor_valor_personal)
                    #Obtener el indice del mejor_valor_global, y con eso tenes que posicion es
mejor_pos_global = posiciones[np.argmin(mejor_valor_personal)].copy()  

# Lista para guardar el mejor valor global en cada iteración
mejores_valores_globales = []

# Ciclo principal del algoritmo de PSO
for iteracion in range(num_iteraciones):
    valor_actual = funcion_objetivo(posiciones[:, 0], posiciones[:, 1])

    # Actualizar las mejores posiciones personales y sus valores
    for k in range(num_particulas):
        if valor_actual[k] < mejor_valor_personal[k]: 
            mejor_valor_personal[k] = valor_actual[k] 
            mejor_pos_personal[k] = posiciones[k].copy() 

    # Actualizar la mejor posición global si se encuentra un mejor valor en las particulas
    minimo_particulas=np.min(mejor_valor_personal)
    if minimo_particulas < mejor_valor_global:
        mejor_valor_global = minimo_particulas
        mejor_pos_global = posiciones[np.argmin(mejor_valor_personal)].copy()  # Asegurarse de que se haga una copia

    # Guardar el mejor valor global de esta iteración
    mejores_valores_globales.append(mejor_valor_global)

    # Generar coeficientes aleatorios r1 y r2 para cada partícula entre 0 y 1
    r1 = np.random.rand(num_particulas, dim) 
    r2 = np.random.rand(num_particulas, dim)  

    # Actualizar las velocidades de cada partícula
    

    for k in range(num_particulas):
        velocidades[k] = (velocidades[k] +
                          c1 * r1[k] * (mejor_pos_personal[k] - posiciones[k]) +
                          c2 * r2[k] * (mejor_pos_global - posiciones[k]))
        # Actualizar las posiciones de las partículas
        posiciones[k]+=velocidades[k]
        # Restringir las posiciones dentro de los límites definidos
        posiciones[k] = np.clip(posiciones[k], limite_inf, limite_sup)
    # Mostrar el progreso cada ciertas iteraciones
    if iteracion % 10 == 0:
        print(f"Iteración {iteracion}: Mejor valor global = {mejor_valor_global}, Mejor posición global = [{mejor_pos_global[0]}, {mejor_pos_global[1]} ] ")

# Al final, imprimir la mejor partícula encontrada y el valor de la función objetivo
print(f"Mejor posición global: [{mejor_pos_global[0]}, {mejor_pos_global[1]} ]")
print(f"Mejor valor global: {mejor_valor_global}")

# Generar un gráfico del mejor valor global a lo largo de las iteraciones
plt.figure()
plt.plot(mejores_valores_globales)
plt.title("Mejor valor global a lo largo de las iteraciones")
plt.xlabel("Iteraciones")
plt.ylabel("Mejor valor global")
plt.grid()
plt.show()



# Finalizar el cronómetro y mostrar el tiempo total de ejecución
fin = time.time()
print(f"Tiempo total de ejecución: {fin - inicio:.2f} segundos")

