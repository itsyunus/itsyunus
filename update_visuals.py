from pathlib import Path
import re, html, json, urllib.request
from datetime import date

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'assets'
LIGHT = dict(paper='#ffffff', ink='#111111', muted='#707070', dim='#999999', rule='#dddddd', accent='#666666', panel='#fafafa', soft='#f3f3f3')
DARK = dict(paper='#0d1117', ink='#e6edf3', muted='#9a9a9a', dim='#707070', rule='#353535', accent='#b6b6b6', panel='#111111', soft='#171717')
BASE_CSS = '''
*{box-sizing:border-box}
text{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono",monospace;fill:var(--ink)}
.small{font-size:12px;letter-spacing:1.5px}.body{font-size:16px}.muted{fill:var(--muted)}.dim{fill:var(--dim)}.accent{fill:var(--accent)}
.rule{stroke:var(--rule);stroke-width:1}.paper{fill:var(--paper)}.panel{fill:var(--panel);stroke:var(--rule);stroke-width:1}
@keyframes draw{to{stroke-dashoffset:0}}@keyframes rise{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
@keyframes fade{from{opacity:0}to{opacity:1}}@keyframes pulse{0%,100%{opacity:.4}50%{opacity:1}}
@keyframes march{to{stroke-dashoffset:-24}}@keyframes spin{to{transform:rotate(360deg)}}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.rise{opacity:0;animation:rise .65s cubic-bezier(.2,.7,.2,1) forwards;transform-box:fill-box;transform-origin:center}
.fade{opacity:0;animation:fade .7s ease forwards}.draw{stroke-dasharray:1400;stroke-dashoffset:1400;animation:draw 1.6s cubic-bezier(.6,0,.2,1) forwards}
.pulse{animation:pulse 2.4s ease-in-out infinite}.march{stroke-dasharray:3 9;animation:march 1.5s linear infinite}
.spin{transform-box:fill-box;transform-origin:center;animation:spin 18s linear infinite}
.grow{transform-box:fill-box;transform-origin:left center;animation:grow 1s cubic-bezier(.2,.7,.2,1) forwards}
@media(prefers-reduced-motion:reduce){.rise,.fade,.draw,.pulse,.march,.spin,.grow,.cell{animation:none!important;opacity:1!important;stroke-dashoffset:0!important;transform:none!important}}
'''

def esc(s): return html.escape(str(s), quote=False)
def svg(name, w, h, title, desc, content, palette):
    css = BASE_CSS + f':root{{--paper:{palette["paper"]};--ink:{palette["ink"]};--muted:{palette["muted"]};--dim:{palette["dim"]};--rule:{palette["rule"]};--accent:{palette["accent"]};--panel:{palette["panel"]};--soft:{palette["soft"]}}}'
    head = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" fill="none" role="img" aria-labelledby="title desc"><title id="title">{esc(title)}</title><desc id="desc">{esc(desc)}</desc><style>{css}</style><rect class="paper" width="{w}" height="{h}"/>'
    return head + content + '</svg>'
def dual(name, w, h, title, desc, content_fn):
    for folder, palette in [(ASSETS, LIGHT),(ASSETS/'dark', DARK)]:
        folder.mkdir(parents=True, exist_ok=True)
        (folder/f'{name}.svg').write_text(svg(name,w,h,title,desc,content_fn(palette),palette))

def section_content(n, label, p):
    return f'''<path d="M24 48H976" class="draw" stroke="var(--rule)"/><g class="rise"><text x="25" y="33" class="small muted">0{n}</text><text x="75" y="34" font-size="19" font-weight="700" letter-spacing="2">{esc(label.upper())}</text><circle cx="958" cy="29" r="4" fill="var(--accent)" class="pulse"/></g>'''
for n,label in [(1,'whoami'),(2,'system map'),(3,'selected work'),(4,'telemetry'),(5,'the route'),(6,'stack')]:
    dual(f's0{n}',1000,58,f'{n:02d} — {label}',f'Section {n}: {label}',lambda p,n=n,label=label: section_content(n,label,p))

