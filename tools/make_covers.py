from playwright.sync_api import sync_playwright
import os, random, base64
B=lambda p:base64.b64encode(open(p,'rb').read()).decode()
FD=''+os.path.dirname(os.path.abspath(__file__))+'/assets/'
FONTS=''.join(f"@font-face{{font-family:'MA';font-weight:{w};src:url(data:font/ttf;base64,{B(FD+'MontserratAlternates-'+n+'.ttf')})}}" for w,n in [(500,'Medium'),(600,'SemiBold'),(700,'Bold'),(800,'ExtraBold')])
LOGO=B(''+os.path.dirname(os.path.abspath(__file__))+'/assets/logo.png')
AV={'ismat':B(''+os.path.dirname(os.path.abspath(__file__))+'/assets/av_ismat.png'),'shamil':B(''+os.path.dirname(os.path.abspath(__file__))+'/assets/av_shamil.png')}

TOOTH = ("M10 30 C10 10 25 4 35 8 C42 3 58 3 65 8 C75 4 90 10 90 30 C90 50 86 62 82 72 "
         "C80 100 78 130 72 155 C70 162 62 162 60 155 C57 135 55 112 50 100 C45 112 43 135 40 155 "
         "C38 162 30 162 28 155 C22 130 20 100 18 72 C14 62 10 50 10 30 Z")
CROWN = ("M10 30 C10 10 25 4 35 8 C42 3 58 3 65 8 C75 4 90 10 90 30 C90 50 86 62 82 72 "
         "L18 72 C14 62 10 50 10 30 Z")
INCISOR = "M8 14 C8 4 16 0 30 0 C44 0 52 4 52 14 L50 58 C49 66 42 70 30 70 C18 70 11 66 10 58 Z"
HL = "M20 22 C22 14 30 12 36 14"

DEFS = """
<defs>
 <linearGradient id="enamel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".55" stop-color="#F4F7FB"/><stop offset="1" stop-color="#D9E1EC"/></linearGradient>
 <linearGradient id="root" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F6EEDC"/><stop offset="1" stop-color="#E8D8B6"/></linearGradient>
 <linearGradient id="gum" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F6A4B2"/><stop offset="1" stop-color="#E77E92"/></linearGradient>
 <linearGradient id="bone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F7ECD6"/><stop offset="1" stop-color="#EAD6AF"/></linearGradient>
 <linearGradient id="ti" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8A95A8"/><stop offset=".3" stop-color="#E9EEF5"/><stop offset=".55" stop-color="#B7C1CF"/><stop offset="1" stop-color="#6E7A8E"/></linearGradient>
 <linearGradient id="zr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".6" stop-color="#F3F6FA"/><stop offset="1" stop-color="#E3EAF3"/></linearGradient>
 <linearGradient id="metal" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5E6676"/><stop offset=".5" stop-color="#A7AFBD"/><stop offset="1" stop-color="#4D5463"/></linearGradient>
 <linearGradient id="acryl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F59AAB"/><stop offset="1" stop-color="#D96A80"/></linearGradient>
 <radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".9"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>
 <filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="6" stdDeviation="7" flood-color="#1B2B4B" flood-opacity=".18"/></filter>
 <filter id="soft"><feGaussianBlur stdDeviation="2"/></filter>
</defs>"""

def bone(y, x0=0, x1=760, dip=None, seed=1):
    rnd = random.Random(seed)
    if dip:
        cx, w, d = dip
        top = f"M{x0} {y} L{cx-w} {y} C{cx-w*.5} {y} {cx-w*.6} {y+d} {cx} {y+d} C{cx+w*.6} {y+d} {cx+w*.5} {y} {cx+w} {y} L{x1} {y}"
    else:
        top = f"M{x0} {y} L{x1} {y}"
    s = f'<path d="{top} L{x1} 520 L{x0} 520 Z" fill="url(#bone)"/>'
    s += f'<path d="{top}" fill="none" stroke="#D9BE8E" stroke-width="7" stroke-linecap="round"/>'
    for _ in range(70):
        px = rnd.uniform(x0 + 10, x1 - 10); py = rnd.uniform(y + 22, 510)
        if dip and abs(px - dip[0]) < dip[1] * .7 and py < y + dip[2] + 10: continue
        rx = rnd.uniform(4, 13); ry = rx * rnd.uniform(.5, .9)
        s += f'<ellipse cx="{px:.0f}" cy="{py:.0f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="#D7BB8A" opacity="{rnd.uniform(.35,.7):.2f}" transform="rotate({rnd.uniform(0,180):.0f} {px:.0f} {py:.0f})"/>'
    return s

