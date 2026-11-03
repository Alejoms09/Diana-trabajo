"""Genera los artefactos documentales de la estación 1 sin crear código Java."""

from html import escape
from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "estacion-01"
PDF = ROOT / "output" / "pdf" / "estacion-01.pdf"
WIDTH, HEIGHT = A4
BLUE = "#235783"
INK = "#1E293B"
MUTED = "#475569"
PALE = "#EEF4FA"


def font_path(name):
    candidates = [
        Path("C:/Windows/Fonts") / name,
        Path("/usr/share/fonts/truetype/msttcorefonts") / name,
    ]
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    raise FileNotFoundError(f"No se encuentra {name}; configure una fuente Arial.")


pdfmetrics.registerFont(TTFont("Arial", font_path("arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Bold", font_path("arialbd.ttf")))
DOCS.mkdir(parents=True, exist_ok=True)
PDF.parent.mkdir(parents=True, exist_ok=True)
c = canvas.Canvas(str(PDF), pagesize=A4, invariant=1)
c.setTitle("Estación 1 - Comprender el problema y modelar el flujo")
c.setAuthor("BibliotecaReservas")
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH:.2f}" height="{HEIGHT:.2f}" viewBox="0 0 {WIDTH:.2f} {HEIGHT:.2f}" role="img" aria-labelledby="title desc">',
       '<title id="title">Estación 1: diagrama del flujo de reservas</title>',
       '<desc id="desc">Ocho pasos de la guía. La decisión ¿hay una sala adecuada? termina sin crear una reserva confirmada si la respuesta es No.</desc>',
       '<rect width="100%" height="100%" fill="white"/>']


def text(x, y, value, size=10, bold=False, color=INK, align="left", svg_on=True):
    font = "Arial-Bold" if bold else "Arial"
    c.setFont(font, size)
    c.setFillColor(colors.HexColor(color))
    draw = {"left": c.drawString, "middle": c.drawCentredString, "right": c.drawRightString}[align]
    draw(x, HEIGHT-y, value)
    if svg_on:
        anchor = {"left": "start", "middle": "middle", "right": "end"}[align]
        svg.append(f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}" text-anchor="{anchor}">{escape(value)}</text>')


def wrapped(value, width, size=10, bold=False):
    font = "Arial-Bold" if bold else "Arial"
    lines = []
    for paragraph in value.split("\n"):
        current = ""
        for word in paragraph.split():
            candidate = (current + " " + word).strip()
            if current and pdfmetrics.stringWidth(candidate, font, size) > width:
                lines.append(current)
                current = word
            else:
                current = candidate
        lines.append(current)
    return lines


def paragraph(x, y, value, width, size=10, leading=14, bold=False, color=INK, svg_on=True):
    for line in wrapped(value, width, size, bold):
        text(x, y, line, size, bold, color, svg_on=svg_on)
        y += leading
    return y


def rect(x, y, w, h, fill=PALE, radius=7, svg_on=True):
    c.setStrokeColor(colors.HexColor(BLUE))
    c.setFillColor(colors.HexColor(fill))
    c.setLineWidth(0.9)
    c.roundRect(x, HEIGHT-y-h, w, h, radius, fill=1, stroke=1)
    if svg_on:
        svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{BLUE}" stroke-width="0.9"/>')


def line(points, arrow=False):
    c.setStrokeColor(colors.HexColor(BLUE))
    c.setLineWidth(1)
    p = c.beginPath()
    p.moveTo(points[0][0], HEIGHT-points[0][1])
    for x, y in points[1:]:
        p.lineTo(x, HEIGHT-y)
    c.drawPath(p)
    svg.append(f'<polyline points="{" ".join(f"{x},{y}" for x, y in points)}" fill="none" stroke="{BLUE}"/>')
    if arrow:
        x, y = points[-1]
        prev_x, prev_y = points[-2]
        if y > prev_y:
            heads = [(x-3,y-5),(x,y),(x+3,y-5)]
        else:
            heads = [(x-5,y-3),(x,y),(x-5,y+3)]
        line(heads)


def box(y, value, height=38):
    x, w = 42, 330
    rect(x, y, w, height)
    lines = wrapped(value, w-24, 10.4)
    base = y + (height - len(lines)*13)/2 + 10
    for i, value_line in enumerate(lines):
        text(x+w/2, base+i*13, value_line, 10.4, align="middle")


def header(page, subtitle):
    text(42, 39, "BIBLIOTECARESERVAS / LABORATORIO DE PATRONES", 9, True, BLUE, svg_on=page==1)
    text(42, 65, "Estación 1", 22, True, BLUE, svg_on=page==1)
    text(42, 84, subtitle, 11, color=MUTED, svg_on=page==1)
    text(42, 818, "Guía proporcionada por el usuario | 03/11/2026 | Solo estación 1", 8, color=MUTED, svg_on=page==1)
    text(WIDTH-42, 818, f"{page} / 2", 8, color=MUTED, align="right", svg_on=page==1)


mmd = (DOCS / "flujo.mmd").read_text(encoding="utf-8")
steps = re.findall(r'P\d\["(\d\. [^"]+)"\]', mmd)
if len(steps) != 8:
    raise ValueError("Se esperaban exactamente los ocho pasos del flujo.")

header(1, "Comprender el problema y modelar el flujo")
rect(154, 101, 106, 22, fill="#FFFFFF", radius=11)
text(207, 116, "Inicio", 10, True, align="middle")
line([(207,123),(207,137)], True)
for i, y in enumerate([137,190,243]):
    box(y, steps[i])
    if i < 2:
        line([(207,y+38),(207,y+53)], True)