def header(p):
    return f'''<path d="M42 358H958" class="draw" stroke="var(--rule)"/><circle cx="785" cy="190" r="148" stroke="var(--rule)" class="spin" opacity=".55"/><circle cx="785" cy="190" r="112" stroke="var(--rule)" opacity=".65"/><circle cx="785" cy="42" r="4" fill="var(--accent)" class="pulse"/><path d="M774 190h22M785 179v22" stroke="var(--accent)"/><g class="rise"><text x="52" y="61" class="small muted">YUNUS  /  DATA SCIENCE  /  MACHINE LEARNING</text><text x="48" y="147" font-size="48" font-weight="700" letter-spacing="-2">Shaik Mohammad</text><text x="48" y="202" font-size="48" font-weight="700" letter-spacing="-2">Yunus</text><text x="52" y="248" class="body muted">Data Specialist · Data Analytics · Applied ML</text><text x="52" y="282" class="body">Bengaluru, India  /  NVIDIA</text></g><g class="rise" style="animation-delay:.35s"><text x="693" y="178" class="small muted">CURRENT FOCUS</text><text x="693" y="207" font-size="18" font-weight="700">GPU TELEMETRY</text><text x="693" y="236" class="small muted">PIPELINES → INSIGHT → IMPACT</text></g><g class="fade" style="animation-delay:.8s"><rect x="52" y="315" width="9" height="9" fill="var(--accent)" class="pulse"/><text x="70" y="324" class="small muted">MEASURE · MODEL · SHIP</text></g>'''
dual('header-v1',1000,400,'Shaik Mohammad Yunus — Data and ML','Editorial profile header with a quiet animated orbit and professional focus.',header)

def whoami(p):
    cols=[('ROLE','Data Specialist','NVIDIA · Bengaluru'),('FOCUS','Data systems','Telemetry · ETL · analytics'),('INTERESTS','Applied ML','NLP · models · products')]
    out=['<rect x="24" y="20" width="952" height="205" rx="4" class="panel"/>']
    out.append('<text x="48" y="57" class="small muted">PROFILE / 2026</text><text x="48" y="91" font-size="22" font-weight="700">I turn complex operational data into trusted decisions.</text>')
    out.append('<path d="M48 112H952" class="rule"/>')
    for i,(a,b,c) in enumerate(cols):
        x=48+i*302
        out.append(f'<g class="rise" style="animation-delay:{.15+i*.12}s"><text x="{x}" y="143" class="small muted">{a}</text><text x="{x}" y="172" font-size="18" font-weight="700">{b}</text><text x="{x}" y="198" class="small muted">{c}</text></g>')
        if i<2: out.append(f'<path d="M{x+270} 128v78" class="rule"/>')
    out.append('<text x="48" y="220" class="small dim">MICROSOFT AI-900  /  ORACLE CERTIFIED CLOUD ENGINEER</text>')
    return ''.join(out)
dual('whoami',1000,245,'About Yunus','Data specialist focused on telemetry, analytics, and applied machine learning.',whoami)

def ecosystem(p):
    # map linking source data to foundations and shipped outcomes
    out=['<path d="M182 333H822M500 166V333M182 333V460M500 333V460M822 333V460" class="draw" stroke="var(--rule)"/>']
    out.append('<path d="M182 333H822M500 166V333M182 333V460M500 333V460M822 333V460" class="march" stroke="var(--accent)" opacity=".55"/>')
    nodes=[(500,110,260,110,'SIGNALS','GPU telemetry · 500K+ records'),(182,270,260,112,'DATA FOUNDATION','Python · SQL · ETL quality'),(500,270,260,112,'ANALYTICS','KPIs · dashboards · root cause'),(818,270,260,112,'PRODUCTS','Allocation · faster reporting'),(182,500,260,112,'OPERATIONS','250K+ records · Cautio'),(500,500,260,112,'RESEARCH','Character-aware NLP · PyTorch'),(818,500,260,112,'ENGINEERING','React · Rails · API systems')]
    for i,(cx,cy,w,h,a,b) in enumerate(nodes):
        x=cx-w/2;y=cy-h/2
        out.append(f'<g class="rise" style="animation-delay:{.12+i*.1}s"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" class="panel"/><circle cx="{x+23}" cy="{y+25}" r="4" fill="var(--accent)" class="pulse"/><text x="{x+38}" y="{y+30}" class="small muted">{a}</text><text x="{x+20}" y="{y+69}" font-size="14">{esc(b)}</text></g>')
    out.append('<circle cx="500" cy="333" r="23" stroke="var(--accent)" class="pulse"/><circle cx="500" cy="333" r="4" fill="var(--accent)"/>')
    return ''.join(out)
dual('ecosystem',1000,640,'Data and ML system map','Animated map of data sources, foundations, analytics, product outcomes, operations, research, and engineering.',ecosystem)

