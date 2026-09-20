#!/usr/bin/env python3
"""Generates the profile README SVG assets (dark + light) into assets/."""
import json, datetime, pathlib
from xml.sax.saxutils import escape as esc

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)

SANS = "-apple-system,'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
SERIF = "Georgia,'Times New Roman',serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

THEMES = {
    "dark": dict(bg="#0d0f12", grid="#151a20", major="#1d232b", line="#2a3038", ink="#e8e9eb",
                 muted="#8a9099", dim="#565c65", accent="#8fb4ff",
                 lanes=["#a7b4c9", "#8ea2c0", "#b9c2d0", "#7f92ad"]),
    "light": dict(bg="#f6f5f1", grid="#ebe9e2", major="#dedbd2", line="#c9c5b9", ink="#15171a",
                  muted="#6b6f76", dim="#a3a29b", accent="#2f5fd0",
                  lanes=["#4f5b6e", "#66758d", "#3d4859", "#7a889e"]),
}


def head(w, h, c, uid, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{esc(label)}">'
            f'<defs><pattern id="g{uid}" width="20" height="20" patternUnits="userSpaceOnUse">'
            f'<path d="M20 0H0V20" fill="none" stroke="{c["grid"]}" stroke-width="1"/></pattern>'
            f'<pattern id="m{uid}" width="100" height="100" patternUnits="userSpaceOnUse">'
            f'<path d="M100 0H0V100" fill="none" stroke="{c["major"]}" stroke-width="1"/></pattern></defs>'
            f'<rect width="{w}" height="{h}" rx="10" fill="{c["bg"]}"/>'
            f'<rect width="{w}" height="{h}" rx="10" fill="url(#g{uid})"/>'
            f'<rect width="{w}" height="{h}" rx="10" fill="url(#m{uid})"/>'
            f'<rect x="10.5" y="10.5" width="{w-21}" height="{h-21}" rx="6" fill="none" stroke="{c["line"]}"/>')


def sheet_label(c, n, title, w):
    return (f'<text x="32" y="36" font-family="{MONO}" font-size="10.5" letter-spacing="1.6" fill="{c["muted"]}">'
            f'SHEET {n:02d} / 06  ·  {esc(title)}</text>'
            f'<line x1="32" y1="46" x2="{w-32}" y2="46" stroke="{c["line"]}"/>')


