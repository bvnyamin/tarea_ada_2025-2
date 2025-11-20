#Implementación usando Minimax y Memoización con HASH (Diccionario)

import sys
from typing import List, Tuple, Dict

# Aumentamos el límite de recursión para evitar errores en casos grandes
sys.setrecursionlimit(5000)

def obtener_suma(prefijos: List[int], i: int, j: int) -> int:
    """Devuelve la suma del segmento s[i...j] en tiempo O(1)."""
    if i > j: return 0
    return prefijos[j + 1] - prefijos[i]

def resolver_minimax(i: int, j: int, memo_hash: Dict, torta: List[int], prefijos: List[int]) -> int:
    """
    Función recursiva (DP) que calcula cuánto puede garantizarse el jugador
    que tiene el turno actual, dado el segmento s[i...j].
    """
  
    if (i, j) in memo_hash:
        return memo_hash[(i, j)]

    # 2. Caso Base: Queda una sola porción
    if i == j:
        return torta[i]

    # 3. Recurrencia (Minimax)
    # El jugador actual quiere maximizar su ganancia.


    # Opción A: Comer izquierda (i)
    total_restante_A = obtener_suma(prefijos, i + 1, j)
    oponente_A = resolver_minimax(i + 1, j, memo_hash, torta, prefijos)
    ganancia_A = torta[i] + (total_restante_A - oponente_A)

    # Opción B: Comer derecha (j)
    total_restante_B = obtener_suma(prefijos, i, j - 1)
    oponente_B = resolver_minimax(i, j - 1, memo_hash, torta, prefijos)
    ganancia_B = torta[j] + (total_restante_B - oponente_B)

    # Elegir la mejor opción
    resultado = max(ganancia_A, ganancia_B)

    # 4. Guardar en Memoización
    memo_hash[(i, j)] = resultado
    return resultado

def max_satisfaccion_hash(s: List[int]) -> Tuple[int, int]:
    """
    Implementación usando Minimax y Memoización con HASH (Diccionario).
    """
    total_porciones = len(s)

    if total_porciones % 2 !=0:
      raise ValueError(f"Error: El arreglo debe ser par")

    mitad_porciones = total_porciones // 2

    torta_extendida = s * 2

    # Pre-cálculo de sumas para optimizar a O(1)
    prefijos_suma = [0] * (len(torta_extendida) + 1)
    for k in range(len(torta_extendida)):
        prefijos_suma[k+1] = prefijos_suma[k] + torta_extendida[k]

    memo: Dict[Tuple[int, int], int] = {}
    mayor_satisfaccion = -float('inf')
    mejor_inicio = -1

    # Probamos todos los posibles cortes iniciales.
    for i in range(total_porciones):

        ganancia_prof_inicial = obtener_suma(prefijos_suma, i, i + mitad_porciones - 1)

        inicio_resto = i + mitad_porciones
        fin_resto = i + total_porciones - 1

        total_resto = obtener_suma(prefijos_suma, inicio_resto, fin_resto)

        # Calculamos cuánto logra sacar la hermana de ese resto jugando óptimo
        ganancia_hermana = resolver_minimax(inicio_resto, fin_resto, memo, torta_extendida, prefijos_suma)

        # Lo que le queda al profesor del resto
        ganancia_prof_resto = total_resto - ganancia_hermana

        ganancia_prof_total = ganancia_prof_inicial + ganancia_prof_resto

        if ganancia_prof_total > mayor_satisfaccion:
            mayor_satisfaccion = ganancia_prof_total
            mejor_inicio = i


    return mayor_satisfaccion, mejor_inicio % total_porciones

if __name__ == "__main__":
    # Prueba con el caso circular del 30
    s = [10, -5, -5, -5, 10, 20]
    resultado = max_satisfaccion_hash(s)
    print("Versión con HASH (Minimax)")
    print("Máxima satisfacción garantizada:", resultado[0])
    print("Inicio del corte:", resultado[1])