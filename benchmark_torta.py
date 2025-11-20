import random
import time
from statistics import mean

# IMPORTA TUS FUNCIONES
from torta_hash import max_satisfaccion_hash as resolver_profesor_hash
from torta_recursiva_arreglo import max_satisfaccion_arreglo as resolver_profesor_arreglo

# CONFIGURACIÓN DEL EXPERIMENTO
valores_n = [20, 40, 60, 80, 100, 120]
repeticiones = 5

def generar_instancia(n):
    # Crea un arreglo de largo 2n con valores entre -10 y 10
    return [random.randint(-10, 10) for _ in range(2*n)]

def medir_tiempo(funcion, s):
    tiempos = []
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        funcion(s)
        fin = time.perf_counter()
        tiempos.append((fin - inicio) * 1000)  # ms
    return mean(tiempos)

print("n | Arreglo(ms) | Hash(ms)")
print("-----------------------------")

resultados = []

for n in valores_n:
    s = generar_instancia(n)
    t_arr = medir_tiempo(resolver_profesor_arreglo, s)
    t_hash = medir_tiempo(resolver_profesor_hash, s)
    resultados.append((n, t_arr, t_hash))
    print(f"{n} | {t_arr:.2f} | {t_hash:.2f}")

# Guarda en CSV si quieres
with open("resultados_torta.csv", "w") as f:
    f.write("n, arreglo_ms, hash_ms\n")
    for n, a, h in resultados:
        f.write(f"{n}, {a:.4f}, {h:.4f}\n")

print("\nDatos exportados a resultados_torta.csv")
