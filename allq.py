import re,json,sys
h=open('/home/claude/work/complexivo/index.html').read()
def grab(name):
    m=re.search(r'const '+name+r'=',h); i=m.end()
    dec=json.JSONDecoder(); v,end=dec.raw_decode(h,i); return v
Q=grab('Q'); EMB=grab('EMB')
items=[]
for x in Q: items.append((x['id'],'data',x['q'],[(o[0],o[1]) for o in x['o']]))
for p in EMB:
    for x in p['preguntas']: items.append((x['id'],p['id'],x['enunciado'],[(o['texto'],o['justificacion']) for o in x['opciones']]))
if __name__=='__main__':
    for pat in sys.argv[1:]:
        r=re.compile(pat,re.I); hits=[]
        for i,src,q,o in items:
            t=q+' || '+' || '.join(a+' ~ '+b for a,b in o)
            m=r.search(t)
            if m: hits.append(f'   {i} [{src}] …{t[max(0,m.start()-120):m.end()+120]}…')
        print(f'## {pat}: {len(hits)}'); print('\n'.join(hits))
