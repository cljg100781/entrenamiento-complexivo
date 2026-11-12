"""Genera banco/pack-008.json (Seminario de Integración Curricular) a partir de p8/s*.txt."""
import json, re, glob, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'complexivo', 'banco', 'pack-008.json')

SEMANAS = {1: 'Semana 1 · Derecho Procesal Constitucional', 2: 'Semana 2 · Derecho Civil (Sucesiones)',
           3: 'Semana 3 · Derecho Procesal General', 4: 'Semana 4 · Derecho Administrativo',
           5: 'Semana 5 · Derecho Civil: Sujetos y Familia', 6: 'Semana 6 · Derecho Mercantil y Societario'}

BIB = {
 'CRE': 'Asamblea Constituyente del Ecuador. (2008). Constitución de la República del Ecuador. Registro Oficial 449, 20 de octubre de 2008, con sus enmiendas. https://www.asambleanacional.gob.ec/',
 'LOGJCC': 'Asamblea Nacional del Ecuador. (2009). Ley Orgánica de Garantías Jurisdiccionales y Control Constitucional. Registro Oficial Segundo Suplemento 52, 22 de octubre de 2009, con sus reformas. https://www.corteconstitucional.gob.ec/',
 'CC': 'Congreso Nacional del Ecuador. (2005). Código Civil (Codificación 2005-010). Registro Oficial Suplemento 46, 24 de junio de 2005; texto vigente con la reforma de 2024 al art. 21 y última actualización en el Segundo Suplemento del R.O. 61, 17 de junio de 2025. https://www.gob.ec/regulaciones/codigo-civil-codificacion-no-2005-010',
 'COGEP': 'Asamblea Nacional del Ecuador. (2015). Código Orgánico General de Procesos. Registro Oficial Suplemento 506, 22 de mayo de 2015; última reforma consultada: Cuarto Suplemento del R.O. 140, 7 de octubre de 2025. https://portal.compraspublicas.gob.ec/sercop/wp-content/uploads/2025/11/CODIGO-ORGANICO-GENERAL-DE-PROCESOS-COGEP.pdf',
 'COFJ': 'Asamblea Nacional del Ecuador. (2009). Código Orgánico de la Función Judicial. Registro Oficial Suplemento 544, 9 de marzo de 2009, con sus reformas. https://www.funcionjudicial.gob.ec/',
 'COA': 'Asamblea Nacional del Ecuador. (2017). Código Orgánico Administrativo. Registro Oficial Segundo Suplemento 31, 7 de julio de 2017; última reforma: 13 de octubre de 2025. https://www.gob.ec/',
 'CONA': 'Congreso Nacional del Ecuador. (2003). Código de la Niñez y Adolescencia. Registro Oficial 737, 3 de enero de 2003; art. 113 sustituido por la ley publicada en el R.O. 347, 14 de agosto de 2026. https://www.registroficial.gob.ec/',
 'CCOM': 'Asamblea Nacional del Ecuador. (2019). Código de Comercio. Registro Oficial Suplemento 497, 29 de mayo de 2019; reformado por la ley publicada en el Tercer Suplemento del R.O. 245, 7 de febrero de 2023. https://lotaip.bomberosquito.gob.ec/transparencia/2025/archivos/cdc25.pdf',
 'LC': 'Congreso Nacional del Ecuador. (1999). Ley de Compañías (Codificación 1999-031). Registro Oficial 312, 5 de noviembre de 1999; reformada por la Ley Reformatoria para la Optimización e Impulso Empresarial y el Fomento del Gobierno Corporativo, R.O. Suplemento 269, 15 de marzo de 2023. https://www.supercias.gob.ec/',
 'LOEI': 'Asamblea Nacional del Ecuador. (2020). Ley Orgánica de Emprendimiento e Innovación. Registro Oficial Suplemento 151, 28 de febrero de 2020. https://www.registroficial.gob.ec/',
 'LOGIDC': 'Asamblea Nacional del Ecuador. (2016). Ley Orgánica de Gestión de la Identidad y Datos Civiles. Registro Oficial Suplemento 684, 4 de febrero de 2016, con sus reformas. https://www.registrocivil.gob.ec/',
 'OC2417': 'Corte Interamericana de Derechos Humanos. (2017). Opinión Consultiva OC-24/17: Identidad de género, e igualdad y no discriminación a parejas del mismo sexo. 24 de noviembre de 2017. https://www.corteidh.or.cr/docs/opiniones/seriea_24_esp.pdf',
 'CCE6615': 'Corte Constitucional del Ecuador. (2019). Sentencia 66-15-JC/19 (medidas cautelares autónomas). https://www.corteconstitucional.gob.ec/',
 'CCE10213': 'Corte Constitucional del Ecuador. (2013). Sentencia 102-13-SEP-CC (interpretación conforme del art. 42 LOGJCC). https://www.corteconstitucional.gob.ec/',
 'CCE00116': 'Corte Constitucional del Ecuador. (2016). Sentencia 001-16-PJO-CC, 22 de marzo de 2016 (jurisprudencia vinculante sobre la acción de protección). https://www.corteconstitucional.gob.ec/',
 'CCE172525': 'Corte Constitucional del Ecuador. (2026). Sentencia 1725-25-JP/26 (procedencia de la acción de protección y vía ordinaria). Comentario: DGA Legal (2026), ¿Es subsidiaria la acción de protección? https://www.dgalegal.com/en/es-subsidiaria-la-accion-de-proteccion-el-nuevo-analisis-de-procedencia-que-establecio-la-corte-constitucional-en-la-sentencia-1725-25-jp-26/',
 'CCE115817': 'Corte Constitucional del Ecuador. (2021). Sentencia 1158-17-EP/21, 20 de octubre de 2021 (garantía de la motivación). https://www.corteconstitucional.gob.ec/',
 'CCE223122': 'Corte Constitucional del Ecuador. (2023). Sentencia 2231-22-JP/23, 7 de junio de 2023 (abuso del derecho en garantías jurisdiccionales). https://www.corteconstitucional.gob.ec/',
 'CCE36518': 'Corte Constitucional del Ecuador. (2021). Sentencia 365-18-JH/21 y acumulados (hábeas corpus correctivo). https://www.corteconstitucional.gob.ec/',
 'CCE83914': 'Corte Constitucional del Ecuador. (2021). Sentencia 839-14-EP/21 (acceso a la información pública y datos de terceros). https://www.corteconstitucional.gob.ec/',
 'CCE206414': 'Corte Constitucional del Ecuador. (2021). Sentencia 2064-14-EP/21, 27 de enero de 2021 (hábeas data y fotografía como dato personal). https://www.corteconstitucional.gob.ec/',
 'CCE2921': 'Corte Constitucional del Ecuador. (2021). Sentencia 29-21-JI y acumulado/21, 1 de diciembre de 2021 (publicidad de la información estatal). https://www.corteconstitucional.gob.ec/',
 'CCE4618': 'Corte Constitucional del Ecuador. (2022). Sentencia 46-18-AN/22 (reclamo previo en la acción por incumplimiento). https://www.corteconstitucional.gob.ec/',
 'CCE10321': 'Corte Constitucional del Ecuador. (2022). Sentencia 103-21-IS/22, 17 de agosto de 2022 (subsidiariedad de la acción de incumplimiento). https://www.corteconstitucional.gob.ec/',
 'CCE1321': 'Corte Constitucional del Ecuador. (2023). Sentencia 13-21-AN/23 (exigibilidad de recomendaciones de la CIDH). https://www.corteconstitucional.gob.ec/',
 'CCE000111': 'Corte Constitucional del Ecuador. (2011). Sentencia 0001-11-SIN-CC. Registro Oficial Segundo Suplemento 452, 19 de mayo de 2011 (afinidad tras el divorcio). https://www.corteconstitucional.gob.ec/',
 'CCE2815': 'Corte Constitucional del Ecuador. (2021). Sentencia 28-15-IN/21 (inconstitucionalidad de la preferencia materna en tenencia). https://www.corteconstitucional.gob.ec/',
 'CCE04813': 'Corte Constitucional del Ecuador. (2013). Sentencia 048-13-SCN-CC (Tabla de pensiones alimenticias mínimas). https://www.corteconstitucional.gob.ec/',
 'CCE01217': 'Corte Constitucional del Ecuador. (2017). Sentencia 012-17-SIN-CC (límites del apremio personal por alimentos). https://www.corteconstitucional.gob.ec/',
 'CCE20012': 'Corte Constitucional del Ecuador. (2021). Sentencia 200-12-JH/21 (retención indebida y apremio). https://www.corteconstitucional.gob.ec/',
}

