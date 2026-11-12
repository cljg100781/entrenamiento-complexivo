"""v3.7: incrusta los 8 paquetes (EMB), agrega el modo «Seminario de Integración» y sube versiones."""
import json, re, os, sys
ROOT = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/work/complexivo'
H = os.path.join(ROOT, 'index.html')
h = open(H, encoding='utf-8').read()

def rep(old, new, count=1):
    global h
    assert h.count(old) >= 1, 'no encontrado: ' + old[:70]
    h = h.replace(old, new, count)

# 1) EMB con todos los paquetes del banco
packs = []
for i in range(1, 9):
    p = os.path.join(ROOT, 'banco', f'pack-{i:03d}.json')
    if os.path.exists(p): packs.append(json.load(open(p, encoding='utf-8')))
m = re.search(r'const EMB=', h); dec = json.JSONDecoder(); _, end = dec.raw_decode(h, m.end())
h = h[:m.end()] + json.dumps(packs, ensure_ascii=False) + h[end:]

# 2) versión
h = re.sub(r'const APP_VERSION="[0-9.]+"', 'const APP_VERSION="3.7"', h)

# 3) mosaico en el inicio
rep('<div class="grid2">\n   <button class="tile" onclick="startDaily()">',
    '<button class="tile" onclick="seminarView()"><span class="tt">Seminario de Integración Curricular</span><span class="ds">${semSummary()}</span></button>\n  <div class="grid2">\n   <button class="tile" onclick="startDaily()">')

# 4) vista del seminario
SEM_JS = r'''
/* ---------- SEMINARIO DE INTEGRACIÓN CURRICULAR (INTC-02004-J) ----------
   Las preguntas del seminario tienen identificador SIC<semana>-<n>. Cada semana se practica por separado o en conjunto. */
const SEM={1:"Derecho Procesal Constitucional",2:"Derecho Civil: Sucesiones",3:"Derecho Procesal General",4:"Derecho Administrativo",5:"Derecho Civil: Sujetos y Familia",6:"Derecho Mercantil y Societario"};
function semOf(q){const m=/^SIC(\d+)-/.exec(q.id);return m?+m[1]:0}
function semName(w,pool){return SEM[w]||((pool.find(q=>semOf(q)==w)||{}).s)||("Semana "+w)}
function semStats(pool){const QS=store.get(K.qs,{});let seen=0,ok=0,tried=0;for(const q of pool){const s=QS[q.id];if(s&&s[0]){tried++;seen+=s[0];ok+=s[1]}}return {tried,acc:seen?ok/seen:null}}
function semSummary(){const p=bank().filter(semOf);if(!p.length)return "Aún no hay preguntas del seminario en el banco";const w=new Set(p.map(semOf)).size,st=semStats(p);
  return `${plural(p.length,"pregunta")} · ${plural(w,"semana")}`+(st.tried?` · ${st.tried} practicadas, ${Math.round(st.acc*100)} % de acierto`:" · practica por semana")}
function seminarView(){
  VIEW="sem";stopTick();stopSpeak();const p=bank().filter(semOf),ws=[...new Set(p.map(semOf))].sort((a,b)=>a-b);
  app().innerHTML=`<header class="top"><button class="ic" onclick="home()">‹</button><div class="mid"><div class="kicker">INTC-02004-J</div><b>Seminario de Integración</b></div></header>
  <main class="wrap">
  <div class="card"><p style="margin:0">El examen complexivo se construye con lo integrado en este seminario. Aquí practicas solo sus contenidos, semana por semana, con la norma vigente y la jurisprudencia que indicó cada docente.</p></div>
  ${p.length?`<button class="tile main" onclick="startSem(0,false)"><span class="tt">Mini simulacro del seminario</span><span class="ds">${Math.min(SEM_MINI,p.length)} preguntas de todas las semanas · con cronómetro · resultados al final</span></button>`:""}
  ${ws.map(w=>{const pw=p.filter(q=>semOf(q)==w),st=semStats(pw),pct=st.acc==null?null:Math.round(st.acc*100);
    return `<div class="card"><div class="kicker">Semana ${w}</div><h3 style="margin:2px 0 4px">${esc(semName(w,p))}</h3>
    <p class="muted" style="font-size:13px;margin:0 0 8px">${plural(pw.length,"pregunta")}${st.tried?` · has practicado ${st.tried} · acierto ${pct} %`:" · aún sin practicar"}</p>
    ${st.tried?`<div class="track ${pct<60?"y":""}"><i style="width:${Math.round(st.tried/pw.length*100)}%"></i></div>`:""}
    <div class="row" style="margin-top:10px"><button class="btn pri" onclick="startSem(${w},true)">Practicar</button><button class="btn" onclick="startSem(${w},false)">Con cronómetro</button></div></div>`}).join("")}
  ${p.length?"":`<div class="card"><p>No hay preguntas del seminario. Conéctate a internet para sincronizar el banco.</p></div>`}
  <p class="note">Contenidos según la guía del seminario: Procesal Constitucional (subárea 1.1.2), Sucesiones, Procesal General, Administrativo, Civil: Sujetos y Familia, y Mercantil y Societario. Las semanas siguientes se agregan cuando el banco se actualiza.</p>
  </main>`;
}
const SEM_MINI=30;
function startSem(w,fb){
  if(!canStart())return;
  const QS=store.get(K.qs,{});let p=bank().filter(q=>semOf(q)&&(!w||semOf(q)==w));
  if(!p.length)return;
  // primero lo no practicado o fallado, luego lo demás
  const sc=q=>{const s=QS[q.id];return !s||!s[0]?0:(s[1]/s[0]<1?1:2)};
  p=shuffle(p).sort((a,b)=>sc(a)-sc(b));
  let ids=p.map(q=>q.id);if(!w)ids=shuffle(ids.slice(0,SEM_MINI));else if(!fb)ids=ids.slice(0,20);else ids=shuffle(ids.slice(0,20));
  const t=w?`Seminario · Semana ${w}`:"Seminario · mini simulacro";
  newExam("prac",t,ids,fb?0:Math.round(ids.length*144000),fb);
}
'''
rep('function validErrs(){', SEM_JS + 'function validErrs(){')