def projects(p):
    rows=[('01','CHARACTER-AWARE LANGUAGE MODEL','PyTorch · NLP · UD English Web Treebank','Improved perplexity on unseen words by 3% vs. a same-size baseline.'),('02','TRANSFORMER + SENTIMENT FOR TRADING','Sequence models · Flask · Go · React · AWS','Market and news signals, REST prediction API, and R back-testing.'),('03','MERAKI POLICY MANAGEMENT','React · Redux · Ruby on Rails','Dashboard features developed with product and engineering; 20+ requirements.'),('04','SCALABLE SERVERLESS FRAMEWORK','Event-driven systems · performance · cost analysis','Research accepted for publication in IJSREM, 2026.'),('05','THE COMPUTE HORIZON','Inference-time scaling · reasoning AI','Research manuscript submitted to JCTSA, 2026.')]
    out=[]
    for i,(num,title,tech,desc) in enumerate(rows):
        y=22+i*194
        out.append(f'<g class="rise" style="animation-delay:{.12+i*.18}s"><rect x="24" y="{y}" width="952" height="170" rx="3" class="panel"/><text x="50" y="{y+38}" class="small muted">WORK / {num}</text><text x="50" y="{y+74}" font-size="19" font-weight="700">{title}</text><text x="50" y="{y+104}" class="small accent">{esc(tech)}</text><path d="M50 {y+120}H950" class="rule"/><text x="50" y="{y+147}" font-size="14" class="muted">{esc(desc)}</text><circle cx="946" cy="{y+35}" r="4" fill="var(--accent)" class="pulse"/></g>')
    return ''.join(out)
dual('projects',1000,1000,'Selected projects','Projects, product work, and research spanning language modeling, trading systems, and serverless architecture.',projects)

def telemetry(p):
    metrics=[('500K+','GPU RECORDS ANALYZED'),('+40%','RESOURCE ALLOCATION EFFICIENCY'),('99.4%','VALIDATED DATA ACCURACY'),('12 HRS','SAVED EACH WEEK')]
    out=['<path d="M34 284H966" class="draw" stroke="var(--rule)"/>']
    for i,(v,l) in enumerate(metrics):
        x=44+i*238
        out.append(f'<g class="rise" style="animation-delay:{.1+i*.14}s"><text x="{x}" y="77" font-size="29" font-weight="700">{v}</text><text x="{x}" y="103" class="small muted">{l}</text><rect x="{x}" y="139" width="190" height="5" fill="var(--soft)"/><rect x="{x}" y="139" width="{[166,142,179,128][i]}" height="5" fill="var(--accent)" class="grow" style="animation-delay:{.4+i*.16}s"/><text x="{x}" y="194" class="small dim">NVIDIA / DATA OPERATIONS</text></g>')
    out.append('<path d="M47 238 C130 218 170 252 240 223 S360 249 435 216 S550 241 630 207 S760 233 850 198 S920 218 957 187" stroke="var(--accent)" stroke-width="2" class="draw"/><circle r="5" fill="var(--accent)" class="pulse"><animateMotion dur="7s" repeatCount="indefinite" path="M47 238 C130 218 170 252 240 223 S360 249 435 216 S550 241 630 207 S760 233 850 198 S920 218 957 187"/></circle>')
    return ''.join(out)
dual('telemetry',1000,320,'Animated data telemetry','Animated operational metrics and a live scanning line, based on experience metrics in Yunus’s CV.',telemetry)

CALENDAR_HTML = ''

def get_calendar():
    global CALENDAR_HTML
    raw=(ROOT/'work'/'contributions.html').read_text() if (ROOT/'work'/'contributions.html').exists() else ''
    if not raw:
        try:
            req=urllib.request.Request('https://github.com/users/itsyunus/contributions',headers={'User-Agent':'Mozilla/5.0'})
            raw=urllib.request.urlopen(req,timeout=20).read().decode()
        except Exception: raw=''
    CALENDAR_HTML = raw
    vals=[]
    for m in re.finditer(r'<td[^>]*data-date="(\d{4}-\d{2}-\d{2})"[^>]*data-level="(\d)"',raw): vals.append((m.group(1),int(m.group(2))))
    if len(vals)<300: raise RuntimeError('GitHub contribution calendar was unavailable; keeping the last generated activity graph.')
    return vals
CALENDAR=get_calendar()
ACTIVE_DAYS=sum(level>0 for _,level in CALENDAR)
CONTRIBUTIONS=0
for m in re.finditer(r'<tool-tip[^>]*for="contribution-day-component-[^"]+"[^>]*>(.*?)</tool-tip>',CALENDAR_HTML,re.S):
    txt=re.sub(r'<[^>]+>','',m.group(1)).strip()
    n=re.match(r'(\d+) contributions?',txt)
    if n: CONTRIBUTIONS+=int(n.group(1))

