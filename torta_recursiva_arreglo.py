# Implementación usando Minimax y Memoización con ARREGLOS (Matriz)

import sys
from typing import List, Tuple

# Aumentar límite de recursión
sys.setrecursionlimit(5000)

def suma_segmento_pref(prefijos: List[int], i: int, j: int) -> int:
    if i > j: return 0
    return prefijos[j + 1] - prefijos[i]

def dp_segmento_arr(i: int, j: int, memo_arr: List[List[int]], torta: List[int], prefijos: List[int]) -> int:

 
    if memo_arr[i][j] > -10**18:
        return memo_arr[i][j]

    # 2. Caso Base
    if i == j:
        return torta[i]

    # 3. Recurrencia Minimax
    # Opción A: Comer izquierda
    total_restante_A = suma_segmento_pref(prefijos, i + 1, j)
    oponente_A = dp_segmento_arr(i + 1, j, memo_arr, torta, prefijos)
    ganancia_A = torta[i] + (total_restante_A - oponente_A)

    # Opción B: Comer derecha
    total_restante_B = suma_segmento_pref(prefijos, i, j - 1)
    oponente_B = dp_segmento_arr(i, j - 1, memo_arr, torta, prefijos)
    ganancia_B = torta[j] + (total_restante_B - oponente_B)

    mejor_opcion = max(ganancia_A, ganancia_B)

    # 4. Guardar en Matriz
    memo_arr[i][j] = mejor_opcion
    return mejor_opcion

def max_satisfaccion_arreglo(torta: List[int]) -> Tuple[int, int]:
    """
    Implementación usando Minimax y Memoización con ARREGLOS (Matriz).
    """
    total_porciones = len(torta)

    if total_porciones % 2 != 0:
        raise ValueError(f"Error: El arreglo debe ser par")

    mitad_porciones = total_porciones // 2
    torta_extendida = torta * 2

    # Sumas prefijas
    prefijos = [0] * (len(torta_extendida) + 1)
    for k in range(len(torta_extendida)):
        prefijos[k+1] = prefijos[k] + torta_extendida[k]

    # Inicializar Matriz de Memoización
    largo_memo = 2 * total_porciones
    valor_inicial_memo = -10**19
    memo_arr = [[valor_inicial_memo] * largo_memo for _ in range(largo_memo)]

    mayor_satisfaccion = valor_inicial_memo
    mejor_inicio = -1

    for i in range(total_porciones):
        # Profesor come semicírculo inicial
        ganancia_inicial_prof = suma_segmento_pref(prefijos, i, i + mitad_porciones - 1)

        # Resto del juego
        ini_segmento_resto = i + mitad_porciones
        fin_resto = i + total_porciones - 1

        total_resto = suma_segmento_pref(prefijos, ini_segmento_resto, fin_resto)

        val_hermana = dp_segmento_arr(ini_segmento_resto, fin_resto, memo_arr, torta_extendida, prefijos)

        val_profesor_resto = total_resto - val_hermana
        ganancia_prof_total = ganancia_inicial_prof + val_profesor_resto

        if ganancia_prof_total > mayor_satisfaccion:
            mayor_satisfaccion = ganancia_prof_total
            mejor_inicio = i

    return mayor_satisfaccion, mejor_inicio % total_porciones

if __name__ == "__main__":
    s = [1, 100, 1, 1, 1, 100]
    resultado = max_satisfaccion_arreglo(s)
    print("Versión con ARREGLO (Minimax)")
    print("Máxima satisfacción:", resultado[0])
    print("Inicio del mejor semicirculo:", resultado[1])