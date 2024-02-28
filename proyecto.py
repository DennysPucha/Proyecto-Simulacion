import random
import matplotlib.pyplot as plt
from tabulate import tabulate

def punto(x, y):
    return (x, y)

def generar_comidas(num_comidas):
    comidas = set()
    while len(comidas) < num_comidas:
        x = random.randint(1, 9)
        y = random.randint(1, 9)
        comidas.add((x, y))
    return list(comidas)

def numeros_controlados(n, comidas, punto_inicio):
    suma_acumulativa = [punto_inicio]
    contador_pasos = 0  # Inicializar el contador de pasos

    while contador_pasos < n:  # Limitar la ejecución al número de pasos especificado
        current_x, current_y = suma_acumulativa[-1]

        allowed_directions = []

        if current_x < 9 and (current_x + 1, current_y) not in suma_acumulativa:
            allowed_directions.append((1, 0))
        if current_x > 1 and (current_x - 1, current_y) not in suma_acumulativa:
            allowed_directions.append((-1, 0))
        if current_y < 9 and (current_x, current_y + 1) not in suma_acumulativa:
            allowed_directions.append((0, 1))
        if current_y > 1 and (current_x, current_y - 1) not in suma_acumulativa:
            allowed_directions.append((0, -1))

        if not allowed_directions:
            break

        nuevo_numero = random.choice(allowed_directions)

        nueva_suma = (
            suma_acumulativa[-1][0] + nuevo_numero[0],
            suma_acumulativa[-1][1] + nuevo_numero[1],
        )

        nueva_suma = tuple(max(1, min(9, val)) for val in nueva_suma)

        suma_acumulativa.append(nueva_suma)
        contador_pasos += 1  # Incrementar el contador de pasos

        if nueva_suma in comidas:
            comidas.remove(nueva_suma)
            # Verificar si se superó el límite de pasos debido a la obtención de comidas adicionales
            if contador_pasos > 15:
                break
            # Añadir 5 pasos adicionales
            for _ in range(5):
                nuevo_numero = random.choice(allowed_directions)
                nueva_suma = (
                    nueva_suma[0] + nuevo_numero[0],
                    nueva_suma[1] + nuevo_numero[1],
                )
                nueva_suma = tuple(max(1, min(9, val)) for val in nueva_suma)
                suma_acumulativa.append(nueva_suma)

    return suma_acumulativa, len(suma_acumulativa) - 1, contador_pasos  # Retornar la cantidad de pasos y el contador de pasos

# MAIN
n = int(input("Ingrese el número de pasos para el borracho: "))
m = int(input("Ingrese el número de borrachos: "))
num_comidas = int(input("Ingrese el número de comidas: "))

comidas = generar_comidas(num_comidas)
comidas_originales = comidas.copy()

caminos = []
for _ in range(m): #NUMERO DE BORRACHOS
    punto_inicio = punto(random.randint(1, 9), random.randint(1, 9))
    camino, pasos, contador_pasos = numeros_controlados(n, comidas, punto_inicio)
    vivio_mas_15 = "Sí" if contador_pasos > 15 else "No"
    print(f"Camino: {pasos} pasos - ¿Vivió más de 15 pasos?: {vivio_mas_15}")
    caminos.append(camino)

# Imprimir tabla con información de los caminos
tabla = [["Camino", "Número de Pasos", "¿Sigue despierto?"]]
for i, (camino, pasos, contador_pasos) in enumerate(zip(caminos, [len(c) - 1 for c in caminos], [contador_pasos for _ in range(m)]), start=1):
    sigue_despierto = "Sí" if pasos > 15 else "No"
    tabla.append([i, pasos, sigue_despierto])
print(tabulate(tabla, headers="firstrow"))

# Graficar las comidas
for comida in comidas_originales:
    plt.scatter(*comida, color='green', marker='o')
    

# Graficar los caminos paso a paso
for i in range(max([len(camino) for camino in caminos])):
    for camino, contador_pasos in zip(caminos, [contador_pasos for _ in range(m)]):
        color = plt.cm.viridis(contador_pasos)  # Color basado en el contador de pasos
        if i < len(camino):
            plt.plot(*zip(*camino[:i+1]), color=color)
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.pause(1)

plt.show()
