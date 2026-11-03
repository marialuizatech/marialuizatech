
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
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'xmlns:xlink="http://www.w3.org/1999/xlink" '
    f'width="100%" viewBox="0 0 {width} {height}">',
    '<rect width="100%" height="100%" rx="12" fill="#16131a"/>',
    '<text x="24" y="25" fill="#f3dce8" '
    'font-family="monospace" font-size="15">'
    'MIKASA ACKERMAN | CONTRIBUTION BATTLE</text>'
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
        f'<title>{escape(day.isoformat())}: '
        f'{count} public commits detected</title>'
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

# Movimento da Mikasa
mikasa_path = "M 0,15 L 760,15 L 760,30 L 0,30 L 0,15"

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
        path="{mikasa_path}"
    />
</g>
""")

# Efeitos de ataque das lâminas
svg.append(f"""
<g>
  <g stroke="#ff426f" stroke-width="5"
     stroke-linecap="round" fill="none">
    <path d="M65 85 L135 25">
      <animate
        attributeName="opacity"
        values="0;1;1;0"
        keyTimes="0;0.15;0.65;1"
        dur="1.8s"
        repeatCount="indefinite"/>
    </path>
  </g>

  <!-- Brilho do corte -->
  <path d="M65 85 L135 25"
        stroke="#ffd5e0"
        stroke-width="2"
        fill="none">
    <animate
      attributeName="opacity"
      values="0;1;0"
      dur="1.8s"
      repeatCount="indefinite"/>
  </path>

  <!-- Partículas do impacto -->
  <g fill="#ff79a9">
    <circle cx="130" cy="30" r="3">
      <animate attributeName="opacity"
        values="0;1;0" dur="1.8s"
        repeatCount="indefinite"/>
      <animate attributeName="r"
        values="1;5;1" dur="1.8s"
        repeatCount="indefinite"/>
    </circle>

    <circle cx="145" cy="42" r="2">
      <animate attributeName="opacity"
        values="0;1;0" dur="1.4s"
        repeatCount="indefinite"/>
    </circle>

    <circle cx="115" cy="20" r="2">
      <animate attributeName="opacity"
        values="0;1;0" dur="1.6s"
        repeatCount="indefinite"/>
    </circle>
  </g>

  <animateMotion
    dur="18s"
    repeatCount="indefinite"
    path="{mikasa_path}"
  />
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
