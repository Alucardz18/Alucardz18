"""Generate the animated SVGs for the concept profile README (light + dark)."""
import os, random, sys

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

THEMES = {
    "dark": dict(bg="#0d1117", card="#161b22", border="#30363d", text="#e6edf3",
                 muted="#8b949e", accent="#ff8a3d", blue="#58a6ff", soft="#1f2a37",
                 term="#0b0f14"),
    "light": dict(bg="#ffffff", card="#f6f8fa", border="#d0d7de", text="#1f2328",
                  muted="#59636e", accent="#d4580a", blue="#0969da", soft="#dbe7f5",
                  term="#1f2328"),
}
SANS = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "Consolas, 'SF Mono', Menlo, 'Courier New', monospace"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def write(name, svg):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(svg)


# ---------------------------------------------------------------- HERO
def hero(t, mode):
    w, h = 1000, 320
    term_text = "#e6edf3"
    term_muted = "#8b949e"
    lines = [
        ("$ psql -d portfolio", term_muted),
        ("=> SELECT role, focus FROM nii_oye;", t["accent"] if mode == "dark" else "#ff9a52"),
        (" role      | focus", term_muted),
        ("-----------+---------------------------", term_muted),
        (" analyst   | SQL, Python, Power BI", term_text),
        (" reservist | $17M+ equipment tracked", term_text),
        (" game dev  | Ashbound, built in Godot", term_text),
        ("(3 rows)", term_muted),
    ]
    tl = []
    y = 104
    for i, (s, c) in enumerate(lines):
        tl.append(f'<text xml:space="preserve" class="ln" style="animation-delay:{0.4 + i * 0.35:.2f}s" x="584" y="{y}" '
                  f'fill="{c}" font-family="{MONO}" font-size="14">{esc(s)}</text>')
        y += 23 if i not in (1,) else 29
    cursor_y = y - 14
    pills = ["SQL", "Python", "Power BI", "Excel", "Godot"]
    px, pill_svg = 40, []
    for p in pills:
        pw = 18 + len(p) * 8.6
        pill_svg.append(f'<rect x="{px}" y="250" width="{pw:.0f}" height="30" rx="15" fill="{t["soft"]}"/>'
                        f'<text x="{px + pw / 2:.0f}" y="270" text-anchor="middle" font-family="{SANS}" '
                        f'font-size="14" font-weight="600" fill="{t["text"]}">{esc(p)}</text>')
        px += pw + 10
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Nii-Oye Kpakpo, data analyst">
<style>
.ln{{opacity:0;animation:fade .45s ease forwards}}
.up{{opacity:0;animation:rise .7s ease forwards}}
.cur{{animation:blink 1s steps(1) infinite}}
@keyframes fade{{to{{opacity:1}}}}
@keyframes rise{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes blink{{50%{{opacity:0}}}}
</style>
<rect width="{w}" height="{h}" rx="18" fill="{t["card"]}" stroke="{t["border"]}"/>
<g class="up">
<text x="40" y="70" font-family="{SANS}" font-size="14" font-weight="700" letter-spacing="3" fill="{t["accent"]}">NII-OYE KPAKPO</text>
<text x="40" y="122" font-family="{SANS}" font-size="40" font-weight="800" fill="{t["text"]}">I turn messy data</text>
<text x="40" y="170" font-family="{SANS}" font-size="40" font-weight="800" fill="{t["text"]}">into clear <tspan fill="{t["accent"]}">decisions.</tspan></text>
<text x="40" y="208" font-family="{SANS}" font-size="16" fill="{t["muted"]}">Data analyst · CS at North Carolina A&amp;T, Dec 2026</text>
<text x="40" y="231" font-family="{SANS}" font-size="16" fill="{t["muted"]}">U.S. Marine Corps Reserve · game developer on the side</text>
{"".join(pill_svg)}
</g>
<rect x="560" y="40" width="404" height="240" rx="12" fill="{t["term"]}"/>
<circle cx="582" cy="60" r="5.5" fill="#ff5f57"/><circle cx="600" cy="60" r="5.5" fill="#febc2e"/><circle cx="618" cy="60" r="5.5" fill="#28c840"/>
<text x="762" y="64" text-anchor="middle" font-family="{MONO}" font-size="12" fill="#8b949e">portfolio.sql</text>
{"".join(tl)}
<rect class="cur" x="664" y="{cursor_y - 13}" width="9" height="16" fill="{t["accent"]}"/>
</svg>'''


# ------------------------------------------------------- PROJECT CARDS
def card_shell(t, w, h, eyebrow, title, question, stat, stat_label, tools, chart):
    q = "".join(f'<text x="36" y="{112 + i * 21}" font-family="{SANS}" font-size="15" fill="{t["muted"]}">{esc(l)}</text>'
                for i, l in enumerate(question))
    sl = "".join(f'<text x="36" y="{208 + i * 19}" font-family="{SANS}" font-size="14" fill="{t["text"]}">{esc(l)}</text>'
                 for i, l in enumerate(stat_label))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">
<style>
.bar{{transform-box:fill-box;animation:grow 1.1s cubic-bezier(.2,.8,.2,1) both}}
.hb{{transform-origin:left center;animation-name:growx}}
.vb{{transform-origin:center bottom;animation-name:growy}}
.lbl{{opacity:0;animation:fade .5s ease forwards}}
@keyframes growx{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
@keyframes growy{{from{{transform:scaleY(0)}}to{{transform:scaleY(1)}}}}
@keyframes fade{{to{{opacity:1}}}}
</style>
<rect width="{w}" height="{h}" rx="16" fill="{t["card"]}" stroke="{t["border"]}"/>
<text x="36" y="44" font-family="{SANS}" font-size="12" font-weight="700" letter-spacing="2" fill="{t["accent"]}">{esc(eyebrow)}</text>
<text x="36" y="78" font-family="{SANS}" font-size="24" font-weight="800" fill="{t["text"]}">{esc(title)}</text>
{q}
<text x="36" y="190" font-family="{SANS}" font-size="44" font-weight="800" fill="{t["accent"]}">{esc(stat)}</text>
{sl}
<text x="36" y="{h - 26}" font-family="{MONO}" font-size="13" fill="{t["muted"]}">{esc(tools)}</text>
<line x1="540" y1="32" x2="540" y2="{h - 32}" stroke="{t["border"]}"/>
{chart}
</svg>'''


def hbars(t, rows, x0, y0, label_w, max_w, max_v, fmt, gap=30, highlight=None, ref=None):
    out = []
    for i, (lab, v) in enumerate(rows):
        y = y0 + i * gap
        is_ref = ref is not None and lab == ref
        col = t["accent"] if (highlight and lab in highlight) else t["blue"]
        bw = max_w * v / max_v
        out.append(f'<text x="{x0 + label_w - 10}" y="{y + 13}" text-anchor="end" font-family="{SANS}" '
                   f'font-size="13" font-weight="{700 if is_ref else 400}" fill="{t["text"] if not is_ref else t["accent"]}">{esc(lab)}</text>')
        if is_ref:
            out.append(f'<rect class="bar hb" style="animation-delay:{0.15 * i:.2f}s" x="{x0 + label_w}" y="{y}" width="{bw:.1f}" height="18" rx="4" '
                       f'fill="none" stroke="{t["accent"]}" stroke-width="2" stroke-dasharray="5 4"/>')
        else:
            out.append(f'<rect class="bar hb" style="animation-delay:{0.15 * i:.2f}s" x="{x0 + label_w}" y="{y}" width="{bw:.1f}" height="18" rx="4" fill="{col}"/>')
        out.append(f'<text class="lbl" style="animation-delay:{0.9 + 0.15 * i:.2f}s" x="{x0 + label_w + bw + 8:.1f}" y="{y + 14}" '
                   f'font-family="{SANS}" font-size="13" font-weight="700" fill="{t["text"]}">{fmt(v)}</text>')
    return "".join(out)


def card_supply(t):
    rows = [("First Class", 95.3), ("All orders", 54.8), ("Standard Class", 38.1)]
    chart = (f'<text x="580" y="62" font-family="{SANS}" font-size="13" font-weight="700" fill="{t["muted"]}">LATE DELIVERY RATE BY SHIPPING MODE</text>'
             + hbars(t, rows, 580, 92, 120, 220, 100, lambda v: f"{v}%", gap=42, highlight={"First Class"}))
    chart += (f'<text class="lbl" style="animation-delay:1.6s" x="580" y="236" font-family="{SANS}" font-size="13" fill="{t["muted"]}">'
              f'The premium 1-day tier is late 95% of the time.</text>')
    return card_shell(t, 1000, 284, "ANALYST MODE · PROJECT 01", "Supply Chain Automation Pipeline",
                      ["Why do most orders arrive late, and which", "shipping promise is breaking?"],
                      "54.8%", ["of 65,752 orders arrived late"],
                      "Python · pandas · SQLite · SQL · Power BI", chart)


def card_airbnb(t):
    months = [11083, 10552, 15985, 17530, 19128, 19314, 20711, 17640, 18001, 19091, 15723, 14501]
    names = "JFMAMJJASOND"
    x0, base, ch, bw, gap = 590, 220, 116, 22, 8
    mx = max(months)
    out = [f'<text x="580" y="62" font-family="{SANS}" font-size="13" font-weight="700" fill="{t["muted"]}">GUEST REVIEWS BY MONTH, 2021 TO 2024</text>']
    for i, v in enumerate(months):
        hgt = ch * v / mx
        x = x0 + i * (bw + gap)
        col = t["accent"] if i in (4, 5, 6) else t["blue"]
        out.append(f'<rect class="bar vb" style="animation-delay:{0.07 * i:.2f}s" x="{x}" y="{base - hgt:.1f}" width="{bw}" height="{hgt:.1f}" rx="3" fill="{col}"/>')
        out.append(f'<text x="{x + bw / 2}" y="{base + 18}" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{t["muted"]}">{names[i]}</text>')
    out.append(f'<text class="lbl" style="animation-delay:1.3s" x="{x0 + 6 * (bw + gap) + bw / 2}" y="{base - ch - 8}" text-anchor="middle" '
               f'font-family="{SANS}" font-size="12" font-weight="700" fill="{t["accent"]}">20.7K</text>')
    return card_shell(t, 1000, 284, "ANALYST MODE · PROJECT 02", "Asheville Airbnb Market Analysis",
                      ["Where do demand, price and supply meet", "in Asheville's short-term rental market?"],
                      "2,332", ["listings analyzed; demand peaks May to July"],
                      "MySQL · Python · Excel · Power Query", "".join(out))


def card_ev(t):
    rows = [("California", 3.41), ("D.C.", 2.60), ("Hawaii", 2.37), ("U.S. rate", 1.24),
            ("Texas", 0.89), ("N. Carolina", 0.77), ("Ohio", 0.49)]
    chart = (f'<text x="580" y="62" font-family="{SANS}" font-size="13" font-weight="700" fill="{t["muted"]}">SHARE OF VEHICLES THAT ARE FULLY ELECTRIC, 2023</text>'
             + hbars(t, rows, 580, 78, 100, 230, 3.41, lambda v: f"{v:.2f}%", gap=25,
                     highlight={"Texas", "N. Carolina", "Ohio"}, ref="U.S. rate"))
    return card_shell(t, 1000, 284, "ANALYST MODE · PROJECT 03", "U.S. EV Market Share",
                      ["Where is EV adoption lagging, and which", "big markets are the opportunity?"],
                      "15 of 23", ["large state markets trail the", "1.24% national EV rate"],
                      "SQL · Power BI", chart)


# ------------------------------------------------------- ASHBOUND SCENE
SPRITE = [
    "..HHHH..",
    ".HHHHHH.",
    ".HFEFEH.",
    ".HFFFFH.",
    "..SSSS..",
    ".CCCCCC.",
    "CCCCCCCC",
    ".CCCCCC.",
]
LEGS_A = ["..L..L..", "..L..L.."]
LEGS_B = [".L....L.", "L......L"]
SCOL = {"H": "#4b5563", "F": "#0b0f14", "E": "#ffb347", "S": "#ff6a2b", "C": "#6b7280", "L": "#374151"}


def pixels(grid, ox, oy, s):
    out = []
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch != ".":
                out.append(f'<rect x="{ox + c * s}" y="{oy + r * s}" width="{s}" height="{s}" fill="{SCOL[ch]}"/>')
    return "".join(out)


def ashbound(t, mode):
    w, h = 1000, 280
    rnd = random.Random(7)
    sky_top, sky_bot = ("#0b0f14", "#2a1410") if mode == "dark" else ("#2b1d2e", "#a9472a")
    embers = []
    for _ in range(34):
        x = rnd.randint(20, 980)
        sz = rnd.choice([3, 3, 4, 5])
        dur = rnd.uniform(4.5, 9)
        delay = -rnd.uniform(0, 9)
        col = rnd.choice(["#ff8a3d", "#ffb347", "#ff6a2b", "#ffd28a"])
        embers.append(f'<rect class="em" style="animation-duration:{dur:.1f}s;animation-delay:{delay:.1f}s" '
                      f'x="{x}" y="230" width="{sz}" height="{sz}" fill="{col}"/>')
    # far ruins (parallax), two copies for a seamless loop
    ruins = []
    for copy in (0, 1000):
        r2 = random.Random(3)
        x = 0
        while x < 1000:
            bw = r2.randint(30, 70)
            bh = r2.randint(30, 110)
            ruins.append(f'<rect x="{x + copy}" y="{214 - bh}" width="{bw}" height="{bh}" fill="#1a1216" opacity=".85"/>')
            x += bw + r2.randint(10, 60)
    # floating platforms (mid layer)
    plats = []
    for copy in (0, 1000):
        for (px, py, n) in [(120, 150, 4), (430, 120, 3), (760, 160, 5)]:
            for k in range(n):
                plats.append(f'<rect x="{px + copy + k * 20}" y="{py}" width="20" height="12" fill="#3b2a2a"/>'
                             f'<rect x="{px + copy + k * 20}" y="{py}" width="20" height="3" fill="#ff8a3d" opacity=".7"/>')
    s = 6
    cx, cy = 690, 214 - (len(SPRITE) + 2) * s
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Ashbound, a roguelite platformer built in Godot">
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{sky_top}"/><stop offset="1" stop-color="{sky_bot}"/></linearGradient>
<pattern id="ground" width="40" height="20" patternUnits="userSpaceOnUse">
<rect width="40" height="20" fill="#2a1d1d"/><rect width="20" height="10" fill="#33231f"/><rect x="20" y="10" width="20" height="10" fill="#33231f"/>
</pattern>
<linearGradient id="fade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{sky_top}" stop-opacity=".92"/><stop offset=".7" stop-color="{sky_top}" stop-opacity=".6"/><stop offset="1" stop-color="{sky_top}" stop-opacity="0"/></linearGradient>
<clipPath id="clip"><rect width="{w}" height="{h}" rx="16"/></clipPath>
</defs>
<style>
.em{{animation:float linear infinite}}
@keyframes float{{0%{{transform:translateY(0);opacity:0}}10%{{opacity:1}}100%{{transform:translateY(-230px);opacity:0}}}}
.far{{animation:scroll 40s linear infinite}}
.mid{{animation:scroll 16s linear infinite}}
.gr{{animation:tile .5s linear infinite}}
@keyframes scroll{{to{{transform:translateX(-1000px)}}}}
@keyframes tile{{to{{transform:translateX(-40px)}}}}
.hero{{animation:bob .36s steps(1) infinite}}
@keyframes bob{{50%{{transform:translateY(-4px)}}}}
.la{{animation:legs .36s steps(1) infinite}}
.lb{{animation:legs .36s steps(1) infinite reverse}}
@keyframes legs{{0%{{opacity:1}}50%{{opacity:0}}}}
.glow{{animation:pulse 2.4s ease-in-out infinite}}
@keyframes pulse{{50%{{opacity:.55}}}}
</style>
<g clip-path="url(#clip)">
<rect width="{w}" height="{h}" fill="url(#sky)"/>
<circle class="glow" cx="840" cy="70" r="34" fill="#ff8a3d" opacity=".85"/>
<g class="far">{"".join(ruins)}</g>
<g class="mid">{"".join(plats)}</g>
<g class="gr"><rect x="0" y="214" width="1080" height="66" fill="url(#ground)"/><rect x="0" y="214" width="1080" height="4" fill="#ff6a2b" opacity=".8"/></g>
{"".join(embers)}
<rect width="560" height="200" fill="url(#fade)"/>
<g class="hero">
{pixels(SPRITE, cx, cy, s)}
<g class="la">{pixels(LEGS_A, cx, cy + len(SPRITE) * s, s)}</g>
<g class="lb">{pixels(LEGS_B, cx, cy + len(SPRITE) * s, s)}</g>
</g>
<text x="40" y="58" font-family="{SANS}" font-size="12" font-weight="700" letter-spacing="3" fill="#ffb347">BUILDER MODE</text>
<text x="40" y="112" font-family="{MONO}" font-size="52" font-weight="700" letter-spacing="6" fill="#fff4e6">ASHBOUND</text>
<text x="42" y="144" font-family="{SANS}" font-size="16" fill="#f3d9c4">A roguelite platformer in Godot,</text>
<text x="42" y="166" font-family="{SANS}" font-size="16" fill="#f3d9c4">built with my senior design team</text>
</g>
<rect width="{w}" height="{h}" rx="16" fill="none" stroke="{t["border"]}"/>
</svg>'''


for mode, t in THEMES.items():
    write(f"hero-{mode}.svg", hero(t, mode))
    write(f"card-supply-{mode}.svg", card_supply(t))
    write(f"card-airbnb-{mode}.svg", card_airbnb(t))
    write(f"card-ev-{mode}.svg", card_ev(t))
    write(f"ashbound-{mode}.svg", ashbound(t, mode))
print("ok")
