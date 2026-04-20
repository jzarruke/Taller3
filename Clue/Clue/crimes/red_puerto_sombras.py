"""
red_puerto_sombras.py — La Red del Puerto de las Sombras

En el Puerto Industrial se encontró mercancía ilegal oculta en contenedores declarados como carga vacía.
El Capitán Herrera tiene registro digital de salida del puerto verificado durante el fin de semana del delito.
El Inspector Nova tiene documentación oficial de inspecciones realizadas fuera del puerto ese fin de semana.
El Oficial Duarte firma todos los manifiestos de carga del puerto; sus manifiestos son fraudulentos.
El Oficial Duarte no tiene coartada verificada.
El Marinero Pinto tiene acceso irrestricto a la bodega de contenedores; fue visto introduciendo mercancía ilegal.
El Marinero Pinto no tiene coartada verificada.
El Oficial Duarte y el Marinero Pinto pertenecen al mismo cartel portuario.
Un informante reportó al Oficial Duarte y al Marinero Pinto por nombre.
El Capitán Herrera acusa al Oficial Duarte.
El Oficial Duarte declara que el Marinero Pinto no estuvo en el puerto ese fin de semana.
El Marinero Pinto declara que el Oficial Duarte firmó los documentos por error administrativo.

Como detective, he llegado a las siguientes conclusiones:
Quien tiene registro oficial que lo ubica fuera del puerto durante el delito está descartado.
Quien firma manifiestos de carga fraudulentos comete fraude documental.
Quien tiene acceso a la bodega y fue visto introduciendo mercancía ilegal introduce contrabando.
Quien comete fraude documental sin coartada es culpable.
Quien introduce contrabando sin coartada es culpable.
Dos personas comparten red si pertenecen al mismo cartel.
Si dos culpables comparten red, su actividad constituye una operación conjunta.
El testimonio de una persona descartada contra alguien es confiable.
Una red está activa si al menos uno de sus miembros es culpable.
"""

from src.crime_case import CrimeCase, QuerySpec
from src.predicate_logic import ExistsGoal, ForallGoal, KnowledgeBase, Predicate, Rule, Term


