from dataclasses import dataclass


@dataclass(frozen=True)
class Arista:
    """Representa una arista del grafo.

    El ZIP original usaba una clase Arista con nodo de inicio, nodo final,
    peso y bandera de dirigido. Esta versión conserva esa idea, pero guarda
    las etiquetas de los nodos para que el código sea más simple de correr.
    """

    origen: str
    destino: str
    peso: float = 1.0
    dirigido: bool = False

    def clave(self) -> tuple[str, str]:
        """Clave única para evitar duplicados en grafos no dirigidos."""
        if self.dirigido:
            return (self.origen, self.destino)
        return tuple(sorted((self.origen, self.destino)))

    def extremos(self) -> tuple[str, str]:
        return self.origen, self.destino

    def __str__(self) -> str:
        simbolo = "->" if self.dirigido else "--"
        return f"{self.origen} {simbolo} {self.destino} [peso={self.peso}]"
