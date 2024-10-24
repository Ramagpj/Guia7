import numpy as np
import matplotlib.pyplot as plt
import time

# Iniciar el cronómetro
inicio = time.time()

# Definir la función objetivo
def funcion_objetivo(x):
    return -x * np.sin(np.sqrt(np.abs(x)))

# Parámetros -----------ENJAMBRE MEJOR GLOBAL
num_particulas = 1000
#Dimension que usamos
dim = 1


limite_inf = -512
limite_sup = 512
num_iteraciones = 1000

c1 = 1.5   #Influencia personal
c2 = 1.5   #Influencia grupo

# Inicializar posiciones y velocidades aleatorias dentro del rango dado
posiciones = np.random.uniform(limite_inf, limite_sup, (num_particulas, dim))

#No se entre cuanto y cuanto tiene que ir las velocidades, probe varios valores y siempre andaba. Supongo que inicia en cero
velocidades = np.random.uniform(0,0, (num_particulas, dim))

# Inicializar las mejores posiciones personales y globales
mejor_pos_personal = np.copy(posiciones)
mejor_valor_personal = funcion_objetivo(posiciones)

# Inicializar el mejor valor global
mejor_valor_global = np.min(mejor_valor_personal)
mejor_pos_global = posiciones[np.argmin(mejor_valor_personal)]

# Lista para guardar el mejor valor global en cada iteración y hacer el grafico despues
mejores_valores_globales = []

# Ciclo principal del algoritmo de 
for iteracion in range(num_iteraciones):
   
    valor_actual = funcion_objetivo(posiciones)

    # Actualizar las mejores posiciones personales y sus valores de cada particula
    for k in range(num_particulas):
        if valor_actual[k] < mejor_valor_personal[k]:  # Minimizar la función objetivo
            mejor_valor_personal[k] = valor_actual[k]  # Actualiza el mejor valor personal
            mejor_pos_personal[k] = posiciones[k]  # Actualiza la mejor posición personal

    # Actualizar la mejor posición global si se encuentra un mejor valor
    if np.min(mejor_valor_personal) < mejor_valor_global:
        mejor_valor_global = np.min(mejor_valor_personal)
        #Use .copy porque a veces no me lo cargaba
        mejor_pos_global = posiciones[np.argmin(mejor_valor_personal)].copy()
       

    # Guardar el mejor valor global de esta iteración para ver como evoluciona con las iteraciones
    mejores_valores_globales.append(mejor_valor_global)

    # Generar coeficientes aleatorios r1 y r2 para cada partícula entre 0 y 1. Son los valores aleatorios que te sirve para explorar todo
    r1 = np.random.rand(num_particulas, dim)  
    r2 = np.random.rand(num_particulas, dim)  



    for k in range(num_particulas):
         # Actualizar el vector de velocidades de cada partícula
        velocidades[k] = (velocidades[k] +
                    c1 * r1[k] * (mejor_pos_personal[k] - posiciones[k]) +
                    c2 * r2[k] * (mejor_pos_global - posiciones[k]))
        # Actualizar las posiciones de las partículas
        posiciones[k]+=velocidades[k]
        # Restringir las posiciones dentro de los límites definidos
        posiciones[k] = np.clip(posiciones[k], limite_inf, limite_sup)

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

