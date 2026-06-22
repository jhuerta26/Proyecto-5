from __future__ import annotations

import argparse
import random
from pathlib import Path

from exportador import guardar_graphviz, guardar_lista_aristas
from generadores import MODELOS_DISPONIBLES, generar_por_modelo
from spring_eades import ParametrosSpring, SpringEades
from visualizador_pygame import ejecutar_interactivo, guardar_captura


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Proyecto 5: disposición de grafos con pygame usando Spring/Eades."
    )

    parser.add_argument("--modelo", choices=MODELOS_DISPONIBLES, default="barabasi_albert")
    parser.add_argument("--n", type=int, default=100, help="Número de nodos")
    parser.add_argument("--m", type=int, default=None, help="Número de aristas para Erdős-Rényi")
    parser.add_argument("--p", type=float, default=None, help="Probabilidad para Gilbert")
    parser.add_argument("--r", type=float, default=None, help="Radio para modelo geográfico")
    parser.add_argument("--d", type=int, default=None, help="Grado/conexiones para Barabási-Albert")
    parser.add_argument("--dirigido", action="store_true", help="Genera grafo dirigido")
    parser.add_argument("--autociclos", action="store_true", help="Permite autociclos cuando el modelo lo soporte")
    parser.add_argument("--semilla", type=int, default=7, help="Semilla aleatoria")

    parser.add_argument("--ancho", type=int, default=1280)
    parser.add_argument("--alto", type=int, default=720)
    parser.add_argument("--fps", type=int, default=60)
    parser.add_argument("--pasos-por-frame", type=int, default=1)
    parser.add_argument("--iteraciones", type=int, default=400, help="Iteraciones para captura o batch")

    parser.add_argument("--c1", type=float, default=2.0)
    parser.add_argument("--c2", type=float, default=90.0)
    parser.add_argument("--c3", type=float, default=35.0)
    parser.add_argument("--c4", type=float, default=0.10)
    parser.add_argument("--sin-repulsion-local", action="store_true")

    parser.add_argument("--captura", default=None, help="Ruta para guardar una captura PNG y terminar")
    parser.add_argument("--exportar", default=None, help="Carpeta para exportar .txt y .gv del grafo")
    parser.add_argument("--batch", action="store_true", help="Genera capturas de todos los modelos con 100 y 500 nodos")
    parser.add_argument("--salida", default="salidas_proyecto5", help="Carpeta de salida para batch/exportación")

    return parser


def crear_grafo(args, modelo: str | None = None, n: int | None = None):
    return generar_por_modelo(
        modelo=modelo or args.modelo,
        n=n or args.n,
        m=args.m,
        p=args.p,
        r=args.r,
        d=args.d,
        dirigido=args.dirigido,
        autociclos=args.autociclos,
    )


def crear_layout(args, grafo):
    parametros = ParametrosSpring(
        c1=args.c1,
        c2=args.c2,
        c3=args.c3,
        c4=args.c4,
        usar_repulsion_local=not args.sin_repulsion_local,
    )
    return SpringEades(
        grafo=grafo,
        ancho=args.ancho,
        alto=args.alto,
        parametros=parametros,
        semilla=args.semilla,
    )


def exportar_si_se_pide(args, grafo, nombre_base: str) -> None:
    if not args.exportar:
        return

    carpeta = Path(args.exportar)
    carpeta.mkdir(parents=True, exist_ok=True)
    guardar_lista_aristas(grafo, str(carpeta / f"{nombre_base}.txt"))
    guardar_graphviz(grafo, str(carpeta / f"{nombre_base}.gv"))


def ejecutar_uno(args) -> None:
    random.seed(args.semilla)
    grafo = crear_grafo(args)
    layout = crear_layout(args, grafo)
    titulo = f"Proyecto 5 - Spring/Eades - {args.modelo} - n={args.n} - m={grafo.numero_aristas()}"
    nombre_base = f"{args.modelo}_{args.n}_nodos"

    print(grafo.resumen())
    exportar_si_se_pide(args, grafo, nombre_base)

    if args.captura:
        layout.ejecutar(args.iteraciones)
        guardar_captura(
            grafo=grafo,
            posiciones=layout.obtener_posiciones(),
            ruta_salida=args.captura,
            ancho=args.ancho,
            alto=args.alto,
            titulo=titulo,
        )
        print(f"Captura guardada en: {args.captura}")
        return

    ejecutar_interactivo(
        grafo=grafo,
        layout=layout,
        titulo=titulo,
        fps=args.fps,
        pasos_por_frame=args.pasos_por_frame,
        carpeta_capturas=args.salida,
    )


def ejecutar_batch(args) -> None:
    carpeta = Path(args.salida)
    carpeta.mkdir(parents=True, exist_ok=True)

    for modelo in MODELOS_DISPONIBLES:
        for n in (100, 500):
            random.seed(args.semilla + n)
            grafo = crear_grafo(args, modelo=modelo, n=n)
            layout = crear_layout(args, grafo)
            layout.ejecutar(args.iteraciones)

            nombre_base = f"{modelo}_{n}_nodos"
            titulo = f"Proyecto 5 - Spring/Eades - {modelo} - n={n} - m={grafo.numero_aristas()}"
            ruta_png = carpeta / f"{nombre_base}.png"

            guardar_captura(
                grafo=grafo,
                posiciones=layout.obtener_posiciones(),
                ruta_salida=str(ruta_png),
                ancho=args.ancho,
                alto=args.alto,
                titulo=titulo,
            )
            guardar_lista_aristas(grafo, str(carpeta / f"{nombre_base}.txt"))
            guardar_graphviz(grafo, str(carpeta / f"{nombre_base}.gv"))
            print(f"Guardado: {ruta_png}")


def main() -> None:
    parser = construir_parser()
    args = parser.parse_args()

    if args.batch:
        ejecutar_batch(args)
    else:
        ejecutar_uno(args)


if __name__ == "__main__":
    main()