RA = {'Recordar': 'Identifica {t} conforme a la norma vigente.', 'Comprender': 'Explica {t} y sus efectos jurídicos.',
      'Aplicar': 'Aplica las reglas de {t} a un caso concreto.', 'Analizar': 'Analiza un caso de {t} distinguiendo figuras afines.',
      'Evaluar': 'Evalúa la corrección de una decisión sobre {t} con base en la norma y la jurisprudencia.'}

def parse(path):
    items, cur = [], None
    for ln in open(path, encoding='utf-8'):
        ln = ln.rstrip('\n')
        if not ln.strip(): continue
        if ln.startswith('@ '):
            p = [x.strip() for x in ln[2:].split('|')]
            assert len(p) == 7, ln
            cur = {'id': p[0], 'area': int(p[1]), 'dificultad': int(p[2]), 'subarea': p[3], 'tema': p[4], 'demanda': p[5],
                   'refs': [r for r in p[6].split(',') if r], 'opciones': []}
            items.append(cur)
        elif ln.startswith('Q: '): cur['enunciado'] = ln[3:].strip()
        elif ln[:2] in ('+ ', '- '):
            t, j = ln[2:].split(' | ', 1)
            cur['opciones'].append({'texto': t.strip(), 'justificacion': j.strip(), 'ok': ln[0] == '+'})
        else: raise SystemExit(f'Línea no reconocida en {path}: {ln[:80]}')
    return items