def gum(y, x0=0, x1=760, papillae=()):
    d = f"M{x0} {y+10}"
    for px in papillae:
        d += f" L{px-34} {y+10} Q{px} {y-24} {px+34} {y+10}"
    d += f" L{x1} {y+10} L{x1} {y+52} Q{(x0+x1)/2} {y+62} {x0} {y+52} Z"
    return (f'<path d="{d}" fill="url(#gum)"/>'
            f'<path d="M{x0} {y+16} L{x1} {y+16}" stroke="#FFFFFF" stroke-opacity=".35" stroke-width="3"/>')

def tooth(x, y, s=1.1, rot=0, op=1, caries=False, root_vis=True):
    g = f'<g transform="translate({x} {y}) rotate({rot} 50 80) scale({s})" opacity="{op}" filter="url(#sh)">'
    g += f'<path d="{TOOTH}" fill="url(#root)" stroke="#CDB98F" stroke-width="2"/>'
    g += f'<path d="{CROWN}" fill="url(#enamel)" stroke="#C9D3E1" stroke-width="2"/>'
    g += '<path d="M34 14 C40 26 60 26 66 14" fill="none" stroke="#C9D3E1" stroke-width="2.4" stroke-linecap="round"/>'
    g += f'<path d="{HL}" stroke="#FFFFFF" stroke-width="5" fill="none" stroke-linecap="round"/>'
    if caries:
        g += '<path d="M60 22 c6 -3 12 2 10 9 c-2 6 -10 7 -13 2 c-2 -4 -1 -9 3 -11z" fill="#6B4A2F" opacity=".85"/>'
    return g + '</g>'

def crown(x, y, s=1.1, fill="url(#enamel)", stroke="#C9D3E1"):
    return (f'<g transform="translate({x} {y}) scale({s})" filter="url(#sh)"><path d="{CROWN}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
            f'<path d="M34 14 C40 26 60 26 66 14" fill="none" stroke="#C9D3E1" stroke-width="2.4" stroke-linecap="round"/>'
            f'<path d="{HL}" stroke="#FFFFFF" stroke-width="5" fill="none" stroke-linecap="round"/></g>')

def implant(cx, top, L=170, w=34):
    s = f'<g filter="url(#sh)">'
    s += f'<path d="M{cx-12} {top} L{cx+12} {top} L{cx+9} {top+26} L{cx-9} {top+26} Z" fill="url(#ti)" stroke="#6E7A8E" stroke-width="1.5"/>'
    b = top + 26
    s += f'<path d="M{cx-w/2} {b} L{cx+w/2} {b} L{cx+w/2-6} {b+L-18} Q{cx} {b+L+6} {cx-w/2+6} {b+L-18} Z" fill="url(#ti)" stroke="#6E7A8E" stroke-width="1.5"/>'
    n = int(L / 15)
    for i in range(n):
        yy = b + 10 + i * (L - 26) / n
        ww = w / 2 + 8 - i * 6 / n
        s += f'<path d="M{cx-ww} {yy+5} L{cx+ww} {yy-5} L{cx+ww} {yy} L{cx-ww} {yy+10} Z" fill="#7C889B" opacity=".75"/>'
        s += f'<path d="M{cx-ww+2} {yy+4} L{cx+ww-2} {yy-6}" stroke="#F4F7FB" stroke-width="2" opacity=".8"/>'
    return s + '</g>'

def label(x, y, text, k, anchor="middle"):
    w = len(text) * 15.5 + 40
    x0 = x - w / 2 if anchor == "middle" else x
    return (f'<g filter="url(#sh)"><rect x="{x0}" y="{y-24}" width="{w}" height="40" rx="20" fill="#FFFFFF"/></g>'
            f'<text x="{x0+w/2}" y="{y+3}" text-anchor="middle" font-size="22" font-weight="700" fill="{k}">{text}</text>')

def note(x, y, text, k, tx, ty):
    return (f'<path d="M{x} {y} L{tx} {ty}" stroke="{k}" stroke-width="2.5" stroke-dasharray="5 5"/><circle cx="{tx}" cy="{ty}" r="6" fill="{k}"/>'
            f'<text x="{x}" y="{y-8}" text-anchor="middle" font-size="20" font-weight="600" fill="#3B4763">{text}</text>')

