from __future__ import annotations

from pathlib import Path

from grafo import Grafo


def guardar_lista_aristas(grafo: Grafo, ruta: str) -> None:
    """Guarda el grafo como lista de aristas en texto."""
    salida = Path(ruta)
    salida.parent.mkdir(parents=True, exist_ok=True)

    with salida.open("w", encoding="utf-8") as archivo:
        archivo.write(f"# {grafo.resumen()}\n")
        archivo.write("# origen destino peso\n")
        for arista in grafo.aristas():
            u, v = arista.extremos()
            archivo.write(f"{u} {v} {arista.peso}\n")


def guardar_graphviz(grafo: Grafo, ruta: str) -> None:
    """Exporta el grafo a formato .gv sin depender de Graphviz ni pydot."""
    salida = Path(ruta)
    salida.parent.mkdir(parents=True, exist_ok=True)

    tipo = "digraph" if grafo.dirigido else "graph"
    conector = "->" if grafo.dirigido else "--"

    with salida.open("w", encoding="utf-8") as archivo:
        archivo.write(f"{tipo} G {{\n")
        for nodo in grafo.nodos():
            archivo.write(f'    "{nodo}";\n')
        for arista in grafo.aristas():
            u, v = arista.extremos()
            archivo.write(f'    "{u}" {conector} "{v}" [label="{arista.peso}"];\n')
        archivo.write("}\n")