PUBLIC_REPOS=62
try:
    req=urllib.request.Request('https://api.github.com/users/itsyunus',headers={'User-Agent':'profile-readme-updater','Accept':'application/vnd.github+json'})
    PUBLIC_REPOS=json.loads(urllib.request.urlopen(req,timeout=20).read().decode())['public_repos']
except Exception:
    pass

def stats(p):
    values=[(str(CONTRIBUTIONS or 0),'CONTRIBUTIONS / 12 MONTHS'),(str(ACTIVE_DAYS),'ACTIVE DAYS'),(str(PUBLIC_REPOS),'PUBLIC REPOSITORIES')]
    out=['<path d="M38 242H962" class="draw" stroke="var(--rule)"/>']
    for i,(num,label) in enumerate(values):
        x=55+i*310
        out.append(f'<g class="rise" style="animation-delay:{.12+i*.18}s"><text x="{x}" y="110" font-size="40" font-weight="700">{num}</text><text x="{x}" y="142" class="small muted">{label}</text><rect x="{x}" y="174" width="250" height="1" fill="var(--rule)"/><rect x="{x}" y="174" width="{[206,170,222][i]}" height="2" fill="var(--accent)" class="grow" style="animation-delay:{.45+i*.18}s"/></g>')
    out.append('<text x="55" y="216" class="small dim">PUBLIC PROFILE SNAPSHOT · UPDATED WITH CONTRIBUTION CALENDAR</text>')
    return ''.join(out)
dual('github-stats',1000,280,'GitHub activity summary','Public contribution activity, days active, and public repository count.',stats)

def activity(p):
    # GitHub returns calendar cells in chronological column order; retain the latest 371.
    vals=CALENDAR[-371:]
    if len(vals)<371: vals=[('2026-01-01',0)]*(371-len(vals))+vals
    cell=11; gap=5; x0=43; y0=50
    out=['<text x="43" y="27" class="small muted">DAILY CONTRIBUTIONS / LAST 12 MONTHS</text>']
    for i,(d,level) in enumerate(vals):
        col,row=divmod(i,7); x=x0+col*(cell+gap); y=y0+row*(cell+gap)
        fill=['var(--soft)','var(--rule)','var(--dim)','var(--muted)','var(--accent)'][min(level,4)]
        out.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{fill}" class="cell" style="--i:{i};animation:fade .35s ease {i*2}ms both"/>')
    out.append(f'<path d="M43 194H957" class="rule"/>')
    # aggregate by week, draw a contribution trend line scaled only to the visible calendar levels
    weeks=[]
    for col in range(53): weeks.append(sum(level for _,level in vals[col*7:(col+1)*7]))
    maxv=max(weeks) or 1
    pts=[]
    for i,v in enumerate(weeks): pts.append((43+i*17.5,182-(v/maxv)*48))
    path='M'+' '.join((f'{x:.1f},{y:.1f}' if i==0 else f'L{x:.1f},{y:.1f}') for i,(x,y) in enumerate(pts))
    out.append(f'<path d="{path}" stroke="var(--accent)" stroke-width="2" class="draw"/><circle r="4" fill="var(--accent)" class="pulse"><animateMotion dur="10s" repeatCount="indefinite" path="{path}"/></circle>')
    out.append('<text x="43" y="222" class="small dim">LESS</text>')
    for i in range(5): out.append(f'<rect x="{846+i*17}" y="211" width="11" height="11" rx="2" fill="{["var(--soft)","var(--rule)","var(--dim)","var(--muted)","var(--accent)"][i]}"/>')
    out.append('<text x="944" y="222" class="small dim" text-anchor="end">MORE</text>')
    return ''.join(out)
dual('activity',1000,245,'Animated GitHub contribution graph','Animated daily GitHub contribution heatmap and weekly trend based on the public contribution calendar.',activity)