def spark(x, y, s, c, op=1):
    return f'<path transform="translate({x} {y}) scale({s})" d="M0-20C2-6 6-2 20 0C6 2 2 6 0 20C-2 6-6 2-20 0C-6-2-2-6 0-20z" fill="{c}" opacity="{op}"/>'

def scene(n, k):
    if n == 1:
        s = bone(195, seed=2)
        s += tooth(15, 80, 1.15) + tooth(245, 80, 1.15)
        s += f'<rect x="110" y="120" width="160" height="26" rx="10" fill="#E9EEF5"/>'
        s += crown(15, 80, 1.15) + crown(130, 80, 1.15) + crown(245, 80, 1.15)
        s += gum(155, 0, 372, (130, 245))
        s += f'<path d="M30 70 Q190 40 350 70" stroke="{k}" stroke-width="3" fill="none" stroke-dasharray="7 6"/>'
        s += f'<line x1="380" y1="20" x2="380" y2="505" stroke="#C9D3E1" stroke-width="3" stroke-dasharray="8 8"/>'
        s += implant(567, 156, 210) + tooth(395, 80, 1.15) + crown(510, 80, 1.15) + tooth(625, 80, 1.15)
        s += gum(155, 388, 760, (510, 625))
        s += label(190, 32, "Мостик", k) + label(567, 32, "Имплант", k)
        s += '<text x="190" y="495" text-anchor="middle" font-size="19" font-weight="600" fill="#5E6A85">соседние зубы обтачивают</text>'
        s += '<text x="567" y="495" text-anchor="middle" font-size="19" font-weight="600" fill="#5E6A85">соседние зубы не трогают</text>'
        return s
    if n == 2:
        s = bone(206, seed=3) + tooth(30, 80, 1.3) + tooth(190, 80, 1.3)
        s += f'<circle cx="470" cy="185" r="70" fill="#E5484D" opacity=".13"/>'
        s += tooth(350, 150, 1.3, rot=42)
        s += gum(166, 0, 760, (190, 330))
        for r in (16, 28, 40):
            s += f'<path d="M{348-r*.3} {250-r} A{r} {r} 0 0 1 {348+r} {250+r*.3}" fill="none" stroke="#E5484D" stroke-width="4.5" stroke-linecap="round" opacity="{1-r/58:.2f}"/>'
        s += note(600, 110, "давит на соседний зуб", k, 352, 248)
        s += label(160, 32, "Норма", k) + label(600, 32, "Зуб мудрости", k)
        s += '<text x="380" y="495" text-anchor="middle" font-size="21" font-weight="600" fill="#5E6A85">растёт под углом и упирается в соседний зуб</text>'
        return s
    if n == 3:
        rnd = random.Random(7)
        s = bone(206, dip=(380, 150, 110), seed=5)
        for _ in range(70):
            px = 380 + rnd.uniform(-115, 115); py = 255 + rnd.uniform(-40, 60)
            if abs(px - 380) < 24: continue
            r = rnd.uniform(6, 12)
            s += f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r:.1f}" fill="#FFFDF7" stroke="#C9A877" stroke-width="2"/>'
        s += tooth(40, 80, 1.3) + tooth(590, 80, 1.3) + implant(380, 172, 220) + crown(315, 80, 1.3)
        s += gum(166, 0, 760, (230, 530))
        s += note(630, 430, "костный материал", k, 470, 290)
        s += note(150, 440, "нехватка кости", k, 280, 300)
        return s
    if n == 4:
        s = f'<circle cx="380" cy="270" r="230" fill="url(#glow)"/>'
        s += f'<g transform="translate(250 60) scale(2.6)" filter="url(#sh)"><path d="{TOOTH}" fill="url(#enamel)" stroke="#C9D3E1" stroke-width="1.4"/><path d="{HL}" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round"/>'
        s += '<circle cx="36" cy="40" r="4.5" fill="#16213A"/><circle cx="64" cy="40" r="4.5" fill="#16213A"/><circle cx="37.5" cy="38.5" r="1.4" fill="#fff"/><circle cx="65.5" cy="38.5" r="1.4" fill="#fff"/>'
        s += '<circle cx="27" cy="52" r="6" fill="#F6A4B2" opacity=".7"/><circle cx="73" cy="52" r="6" fill="#F6A4B2" opacity=".7"/>'
        s += '<path d="M40 52 Q50 62 60 52" stroke="#16213A" stroke-width="3" fill="none" stroke-linecap="round"/></g>'
        s += f'<g transform="translate(520 120) rotate(30)" filter="url(#sh)"><rect x="0" y="40" width="26" height="250" rx="13" fill="{k}"/><rect x="2" y="0" width="22" height="50" rx="6" fill="#FFFFFF" stroke="#C9D3E1" stroke-width="2"/>'
        for i in range(5):
            s += f'<rect x="{4+i*4}" y="4" width="2.5" height="40" fill="#9FD9F5"/>'
        s += '</g>'
        s += f'<g filter="url(#sh)"><circle cx="150" cy="140" r="62" fill="#FFFFFF"/></g><text x="150" y="132" text-anchor="middle" font-size="40" font-weight="800" fill="{k}">≈1</text><text x="150" y="166" text-anchor="middle" font-size="22" font-weight="700" fill="#5E6A85">год</text>'
        s += spark(110, 330, 1.6, k) + spark(640, 70, 1.2, "#F5B83D") + spark(600, 420, 1.0, k, .6) + spark(200, 450, .9, "#F5B83D")
        return s
    if n == 5:
        s = bone(250, seed=9)
        s += implant(210, 214, 180) + implant(550, 214, 180)
        s += (f'<g transform="translate(135 110) scale(1.5)" filter="url(#sh)"><path d="{CROWN}" fill="url(#enamel)" stroke="#C9D3E1" stroke-width="2"/>'
              f'<path d="M26 30 C26 20 34 18 50 18 C66 18 74 20 74 30 L72 66 L28 66 Z" fill="url(#metal)" opacity=".28"/>'
              f'<path d="M18 66 L82 66 L82 72 L18 72 Z" fill="url(#metal)"/><path d="{HL}" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/></g>')
        s += (f'<g transform="translate(475 110) scale(1.5)" filter="url(#sh)"><path d="{CROWN}" fill="url(#zr)" stroke="#D6DEE9" stroke-width="2"/>'
              f'<path d="M14 40 C16 58 22 68 30 72" stroke="#FFFFFF" stroke-width="6" fill="none" opacity=".9"/><path d="{HL}" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/></g>')
        s += gum(210, 0, 760, ())
        s += note(170, 470, "тёмная кромка у десны", k, 180, 212)
        s += label(210, 32, "Металлокерамика", k) + label(550, 32, "Цирконий", k)
        s += '<text x="590" y="462" text-anchor="middle" font-size="19" font-weight="600" fill="#3B4763">без металла, естественный цвет</text>'
        return s
    if n == 6:
        s = bone(225, seed=11)
        s += f'<g transform="translate(330 330)"><path d="{CROWN}" fill="#FFFFFF" fill-opacity=".7" stroke="{k}" stroke-width="3" stroke-dasharray="6 5"/></g>'
        s += tooth(120, 110, 1.15) + tooth(320, 110, 1.15, caries=True) + tooth(520, 110, 1.15)
        s += gum(185, 0, 760, (275, 475))
        s += note(600, 470, "зачаток постоянного зуба", k, 440, 380)
        s += note(560, 80, "кариес", k, 400, 140)
        s += f'<g transform="translate(680 120) rotate(-15)" filter="url(#sh)"><rect x="-6" y="40" width="12" height="130" rx="6" fill="#FFFFFF" stroke="#C9D3E1" stroke-width="2"/><circle r="48" fill="#F25C7A"/><path d="M0 0 m-32 0 a32 32 0 1 0 64 0 a21 21 0 1 0 -42 0 a10 10 0 1 0 20 0" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round"/></g>'
        s += label(150, 32, "Молочные зубы", k)
        return s
    if n == 7:
        s = bone(300, seed=13)
        for x in (150, 300, 460, 610):
            s += implant(x, 250, 150, 30)
        s += f'<path d="M40 250 C40 210 80 196 380 196 C680 196 720 210 720 250 L720 300 C720 320 700 326 380 326 C60 326 40 320 40 300 Z" fill="url(#acryl)" filter="url(#sh)"/>'
        xs = [60, 122, 182, 240, 296, 352, 408, 464, 520, 578, 638]
        for i, x in enumerate(xs):
            h = 92 - abs(i - 5) * 4
            s += f'<g transform="translate({x} {214-h+70}) scale({1.0} {h/70})" filter="url(#sh)"><path d="{INCISOR}" fill="url(#enamel)" stroke="#C9D3E1" stroke-width="1.6"/><path d="M14 12 C16 8 22 6 26 7" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round"/></g>'
        s += f'<path d="M60 236 Q380 210 700 236" stroke="#FFFFFF" stroke-opacity=".35" stroke-width="4" fill="none"/>'
        s += note(380, 470, "протез держится на 4 имплантах", k, 460, 380)
        s += spark(700, 90, 1.4, k) + spark(70, 120, 1.0, "#F5B83D")
        return s