def crear_kb() -> KnowledgeBase:
    """Construye la KB según la narrativa del módulo."""
    kb = KnowledgeBase()

    # Constantes del caso
    capitan_herrera  = Term("capitan_herrera")
    oficial_duarte   = Term("oficial_duarte")
    marinero_pinto   = Term("marinero_pinto")
    inspector_nova   = Term("inspector_nova")
    cartel_portuario = Term("cartel_portuario")

    # Variables para las reglas
    X = Term("$X")
    Y = Term("$Y")
    C = Term("$C")
    R = Term("$R")

    # ─── HECHOS ──────────────────────────────────────────────────────

    # Registros oficiales que ubican a estos fuera del puerto
    kb.add_fact(Predicate("registro_salida_verificado", (capitan_herrera,)))
    kb.add_fact(Predicate("registro_salida_verificado", (inspector_nova,)))

    # Oficial Duarte: firma manifiestos fraudulentos, sin coartada
    kb.add_fact(Predicate("firma_manifiestos_fraudulentos", (oficial_duarte,)))
    kb.add_fact(Predicate("sin_coartada", (oficial_duarte,)))

    # Marinero Pinto: acceso a bodega, visto introduciendo ilegales, sin coartada
    kb.add_fact(Predicate("acceso_bodega", (marinero_pinto,)))
    kb.add_fact(Predicate("visto_introduciendo_ilegales", (marinero_pinto,)))
    kb.add_fact(Predicate("sin_coartada", (marinero_pinto,)))

    # Ambos pertenecen al mismo cartel portuario
    kb.add_fact(Predicate("pertenece_a_cartel", (oficial_duarte, cartel_portuario)))
    kb.add_fact(Predicate("pertenece_a_cartel", (marinero_pinto, cartel_portuario)))

    # Informante los reporto a ambos por nombre
    kb.add_fact(Predicate("reportado_informante", (oficial_duarte,)))
    kb.add_fact(Predicate("reportado_informante", (marinero_pinto,)))

    # Capitan Herrera acusa al Oficial Duarte
    kb.add_fact(Predicate("acusa", (capitan_herrera, oficial_duarte)))

    # ─── REGLAS ──────────────────────────────────────────────────────

    # R1: registro oficial fuera del puerto -> descartado
    kb.add_rule(Rule(
        head=Predicate("descartado", (X,)),
        body=(Predicate("registro_salida_verificado", (X,)),),
    ))

    # R2: firma manifiestos fraudulentos -> fraude documental
    kb.add_rule(Rule(
        head=Predicate("fraude_documental", (X,)),
        body=(Predicate("firma_manifiestos_fraudulentos", (X,)),),
    ))

    # R3: acceso a bodega + visto introduciendo ilegales -> introduce contrabando
    kb.add_rule(Rule(
        head=Predicate("introduce_contrabando", (X,)),
        body=(
            Predicate("acceso_bodega", (X,)),
            Predicate("visto_introduciendo_ilegales", (X,)),
        ),
    ))

    # R4: fraude documental + sin coartada -> culpable
    kb.add_rule(Rule(
        head=Predicate("culpable", (X,)),
        body=(
            Predicate("fraude_documental", (X,)),
            Predicate("sin_coartada", (X,)),
        ),
    ))

    # R5: introduce contrabando + sin coartada -> culpable
    kb.add_rule(Rule(
        head=Predicate("culpable", (X,)),
        body=(
            Predicate("introduce_contrabando", (X,)),
            Predicate("sin_coartada", (X,)),
        ),
    ))

    # R6: mismo cartel -> comparten red
    kb.add_rule(Rule(
        head=Predicate("comparten_red", (X, Y)),
        body=(
            Predicate("pertenece_a_cartel", (X, C)),
            Predicate("pertenece_a_cartel", (Y, C)),
        ),
    ))

    # R7: dos culpables que comparten red -> operacion conjunta
    kb.add_rule(Rule(
        head=Predicate("operacion_conjunta", (X, Y)),
        body=(
            Predicate("culpable", (X,)),
            Predicate("culpable", (Y,)),
            Predicate("comparten_red", (X, Y)),
        ),
    ))

    # R8: descartado + acusa -> testimonio confiable
    kb.add_rule(Rule(
        head=Predicate("testimonio_confiable", (X, Y)),
        body=(
            Predicate("descartado", (X,)),
            Predicate("acusa", (X, Y)),
        ),
    ))

    # R9: miembro culpable del cartel -> red activa
    kb.add_rule(Rule(
        head=Predicate("red_activa", (R,)),
        body=(
            Predicate("pertenece_a_cartel", (X, R)),
            Predicate("culpable", (X,)),
        ),
    ))

    return kb


CASE = CrimeCase(
    id="red_puerto_sombras",
    title="La Red del Puerto de las Sombras",
    suspects=("capitan_herrera", "oficial_duarte", "marinero_pinto", "inspector_nova"),
    narrative=__doc__,
    description=(
        "Contrabando en el Puerto Industrial: manifiestos fraudulentos y mercancia ilegal. "
        "Dos culpables con roles distintos operan como red. Identifica a ambos, verifica "
        "si su operacion es conjunta y si hay redes activas."
    ),
    create_kb=crear_kb,
    queries=(
        QuerySpec(
            description="El Oficial Duarte cometio fraude documental?",
            goal=Predicate("fraude_documental", (Term("oficial_duarte"),)),
        ),
        QuerySpec(
            description="El Marinero Pinto es culpable?",
            goal=Predicate("culpable", (Term("marinero_pinto"),)),
        ),
        QuerySpec(
            description="Hay operacion conjunta entre Duarte y Pinto?",
            goal=Predicate("operacion_conjunta", (Term("oficial_duarte"), Term("marinero_pinto"))),
        ),
        QuerySpec(
            description="El testimonio del Capitan Herrera contra Duarte es confiable?",
            goal=Predicate("testimonio_confiable", (Term("capitan_herrera"), Term("oficial_duarte"))),
        ),
        QuerySpec(
            description="Existe alguna red activa?",
            goal=ExistsGoal("$R", Predicate("red_activa", (Term("$R"),))),
        ),
        QuerySpec(
            description="Todo reportado por informante es culpable?",
            goal=ForallGoal(
                "$X",
                Predicate("reportado_informante", (Term("$X"),)),
                Predicate("culpable", (Term("$X"),)),
            ),
        ),
    ),
)