"""
sabotaje_pharmax.py — El Sabotaje en Laboratorio Pharmax

Los cultivos del Proyecto Ámbar fueron destruidos en el Laboratorio Pharmax durante el fin de semana.
La Dra. Santos asistió a un congreso internacional ese fin de semana con documentación oficial de viaje al exterior.
El Director Vega participó en una conferencia en Bruselas con registro verificado de asistencia.
El Técnico Ríos fue despedido recientemente por filtrar información confidencial; no tiene coartada para el fin de semana.
El Asistente Mora fue amenazado con despido; tampoco tiene coartada para el fin de semana.
El registro de acceso muestra que el Técnico Ríos entró a la sala de cultivos el sábado.
El mismo registro muestra que el Asistente Mora también entró a la sala de cultivos el sábado.
Registros bancarios muestran que el Técnico Ríos recibió pagos de Syntek Corp. durante los últimos meses.
Syntek Corp. es la empresa rival que competía por la misma patente farmacéutica.
El Asistente Mora acusa directamente al Técnico Ríos.
El Técnico Ríos declara que el Asistente Mora estuvo con él durante todo el fin de semana.

Como detective, he llegado a las siguientes conclusiones:
Documentación oficial de ausencia del país constituye coartada verificada.
Un registro oficial de conferencia también constituye coartada verificada.
Quien tiene coartada verificada queda descartado como autor del sabotaje.
Quien recibió pagos de una empresa que se beneficia del sabotaje tiene conflicto de intereses con ella.
El conflicto de intereses con la empresa beneficiada constituye motivo económico para el sabotaje.
Quien tuvo acceso registrado al lugar saboteado estuvo en el momento del crimen.
Quien sin coartada tiene motivo económico y estuvo en el lugar del sabotaje es culpable.
La denuncia de alguien que también estuvo en el lugar del sabotaje es una denuncia informada.
"""

from src.crime_case import CrimeCase, QuerySpec
from src.predicate_logic import ForallGoal, KnowledgeBase, Predicate, Rule, Term


def crear_kb() -> KnowledgeBase:
    """Construye la KB según la narrativa del módulo."""
    kb = KnowledgeBase()

    # Constantes del caso
    tec_rios       = Term("tec_rios")
    asistente_mora = Term("asistente_mora")
    dra_santos     = Term("dra_santos")
    director_vega  = Term("director_vega")
    syntek_corp    = Term("syntek_corp")
    sala_cultivos  = Term("sala_cultivos")

    # Variables para las reglas
    X = Term("$X")
    Y = Term("$Y")
    E = Term("$E")
    L = Term("$L")

    # Hechos

    # Coartadas verificadas por documentacion oficial
    kb.add_fact(Predicate("documentacion_viaje_exterior", (dra_santos,)))
    kb.add_fact(Predicate("registro_conferencia_oficial", (director_vega,)))

    # Sin coartada
    kb.add_fact(Predicate("sin_coartada", (tec_rios,)))
    kb.add_fact(Predicate("sin_coartada", (asistente_mora,)))

    # Acceso registrado a la sala de cultivos
    kb.add_fact(Predicate("acceso_registrado", (tec_rios, sala_cultivos)))
    kb.add_fact(Predicate("acceso_registrado", (asistente_mora, sala_cultivos)))

    # Pagos de empresa rival al tecnico Rios
    kb.add_fact(Predicate("recibio_pagos_de", (tec_rios, syntek_corp)))

    # Syntek Corp se beneficia del sabotaje
    kb.add_fact(Predicate("empresa_beneficiada", (syntek_corp,)))

    # Acusacion directa
    kb.add_fact(Predicate("acusa", (asistente_mora, tec_rios)))

    # Reglas

    # R1: documentacion oficial de viaje -> coartada verificada
    kb.add_rule(Rule(
        head=Predicate("coartada_verificada", (X,)),
        body=(Predicate("documentacion_viaje_exterior", (X,)),),
    ))

    # R2: registro oficial de conferencia -> coartada verificada
    kb.add_rule(Rule(
        head=Predicate("coartada_verificada", (X,)),
        body=(Predicate("registro_conferencia_oficial", (X,)),),
    ))

    # R3: coartada verificada -> descartado
    kb.add_rule(Rule(
        head=Predicate("descartado", (X,)),
        body=(Predicate("coartada_verificada", (X,)),),
    ))

    # R4: recibio pagos de empresa beneficiada -> conflicto de intereses
    kb.add_rule(Rule(
        head=Predicate("conflicto_intereses", (X, E)),
        body=(
            Predicate("recibio_pagos_de", (X, E)),
            Predicate("empresa_beneficiada", (E,)),
        ),
    ))

    # R5: conflicto de intereses -> motivo económico
    kb.add_rule(Rule(
        head=Predicate("motivo_economico", (X,)),
        body=(Predicate("conflicto_intereses", (X, E)),),
    ))

    # R6: acceso registrado al lugar -> acceso en momento del crimen
    kb.add_rule(Rule(
        head=Predicate("acceso_en_momento", (X,)),
        body=(Predicate("acceso_registrado", (X, L)),),
    ))

    # R7: sin coartada + motivo economico + acceso en momento -> culpable
    kb.add_rule(Rule(
        head=Predicate("culpable", (X,)),
        body=(
            Predicate("sin_coartada", (X,)),
            Predicate("motivo_economico", (X,)),
            Predicate("acceso_en_momento", (X,)),
        ),
    ))

    # R8: tuvo acceso en momento + acusa -> denuncia informada
    kb.add_rule(Rule(
        head=Predicate("denuncia_informada", (X, Y)),
        body=(
            Predicate("acceso_en_momento", (X,)),
            Predicate("acusa", (X, Y)),
        ),
    ))

    return kb


CASE = CrimeCase(
    id="sabotaje_pharmax",
    title="El Sabotaje en Laboratorio Pharmax",
    suspects=("tec_rios", "asistente_mora", "dra_santos", "director_vega"),
    narrative=__doc__,
    description=(
        "Cuatro años de investigacion farmacéutica destruida en una noche. "
        "Un caso donde motivo economico, ausencia de coartada y registro de acceso "
        "convergen para identificar al saboteador."
    ),
    create_kb=crear_kb,
    queries=(
        QuerySpec(
            description="La Dra. Santos esta descartada?",
            goal=Predicate("descartado", (Term("dra_santos"),)),
        ),
        QuerySpec(
            description="Tecnico Ríos tiene conflicto de intereses con Syntek Corp.?",
            goal=Predicate("conflicto_intereses", (Term("tec_rios"), Term("syntek_corp"))),
        ),
        QuerySpec(
            description="Tecnico Ríos es culpable?",
            goal=Predicate("culpable", (Term("tec_rios"),)),
        ),
        QuerySpec(
            description="La denuncia de Asistente Mora es una denuncia informada?",
            goal=Predicate("denuncia_informada", (Term("asistente_mora"), Term("tec_rios"))),
        ),
        QuerySpec(
            description="Todo culpable tuvo acceso en el momento del sabotaje?",
            goal=ForallGoal(
                "$X",
                Predicate("culpable", (Term("$X"),)),
                Predicate("acceso_en_momento", (Term("$X"),)),
            ),
        ),
    ),
)