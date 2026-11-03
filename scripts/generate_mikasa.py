
import json
import base64
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path
from xml.sax.saxutils import escape

USERNAME = "marialuizatech"

# Busca eventos públicos recentes do GitHub
url = f"https://api.github.com/users/{USERNAME}/events/public?per_page=100"

request = urllib.request.Request(
    url,
    headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "Mikasa-Contribution-Battle"
    }
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

# Configurações do calendário
today = datetime.now(timezone.utc).date()

width = 1000
height = 210
cell = 12
gap = 4
step = cell + gap

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="100%" viewBox="0 0 {width} {height}">',
    '<rect width="100%" height="100%" rx="12" fill="#16131a"/>',
    '<text x="24" y="25" fill="#f3dce8" font-family="monospace" font-size="15">MIKASA ACKERMAN | CONTRIBUTION BATTLE</text>'
]

# Desenha os últimos 365 dias
for index in range(365):
    day = today - timedelta(days=364 - index)
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

# Carrega a imagem original da Mikasa
image_path = Path("mikasa.png")

if not image_path.exists():
    raise FileNotFoundError(
        "Não encontrei mikasa.png na raiz do repositório."
    )

sprite_data = base64.b64encode(
    image_path.read_bytes()
).decode("ascii")

# Animação da Mikasa
svg.append(f"""
<g>
    <image
        xlink:href="data:image/png;base64,{sprite_data}"
        x="0"
        y="0"
        width="150"
        height="135"
        preserveAspectRatio="xMidYMid meet"
    />
    <animateMotion
        dur="18s"
        repeatCount="indefinite"
        path="M 0,15 L 760,15 L 760,30 L 0,30 L 0,15"
    />
</g>
""")

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

# Rodapé
svg.append("""
<text x="24" y="195" fill="#e9a4b9"
 font-family="monospace" font-size="11">
Mikasa is protecting your contributions!
</text>
</svg>
""")

# Salva o SVG
Path("output").mkdir(exist_ok=True)

Path("output/mikasa-contribution-graph.svg").write_text(
    "\n".join(svg),
    encoding="utf-8"
)

print("Mikasa animation generated successfully!")
print(f"Public commits detected: {sum(contributions.values())}")
