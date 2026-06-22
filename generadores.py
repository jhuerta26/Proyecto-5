from __future__ import annotations

import math
import random

from grafo import Grafo


MODELOS_DISPONIBLES = (
    "malla",
    "erdos_renyi",
    "gilbert",
    "geografico",
    "barabasi_albert",
    "dorogovtsev_mendes",
)


def _peso_aleatorio() -> int:
    return random.randint(1, 999)


def generar_malla_por_n(n: int, dirigido: bool = False) -> Grafo:
    """Genera una malla rectangular usando aproximadamente n nodos.

    El ZIP original tenía grafo_malla(m, n). Aquí se permite pedir directamente
    100 o 500 nodos, como solicita el proyecto.
    """
    if n <= 0:
        raise ValueError("n debe ser mayor que 0")

    columnas = math.ceil(math.sqrt(n))
    filas = math.ceil(n / columnas)

    grafo = Grafo(dirigido=dirigido)
    for i in range(n):
        grafo.agregar_nodo(str(i))

    for fila in range(filas):
        for col in range(columnas):
            actual = fila * columnas + col
            if actual >= n:
                continue

            derecha = actual + 1
            abajo = actual + columnas

            if col + 1 < columnas and derecha < n:
                grafo.agregar_arista(str(actual), str(derecha), _peso_aleatorio())
            if abajo < n:
                grafo.agregar_arista(str(actual), str(abajo), _peso_aleatorio())

    return grafo


def generar_erdos_renyi(n: int, m: int, dirigido: bool = False, autociclos: bool = False) -> Grafo:
    """Modelo Erdős-Rényi G(n, m): n nodos y m aristas."""
    if n <= 0:
        raise ValueError("n debe ser mayor que 0")

    max_aristas = n * n if dirigido else n * (n - 1) // 2
    if not autociclos:
        max_aristas = n * (n - 1) if dirigido else n * (n - 1) // 2
    m = min(m, max_aristas)

    grafo = Grafo(dirigido=dirigido)
    for i in range(n):
        grafo.agregar_nodo(str(i))

    intentos = 0
    limite_intentos = max(1000, m * 50)
    while grafo.numero_aristas() < m and intentos < limite_intentos:
        u = random.randrange(n)
        v = random.randrange(n)
        intentos += 1

        if not autociclos and u == v:
            continue
        grafo.agregar_arista(str(u), str(v), _peso_aleatorio())

    return grafo


def generar_gilbert(n: int, p: float, dirigido: bool = False, autociclos: bool = False) -> Grafo:
    """Modelo Gilbert G(n, p): cada arista aparece con probabilidad p."""
    if n <= 0:
        raise ValueError("n debe ser mayor que 0")
    if not 0 <= p <= 1:
        raise ValueError("p debe estar entre 0 y 1")

    grafo = Grafo(dirigido=dirigido)
    for i in range(n):
        grafo.agregar_nodo(str(i))

    if dirigido:
        pares = ((i, j) for i in range(n) for j in range(n))
    else:
        pares = ((i, j) for i in range(n) for j in range(i + 1, n))

    for i, j in pares:
        if not autociclos and i == j:
            continue
        if random.random() <= p:
            grafo.agregar_arista(str(i), str(j), _peso_aleatorio())

    return grafo


def generar_geografico(n: int, r: float, dirigido: bool = False, autociclos: bool = False) -> Grafo:
    """Modelo geográfico simple: conecta nodos con distancia euclidiana <= r.

    Las coordenadas solo se usan para decidir aristas; el dibujo final lo calcula
    el método Spring de Eades.
    """
    if n <= 0:
        raise ValueError("n debe ser mayor que 0")
    if r <= 0:
        raise ValueError("r debe ser mayor que 0")

    grafo = Grafo(dirigido=dirigido)
    puntos: dict[int, tuple[float, float]] = {}

    for i in range(n):
        grafo.agregar_nodo(str(i))
        puntos[i] = (random.random(), random.random())

    if dirigido:
        pares = ((i, j) for i in range(n) for j in range(n))
    else:
        pares = ((i, j) for i in range(n) for j in range(i + 1, n))

    r2 = r * r
    for i, j in pares:
        if not autociclos and i == j:
            continue
        dx = puntos[i][0] - puntos[j][0]
        dy = puntos[i][1] - puntos[j][1]
        if dx * dx + dy * dy <= r2:
            grafo.agregar_arista(str(i), str(j), _peso_aleatorio())

    return grafo