# 5) práctica: filtrar por contenido
rep('<label class="fld">Número de preguntas</label>',
    '<label class="fld">Contenido</label>\n  <select id="pc"><option value="all">Todo el banco</option><option value="sem">Solo el Seminario de Integración Curricular</option></select>\n  <label class="fld">Número de preguntas</label>')
rep('let pool=shuffle(bank().filter(q=>ar.includes(q.a)).map(q=>q.id));',
    'const sm=(document.getElementById("pc")||{}).value==="sem";let pool=shuffle(bank().filter(q=>ar.includes(q.a)&&(!sm||semOf(q))).map(q=>q.id));')
rep('if(!pool.length){alert("No hay preguntas en esas áreas.");return}',
    'if(!pool.length){alert(sm?"No hay preguntas del seminario en esas áreas.":"No hay preguntas en esas áreas.");return}')

# 6) botón atrás del sistema en la vista del seminario: ya cae en «VIEW!=="home"» → home()
open(H, 'w', encoding='utf-8').write(h)

sw = os.path.join(ROOT, 'sw.js'); s = open(sw).read()
s = re.sub(r'complexivo-v[0-9.]+', 'complexivo-v3.7', s); open(sw, 'w').write(s)

mf = os.path.join(ROOT, 'banco', 'manifest.json'); M = json.load(open(mf))
for x in M['paquetes']:
    if x['id'] in ('pack-004', 'pack-006'): x['version'] += 1
P8 = json.load(open(os.path.join(ROOT, 'banco', 'pack-008.json')))
if not any(x['id'] == 'pack-008' for x in M['paquetes']):
    M['paquetes'].append({'id': 'pack-008', 'archivo': 'pack-008.json', 'version': 1, 'titulo': P8['titulo'], 'preguntas': len(P8['preguntas'])})
M['actualizado'] = '2026-11-12'
json.dump(M, open(mf, 'w'), ensure_ascii=False, indent=1)
print('ok', len(packs), 'paquetes;', sum(len(p['preguntas']) for p in packs), 'preguntas incrustadas')
