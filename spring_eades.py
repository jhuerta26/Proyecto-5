from __future__ import annotations

import math
import random
from dataclasses import dataclass

from grafo import Grafo


@dataclass
class ParametrosSpring:
    """Parámetros del método Spring/Eades.

    c1 y c2 corresponden al resorte logarítmico: c1 * log(d / c2).
    c3 controla una repulsión local entre vértices cercanos para evitar traslapes.
    c4 controla cuánto se mueve un vértice por iteración.
    """

    c1: float = 2.0
    c2: float = 90.0
    c3: float = 35.0
    c4: float = 0.10
    amortiguamiento: float = 0.85
    margen: int = 40
    max_desplazamiento: float = 18.0
    gravedad_centro: float = 0.002
    usar_repulsion_local: bool = True


class SpringEades:
    """Layout de grafos con el método de resortes de P. Eades.

    Idea del algoritmo:
      1. Colocar los vértices en posiciones iniciales aleatorias.
      2. Calcular fuerzas de atracción en las aristas con resorte logarítmico.
      3. Aplicar repulsión local entre vértices cercanos para mejorar la lectura.
      4. Mover cada vértice una pequeña cantidad y repetir.

    Se separó esta parte porque en el ZIP original el layout estaba mezclado
    dentro de grafo.py. Así puedes modificar el algoritmo sin tocar los modelos
    de generación ni la ventana de pygame.
    """

    def __init__(
        self,
        grafo: Grafo,
        ancho: int = 1280,
        alto: int = 720,
        parametros: ParametrosSpring | None = None,
        semilla: int | None = None,
    ):
        if grafo.esta_vacio():
            raise ValueError("No se puede calcular layout de un grafo vacío")

        self.grafo = grafo
        self.ancho = ancho
        self.alto = alto
        self.parametros = parametros or ParametrosSpring()
        self.random = random.Random(semilla)
        self.iteracion = 0

        self.posiciones: dict[str, list[float]] = {}
        self.velocidades: dict[str, list[float]] = {}
        self.reiniciar_posiciones()

    def reiniciar_posiciones(self) -> None:
        margen = self.parametros.margen
        for nodo in self.grafo.nodos():
            self.posiciones[nodo] = [
                self.random.uniform(margen, self.ancho - margen),
                self.random.uniform(margen, self.alto - margen),
            ]
            self.velocidades[nodo] = [0.0, 0.0]
        self.iteracion = 0

    def obtener_posiciones(self) -> dict[str, tuple[float, float]]:
        return {n: (p[0], p[1]) for n, p in self.posiciones.items()}

    def ejecutar(self, iteraciones: int) -> dict[str, tuple[float, float]]:
        for _ in range(iteraciones):
            self.paso()
        return self.obtener_posiciones()

    def paso(self) -> None:
        p = self.parametros
        fuerzas = {nodo: [0.0, 0.0] for nodo in self.grafo.nodos()}

        self._fuerzas_atraccion(fuerzas)

        if p.usar_repulsion_local:
            self._fuerzas_repulsion_local(fuerzas)

        self._fuerza_centro(fuerzas)
        self._mover_vertices(fuerzas)
        self.iteracion += 1

    def _fuerzas_atraccion(self, fuerzas: dict[str, list[float]]) -> None:
        p = self.parametros

        for arista in self.grafo.aristas():
            u, v = arista.extremos()
            xu, yu = self.posiciones[u]
            xv, yv = self.posiciones[v]

            dx = xv - xu
            dy = yv - yu
            distancia = math.hypot(dx, dy)
            if distancia < 1e-9:
                dx = self.random.uniform(-1, 1)
                dy = self.random.uniform(-1, 1)
                distancia = math.hypot(dx, dy)

            # Resorte logarítmico de Eades: c1 * log(d / c2).
            magnitud = p.c1 * math.log(max(distancia, 1e-9) / p.c2)
            fx = magnitud * dx / distancia
            fy = magnitud * dy / distancia

            fuerzas[u][0] += fx
            fuerzas[u][1] += fy
            fuerzas[v][0] -= fx
            fuerzas[v][1] -= fy

    def _fuerzas_repulsion_local(self, fuerzas: dict[str, list[float]]) -> None:
        """Repulsión aproximada con una cuadrícula.

        En el archivo original se usaba una matriz completa de distancias.
        Aquí se usa una cuadrícula espacial para comparar principalmente vértices
        cercanos y mantener la ejecución fluida con 100 y 500 nodos.
        """
        p = self.parametros
        celda = max(p.c2 * 2.0, 1.0)
        grilla: dict[tuple[int, int], list[str]] = {}

        for nodo, (x, y) in self.posiciones.items():
            clave = (int(x // celda), int(y // celda))
            grilla.setdefault(clave, []).append(nodo)

        visitados: set[tuple[str, str]] = set()
        for (cx, cy), nodos in grilla.items():
            cercanas: list[str] = []
            for ox in (-1, 0, 1):
                for oy in (-1, 0, 1):
                    cercanas.extend(grilla.get((cx + ox, cy + oy), []))

            for u in nodos:
                for v in cercanas:
                    if u == v:
                        continue
                    clave_par = tuple(sorted((u, v)))
                    if clave_par in visitados:
                        continue
                    visitados.add(clave_par)
                    self._aplicar_repulsion(u, v, fuerzas)

    def _aplicar_repulsion(self, u: str, v: str, fuerzas: dict[str, list[float]]) -> None:
        p = self.parametros
        xu, yu = self.posiciones[u]
        xv, yv = self.posiciones[v]

        dx = xv - xu
        dy = yv - yu
        distancia = math.hypot(dx, dy)

        if distancia < 1e-9:
            dx = self.random.uniform(-1, 1)
            dy = self.random.uniform(-1, 1)
            distancia = math.hypot(dx, dy)

        # Repulsión local inversa a la raíz de la distancia, siguiendo la idea
        # usada en el modelo Spring para separar vértices no adyacentes.
        magnitud = p.c3 / math.sqrt(max(distancia, 1e-9))
        fx = magnitud * dx / distancia
        fy = magnitud * dy / distancia

        fuerzas[u][0] -= fx
        fuerzas[u][1] -= fy
        fuerzas[v][0] += fx
        fuerzas[v][1] += fy

    def _fuerza_centro(self, fuerzas: dict[str, list[float]]) -> None:
        """Evita que componentes desconectadas se salgan de la pantalla."""
        p = self.parametros
        cx = self.ancho / 2
        cy = self.alto / 2

        for nodo, (x, y) in self.posiciones.items():
            fuerzas[nodo][0] += (cx - x) * p.gravedad_centro
            fuerzas[nodo][1] += (cy - y) * p.gravedad_centro

    def _mover_vertices(self, fuerzas: dict[str, list[float]]) -> None:
        p = self.parametros
        margen = p.margen

        for nodo in self.grafo.nodos():
            fx, fy = fuerzas[nodo]
            vx, vy = self.velocidades[nodo]

            vx = (vx + p.c4 * fx) * p.amortiguamiento
            vy = (vy + p.c4 * fy) * p.amortiguamiento

            desplazamiento = math.hypot(vx, vy)
            if desplazamiento > p.max_desplazamiento:
                escala = p.max_desplazamiento / desplazamiento
                vx *= escala
                vy *= escala

            x, y = self.posiciones[nodo]
            x += vx
            y += vy

            if x < margen or x > self.ancho - margen:
                vx *= -0.35
            if y < margen or y > self.alto - margen:
                vy *= -0.35

            x = min(self.ancho - margen, max(margen, x))
            y = min(self.alto - margen, max(margen, y))

            self.posiciones[nodo] = [x, y]
            self.velocidades[nodo] = [vx, vy]