def main():
    allit = []
    for f in sorted(glob.glob(os.path.join(HERE, 's[0-9].txt'))): allit += parse(f)
    out, ids = [], set()
    for it in allit:
        assert it['id'] not in ids, it['id']; ids.add(it['id'])
        o = it['opciones']; assert len(o) == 4 and o[0]['ok'] and not any(x['ok'] for x in o[1:]), it['id']
        assert it['enunciado'], it['id']
        for r in it['refs']: assert r in BIB, (it['id'], r)
        assert o[0]['justificacion'].startswith('Correcta.'), it['id']
        assert all(x['justificacion'].startswith('Incorrecta.') for x in o[1:]), it['id']
        sem = int(re.match(r'SIC(\d)-', it['id']).group(1))
        out.append({'id': it['id'], 'area': it['area'], 'dificultad': it['dificultad'], 'subarea': it['subarea'],
                    'tema': it['tema'], 'semana': sem, 'resultado': RA[it['demanda']].format(t=it['tema'].lower()),
                    'demanda': it['demanda'], 'enunciado': it['enunciado'],
                    'opciones': [{'texto': x['texto'], 'justificacion': x['justificacion']} for x in o],
                    'referencias': it['refs']})
    used = sorted({r for q in out for r in q['referencias']})
    pack = {'id': 'pack-008', 'titulo': f'Paquete 8 · Seminario de Integración Curricular, semanas 1 a 6 ({len(out)} preguntas)',
            'semanas': SEMANAS, 'bibliografia': {k: BIB[k] for k in used}, 'preguntas': out}
    json.dump(pack, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    from collections import Counter
    print(len(out), 'preguntas', dict(Counter(q['semana'] for q in out)), 'áreas', dict(Counter(q['area'] for q in out)))
    longest = sum(1 for q in out if len(q['opciones'][0]['texto']) >= max(len(x['texto']) for x in q['opciones']))
    print(f'correcta es la más larga (o empatada): {longest}/{len(out)} = {longest/len(out):.0%}')

main()