line([(207,281),(207,292)], True)
diamond = [(207,292),(322,326),(207,360),(92,326),(207,292)]
c.setFillColor(colors.HexColor("#DFECF7"))
c.setStrokeColor(colors.HexColor(BLUE))
p = c.beginPath()
p.moveTo(207, HEIGHT-292)
for x,y in diamond[1:]:
    p.lineTo(x, HEIGHT-y)
c.drawPath(p, fill=1, stroke=1)
svg.append(f'<polygon points="{" ".join(f"{x},{y}" for x,y in diamond)}" fill="#DFECF7" stroke="{BLUE}"/>')
text(207, 324, "¿hay una sala", 10.4, True, align="middle")
text(207, 338, "adecuada?", 10.4, True, align="middle")
line([(322,326),(408,326)], True)
text(358, 317, "No", 10, True, align="middle")
rect(408, 294, 145, 64, fill="#FFFFFF", radius=12)
for i, t in enumerate(["Fin sin crear", "una reserva", "confirmada."]):
    text(480.5, 314+i*14, t, 10.4, align="middle")
line([(207,360),(207,393)], True)
text(219, 382, "Sí", 10, True)
for i, y in enumerate([393,446,499,552,605], start=3):
    h = 48 if i == 7 else 38
    box(y, steps[i], h)
    if i < 7:
        line([(207,y+h),(207,y+53)], True)
line([(207,653),(207,678)], True)
rect(154, 678, 106, 23, fill="#FFFFFF", radius=11)
text(207, 694, "Fin", 10, True, align="middle")
paragraph(42, 731, "Los cambios del paso 8 se validan con State y, si se aceptan, se comunican con Observer. Una transición rechazada no genera notificación.", 511, size=9.5, leading=13, color=MUTED)
paragraph(42, 773, "Transiciones: Pendiente a Confirmada o Cancelada; Confirmada a Cancelada o Finalizada.", 511, size=9.5, leading=13, color=MUTED)
svg.append("</svg>")
(DOCS / "flujo.svg").write_text("\n".join(svg)+"\n", encoding="utf-8")
c.showPage()

header(2, "Responsabilidades, comprobación y fidelidad a la guía")
text(42, 117, "Responsabilidades que deben separarse de Main", 13, True, BLUE, svg_on=False)
roles = [
    ("Consultar salas", "RepositorioSalas y RepositorioSalasMemoria consultarán la disponibilidad simulada."),
    ("Seleccionar una sala", "EstrategiaSeleccionSala definirá el contrato; SeleccionPorCapacidad y SeleccionSalaPreferida aplicarán el criterio."),
    ("Construir y validar", "ReservaBuilder reunirá los datos y validará la construcción de Reserva."),
    ("Registrar reservas", "RepositorioReservas y RepositorioReservasMemoria separarán el registro de la coordinación del caso de uso."),
    ("Coordinar el caso de uso", "ReservaFacade consultará, seleccionará, construirá, registrará y coordinará la confirmación."),
    ("Controlar los estados", "EstadoReserva, Pendiente, Confirmada, Cancelada y Finalizada definirán las operaciones permitidas."),
    ("Comunicar los cambios", "ObservadorReserva, NotificadorEstudiante y RegistroEventos separarán los eventos de sus mecanismos de notificación."),
]
y=139
for label, description in roles:
    text(42, y, label, 10, True, svg_on=False)
    y=paragraph(42,y+14,description,511,size=9.4,leading=12,svg_on=False)+12

text(42, y+2, "Comprobación: cohesión y mantenimiento de Main", 13, True, BLUE, svg_on=False)
y=paragraph(42,y+21,"Si Main consultara salas, validara datos, construyera reservas, notificara y controlara estados, reuniría responsabilidades con objetivos y motivos de cambio distintos. Tendría baja cohesión: sus métodos no estarían centrados en una sola función. Cambiar una validación, un criterio de selección o una notificación obligaría a modificar la misma clase, dificultaría las pruebas aisladas y aumentaría el riesgo de afectar otras tareas. Main debe configurar las dependencias y presentar el flujo.",511,size=10,leading=14,svg_on=False)+22
text(42,y,"Comparación con las capturas originales",13,True,BLUE,svg_on=False)
y+=21
for item in [
    "103519.png: se conservan literalmente los pasos 1 a 5 y la decisión exigida.",
    "103535.png: se conservan literalmente los pasos 6 a 8; se desarrollan siete responsabilidades y la comprobación de cohesión.",
    "La rama No termina sin crear una reserva confirmada; la rama Sí continúa con Builder.",
    "La guía no proporciona código de estación 1: esta entrega es documental. Compilación y ejecución Java no aplican en esta estación.",
    "Los nombres de las futuras clases son los de la guía; no se han implementado estaciones posteriores.",
]:
    y=paragraph(42,y,item,511,size=9.5,leading=13,svg_on=False)+8

text(42,y+5,"Revisión requerida antes de la estación 2",12,True,BLUE,svg_on=False)
paragraph(42,y+24,"Revisar el diagrama, las responsabilidades, la comparación y el registro real de verificaciones. La siguiente estación requiere autorización del usuario. El detalle de evidencias está en docs/estacion-01/estacion-01.md.",511,size=9.5,leading=13,svg_on=False)
c.save()
print(f"Creado: {PDF.relative_to(ROOT)}")
print(f"Creado: {(DOCS / 'flujo.svg').relative_to(ROOT)}")
