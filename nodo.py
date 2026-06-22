class Nodo:
    """Nodo básico para el grafo.

    Mantiene una etiqueta y el conjunto de vecinos. Esta separación viene de
    la estructura original del ZIP, donde existían nodo.py, arista.py y grafo.py.
    """

    def __init__(self, etiqueta: str):
        self.etiqueta = str(etiqueta)
        self.vecinos: set[str] = set()

    def agregar_vecino(self, etiqueta: str) -> None:
        self.vecinos.add(str(etiqueta))

    def quitar_vecino(self, etiqueta: str) -> None:
        self.vecinos.discard(str(etiqueta))

    def grado(self) -> int:
        return len(self.vecinos)

    def __str__(self) -> str:
        return self.etiqueta
