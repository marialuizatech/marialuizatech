
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

USERNAME = "marialuizatech"

# Busca eventos públicos recentes do GitHub
url = f"https://api.github.com/users/{USERNAME}/events/public?per_page=100"

request = urllib.request.Request(
    url,
    headers={"Accept": "application/vnd.github+json",
             "User-Agent": "Mikasa-Contribution-Battle"}
)

with urllib.request.urlopen(request) as response:
    events = json.loads(response.read())

# Conta commits públicos por dia
contributions = {}

for event in events:
    if event.get("type") == "PushEvent":
        date = event["created_at"][:10]
        commits = len(event.get("payload", {}).get("commits", []))
        contributions[date] = contributions.get(date, 0) + commits

# Prepara o calendário
today = datetime.now(timezone.utc).date()
width = 1000
height = 190
cell = 12
gap = 4
step = cell + gap

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {width} {height}">',
    '<rect width="100%" height="100%" rx="12" fill="#16131a"/>',
    '<text x="24" y="25" fill="#f3dce8" font-family="monospace" font-size="15">MIKASA ACKERMAN | CONTRIBUTION BATTLE</text>'
]

# Desenha os últimos 365 dias
for index in range(365):
    day = today.fromordinal(today.toordinal() - (364 - index))
    count = contributions.get(day.isoformat(), 0)

    column = index // 7
    row = index % 7

    x = 24 + column * step
    y = 45 + row * step

    if count == 0:
        color = "#29232e"
    elif count < 3:
        color = "#77334f"
    elif count < 6:
        color = "#c43c68"
    else:
        color = "#ff79a9"

    svg.append(
        f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" '
        f'rx="2" fill="{color}">'
        f'<title>{escape(day.isoformat())}: {count} public commits detected</title>'
        '</rect>'
    )

# Personagem Mikasa em pixel art
character = """
<g shape-rendering="crispEdges">
  <rect x="10" y="0" width="18" height="8" fill="#38252b"/>
  <rect x="6" y="7" width="24" height="15" fill="#38252b"/>
  <rect x="13" y="9" width="13" height="11" fill="#f0c5ae"/>
  <rect x="15" y="13" width="3" height="2" fill="#211923"/>
  <rect x="22" y="13" width="3" height="2" fill="#211923"/>
  <rect x="10" y="21" width="20" height="7" fill="#bd263d"/>
  <rect x="25" y="24" width="13" height="5" fill="#e13c50"/>
  <rect x="11" y="28" width="19" height="13" fill="#594d43"/>
  <rect x="15" y="28" width="4" height="13" fill="#ded4c5"/>
  <rect x="12" y="41" width="7" height="7" fill="#272631"/>
  <rect x="23" y="41" width="7" height="7" fill="#272631"/>
  <rect x="0" y="25" width="3" height="23" fill="#dce8f1"/>
  <rect x="37" y="25" width="3" height="23" fill="#dce8f1"/>
</g>
"""

svg.append(
    f'<g>{character}'
    '<animateMotion dur="18s" repeatCount="indefinite" '
    'path="M 35,45 L 850,45 L 850,105 L 35,105 L 35,45"/>'
    '</g>'
)

# Efeitos de ataque
svg.append("""
<g fill="none" stroke="#e94b70" stroke-width="4">
  <path d="M0 0 L35 0">
    <animate attributeName="opacity" values="0;1;0"
      dur="1.5s" repeatCount="indefinite"/>
    <animateMotion dur="1.5s" repeatCount="indefinite"
      path="M 60,95 L 880,95"/>
  </path>
</g>
""")

svg.append("""
<text x="24" y="175" fill="#e9a4b9"
 font-family="monospace" font-size="11">
Mikasa is protecting your contributions!
</text>
</svg>
""")

Path("output").mkdir(exist_ok=True)

Path("output/mikasa-contribution-graph.svg").write_text(
    "\n".join(svg), encoding="utf-8"
)

print("Mikasa animation generated successfully!")
print(f"Public commits detected: {sum(contributions.values())}")