def timeline(p):
    items=[('2023','LANGUAGE MODEL','Character-aware NLP research'),('2024','BOARD INFINITY','Software engineering internship'),('MAR 2026','LAUNCHED GLOBAL','Product engineering / Meraki'),('JUN 2026','CAUTIO','Operations analytics'),('AUG 2026','B.TECH (HONS.)','Computer Science · LPU'),('OCT 2026','NVIDIA','GPU data specialist')]
    xs=[88,286,485,684,883,1082]
    out=['<path d="M58 126H1142" stroke="var(--rule)" class="axis draw"/>','<path d="M58 126H1142" stroke="var(--accent)" stroke-width="1" class="march"/>']
    for i,((when,org,desc),x) in enumerate(zip(items,xs)):
        up=i%2==0; y=126-48 if up else 126+60; align='start' if x<950 else 'end'; tx=x+(12 if align=='start' else -12)
        out.append(f'<g class="rise" style="animation-delay:{.16+i*.16}s"><circle cx="{x}" cy="126" r="7" fill="var(--paper)" stroke="var(--accent)" stroke-width="2"/><circle cx="{x}" cy="126" r="13" stroke="var(--accent)" class="pulse" opacity=".6"/><path d="M{x} 126V{y+(18 if up else -25)}" class="rule"/><text x="{tx}" y="{y}" text-anchor="{align}" class="small accent">{when}</text><text x="{tx}" y="{y+20}" text-anchor="{align}" font-size="13" font-weight="700">{org}</text><text x="{tx}" y="{y+40}" text-anchor="{align}" font-size="11" class="muted">{esc(desc)}</text></g>')
    out.append('<circle cx="1138" cy="126" r="4" fill="var(--accent)" class="pulse"/>')
    return ''.join(out)
dual('timeline',1200,250,'Development timeline','Animated timeline from neural language modeling and software engineering to product analytics and NVIDIA GPU data work.',timeline)

def experience(p):
    rows=[('01','OCT 2026 — PRESENT','DATA SPECIALIST','NVIDIA · Bengaluru','500K+ GPU telemetry records · 10+ KPI dashboards · 99.4% data accuracy'),('02','JUN 2026 — PRESENT','DATA ANALYST','CAUTIO · Bengaluru','250K+ operational records · 45% less manual reporting · 10+ hours saved weekly'),('03','MAR — MAY 2026','BUSINESS ANALYST INTERN','LAUNCHED GLOBAL · Bengaluru','React/Redux + Rails policy features · 20+ business requirements'),('04','JUN — AUG 2024','SOFTWARE ENGINEERING INTERN','BOARD INFINITY · Remote','C++ · algorithms · object-oriented programming · Git code reviews')]
    out=[]
    for i,(num,when,role,company,desc) in enumerate(rows):
        y=17+i*86
        out.append(f'<g class="rise" style="animation-delay:{.12+i*.16}s"><path d="M40 {y+75}H960" class="rule"/><text x="46" y="{y+24}" class="small dim">{num}</text><text x="96" y="{y+23}" class="small muted">{when}</text><text x="330" y="{y+25}" font-size="15" font-weight="700">{role}</text><text x="330" y="{y+48}" class="small accent">{company}</text><text x="600" y="{y+36}" font-size="12" class="muted">{esc(desc)}</text></g>')
    return ''.join(out)
dual('experience',1000,370,'Professional experience','Four roles with employers, dates, scope, and outcomes.',experience)

def stack(p):
    groups=[('DATA / ANALYTICS',['Python','SQL','MySQL','Power BI','Tableau','Excel','Pandas']),('ML / RESEARCH',['PyTorch','NLP','Transformers','NumPy','scikit-learn']),('ENGINEERING / CLOUD',['C++','React','Redux','Rails','Flask','Go','AWS','Docker','Git'])]
    out=[]
    for gi,(label,tags) in enumerate(groups):
        y=35+gi*68
        out.append(f'<text x="42" y="{y}" class="small muted">{label}</text>')
        x=300
        for j,tag in enumerate(tags):
            width=23+len(tag)*8
            out.append(f'<g class="rise" style="animation-delay:{.08+(gi*len(tags)+j)*.035}s"><rect x="{x}" y="{y-20}" width="{width}" height="30" rx="2" class="panel"/><text x="{x+12}" y="{y}" font-size="12">{esc(tag)}</text></g>')
            x += width+10
    return ''.join(out)
dual('stack',1000,238,'Technical stack','Tools grouped into analytics, machine learning, and software engineering.',stack)

def footer(p):
    return '<path d="M30 22H970" class="draw" stroke="var(--rule)"/><circle cx="55" cy="62" r="5" fill="var(--accent)" class="pulse"/><circle cx="55" cy="62" r="15" stroke="var(--accent)" class="pulse" opacity=".5"/><text x="86" y="59" class="small muted">CURRENT STATUS</text><text x="86" y="83" font-size="16" font-weight="700">Building reliable data systems and applied ML.</text><text x="954" y="70" class="small accent" text-anchor="end">BENGALURU, INDIA · 2026</text>'
dual('footer',1000,110,'Current status','Current focus: reliable data systems and applied machine learning in Bengaluru.',footer)
# Dynamic card refreshed by update_visuals.py; snapshot generated from current public profile.
