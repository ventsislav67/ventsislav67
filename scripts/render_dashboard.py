#!/usr/bin/env python3
"""Turn automatically refreshed GitHub API SVG data into neon animated cards."""
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone, date
from pathlib import Path
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
USER = "ventsislav67"
CYAN = "#31E5F8"
FG = "#ECF8FF"
SUB = "#95BED7"


def txt(x, y, t, size=14, color=FG, weight=500, extra=""):
    return f'<text x="{x}" y="{y}" font-family="Arial,Segoe UI,sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}" {extra}>{escape(str(t))}</text>'


def base(w, h, title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
<title>{escape(title)}</title>
<defs>
<linearGradient id="bg" x2="1" y2="1"><stop stop-color="#0C1D37"/><stop offset="1" stop-color="#061020"/></linearGradient>
<linearGradient id="line"><stop stop-color="#32BDFF"/><stop offset=".5" stop-color="#17F2C5"/><stop offset="1" stop-color="#8266FF"/></linearGradient>
<pattern id="grid" width="26" height="26" patternUnits="userSpaceOnUse"><path d="M 26 0 L 0 0 0 26" stroke="#2E4E6E" stroke-opacity=".22" fill="none"/></pattern>
</defs>
<style>
.blink{{animation:blink 2.5s ease-in-out infinite}}
.bar{{transform-box:fill-box;transform-origin:center bottom;animation:grow 850ms ease-out backwards}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
@keyframes grow{{from{{transform:scaleY(.08);opacity:.2}}to{{transform:scaleY(1);opacity:1}}}}
@media(prefers-reduced-motion:reduce){{.blink,.bar{{animation:none}}}}
</style>
<rect width="{w}" height="{h}" rx="22" fill="url(#bg)"/>
<rect width="{w}" height="{h}" rx="22" fill="url(#grid)"/>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="21" fill="none" stroke="#1B668B"/>
<rect width="{w}" height="3" rx="1.5" fill="url(#line)"/>
'''


def save(name, content):
    (ROOT / name).write_text(content + '</svg>\n', encoding="utf-8")
    print("Updated", name)


def read_stats():
    root = ET.parse(ROOT / "github-stats.svg").getroot()
    result = {}
    for node in root.iter():
        kind = node.get("data-testid")
        if kind in ("commits", "stars", "prs", "issues"):
            result[kind] = "".join(node.itertext()).strip()
    for required in ("commits", "stars", "prs", "issues"):
        if not re.fullmatch(r"[\d,\.kKM]+", result.get(required, "")):
            raise RuntimeError("Missing valid GitHub stat: " + required)
    return result


def read_languages():
    root = ET.parse(ROOT / "top-languages.svg").getroot()
    languages = []
    for node in root.iter():
        if node.get("data-testid") == "lang-name":
            m = re.fullmatch(r"(.+?)\s+([\d.]+)%", " ".join("".join(node.itertext()).split()))
            if m:
                languages.append((m.group(1), float(m.group(2))))
    if not languages:
        raise RuntimeError("No language statistics found")
    return sorted(languages, key=lambda p: p[1], reverse=True)[:6]


def render_stats(data):
    s = base(620, 350, "Ventsislav Kolev GitHub statistics")
    s += '<circle class="blink" cx="35" cy="38" r="5" fill="#13FDD9"/>'
    s += txt(49, 43, "DEVELOPER  /  GITHUB METRICS", 15, CYAN, 800, 'letter-spacing="1.1"')
    s += txt(35, 68, "AUTOMATICALLY SYNCED PUBLIC ACTIVITY", 11, SUB, 600, 'letter-spacing=".9"')
    values = [("COMMITS", data["commits"], "LAST 12 MONTHS"),
              ("STARS", data["stars"], "RECEIVED"),
              ("PULL REQUESTS", data["prs"], "ALL TIME"),
              ("ISSUES", data["issues"], "ALL TIME")]
    for i, (name, number, sub) in enumerate(values):
        x, y = 35 + i % 2 * 278, 86 + i // 2 * 111
        s += f'<rect x="{x}" y="{y}" width="267" height="100" rx="13" fill="#0D233C" stroke="#255472"/>'
        s += f'<path d="M{x+15} {y+15} h23" stroke="url(#line)" stroke-width="3"/>'
        s += txt(x+17, y+35, name, 12, "#ACD0E9", 750, 'letter-spacing="1"')
        s += txt(x+17, y+79, number, 38, FG, 800)
        s += txt(x+122, y+77, sub, 10, SUB, 600)
        s += f'<circle class="blink" cx="{x+244}" cy="{y+20}" r="3.5" fill="#19EBCE"/>'
    s += txt(35, 336, "SOURCE: GITHUB STATS ACTION  •  REFRESHED AUTOMATICALLY", 10, SUB, 600, 'letter-spacing=".6"')
    save("developer-stats.svg", s)


def render_languages(languages):
    s = base(620, 350, "Repository language distribution")
    s += '<circle class="blink" cx="35" cy="38" r="5" fill="#13FDD9"/>'
    s += txt(49, 43, "LANGUAGE SPECTRUM", 16, CYAN, 800, 'letter-spacing="1.5"')
    s += txt(35, 68, "BY REPOSITORY CODE SIZE  /  NOT SKILL LEVEL", 11, SUB, 600, 'letter-spacing=".9"')
    colors = ["#37DBFF", "#28E6C3", "#7F9BFF", "#B99AFF", "#FFB56C", "#EE8FB8"]
    for i, (name, pct) in enumerate(languages):
        y = 96 + i * 37
        col = colors[i]
        s += txt(36, y, name.upper(), 13, FG, 750, 'letter-spacing=".4"')
        s += txt(578, y, f"{pct:.2f}%", 12, col, 750, 'text-anchor="end"')
        s += f'<rect x="36" y="{y+8}" width="542" height="7" rx="3.5" fill="#1B3852"/>'
        s += f'<rect class="bar" x="36" y="{y+8}" width="{max(2,542*pct/100):.1f}" height="7" rx="3.5" fill="{col}" style="animation-delay:{i*80}ms"/>'
    s += txt(35, 336, "GITHUB REPOSITORY LANGUAGES  •  REFRESHED AUTOMATICALLY", 10, SUB, 600, 'letter-spacing=".7"')
    save("developer-languages.svg", s)


def fetch_contributions():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN missing")
    payload = {"query": """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}""",
               "variables": {"login": USER}}
    request = Request("https://api.github.com/graphql", data=json.dumps(payload).encode(),
                      headers={"Authorization": "Bearer " + token,
                               "Content-Type": "application/json", "Accept": "application/vnd.github+json",
                               "User-Agent": "profile-neon-dashboard"})
    with urlopen(request, timeout=30) as resp:
        answer = json.load(resp)
    if answer.get("errors"):
        raise RuntimeError(str(answer["errors"]))
    return answer["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def render_activity(calendar):
    weeks = calendar["weeks"][-52:]
    scores = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in weeks]
    days = [d for w in weeks for d in w["contributionDays"]]
    active = sum(d["contributionCount"] > 0 for d in days)
    by_day = {d["date"]: d["contributionCount"] for d in days}
    today = datetime.now(timezone.utc).date()
    pointer = today if by_day.get(str(today), 0) else today-timedelta(days=1)
    streak = 0
    while by_day.get(str(pointer), 0):
        streak += 1
        pointer -= timedelta(days=1)
    total = calendar["totalContributions"]
    s = base(1260, 280, "Real GitHub weekly contribution activity for the past year")
    s += '<circle class="blink" cx="40" cy="37" r="5" fill="#13FDD9"/>'
    s += txt(54, 43, "CONTRIBUTION SIGNAL", 17, CYAN, 800, 'letter-spacing="2"')
    s += txt(40, 70, "ACTUAL WEEKLY CONTRIBUTIONS  /  LAST 52 WEEKS", 11, SUB, 650, 'letter-spacing="1"')
    s += txt(1215, 42, total, 30, FG, 800, 'text-anchor="end"')
    s += txt(1215, 61, "12-MONTH CONTRIBUTIONS", 10, SUB, 700, 'text-anchor="end"')
    high = max(scores + [1])
    s += '<path d="M40 224 H1216" stroke="#29536E"/>'
    for i, n in enumerate(scores):
        x = 40 + i * 22.4
        height = 7 if n == 0 else 10 + 108*n/high
        y = 224-height
        color = "#234563" if n == 0 else ("#23E8CA" if n/high >= .6 else "#28B8EF")
        s += f'<rect class="bar" x="{x:.1f}" y="{y:.1f}" width="14" height="{height:.1f}" rx="3" fill="{color}" style="animation-delay:{i*16}ms"/>'
        if i % 9 == 0 and weeks[i]["contributionDays"]:
            s += txt(f"{x:.1f}", 243, weeks[i]["contributionDays"][0]["date"][:7], 10, SUB, 650)
    s += txt(40, 266, f"ACTIVE DAYS: {active}", 12, FG, 700)
    s += txt(320, 266, f"CURRENT STREAK: {streak} DAYS", 12, FG, 700)
    s += txt(1214, 266, "SOURCE: GITHUB CONTRIBUTION CALENDAR", 10, SUB, 600, 'text-anchor="end"')
    save("contribution-signal.svg", s)


def main():
    render_stats(read_stats())
    render_languages(read_languages())
    try:
        render_activity(fetch_contributions())
    except Exception as exc:
        print("Contribution API unavailable:", exc, file=sys.stderr)
        if not (ROOT / "contribution-signal.svg").exists():
            s = base(1260, 160, "Contribution activity is syncing")
            s += txt(42, 70, "CONTRIBUTION SIGNAL", 22, CYAN, 750)
            s += txt(42, 103, "Waiting for contribution data. The snake below remains animated.", 15, FG, 500)
            save("contribution-signal.svg", s)


if __name__ == "__main__":
    main()
