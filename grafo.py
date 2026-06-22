from __future__ import annotations

from arista import Arista
from nodo import Nodo


def _orden_etiqueta(etiqueta: str):
    """Ordena etiquetas numéricas como números y las demás como texto."""
    texto = str(etiqueta)
    try:
        return (0, int(texto))
    except ValueError:
        return (1, texto)


class Grafo:
    """Estructura de grafo no dirigido/dirigido.

    Esta clase reemplaza la parte de estructura del archivo grafo.py original,
    dejando solo lo necesario para el Proyecto 5: crear nodos, crear aristas,
    consultar vecinos y entregar la información al layout Spring de Eades.
    """

    def __init__(self, dirigido: bool = False):
        self.dirigido = dirigido
        self._nodos: dict[str, Nodo] = {}
        self._aristas: dict[tuple[str, str], Arista] = {}

    def agregar_nodo(self, etiqueta: str) -> None:
        etiqueta = str(etiqueta)
        if etiqueta not in self._nodos:
            self._nodos[etiqueta] = Nodo(etiqueta)

    def agregar_arista(self, origen: str, destino: str, peso: float = 1.0) -> bool:
        origen = str(origen)
        destino = str(destino)

        self.agregar_nodo(origen)
        self.agregar_nodo(destino)

        arista = Arista(origen, destino, peso, self.dirigido)
        clave = arista.clave()

        if clave in self._aristas:
            return False

        self._aristas[clave] = arista
        self._nodos[origen].agregar_vecino(destino)
        if not self.dirigido and origen != destino:
            self._nodos[destino].agregar_vecino(origen)
        return True

    def existe_arista(self, origen: str, destino: str) -> bool:
        arista = Arista(str(origen), str(destino), dirigido=self.dirigido)
        return arista.clave() in self._aristas

    def nodos(self) -> list[str]:
        return sorted(self._nodos.keys(), key=_orden_etiqueta)

    def aristas(self) -> list[Arista]:
        return list(self._aristas.values())

    def vecinos(self, etiqueta: str) -> set[str]:
        return set(self._nodos[str(etiqueta)].vecinos)

    def grado(self, etiqueta: str) -> int:
        return self._nodos[str(etiqueta)].grado()

    def numero_nodos(self) -> int:
        return len(self._nodos)

    def numero_aristas(self) -> int:
        return len(self._aristas)

    def esta_vacio(self) -> bool:
        return not self._nodos

    def resumen(self) -> str:
        tipo = "dirigido" if self.dirigido else "no dirigido"
        return f"Grafo {tipo}: {self.numero_nodos()} nodos, {self.numero_aristas()} aristas"

    def __str__(self) -> str:
        lineas = [self.resumen()]
        for arista in self.aristas():
            lineas.append(str(arista))
        return "\n".join(lineas)
