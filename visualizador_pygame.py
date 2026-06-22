from __future__ import annotations

import os
from pathlib import Path

from grafo import Grafo
from spring_eades import SpringEades


COLOR_FONDO = (18, 18, 22)
COLOR_ARISTA = (90, 200, 230)
COLOR_NODO = (240, 80, 80)
COLOR_BORDE_NODO = (20, 20, 20)
COLOR_TEXTO = (240, 240, 240)
COLOR_INFO = (210, 210, 210)


def _importar_pygame():
    try:
        import pygame
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "No se encontró pygame. Instálalo con:\n"
            "    python -m pip install pygame"
        ) from exc
    return pygame


def dibujar_grafo(surface, grafo: Grafo, posiciones: dict[str, tuple[float, float]], titulo: str = "") -> None:
    pygame = _importar_pygame()
    surface.fill(COLOR_FONDO)

    ancho, alto = surface.get_size()
    radio = 6 if grafo.numero_nodos() > 150 else 9
    grosor_arista = 1 if grafo.numero_nodos() > 250 else 2
    mostrar_etiquetas = grafo.numero_nodos() <= 120

    for arista in grafo.aristas():
        u, v = arista.extremos()
        if u not in posiciones or v not in posiciones:
            continue
        x1, y1 = posiciones[u]
        x2, y2 = posiciones[v]
        pygame.draw.line(surface, COLOR_ARISTA, (x1, y1), (x2, y2), grosor_arista)

    fuente = pygame.font.SysFont("arial", 13)
    for nodo in grafo.nodos():
        x, y = posiciones[nodo]
        pygame.draw.circle(surface, COLOR_NODO, (int(x), int(y)), radio)
        pygame.draw.circle(surface, COLOR_BORDE_NODO, (int(x), int(y)), radio, 1)

        if mostrar_etiquetas:
            etiqueta = fuente.render(nodo, True, COLOR_TEXTO)
            surface.blit(etiqueta, (x + radio + 2, y - radio - 2))

    fuente_info = pygame.font.SysFont("arial", 18)
    if not titulo:
        titulo = grafo.resumen()
    texto = fuente_info.render(titulo, True, COLOR_INFO)
    surface.blit(texto, (12, 10))

    ayuda = "ESC: salir | ESPACIO: pausar | S: guardar captura | R: reiniciar"
    texto_ayuda = pygame.font.SysFont("arial", 15).render(ayuda, True, COLOR_INFO)
    surface.blit(texto_ayuda, (12, alto - 28))


def ejecutar_interactivo(
    grafo: Grafo,
    layout: SpringEades,
    titulo: str,
    fps: int = 60,
    pasos_por_frame: int = 1,
    carpeta_capturas: str = "capturas",
) -> None:
    pygame = _importar_pygame()
    pygame.init()

    pantalla = pygame.display.set_mode((layout.ancho, layout.alto))
    pygame.display.set_caption(titulo)
    reloj = pygame.time.Clock()
    pausado = False

    Path(carpeta_capturas).mkdir(parents=True, exist_ok=True)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if evento.key == pygame.K_SPACE:
                    pausado = not pausado
                if evento.key == pygame.K_r:
                    layout.reiniciar_posiciones()
                if evento.key == pygame.K_s:
                    nombre = f"captura_{layout.iteracion}.png"
                    ruta = Path(carpeta_capturas) / nombre
                    pygame.image.save(pantalla, str(ruta))
                    print(f"Captura guardada en: {ruta}")

        if not pausado:
            for _ in range(max(1, pasos_por_frame)):
                layout.paso()

        titulo_iteracion = f"{titulo} | iteración {layout.iteracion}"
        dibujar_grafo(pantalla, grafo, layout.obtener_posiciones(), titulo_iteracion)
        pygame.display.flip()
        reloj.tick(fps)


def guardar_captura(
    grafo: Grafo,
    posiciones: dict[str, tuple[float, float]],
    ruta_salida: str,
    ancho: int = 1280,
    alto: int = 720,
    titulo: str = "",
) -> None:
    pygame = _importar_pygame()

    # Permite generar capturas en equipos sin pantalla si se configura SDL.
    os.environ.setdefault("SDL_VIDEODRIVER", os.environ.get("SDL_VIDEODRIVER", "dummy"))
    pygame.init()
    pygame.font.init()

    surface = pygame.Surface((ancho, alto))
    dibujar_grafo(surface, grafo, posiciones, titulo)

    ruta = Path(ruta_salida)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    pygame.image.save(surface, str(ruta))
    pygame.quit()