# ------------------------------------------------------------------ banner
def banner(c, uid):
    w, h = 1000, 320
    s = head(w, h, c, uid, "Daksh Yadav, Software and AI Engineer, IIT Kharagpur")
    s += sheet_label(c, 1, "PROFILE", w)
    s += (f'<text x="48" y="150" font-family="{SERIF}" font-size="66" fill="{c["ink"]}">Daksh Yadav</text>'
          f'<text x="50" y="188" font-family="{SANS}" font-size="20" fill="{c["muted"]}">Software &amp; AI Engineer</text>'
          f'<text x="50" y="214" font-family="{MONO}" font-size="11.5" letter-spacing="1.8" fill="{c["dim"]}">'
          f'IIT KHARAGPUR  ·  B.TECH.  ·  CLASS OF 2027</text>')
    # dimension line under the name
    y = 240
    s += (f'<line x1="50" y1="{y}" x2="430" y2="{y}" stroke="{c["dim"]}"/>'
          f'<line x1="50" y1="{y-6}" x2="50" y2="{y+6}" stroke="{c["dim"]}"/>'
          f'<line x1="430" y1="{y-6}" x2="430" y2="{y+6}" stroke="{c["dim"]}"/>'
          f'<rect x="212" y="{y-8}" width="66" height="16" fill="{c["bg"]}"/>'
          f'<text x="245" y="{y+4}" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{c["dim"]}">SCALE 1:1</text>')
    # five-signal router schematic
    sig = ["affordance", "semantics", "structure", "context", "index"]
    ys = [92, 126, 160, 194, 228]
    nx, ny = 830, 160
    for i, (name, yy) in enumerate(zip(sig, ys)):
        path = f"M700 {yy} C 765 {yy}, 775 {ny}, {nx-26} {ny}"
        s += (f'<rect x="588" y="{yy-12}" width="112" height="24" rx="4" fill="{c["bg"]}" stroke="{c["line"]}"/>'
              f'<text x="644" y="{yy+4}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{c["muted"]}">{name}</text>'
              f'<path d="{path}" fill="none" stroke="{c["line"]}" stroke-width="1.2"/>'
              f'<circle r="3" fill="{c["accent"]}" opacity="0"><animateMotion dur="3.4s" begin="{i*0.55:.2f}s" '
              f'repeatCount="indefinite" path="{path}"/>'
              f'<animate attributeName="opacity" values="0;1;1;0" dur="3.4s" begin="{i*0.55:.2f}s" repeatCount="indefinite"/></circle>')
    s += (f'<circle cx="{nx}" cy="{ny}" r="26" fill="{c["bg"]}" stroke="{c["accent"]}" stroke-width="1.4"/>'
          f'<circle cx="{nx}" cy="{ny}" r="22" fill="none" stroke="{c["accent"]}" opacity="0.5">'
          f'<animate attributeName="r" values="26;38" dur="3.4s" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values="0.5;0" dur="3.4s" repeatCount="indefinite"/></circle>'
          f'<text x="{nx}" y="{ny+4}" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{c["accent"]}">router</text>'
          f'<line x1="{nx+26}" y1="{ny}" x2="924" y2="{ny}" stroke="{c["accent"]}" stroke-width="1.2"/>'
          f'<path d="M918 {ny-4} L924 {ny} L918 {ny+4}" fill="none" stroke="{c["accent"]}" stroke-width="1.2"/>'
          f'<rect x="926" y="{ny-12}" width="34" height="24" rx="4" fill="{c["accent"]}"/>'
          f'<text x="943" y="{ny+4}" text-anchor="middle" font-family="{MONO}" font-size="9.5" fill="{c["bg"]}">DOM</text>')
    s += (f'<text x="588" y="272" font-family="{MONO}" font-size="10" letter-spacing="1.2" fill="{c["dim"]}">'
          f'FIG. 1  —  FIVE-SIGNAL ELEMENT RESOLVER (GIMBAL)</text>'
          f'<text x="{w-32}" y="{h-26}" text-anchor="end" font-family="{MONO}" font-size="10" fill="{c["dim"]}">REV 2026.09</text>')
    return s + '</svg>'


# ------------------------------------------------------------------ numbers
def numbers(c, uid):
    w, h = 1000, 226
    s = head(w, h, c, uid, "Selected results")
    s += sheet_label(c, 2, "BY THE NUMBERS", w)
    items = [("93%", ["reduction in", "form-filling time"], "EMORA HEALTH"),
             ("83%", ["faster peak gate entry,", "2 min down to 20 sec"], "PALE SYSTEM"),
             ("86%", ["of UI drift resolved", "without a runtime LLM"], "GIMBAL"),
             ("15,000+", ["students served by", "systems I built"], "PALE  \u00b7  TECH GYMKHANA")]
    col = (w - 64) / 4
    for i, (n, lines, src) in enumerate(items):
        x = 32 + i * col + (18 if i else 0)
        if i:
            s += f'<line x1="{32+i*col}" y1="70" x2="{32+i*col}" y2="{h-34}" stroke="{c["line"]}"/>'
        s += f'<text x="{x}" y="126" font-family="{SERIF}" font-size="50" fill="{c["ink"]}">{esc(n)}</text>'
        for j, ln in enumerate(lines):
            s += f'<text x="{x}" y="{150+j*17}" font-family="{SANS}" font-size="12.5" fill="{c["muted"]}">{esc(ln)}</text>'
        s += f'<text x="{x}" y="{198}" font-family="{MONO}" font-size="9.5" letter-spacing="1.4" fill="{c["accent"]}">{src}</text>'
    return s + '</svg>'


