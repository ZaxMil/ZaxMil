#!/usr/bin/env python3
"""Generate the original neon visual assets for the ZaxMil profile README.
Uses only Python standard library. All vector graphics are source-controlled SVG.
"""
from pathlib import Path
from html import escape
import random

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

BASE_DEFS = """
<defs>
 <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#071527"/><stop offset=".48" stop-color="#090f25"/><stop offset="1" stop-color="#1a0d33"/></linearGradient>
 <linearGradient id="panel" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#10233f"/><stop offset=".55" stop-color="#0c152e"/><stop offset="1" stop-color="#1c1036"/></linearGradient>
 <linearGradient id="cyan" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#23e5f5"/><stop offset="1" stop-color="#7a83ff"/></linearGradient>
 <linearGradient id="purple" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#1df4f4"/><stop offset=".5" stop-color="#7467fc"/><stop offset="1" stop-color="#e150fc"/></linearGradient>
 <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#12113c"/><stop offset=".65" stop-color="#303579"/><stop offset="1" stop-color="#061828"/></linearGradient>
 <radialGradient id="moon"><stop stop-color="#bdffff"/><stop offset=".55" stop-color="#4fb8fa"/><stop offset="1" stop-color="#7765ea"/></radialGradient>
 <radialGradient id="haze"><stop stop-color="#ab50ff" stop-opacity=".65"/><stop offset="1" stop-color="#aa45f8" stop-opacity="0"/></radialGradient>
 <filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="7"/></filter>
 <filter id="soft" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="21"/></filter>
 <pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse"><path d="M48 0H0V48" fill="none" stroke="#5b89d1" stroke-opacity=".10"/></pattern>
 <pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="#78d7fe" opacity=".14"/></pattern>
</defs>
"""

def save(name, width, height, inner):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
           f'viewBox="0 0 {width} {height}" role="img" aria-label="ZaxMil profile design">'
           + BASE_DEFS + inner + '</svg>\n')
    (ASSETS / name).write_text(svg, encoding="utf-8")
    print("created", name, len(svg))

def label(x, y, val, size=18, color="#b6c6e3", spacing=1.6, weight=600):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" letter-spacing="{spacing}" font-family="Segoe UI,Arial,sans-serif">{escape(val)}</text>'

