#******************************************************************************
from grafoMalla import grafoMalla
from grafoGeografico import grafoGeografico
from grafoErdosRenyi import grafoErdosRenyi
from grafoGilbert import grafoGilbert
from grafoBarabasiAlbert import grafoBarabasiAlbert
from grafoDorogovtsevMendes import grafoDorogovtsevMendes
#******************************************************************************

# Nota:
# Cada grafo se acomoda con Spring, guarda captura PNG y guarda archivo .gv.
# Las capturas se guardan en: capturas_pygame/
# Los archivos .gv se guardan en: gv/

#******************************************************************************
# gfGeografico - 100 nodos
#******************************************************************************
gfGeografico = grafoGeografico(n=100, r=0.3, dirigido=False, auto=False)
gfGeografico.display()
gfGeografico.playSpringAnimation(
    "grafoGeografico 100 nodos",
    guardar_imagen=True,
    iteraciones_guardar=300,
    cerrar_al_guardar=True,
    auto_zoom=True,
    margen_zoom=40,
    guardar_gv=True
)

#******************************************************************************
# gfGeografico - 500 nodos
#******************************************************************************
gfGeografico = grafoGeografico(n=500, r=0.12, dirigido=False, auto=False)
gfGeografico.display()
gfGeografico.playSpringAnimation(
    "grafoGeografico 500 nodos",
    guardar_imagen=True,
    iteraciones_guardar=300,
    cerrar_al_guardar=True,
    auto_zoom=True,
    margen_zoom=40,
    guardar_gv=True
)

#******************************************************************************
# gfMalla - 100 nodos
#******************************************************************************
gfMalla = grafoMalla(10, 10, dirigido=False)
gfMalla.display()
gfMalla.playSpringAnimation(
    "grafo Malla 100 nodos",
    guardar_imagen=True,
    iteraciones_guardar=300,
    cerrar_al_guardar=True,
    auto_zoom=True,
    margen_zoom=40,
    guardar_gv=True
)

#******************************************************************************
# gfMalla - 180 nodos
#******************************************************************************
gfMalla = grafoMalla(15, 12, dirigido=False)
gfMalla.display()
gfMalla.playSpringAnimation(
    "grafo Malla 180 nodos",
    guardar_imagen=True,
    iteraciones_guardar=300,
    cerrar_al_guardar=True,
    auto_zoom=True,
    margen_zoom=40,
    guardar_gv=True
)

#******************************************************************************
# gfMalla - 289 nodos
#******************************************************************************
gfMalla = grafoMalla(17, 17, dirigido=False)
gfMalla.display()
gfMalla.playSpringAnimation(
    "grafo Malla 289 nodos",
    guardar_imagen=True,
    iteraciones_guardar=300,
    cerrar_al_guardar=True,
    auto_zoom=True,
    margen_zoom=40,
    guardar_gv=True
)

#******************************************************************************
# gfMalla - 506 nodos
#******************************************************************************
gfMalla = grafoMalla(23, 22, dirigido=False)
gfMalla.display()
gfMalla.playSpringAnimation(
    "grafo Malla 506 nodos",
    guardar_imagen=True,
    iteraciones_guardar=300,
    cerrar_al_guardar=True,
    auto_zoom=True,
    margen_zoom=40,
    guardar_gv=True
)

#******************************************************************************
# gfErdosRenyi - 100 nodos
#******************************************************************************
gfErdosRenyi = grafoErdosRenyi(n=100, m=100, dirigido=False, auto=False)
gfErdosRenyi.display()
gfErdosRenyi.playSpringAnimation(
    "grafo Erdos Renyi 100 nodos",
    guardar_imagen=True,
    iteraciones_guardar=300,
    cerrar_al_guardar=True,
    auto_zoom=True,
    margen_zoom=40,
    guardar_gv=True
)

#******************************************************************************
# gfErdosRenyi - 500 nodos
#******************************************************************************
gfErdosRenyi = grafoErdosRenyi(n=500, m=500, dirigido=False, auto=False)
gfErdosRenyi.display()
gfErdosRenyi.playSpringAnimation(
    "grafo Erdos Renyi 500 nodos",
    guardar_imagen=True,
    iteraciones_guardar=300,
    cerrar_al_guardar=True,
    auto_zoom=True,
    margen_zoom=40,
    guardar_gv=True
)

#******************************************************************************
# grafoGilbert - 100 nodos
#******************************************************************************
gfGilbert = grafoGilbert(n=100, p=0.1, dirigido=False, auto=False)
gfGilbert.display()
gfGilbert.playSpringAnimation(
    "grafo Gilbert 100 nodos",
    guardar_imagen=True,
    iteraciones_guardar=300,
    cerrar_al_guardar=True,
    auto_zoom=True,
    margen_zoom=40,
    guardar_gv=True
)

#******************************************************************************
# grafoGilbert - 500 nodos
#******************************************************************************
gfGilbert = grafoGilbert(n=500, p=0.1, dirigido=False, auto=False)
gfGilbert.display()
gfGilbert.playSpringAnimation(
    "grafo Gilbert 500 nodos",
    guardar_imagen=True,
    iteraciones_guardar=300,
    cerrar_al_guardar=True,
    auto_zoom=True,
    margen_zoom=40,
    guardar_gv=True
)

#******************************************************************************
# grafoBarabasiAlbert - 100 nodos
#******************************************************************************
gfBarabasiAlbert = grafoBarabasiAlbert(n=100, d=4, dirigido=False, auto=False)
gfBarabasiAlbert.display()
gfBarabasiAlbert.playSpringAnimation(
    "grafo Barabasi Albert 100 nodos",
    guardar_imagen=True,
    iteraciones_guardar=300,
    cerrar_al_guardar=True,
    auto_zoom=True,
    margen_zoom=40,
    guardar_gv=True
)

#******************************************************************************
# grafoBarabasiAlbert - 500 nodos
#******************************************************************************
gfBarabasiAlbert = grafoBarabasiAlbert(n=500, d=3, dirigido=False, auto=False)
gfBarabasiAlbert.display()
gfBarabasiAlbert.playSpringAnimation(
    "grafo Barabasi Albert 500 nodos",
    guardar_imagen=True,
    iteraciones_guardar=300,
    cerrar_al_guardar=True,
    auto_zoom=True,
    margen_zoom=40,
    guardar_gv=True
)

#******************************************************************************
# grafoDorogovtsevMendes - 100 nodos
#******************************************************************************
gfDorogovtsevMendes = grafoDorogovtsevMendes(100, dirigido=False)
gfDorogovtsevMendes.display()
gfDorogovtsevMendes.playSpringAnimation(
    "grafo Dorogovtsev Mendes 100 nodos",
    guardar_imagen=True,
    iteraciones_guardar=300,
    cerrar_al_guardar=True,
    auto_zoom=True,
    margen_zoom=40,
    guardar_gv=True
)

#******************************************************************************
# grafoDorogovtsevMendes - 500 nodos
#******************************************************************************
gfDorogovtsevMendes = grafoDorogovtsevMendes(500, dirigido=False)
gfDorogovtsevMendes.display()
gfDorogovtsevMendes.playSpringAnimation(
    "grafo Dorogovtsev Mendes 500 nodos",
    guardar_imagen=True,
    iteraciones_guardar=300,
    cerrar_al_guardar=True,
    auto_zoom=True,
    margen_zoom=40,
    guardar_gv=True
)
#******************************************************************************