# ------------------------------------------------------------------ history
def history(c, uid):
    w, rowh, y0 = 1000, 46, 84
    Y = lambda r: y0 + rowh * r
    h = Y(13) + 52
    s = head(w, h, c, uid, "Career history drawn as a git branch graph")
    s += sheet_label(c, 4, "BRANCH HISTORY", w)
    TX, LX = 60, 290
    lane = {"axiom": 204, "gym": 156, "emora": 108, "pale": 108, "wede": 108, "inter": 108}
    col = {"axiom": c["accent"], "gym": c["lanes"][0], "emora": c["lanes"][1], "pale": c["lanes"][2],
           "wede": c["lanes"][3], "inter": c["lanes"][1]}
    # trunk
    s += f'<line x1="{TX}" y1="{Y(0)}" x2="{TX}" y2="{Y(13)}" stroke="{c["dim"]}" stroke-width="2"/>'
    # branches: name, start row (older), end row (newer), merged?
    br = [("gym", 9, 3, True), ("axiom", 6, 1, False), ("emora", 4, 2, True),
          ("pale", 7, 5, True), ("wede", 10, 8, True), ("inter", 12, 11, True)]
    for name, rs, re_, merged in br:
        lx, cl = lane[name], col[name]
        ys, ye = Y(rs), Y(re_)
        d = f"M{TX} {ys} C {TX} {ys-16}, {lx} {ys-10}, {lx} {ys-26} L {lx} {ye}"
        if merged:
            d = (f"M{TX} {ys} C {TX} {ys-16}, {lx} {ys-10}, {lx} {ys-26} L {lx} {ye} "
                 f"C {lx} {ye-14}, {TX} {ye-10}, {TX} {ye-26}")
        s += f'<path d="{d}" fill="none" stroke="{cl}" stroke-width="2" stroke-linecap="round"/>'
        s += f'<circle cx="{TX}" cy="{ys}" r="4" fill="{c["bg"]}" stroke="{cl}" stroke-width="2"/>'
        if merged:
            s += f'<circle cx="{TX}" cy="{ye-26}" r="4" fill="{cl}"/>'
        s += (f'<circle cx="{lx}" cy="{ye}" r="5.5" fill="{cl if merged else c["bg"]}" stroke="{cl}" stroke-width="2"/>')
    # HEAD + init
    s += (f'<circle cx="{TX}" cy="{Y(0)}" r="7" fill="{c["accent"]}"/>'
          f'<circle cx="{TX}" cy="{Y(0)}" r="12" fill="none" stroke="{c["accent"]}" opacity="0.5">'
          f'<animate attributeName="r" values="8;15" dur="3s" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values="0.6;0" dur="3s" repeatCount="indefinite"/></circle>'
          f'<circle cx="{TX}" cy="{Y(13)}" r="4" fill="{c["dim"]}"/>')
    # labels
    def big(r, x, name, dates, msg, cl):
        y = Y(r)
        return (f'<line x1="{x+12}" y1="{y}" x2="{LX-12}" y2="{y}" stroke="{c["line"]}" stroke-dasharray="2 4"/>'
                f'<text x="{LX}" y="{y-2}" font-family="{MONO}" font-size="13" fill="{cl}">{esc(name)}</text>'
                f'<text x="{w-32}" y="{y-2}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{c["dim"]}">{esc(dates)}</text>'
                f'<text x="{LX}" y="{y+15}" font-family="{SANS}" font-size="12.5" fill="{c["muted"]}">{esc(msg)}</text>')

    def small(r, text):
        return (f'<text x="{LX}" y="{Y(r)+4}" font-family="{MONO}" font-size="10.5" fill="{c["dim"]}">{esc(text)}</text>')
    s += (f'<text x="{LX}" y="{Y(0)+4}" font-family="{MONO}" font-size="13" fill="{c["accent"]}">HEAD → main</text>'
          f'<text x="{w-32}" y="{Y(0)+4}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{c["dim"]}">Sep \'26</text>')
    s += big(1, lane["axiom"], "gimbal", "Dec '25 – present",
             "Open-source self-healing E2E testing platform (formerly Axiom). Awardee, IIT KGP Innovation Challenge '26.", c["accent"])
    s += big(2, lane["emora"], "emora-health", "May '26 – Jul '26",
             "Credentialing infrastructure and self-healing form automation, New York. Form filling 93% faster.", col["emora"])
    s += big(3, lane["gym"], "tech-gymkhana", "Jun '25 – Jun '26",
             "Technology Coordinator. Led 6 secretaries; 4 production campus portals for 15,000+ students.", col["gym"])
    s += small(4, "branch  emora-health")
    s += big(5, lane["pale"], "pale", "Nov '25 – Apr '26",
             "Offline-first cryptographic QR entry system for the Central Library. Gate time 2 min to 20 sec.", col["pale"])
    s += small(6, "branch  gimbal")
    s += small(7, "branch  pale")
    s += big(8, lane["wede"], "wed-e", "Apr '25 – Jul '25",
             "Serverless AI platform. API throughput up 68%, compute cost down 65%, Recall@5 up 42%.", col["wede"])
    s += small(9, "branch  tech-gymkhana")
    s += small(10, "branch  wed-e")
    s += big(11, lane["inter"], "inter-iit-13", "Nov '24 – Dec '24",
             "Dream11 sports analytics engine at Inter IIT Tech Meet 13.0. Gold.", col["inter"])
    s += small(12, "branch  inter-iit-13")
    s += small(13, "init  IIT Kharagpur, B.Tech.")
    return s + '</svg>'


