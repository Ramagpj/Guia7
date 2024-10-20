import numpy as np
import matplotlib.pyplot as plt
import time

# Iniciar el cronómetro
inicio = time.time()

# Definir la función objetivo
def funcion_objetivo(x):
    return -x * np.sin(np.sqrt(np.abs(x)))

# Parámetros del PSO
num_particulas = 30
dim = 1
limite_inf = -512
limite_sup = 512
num_iteraciones = 100

c1 = 1.5  # Término cognitivo
c2 = 1.5  # Término social

# Inicializar posiciones y velocidades aleatorias dentro del rango dado
posiciones = np.random.uniform(limite_inf, limite_sup, (num_particulas, dim))
velocidades = np.random.uniform(-5, 5, (num_particulas, dim))

# Inicializar las mejores posiciones personales y globales
mejor_pos_personal = np.copy(posiciones)
mejor_valor_personal = funcion_objetivo(posiciones)

# Inicializar el mejor valor global
mejor_valor_global = np.min(mejor_valor_personal)
mejor_pos_global = posiciones[np.argmin(mejor_valor_personal)]

# Lista para guardar el mejor valor global en cada iteración
mejores_valores_globales = []

# Ciclo principal del algoritmo de PSO
for iteracion in range(num_iteraciones):
    valor_actual = funcion_objetivo(posiciones)

    # Actualizar las mejores posiciones personales y sus valores
    for k in range(num_particulas):
        if valor_actual[k] < mejor_valor_personal[k]:  # Minimizar la función objetivo
            mejor_valor_personal[k] = valor_actual[k]  # Actualiza el mejor valor personal
            mejor_pos_personal[k] = posiciones[k]  # Actualiza la mejor posición personal

    # Actualizar la mejor posición global si se encuentra un mejor valor
    if np.min(mejor_valor_personal) < mejor_valor_global:
        mejor_valor_global = np.min(mejor_valor_personal)
        mejor_pos_global = posiciones[np.argmin(mejor_valor_personal)].copy()
       

    # Guardar el mejor valor global de esta iteración
    mejores_valores_globales.append(mejor_valor_global)

    # Generar coeficientes aleatorios r1 y r2 para cada partícula entre 0 y 1
    r1 = np.random.rand(num_particulas, dim)  # Término cognitivo
    r2 = np.random.rand(num_particulas, dim)  # Término social

    # Actualizar las velocidades de cada partícula
    velocidades = (velocidades +
                   c1 * r1 * (mejor_pos_personal - posiciones) +
                   c2 * r2 * (mejor_pos_global - posiciones))

    # Actualizar las posiciones de las partículas
    posiciones += velocidades

    # Restringir las posiciones dentro de los límites definidos
    posiciones = np.clip(posiciones, limite_inf, limite_sup)

    # Mostrar el progreso cada ciertas iteraciones
    if iteracion % 10 == 0:
        print(f"Iteración {iteracion}: Mejor valor global = {mejor_valor_global}")
        
 

# Al final, imprimir la mejor partícula encontrada y el valor de la función objetivo
print(f"Mejor posición global: {mejor_pos_global}")
print(f"Mejor valor global: {mejor_valor_global}")

# Generar un gráfico del mejor valor global a lo largo de las iteraciones
plt.figure()
plt.plot(mejores_valores_globales)
plt.title("Mejor valor global a lo largo de las iteraciones")
plt.xlabel("Iteraciones")
plt.ylabel("Mejor valor global")
plt.grid()
plt.show()

# Genera un rango de valores de -512 a 512 para graficar la función objetivo
x1 = np.linspace(-512, 512, 1000)  # Genera 1000 puntos en el rango
f1 = funcion_objetivo(x1)  # Evalúa la función objetivo en esos puntos

# Grafica la función objetivo para ver cómo se comporta
plt.figure()
plt.plot(x1, f1)
plt.title("Función objetivo")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.grid()
plt.show()

# Finalizar el cronómetro y mostrar el tiempo total de ejecución
fin = time.time()
print(f"Tiempo total de ejecución: {fin - inicio:.2f} segundos")
