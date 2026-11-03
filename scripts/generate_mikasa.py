
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
character = """
<g shape-rendering="crispEdges">

  <!-- Cabelo preto -->
  <rect x="20" y="2" width="30" height="7" fill="#17151b"/>
  <rect x="13" y="9" width="44" height="9" fill="#17151b"/>
  <rect x="10" y="18" width="12" height="28" fill="#17151b"/>
  <rect x="49" y="18" width="12" height="31" fill="#17151b"/>
  <rect x="15" y="38" width="9" height="17" fill="#17151b"/>
  <rect x="48" y="42" width="10" height="15" fill="#17151b"/>
  <rect x="19" y="5" width="8" height="7" fill="#39303a"/>

  <!-- Rosto -->
  <rect x="22" y="15" width="26" height="25" fill="#edc3a9"/>
  <rect x="19" y="20" width="5" height="15" fill="#edc3a9"/>
  <rect x="46" y="20" width="5" height="15" fill="#edc3a9"/>

  <!-- Franja -->
  <rect x="20" y="12" width="30" height="7" fill="#17151b"/>
  <rect x="25" y="17" width="7" height="7" fill="#17151b"/>
  <rect x="37" y="17" width="7" height="5" fill="#17151b"/>

  <!-- Olhos -->
  <rect x="26" y="27" width="5" height="3" fill="#30232a"/>
  <rect x="39" y="27" width="5" height="3" fill="#30232a"/>
  <rect x="28" y="28" width="2" height="2" fill="#f4e8dc"/>
  <rect x="41" y="28" width="2" height="2" fill="#f4e8dc"/>

  <!-- Pescoço -->
  <rect x="30" y="38" width="12" height="9" fill="#dba58e"/>

  <!-- Cachecol vermelho -->
  <rect x="19" y="41" width="32" height="10" fill="#a91e32"/>
  <rect x="14" y="43" width="12" height="7" fill="#c62b43"/>
  <rect x="43" y="47" width="23" height="7" fill="#c62b43"/>
  <rect x="59" y="52" width="7" height="13" fill="#a91e32"/>
  <rect x="25" y="43" width="17" height="3" fill="#e34a59"/>

  <!-- Jaqueta do uniforme -->
  <rect x="19" y="51" width="32" height="22" fill="#786b55"/>
  <rect x="24" y="51" width="10" height="22" fill="#9a896b"/>
  <rect x="38" y="51" width="10" height="22" fill="#625847"/>

  <!-- Camisa -->
  <rect x="32" y="52" width="8" height="16" fill="#e1d9c8"/>

  <!-- Cinto e equipamento -->
  <rect x="18" y="69" width="36" height="5" fill="#38343a"/>
  <rect x="32" y="68" width="8" height="7" fill="#c4a66d"/>
  <rect x="12" y="54" width="7" height="19" fill="#77736c"/>
  <rect x="51" y="54" width="7" height="19" fill="#77736c"/>

  <!-- Alças do equipamento -->
  <rect x="23" y="52" width="4" height="19" fill="#d5c7a7"/>
  <rect x="44" y="52" width="4" height="19" fill="#d5c7a7"/>
  <rect x="26" y="57" width="19" height="3" fill="#d5c7a7"/>

  <!-- Calças -->
  <rect x="22" y="74" width="13" height="15" fill="#514d4a"/>
  <rect x="39" y="74" width="13" height="15" fill="#514d4a"/>
  <rect x="27" y="75" width="4" height="12" fill="#71665c"/>
  <rect x="43" y="75" width="4" height="12" fill="#71665c"/>

  <!-- Botas -->
  <rect x="20" y="87" width="16" height="6" fill="#29272b"/>
  <rect x="38" y="87" width="17" height="6" fill="#29272b"/>

  <!-- Equipamento de manobra tridimensional -->
  <rect x="5" y="57" width="8" height="19" fill="#aaa49a"/>
  <rect x="4" y="60" width="3" height="12" fill="#e1d9c8"/>
  <rect x="57" y="57" width="8" height="19" fill="#aaa49a"/>
  <rect x="65" y="60" width="3" height="12" fill="#e1d9c8"/>
  <rect x="7" y="75" width="5" height="7" fill="#77736c"/>
  <rect x="58" y="75" width="5" height="7" fill="#77736c"/>

  <!-- Lâminas -->
  <rect x="0" y="39" width="3" height="37" fill="#dce8f1"/>
  <rect x="1" y="35" width="2" height="7" fill="#ffffff"/>
  <rect x="68" y="39" width="3" height="37" fill="#dce8f1"/>
  <rect x="68" y="35" width="2" height="7" fill="#ffffff"/>

</g>
"""
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