# ------------------------------------------------------------------ materials
def materials(c, uid):
    w = 1000
    cols = [("LANGUAGES & WEB", ["Python", "TypeScript", "Go", "C++", "SQL", "React", "Next.js", "Node.js", "Django", "Tailwind CSS"]),
            ("CLOUD & INFRASTRUCTURE", ["PostgreSQL", "MongoDB", "Redis", "SQLite", "Prisma", "AWS", "GCP", "Docker", "Kubernetes", "GitHub Actions", "Proxmox"]),
            ("AI, ML & DATA", ["Hugging Face", "LangChain", "LangGraph", "Qdrant", "Pinecone", "scikit-learn", "TensorFlow", "Pandas", "NumPy"]),
            ("TESTING & TOOLING", ["Playwright", "Cypress", "Selenium", "Vitest", "Jest", "Pytest", "Modal", "GraphQL", "Nginx", "OpenAPI"])]
    n = max(len(i) for _, i in cols)
    h = 96 + n * 24 + 26
    s = head(w, h, c, uid, "Skills")
    s += sheet_label(c, 5, "BILL OF MATERIALS", w)
    cw = (w - 64) / 4
    for k, (title, items) in enumerate(cols):
        x = 32 + k * cw + (18 if k else 0)
        if k:
            s += f'<line x1="{32+k*cw}" y1="66" x2="{32+k*cw}" y2="{h-30}" stroke="{c["line"]}"/>'
        s += f'<text x="{x}" y="82" font-family="{MONO}" font-size="10.5" letter-spacing="1.4" fill="{c["accent"]}">{esc(title)}</text>'
        for i, it in enumerate(items):
            yy = 110 + i * 24
            s += (f'<text x="{x}" y="{yy}" font-family="{MONO}" font-size="10" fill="{c["dim"]}">{i+1:02d}</text>'
                  f'<text x="{x+26}" y="{yy}" font-family="{SANS}" font-size="13.5" fill="{c["ink"]}">{esc(it)}</text>')
    return s + '</svg>'


# ------------------------------------------------------------------ text sheets
import textwrap