OUT = os.environ.get("OUT", os.path.join(os.getcwd(), "out"))
POSTS = [
    (1, "17", "Имплант или мостик: что выбрать?", "ismat"),
    (2, "18", "Зуб мудрости: удалять или нет?", "shamil"),
    (3, "19", "«Не хватает кости». Что это значит?", "ismat"),
    (4, "20", "Когда первый раз вести ребёнка к стоматологу?", "shamil"),
    (5, "21", "Цирконий или металлокерамика?", "ismat"),
    (6, "22", "Нужно ли лечить молочные зубы?", "shamil"),
    (7, "23", "Если зубов почти не осталось", "ismat"),
]
DOC = {"ismat": ("Исмат Дабузович", "ортопед, хирург, имплантолог", "#2F6BFF", "#E3ECFF", "#F1F5FF"),
       "shamil": ("Шамиль Ильясович", "терапевт, хирург, гигиенист", "#0E9F7E", "#D6F4EC", "#EEFBF7")}

HTML = """<html><head><style>
{fonts} body{{margin:0}}
.c{{width:1080px;height:1080px;background:{bg};font-family:MA,Inter,sans-serif;color:#16213A;position:relative;overflow:hidden}}
.top{{position:absolute;left:72px;right:72px;top:56px;display:flex;align-items:center;justify-content:space-between}}
.brand{{display:flex;align-items:center;gap:16px;font-size:28px;font-weight:700}}
.logo{{width:72px;height:72px;border-radius:50%;box-shadow:0 6px 16px rgba(29,78,216,.3)}}
.tag{{font-size:22px;font-weight:700;color:{k};background:#fff;border-radius:999px;padding:10px 20px;box-shadow:0 4px 14px rgba(27,43,75,.08)}}
.panel{{position:absolute;left:72px;top:148px;width:936px;height:600px;border-radius:36px;background:linear-gradient(180deg,#FFFFFF 0%,{t} 100%);box-shadow:0 18px 40px rgba(27,43,75,.10);overflow:hidden}}
.panel:before{{content:"";position:absolute;inset:0;background-image:radial-gradient({k}22 1.6px,transparent 1.6px);background-size:26px 26px;opacity:.6}}
.panel svg{{position:absolute;left:88px;top:40px;width:760px;height:520px}}
.title{{position:absolute;left:72px;right:72px;top:784px;font-size:56px;line-height:1.12;font-weight:700;letter-spacing:-.5px}}
.bot{{position:absolute;left:72px;right:72px;bottom:56px;display:flex;justify-content:space-between;align-items:center}}
.doc{{display:flex;align-items:center;gap:14px}}
.av{{width:76px;height:76px;border-radius:50%;border:4px solid #fff;box-shadow:0 0 0 3px {k},0 6px 16px rgba(27,43,75,.15)}}
.dn{{font-size:26px;font-weight:700}} .dr{{font-size:20px;color:#5E6A85;font-weight:500}}
.ph{{font-size:28px;font-weight:700;color:#16213A;background:#fff;border-radius:16px;padding:12px 20px;box-shadow:0 4px 14px rgba(27,43,75,.08)}}
</style></head><body><div class="c">
<div class="top"><div class="brand"><img class="logo" src="data:image/png;base64,{logo}">Dental clinic MEDI+</div><div class="tag">Полезно знать</div></div>
<div class="panel"><svg viewBox="0 0 760 520" font-family="MA">{defs}{ill}</svg></div>
<div class="title">{title}</div>
<div class="bot"><div class="doc"><img class="av" src="data:image/png;base64,{av}"><div><div class="dn">{dn}</div><div class="dr">{dr}</div></div></div><div class="ph">8 (911) 211-11-30</div></div>
</div></body></html>"""

os.makedirs(OUT, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1080})
    for n, day, title, d in POSTS:
        dn, dr, k, t, bg = DOC[d]
        pg.set_content(HTML.format(bg=bg, t=t, k=k, defs=DEFS, ill=scene(n, k), title=title, dn=dn, dr=dr, fonts=FONTS, logo=LOGO, av=AV[d]))
        pg.screenshot(path=f"{OUT}/post_{day}.png")
    b.close()
print("done")
