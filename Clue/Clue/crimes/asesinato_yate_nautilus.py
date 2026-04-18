"""
asesinato_yate_nautilus.py — Asesinato a Bordo del Yate Nautilus

Durante una travesia nocturna por el Mediterraneo, el magnate Alejandro Varela cayo por la borda del yate privado Nautilus y fue hallado muerto en el agua al amanecer.
En la cubierta de popa se encontro su reloj roto y un boton desgarrado de un saco masculino.
El boton desgarrado pertenece al saco del socio comercial Marcos Duarte.
Marcos Duarte iba a ser demandado por Alejandro al dia siguiente por desvio de fondos de la empresa.
Sofia Rios, la nueva novia, hereda toda la fortuna segun el testamento firmado la semana anterior.
Alicia Varela, la ex esposa, perderia su pension alimenticia en cuanto Alejandro se casara con Sofia.
El Capitan Olmos estuvo al mando del puente toda la noche con tres tripulantes como testigos independientes.
La Chef Renata estuvo en la cocina preparando el desayuno; la camara de seguridad de la cocina registra toda su jornada.
El Dr. Pacheco, medico personal, dice que estaba dormido en su camarote y no tiene coartada verificada.
Marcos Duarte, Sofia Rios, Alicia Varela y el Dr. Pacheco no tienen coartada verificada por medios objetivos.
Marcos declara que Sofia estuvo con el en el salon principal toda la noche.
Sofia declara que Marcos estuvo con ella en el salon principal toda la noche.
El Dr. Pacheco acusa directamente a Marcos Duarte.

Como detective, he llegado a las siguientes conclusiones:
Quien tiene registro en camara de seguridad que lo ubica lejos de la escena queda descartado.
Quien estuvo al mando del puente con testigos independientes tambien queda descartado.
Quien hereda con un testamento firmado poco antes del crimen tiene motivo economico.
Quien perderia un beneficio economico a causa de los planes de la victima tambien tiene motivo economico.
Quien iba a ser demandado por la victima tiene motivo defensivo.
Tener motivo economico o motivo defensivo cuenta como tener algun motivo.
Quien dejo una prenda personal en la escena del crimen tiene evidencia fisica en su contra.
Quien tiene algun motivo, evidencia fisica en su contra y no tiene coartada verificada es culpable.
Si dos personas se dan coartada mutuamente, existe una alianza de coartadas entre ellas.
Quien forma alianza de coartadas con un culpable esta encubriendo el crimen.
Una acusacion es interesada cuando el acusador tambien tiene algun motivo.
"""

from src.crime_case import CrimeCase, QuerySpec
from src.predicate_logic import ExistsGoal, ForallGoal, KnowledgeBase, Predicate, Rule, Term


