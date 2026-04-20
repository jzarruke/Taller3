"""
robo_expreso_sur.py — El Robo en el Expreso del Sur

El collar de esmeraldas de la Marquesa desaparecio del vagon privado del tren nocturno.
Elena fue vista en el vagon privado durante el robo; sus huellas están en el estuche de joyas.
Don Rodrigo fue grabado por la cámara de seguridad en el vagon de equipaje durante toda la noche.
El vagon de equipaje es el extremo opuesto al vagon privado; es imposible haber estado en ambos a la vez.
La Marquesa es la victima directa del robo y presencio el incidente.
La Marquesa acusa a Elena.
Victor declara que Elena estuvo con él en el vagon comedor toda la noche.
Elena declara que Victor estuvo con ella en el vagon comedor toda la noche.

Como detective, he llegado a las siguientes conclusiones:
Quien fue grabado en cámara en un lugar alejado de la escena durante el crimen está descartado.
La victima del crimen no tiene razon para mentir; es testigo imparcial.
La acusacion de un testigo imparcial es creible.
Quien estaba en la escena y es acusado de forma creible es culpable.
Quien da coartada a un culpable lo está defendiendo.
Si dos personas se dan coartada mutuamente, tienen una alianza de coartadas entre si.
"""

from src.crime_case import CrimeCase, QuerySpec
from src.predicate_logic import ExistsGoal, KnowledgeBase, Predicate, Rule, Term


def crear_kb() -> KnowledgeBase:
    """Construye la KB según la narrativa del modulo."""
    kb = KnowledgeBase()

    # Constantes del caso
    elena          = Term("elena")
    victor         = Term("victor")
    don_rodrigo    = Term("don_rodrigo")
    marquesa       = Term("marquesa")
    estuche_joyas  = Term("estuche_joyas")
    vagon_equipaje = Term("vagon_equipaje")

    # Variables para las reglas
    X = Term("$X")
    Y = Term("$Y")

    # ─── HECHOS ──────────────────────────────────────────────────────

    # Elena estaba en la escena y tiene huellas en el objeto robado
    kb.add_fact(Predicate("en_escena", (elena,)))
    kb.add_fact(Predicate("huellas_en", (elena, estuche_joyas)))

    # Don Rodrigo fue grabado en lugar alejado (coartada de camara)
    kb.add_fact(Predicate("grabado_camara_lugar_alejado", (don_rodrigo, vagon_equipaje)))

    # La Marquesa es la victima y acusa a Elena
    kb.add_fact(Predicate("victima", (marquesa,)))
    kb.add_fact(Predicate("acusa", (marquesa, elena)))

    # Coartadas cruzadas entre Victor y Elena
    kb.add_fact(Predicate("da_coartada", (victor, elena)))
    kb.add_fact(Predicate("da_coartada", (elena, victor)))

    # ─── REGLAS ──────────────────────────────────────────────────────

    # R1: grabado en camara en lugar alejado -> descartado
    kb.add_rule(Rule(
        head=Predicate("descartado", (X,)),
        body=(Predicate("grabado_camara_lugar_alejado", (X, Y)),),
    ))

    # R2: victima -> testigo imparcial
    kb.add_rule(Rule(
        head=Predicate("testigo_imparcial", (X,)),
        body=(Predicate("victima", (X,)),),
    ))

    # R3: testigo imparcial + acusa -> acusacion creible
    kb.add_rule(Rule(
        head=Predicate("acusacion_creible", (X, Y)),
        body=(
            Predicate("testigo_imparcial", (X,)),
            Predicate("acusa", (X, Y)),
        ),
    ))

    # R4: en la escena + acusado de forma creible -> culpable
    kb.add_rule(Rule(
        head=Predicate("culpable", (Y,)),
        body=(
            Predicate("en_escena", (Y,)),
            Predicate("acusacion_creible", (X, Y)),
        ),
    ))

    # R5: dar coartada a culpable -> defiende al culpable
    kb.add_rule(Rule(
        head=Predicate("defiende_al_culpable", (X,)),
        body=(
            Predicate("da_coartada", (X, Y)),
            Predicate("culpable", (Y,)),
        ),
    ))

    # R6: coartada mutua -> alianza de coartadas
    kb.add_rule(Rule(
        head=Predicate("alianza_coartadas", (X, Y)),
        body=(
            Predicate("da_coartada", (X, Y)),
            Predicate("da_coartada", (Y, X)),
        ),
    ))

    return kb


CASE = CrimeCase(
    id="robo_expreso_sur",
    title="El Robo en el Expreso del Sur",
    suspects=("elena", "victor", "don_rodrigo"),
    narrative=__doc__,
    description=(
        "El collar de la Marquesa desaparecio en un tren nocturno. "
        "Don Rodrigo tiene coartada de camara. Elena estaba en la escena con huellas en el estuche. "
        "La victima la acusa. Victor y Elena se cubren mutuamente."
    ),
    create_kb=crear_kb,
    queries=(
        QuerySpec(
            description="Don Rodrigo esta descartado?",
            goal=Predicate("descartado", (Term("don_rodrigo"),)),
        ),
        QuerySpec(
            description="La acusacion de la Marquesa contra Elena es creible?",
            goal=Predicate("acusacion_creible", (Term("marquesa"), Term("elena"))),
        ),
        QuerySpec(
            description="Elena es culpable?",
            goal=Predicate("culpable", (Term("elena"),)),
        ),
        QuerySpec(
            description="Victor defiende al culpable?",
            goal=Predicate("defiende_al_culpable", (Term("victor"),)),
        ),
        QuerySpec(
            description="Existe alianza de coartadas entre Elena y Victor?",
            goal=ExistsGoal("$X", Predicate("alianza_coartadas", (Term("$X"), Term("victor")))),
        ),
    ),
)