def generar_barabasi_albert(n: int, d: int, dirigido: bool = False) -> Grafo:
    """Modelo Barabási-Albert por conexión preferencial.

    d indica cuántas conexiones intenta crear cada nuevo nodo.
    """
    if n <= 0:
        raise ValueError("n debe ser mayor que 0")
    if d <= 0:
        raise ValueError("d debe ser mayor que 0")

    grafo = Grafo(dirigido=dirigido)
    inicial = min(max(d + 1, 2), n)

    for i in range(inicial):
        grafo.agregar_nodo(str(i))

    for i in range(inicial):
        for j in range(i + 1, inicial):
            grafo.agregar_arista(str(i), str(j), _peso_aleatorio())

    for nuevo in range(inicial, n):
        grafo.agregar_nodo(str(nuevo))
        candidatos = grafo.nodos()[:-1]
        pesos = [max(1, grafo.grado(v)) for v in candidatos]
        elegidos: set[str] = set()

        while len(elegidos) < min(d, len(candidatos)):
            elegido = random.choices(candidatos, weights=pesos, k=1)[0]
            elegidos.add(elegido)

        for existente in elegidos:
            grafo.agregar_arista(str(nuevo), existente, _peso_aleatorio())

    return grafo


def generar_dorogovtsev_mendes(n: int, dirigido: bool = False) -> Grafo:
    """Modelo Dorogovtsev-Mendes.

    Inicia con un triángulo. Cada nuevo nodo elige una arista existente y se
    conecta a sus dos extremos.
    """
    if n < 3:
        raise ValueError("Dorogovtsev-Mendes requiere al menos 3 nodos")

    grafo = Grafo(dirigido=dirigido)
    for i in range(3):
        grafo.agregar_nodo(str(i))

    grafo.agregar_arista("0", "1", _peso_aleatorio())
    grafo.agregar_arista("1", "2", _peso_aleatorio())
    grafo.agregar_arista("2", "0", _peso_aleatorio())

    for nuevo in range(3, n):
        arista = random.choice(grafo.aristas())
        u, v = arista.extremos()
        grafo.agregar_nodo(str(nuevo))
        grafo.agregar_arista(str(nuevo), u, _peso_aleatorio())
        grafo.agregar_arista(str(nuevo), v, _peso_aleatorio())

    return grafo


def generar_por_modelo(
    modelo: str,
    n: int,
    m: int | None = None,
    p: float | None = None,
    r: float | None = None,
    d: int | None = None,
    dirigido: bool = False,
    autociclos: bool = False,
) -> Grafo:
    modelo = modelo.lower().strip()

    if modelo == "malla":
        return generar_malla_por_n(n, dirigido=dirigido)

    if modelo == "erdos_renyi":
        if m is None:
            m = 3 * n
        return generar_erdos_renyi(n, m, dirigido=dirigido, autociclos=autociclos)

    if modelo == "gilbert":
        if p is None:
            p = min(0.12, 5 / max(1, n))
        return generar_gilbert(n, p, dirigido=dirigido, autociclos=autociclos)

    if modelo == "geografico":
        if r is None:
            r = 0.16 if n <= 100 else 0.075
        return generar_geografico(n, r, dirigido=dirigido, autociclos=autociclos)

    if modelo == "barabasi_albert":
        if d is None:
            d = 4
        return generar_barabasi_albert(n, d, dirigido=dirigido)

    if modelo == "dorogovtsev_mendes":
        return generar_dorogovtsev_mendes(n, dirigido=dirigido)

    disponibles = ", ".join(MODELOS_DISPONIBLES)
    raise ValueError(f"Modelo no válido: {modelo}. Modelos disponibles: {disponibles}")