def outer(w, h, r=24):
    return (f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{r}" fill="url(#bg)" stroke="#4173ae" stroke-opacity=".66" stroke-width="2"/>'
            f'<rect x="2" y="2" width="{w-4}" height="{h-4}" rx="{r}" fill="url(#grid)" opacity=".5"/>')

# HERO — cinematic skyline and hooded developer silhouette
random.seed(710)
hero = outer(1200, 407, 26)
hero += '<clipPath id="crop"><rect width="1200" height="407" rx="26"/></clipPath><g clip-path="url(#crop)">'
hero += '<rect x="570" y="0" width="630" height="407" fill="url(#sky)" opacity=".83"/>'
hero += '<circle cx="1002" cy="151" r="230" fill="url(#haze)" opacity=".6"/>'
hero += '<circle cx="999" cy="155" r="117" fill="#28ccfd" opacity=".38" filter="url(#soft)"/>'
hero += '<circle cx="999" cy="155" r="108" fill="url(#moon)" opacity=".92"/>'
hero += '<circle cx="999" cy="155" r="124" fill="none" stroke="#9b73ff" stroke-width="3" opacity=".7"/>'
hero += '<circle cx="999" cy="155" r="133" fill="none" stroke="#2de8ee" stroke-width="1" stroke-dasharray="8 14" opacity=".65"/>'
hero += '<path d="M840 160 Q986 91 1153 149" stroke="#e19dff" stroke-width="3" fill="none" opacity=".5"/>'
for _ in range(50):
    x=random.randint(620,1180); y=random.randint(35,300)
    r=random.choice([.8,1.2,1.6])
    hero += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#b0e9ff" opacity=".65"/>'
hero += '<path d="M610 350L693 282L732 307L810 227L875 287L940 216L1000 301L1070 229L1143 298L1200 264V407H610Z" fill="#2c3169" opacity=".67"/>'
hero += '<path d="M620 368L750 302L835 339L938 277L1010 346L1110 301L1200 342V407H620Z" fill="#171e4b" opacity=".95"/>'
# cyber city silhouettes
for x,w,h in [(620,27,85),(656,43,125),(717,34,90),(766,50,131),(821,30,101),(875,35,157),(924,20,108),(1120,32,120),(1168,37,158)]:
    hero += f'<path d="M{x} 407V{407-h}l{w//3} -13h{w//3}l{w//3} 13V407Z" fill="#071426" opacity=".95"/>'
    for yy in range(407-h+23,390,28):
        hero += f'<path d="M{x+8} {yy}h{max(5,w-16)}" stroke="#25d9f2" stroke-width="2" opacity=".3"/>'
# futuristic caped coder, purposeful silhouette, no fake photo
hero += '<ellipse cx="998" cy="404" rx="177" ry="25" fill="#00eaff" opacity=".24" filter="url(#soft)"/>'
hero += '<path d="M935 270 C904 300 873 345 857 407H1136C1111 341 1089 294 1051 270Z" fill="#0a1025" stroke="#6350aa" stroke-width="3"/>'
hero += '<path d="M941 269 C917 228 926 180 953 163Q1000 128 1039 165C1071 203 1072 241 1051 271L1029 294H963Z" fill="#0b142d" stroke="#3a73a3" stroke-width="3"/>'
hero += '<path d="M960 199Q1000 171 1034 203L1030 255Q997 283 965 251Z" fill="#101a38"/>'
hero += '<path d="M956 221L995 211L1036 221L1017 249H981Z" fill="#06101d" stroke="#22c7fa" stroke-width="2"/>'
hero += '<path d="M976 232h48" stroke="#42f4ff" stroke-width="3" opacity=".8"/>'
hero += '<path d="M945 289L982 330 1016 330 1054 287" stroke="#4b88c3" stroke-width="4" fill="none"/>'
hero += '<path d="M987 351l12 12 12-12M989 362h20" stroke="#1ce7f1" stroke-width="5" fill="none" stroke-linejoin="round"/>'
hero += '<path d="M947 290L895 399M1055 289L1109 399" stroke="#305580" stroke-width="3"/>'
hero += '<path d="M563 0V407" stroke="#23f0ef" stroke-opacity=".13" stroke-width="2"/>'
hero += '</g>'
# top chrome, deliberately prominent branded layout
hero += '<rect x="32" y="29" width="310" height="34" rx="17" fill="#0a1d35" stroke="#276a9a"/>'
hero += '<circle cx="54" cy="46" r="5" fill="#27f1ea"/>'
hero += label(68, 52, "ZAXMIL / SYSTEM ONLINE", 14, "#a3eaff", 1.7, 700)
hero += '<path d="M52 90H164" stroke="url(#cyan)" stroke-width="5" stroke-linecap="round"/>'
hero += label(48, 182, "ZAXMIL", 86, "#f4f7ff", 1.8, 800)
hero += label(52, 225, "DEVELOPER   /   BUILDER   /   CREATOR", 19, "#7ef1fc", 2.1, 700)
hero += '<path d="M52 249H479" stroke="#304c78" stroke-width="2"/>'
hero += label(52, 290, "Building software, games and AI-powered tools.", 21, "#c5cde5", .35, 500)
hero += label(52, 320, "Always shipping. Always learning.", 21, "#c5cde5", .35, 500)
for x, name in [(52,"OPEN SOURCE"),(219,"AUTOMATION"),(387,"GAME DEV")]:
    ww = 150 if name!="AUTOMATION" else 154
    hero += f'<rect x="{x}" y="347" width="{ww}" height="37" rx="12" fill="#0c2640" stroke="#276384"/>'
    hero += label(x+17, 371, name, 13, "#8ddffa", 1.0, 700)
save("hero.svg",1200,407,hero)

# SECTION HEADING — consistent visual system without markdown default heading styles
for slug, title, sub, no in [
    ("about","ABOUT / ME","A BRIEF INTRODUCTION","01"),
    ("signal","LIVE / SIGNAL","PUBLIC GITHUB METRICS","02"),
    ("works","FEATURED / WORK","SELECTED OPEN SOURCE PROJECTS","03"),
    ("stack","THE / TOOLKIT","TECHNOLOGIES BEHIND THE BUILDS","04")]:
    b='<rect x="1" y="1" width="1198" height="84" rx="18" fill="url(#panel)" stroke="#224e77"/>'
    b+='<rect x="24" y="17" width="5" height="51" rx="2" fill="url(#purple)"/>'
    b+=label(51,51,no,29,"#5bf1f5",1,800)
    b+=label(126,52,title,30,"#f6f7ff",1.8,800)
    b+=label(850,50,sub,14,"#a8b9db",1.4,600)
    b+='<path d="M52 71H1161" stroke="#283b60" stroke-width="1"/>'
    save(f"section-{slug}.svg",1200,86,b)

# ABOUT — original designed vector panel
about=outer(1200,214,24)
about+='<circle cx="117" cy="106" r="65" fill="#32d8ef" opacity=".2" filter="url(#glow)"/>'
about+='<rect x="47" y="46" width="139" height="122" rx="23" fill="#0f2850" stroke="#3c87ba" stroke-width="2"/>'
about+=label(68,131,"</>",56,"#52effb",0,800)
about+=label(231,86,"Hey, I am Zax.",35,"#eff8ff",0.3,800)
about+=label(231,127,"I turn ideas into software people can use.",23,"#c3cee3",0.2,500)
about+=label(231,161,"AI tools  •  developer workflows  •  desktop apps  •  games",20,"#77cfe0",0.4,600)
save("about.svg",1200,214,about)

def project_card(slug, number, name, kicker, subtitle, color, icon):
    W,H=1200,244
    b=outer(W,H,24)
    b+='<rect x="29" y="28" width="211" height="186" rx="20" fill="#102542" stroke="'+color+'" stroke-opacity=".62"/>'
    b+='<circle cx="136" cy="121" r="71" fill="'+color+'" opacity=".12"/>'
    b+='<circle cx="136" cy="121" r="56" fill="none" stroke="'+color+'" opacity=".44" stroke-width="2"/>'
    b+=icon
    b+=label(273,55,f"{number}  /  FEATURED REPOSITORY",15,color,1.6,700)
    b+=label(272,113,name,44,"#f6f7ff",.1,800)
    b+=label(273,155,subtitle,23,"#b6c7e2",.3,500)
    b+='<rect x="273" y="176" width="420" height="39" rx="11" fill="#10223d" stroke="#2b4b70"/>'
    b+=label(294,201,kicker,15,color,1.1,700)
    b+=label(1041,197,"VIEW REPO  >",15,"#bafcff",1.1,800)
    b+='<path d="M1025 1V241" stroke="#344978" stroke-opacity=".28"/>'
    save(f"project-{slug}.svg",W,H,b)
project_card("zerocoding","01","ZeroCoding","AI AGENTS / SKILLS","Modular skills that help coding agents work smarter.","#58effd",
             '<path d="M95 98L70 120 95 142M176 98L202 120 176 142M153 89L122 155" stroke="#58effd" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
project_card("downloader","02","FastDownloader Pro","DESKTOP / PERFORMANCE","A powerful download manager built for speed.","#7e8afc",
             '<path d="M136 74V142M101 119L136 155 171 119" stroke="#9d9dff" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M95 170H177" stroke="#9d9dff" stroke-width="8" stroke-linecap="round"/>')
project_card("skills","03","Agent Skill Bundle","DEVELOPER / TOOLING","A curated collection of useful AI-agent skills.","#b27dff",
             '<path d="M135 77L178 99V146L135 168 92 146V99Z M135 77V124M92 99L135 124 178 99M135 124V168" fill="none" stroke="#c5a2ff" stroke-width="6" stroke-linejoin="round"/>')

# TECH STRIP
tech=outer(1200,180,24)
for i,(name,color) in enumerate([("PYTHON","#62d5f9"),("TYPESCRIPT","#6888ff"),("C#","#b888f6"),("HTML","#fb986e"),("GITHUB","#a4aaf7"),("AUTOMATION","#51efd0")]):
    x=32+i*194
    tech+=f'<rect x="{x}" y="39" width="171" height="105" rx="18" fill="#10213b" stroke="{color}" stroke-opacity=".65"/>'
    tech+=f'<circle cx="{x+32}" cy="72" r="12" fill="{color}" opacity=".82"/>'
    tech+=label(x+19,114,name,17,"#e7efff",.55,700)
save("toolkit.svg",1200,180,tech)

footer=outer(1200,111,23)
footer+='<path d="M36 56H90L107 34 124 77 145 50 165 56H1132" fill="none" stroke="url(#purple)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
footer+='<rect x="430" y="24" width="376" height="63" rx="17" fill="#0c172e" stroke="#3b4f8c"/>'
footer+=label(460,62,"KEEP BUILDING. KEEP SHIPPING.",19,"#ccecff",1,800)
save("footer.svg",1200,111,footer)