def bare(w, h, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{esc(label)}">')


def intro(c, uid):
    text = ("Software and AI engineer, B.Tech. at IIT Kharagpur (class of 2027). Founder of Gimbal (formerly Axiom), "
            "an open-source self-healing testing platform. Previously at Emora Health (New York) and Wed-E.")
    lines = textwrap.wrap(text, 132)
    h = 26 + 26 * len(lines)
    s = bare(1000, h, text)
    for i, ln in enumerate(lines):
        s += (f'<text x="32" y="{30+i*26}" font-family="{SANS}" font-size="16" fill="{c["ink"]}">{esc(ln)}</text>')
    return s + '</svg>'


def workhead(c, uid):
    s = bare(1000, 56, "Selected work")
    s += (f'<text x="32" y="36" font-family="{MONO}" font-size="10.5" letter-spacing="1.6" fill="{c["muted"]}">'
          f'SHEET 03 / 06  \u00b7  SELECTED WORK</text>'
          f'<line x1="32" y1="46" x2="968" y2="46" stroke="{c["line"]}"/>')
    return s + '</svg>'


WORK = [
    ("01", "gimbal", "Gimbal", "formerly Axiom", "TESTING INFRASTRUCTURE",
     "Open-source, self-healing end-to-end testing platform. A local MCP server for autonomous test generation "
     "and a five-signal resolver that repairs broken selectors without a runtime LLM. Awardee, IIT KGP "
     "Innovation Challenge 2026.", "https://github.com/dakshyadav1810/gimbal"),
    ("02", "metacortex", "MetaCortex", "", "LLM VERIFICATION",
     "Graph-of-thought reasoning system over the MetaKGP wiki, combining FAISS retrieval with multi-expert "
     "claim verification on LLaMA 3.3 70B.", "https://github.com/dakshyadav1810/metacortex"),
    ("03", "ferp", "fERP v2.0", "", "BROWSER EXTENSION",
     "Automates the IIT KGP ERP feedback forms and verifies every submission against the server. "
     "The CAPTCHA stays manual.", "https://github.com/dakshyadav1810/fERP-v2"),
    ("04", "pathfinding", "Multi-agent pathfinding", "", "ALGORITHMS",
     "A* implementations for single-agent and multi-agent planning in Python.",
     "https://github.com/dakshyadav1810/multi-agent-pathfinding"),
    ("05", "camera", "Subject-tracking camera", "", "EMBEDDED SYSTEMS",
     "ESP32 firmware that drives a servo mount from a React Native companion app to keep a subject in frame.",
     "https://github.com/dakshyadav1810/subject-tracking-camera"),
]


def card(item):
    idx, key, title, aka, tag, desc, url = item

    def render(c, uid):
        lines = textwrap.wrap(desc, 124)
        h = 98 + 20 * (len(lines) - 1) + 34
        s = head(1000, h, c, uid, f"{title}. {desc}")
        s += (f'<text x="32" y="68" font-family="{SERIF}" font-size="26" fill="{c["dim"]}">{idx}</text>'
              f'<text x="76" y="42" font-family="{MONO}" font-size="10.5" letter-spacing="1.6" fill="{c["accent"]}">{tag}</text>'
              f'<text x="968" y="42" text-anchor="end" font-family="{MONO}" font-size="10.5" letter-spacing="1.4" fill="{c["dim"]}">VIEW REPOSITORY \u2197</text>')
        aka_t = (f'<tspan font-family="{SANS}" font-size="13.5" fill="{c["muted"]}" dx="12">({esc(aka)})</tspan>' if aka else "")
        s += f'<text x="76" y="72" font-family="{SERIF}" font-size="26" fill="{c["ink"]}">{esc(title)}{aka_t}</text>'
        for i, ln in enumerate(lines):
            s += f'<text x="76" y="{102+i*20}" font-family="{SANS}" font-size="13.5" fill="{c["muted"]}">{esc(ln)}</text>'
        return s + '</svg>'
    return f"work-{key}", render


# ------------------------------------------------------------------ languages
def load_langs():
    skip = {"CSS", "HTML", "SCSS", "Jupyter Notebook"}
    names = {"PLpgSQL": "PL/pgSQL"}
    data = [(names.get(k, k), v) for k, v in json.load(open(HERE / "data/langs.json")) if k not in skip][:6]
    tot = sum(v for _, v in data)
    return [(k, v / tot * 100) for k, v in data]


def languages(c, uid):
    w = 1000
    langs = load_langs()
    h = 92 + len(langs) * 30
    s = head(w, h, c, uid, "Most used languages across public repositories")
    s += sheet_label(c, 6, "LANGUAGES BY CODE VOLUME", w)
    tints = [c["accent"]] + c["lanes"] + [c["dim"], c["dim"]]
    top = max(p for _, p in langs)
    for i, (name, pct) in enumerate(langs):
        y = 84 + i * 30
        full = w - 64 - 200 - 90
        s += (f'<text x="32" y="{y+4}" font-family="{SANS}" font-size="13.5" fill="{c["ink"]}">{esc(name)}</text>'
              f'<rect x="200" y="{y-4}" width="{full}" height="8" rx="4" fill="{c["line"]}" opacity="0.5"/>'
              f'<rect x="200" y="{y-4}" width="{full*pct/top:.1f}" height="8" rx="4" fill="{tints[i]}"/>'
              f'<text x="{w-32}" y="{y+4}" text-anchor="end" font-family="{MONO}" font-size="11.5" fill="{c["muted"]}">{pct:.1f}%</text>')
    return s + '</svg>'


# ------------------------------------------------------------------ assemble
FILES = {"banner": banner, "intro": intro, "numbers": numbers, "workhead": workhead}
for _it in WORK:
    _k, _fn = card(_it)
    FILES[_k] = _fn
FILES.update({"history": history, "materials": materials, "languages": languages})

ALT = {
    "banner": "Daksh Yadav, Software and AI Engineer, IIT Kharagpur",
    "intro": "Software and AI engineer, B.Tech. at IIT Kharagpur (class of 2027). Founder of Gimbal (formerly Axiom), an open-source self-healing testing platform. Previously at Emora Health (New York) and Wed-E.",
    "numbers": "Selected results: 93% reduction in form-filling time, 83% faster peak gate entry, 86% of UI drift resolved without a runtime LLM, 15,000+ students served",
    "workhead": "Selected work",
    "history": "Career history drawn as a git branch graph: Gimbal, Emora Health, Technology Gymkhana, PALE, Wed-E, Inter IIT Tech Meet 13",
    "materials": "Skills: Python, TypeScript, Go, C++, React, Next.js, PostgreSQL, Redis, AWS, Docker, Kubernetes, Qdrant, LangChain, Playwright and more",
    "languages": "Most used languages: Python, TypeScript, JavaScript, PL/pgSQL, C++, Shell",
}
for _it in WORK:
    ALT[f"work-{_it[1]}"] = f"{_it[2]}{' (' + _it[3] + ')' if _it[3] else ''}. {_it[5]}"
LINKS = {f"work-{_it[1]}": _it[6] for _it in WORK}


def pic(name):
    tag = (f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="assets/{name}-dark.svg">\n'
           f'  <img alt="{esc(ALT[name], {chr(34): "&quot;"})}" src="assets/{name}-light.svg" width="100%">\n</picture>')
    if name in LINKS:
        tag = f'<a href="{LINKS[name]}">\n{tag}\n</a>'
    return f"<p>\n{tag}\n</p>"


def readme():
    order = ["banner", "intro", "numbers", "workhead"] + [f"work-{i[1]}" for i in WORK] + ["history", "materials", "languages"]
    return "\n\n".join(pic(n) for n in order) + "\n"


if __name__ == "__main__":
    for old in OUT.glob("*.svg"):
        old.unlink()
    for theme, c in THEMES.items():
        for name, fn in FILES.items():
            (OUT / f"{name}-{theme}.svg").write_text(fn(c, f"{name[:4]}{name[-2:]}{theme[0]}"), encoding="utf-8")
    (ROOT / "README.md").write_text(readme(), encoding="utf-8")
    print("wrote", len(list(OUT.glob("*.svg"))), "svgs + README.md")