def crear_kb() -> KnowledgeBase:
    """Construye la KB segun la narrativa del modulo."""
    kb = KnowledgeBase()

    # Constantes del caso
    capitan_olmos = Term("capitan_olmos")
    chef_renata   = Term("chef_renata")
    marcos        = Term("marcos")
    sofia         = Term("sofia")
    alicia        = Term("alicia")
    dr_pacheco    = Term("dr_pacheco")
    alejandro     = Term("alejandro")   # victima

    # Variables para las reglas
    X = Term("$X")
    Y = Term("$Y")

    # ─── HECHOS ──────────────────────────────────────────────────────

    # Coartadas objetivas (verificadas por medios independientes)
    kb.add_fact(Predicate("registro_camara_seguridad", (chef_renata,)))
    kb.add_fact(Predicate("mando_puente_con_testigos", (capitan_olmos,)))

    # Sospechosos sin coartada verificada
    kb.add_fact(Predicate("sin_coartada", (marcos,)))
    kb.add_fact(Predicate("sin_coartada", (sofia,)))
    kb.add_fact(Predicate("sin_coartada", (alicia,)))
    kb.add_fact(Predicate("sin_coartada", (dr_pacheco,)))

    # Motivos
    kb.add_fact(Predicate("hereda_nuevo_testamento", (sofia,)))
    kb.add_fact(Predicate("perderia_beneficio", (alicia,)))
    kb.add_fact(Predicate("iba_a_ser_demandado_por", (marcos, alejandro)))

    # Evidencia fisica en la escena
    kb.add_fact(Predicate("prenda_personal_en_escena", (marcos,)))

    # Coartadas mutuas (cada direccion por separado, sin simetria implicita)
    kb.add_fact(Predicate("coartada_mutua", (marcos, sofia)))
    kb.add_fact(Predicate("coartada_mutua", (sofia, marcos)))

    # Acusaciones directas
    kb.add_fact(Predicate("acusa", (dr_pacheco, marcos)))

    # ─── REGLAS ──────────────────────────────────────────────────────

    # R1: registro en camara implica descartado
    kb.add_rule(Rule(
        head=Predicate("descartado", (X,)),
        body=(Predicate("registro_camara_seguridad", (X,)),),
    ))

    # R2: mando del puente con testigos implica descartado
    kb.add_rule(Rule(
        head=Predicate("descartado", (X,)),
        body=(Predicate("mando_puente_con_testigos", (X,)),),
    ))

    # R3: heredar con nuevo testamento implica motivo economico
    kb.add_rule(Rule(
        head=Predicate("motivo_economico", (X,)),
        body=(Predicate("hereda_nuevo_testamento", (X,)),),
    ))

    # R4: perderia beneficio implica motivo economico
    kb.add_rule(Rule(
        head=Predicate("motivo_economico", (X,)),
        body=(Predicate("perderia_beneficio", (X,)),),
    ))

    # R5: iba a ser demandado implica motivo defensivo
    kb.add_rule(Rule(
        head=Predicate("motivo_defensivo", (X,)),
        body=(Predicate("iba_a_ser_demandado_por", (X, Y)),),
    ))

    # R6: motivo economico cuenta como algun motivo
    kb.add_rule(Rule(
        head=Predicate("algun_motivo", (X,)),
        body=(Predicate("motivo_economico", (X,)),),
    ))

    # R7: motivo defensivo cuenta como algun motivo
    kb.add_rule(Rule(
        head=Predicate("algun_motivo", (X,)),
        body=(Predicate("motivo_defensivo", (X,)),),
    ))

    # R8: prenda personal en la escena implica evidencia fisica
    kb.add_rule(Rule(
        head=Predicate("evidencia_fisica", (X,)),
        body=(Predicate("prenda_personal_en_escena", (X,)),),
    ))

    # R9: motivo + evidencia fisica + sin coartada implica culpable
    kb.add_rule(Rule(
        head=Predicate("culpable", (X,)),
        body=(
            Predicate("algun_motivo", (X,)),
            Predicate("evidencia_fisica", (X,)),
            Predicate("sin_coartada", (X,)),
        ),
    ))

    # R10: coartada mutua implica alianza de coartadas
    kb.add_rule(Rule(
        head=Predicate("alianza_coartadas", (X, Y)),
        body=(Predicate("coartada_mutua", (X, Y)),),
    ))

    # R11: alianza de coartadas con culpable implica encubridor
    kb.add_rule(Rule(
        head=Predicate("encubridor", (X,)),
        body=(
            Predicate("alianza_coartadas", (X, Y)),
            Predicate("culpable", (Y,)),
        ),
    ))

    # R12: acusar teniendo algun motivo implica acusacion interesada
    kb.add_rule(Rule(
        head=Predicate("acusacion_interesada", (X, Y)),
        body=(
            Predicate("acusa", (X, Y)),
            Predicate("algun_motivo", (X,)),
        ),
    ))

    return kb


CASE = CrimeCase(
    id="asesinato_yate_nautilus",
    title="Asesinato a Bordo del Yate Nautilus",
    suspects=(
        "capitan_olmos",
        "chef_renata",
        "marcos",
        "sofia",
        "alicia",
        "dr_pacheco",
    ),
    narrative=__doc__,
    description=(
        "El magnate Alejandro Varela cayo por la borda del yate Nautilus durante una travesia. "
        "Seis sospechosos a bordo, un boton desgarrado en la cubierta, coartadas cruzadas y "
        "un nuevo testamento firmado hace una semana. Identifica al culpable, al encubridor, "
        "y verifica si hay alguna acusacion sesgada."
    ),
    create_kb=crear_kb,
    queries=(
        QuerySpec(
            description="¿La Chef Renata esta descartada?",
            goal=Predicate("descartado", (Term("chef_renata"),)),
        ),
        QuerySpec(
            description="¿Marcos tiene motivo defensivo?",
            goal=Predicate("motivo_defensivo", (Term("marcos"),)),
        ),
        QuerySpec(
            description="¿Marcos Duarte es culpable?",
            goal=Predicate("culpable", (Term("marcos"),)),
        ),
        QuerySpec(
            description="¿Sofia esta encubriendo el crimen?",
            goal=Predicate("encubridor", (Term("sofia"),)),
        ),
        QuerySpec(
            description="¿Existe algun culpable a bordo?",
            goal=ExistsGoal("$X", Predicate("culpable", (Term("$X"),))),
        ),
        QuerySpec(
            description="¿Todo culpable tiene evidencia fisica en su contra?",
            goal=ForallGoal(
                "$X",
                Predicate("culpable", (Term("$X"),)),
                Predicate("evidencia_fisica", (Term("$X"),)),
            ),
        ),
    ),
)
