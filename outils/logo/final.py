"""Logo définitif Alphanet Group : « A » coupé par un trait de raclette.
Formes calculées (pas de masque) pour rester lisibles partout : site, mails, logiciels.
Usage : python3 outils/logo/final.py <archivo-latin-wdth-normal.woff2> <dossier de sortie>
La police vient du paquet npm @fontsource-variable/archivo (licence SIL OFL)."""
import sys, importlib.util, math
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

import os
ARCH, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('g', os.path.join(HERE, 'gen_logo_lib.py'))
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
A800 = instancer.instantiateVariableFont(TTFont(ARCH), {'wght': 800, 'wdth': 125})
A600 = instancer.instantiateVariableFont(TTFont(ARCH), {'wght': 600, 'wdth': 125})

# --- Géométrie du pictogramme (repère 64 x 64) ------------------------------
X0, X1 = 1.0, 63.0            # extrémités du trait
Y_TOP0, Y_TOP1 = 42.0, 34.0   # bord haut du trait, à gauche puis à droite
THICK = 7.5                   # épaisseur verticale du trait
GAP = 2.4                     # espace entre le trait et le « A »
slope = (Y_TOP1 - Y_TOP0) / (X1 - X0)
cosang = 1 / math.sqrt(1 + slope ** 2)
off = GAP / cosang            # décalage vertical équivalent à l'espace perpendiculaire

def top(x): return Y_TOP0 + slope * (x - X0)

# Le « A » en deux jambages convexes (ils se recouvrent un peu au milieu pour éviter tout liseré).
LEFT = [(26.2, 4), (32.4, 4), (32.4, 21.5 - 1.05), (17.4, 60), (4, 60)]
RIGHT = [(64 - x, y) for (x, y) in LEFT][::-1]

def clip(poly, keep):
    """Sutherland-Hodgman sur un demi-plan défini par keep(x, y) -> valeur signée (>= 0 gardé)."""
    out = []
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        fp, fq = keep(*p), keep(*q)
        if fp >= 0: out.append(p)
        if (fp >= 0) != (fq >= 0):
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out

above = lambda x, y: (top(x) - off) - y                 # au-dessus du trait (moins l'espace)
below = lambda x, y: y - (top(x) + THICK + off)          # en dessous du trait (plus l'espace)

def d(poly):
    return 'M' + ' '.join(f'{x:.2f} {y:.2f}' for x, y in poly) + 'Z'

pieces = [clip(p, above) for p in (LEFT, RIGHT)] + [clip(p, below) for p in (LEFT, RIGHT)]
A_D = ''.join(d(p) for p in pieces if len(p) >= 3)
BAND_D = d([(X0, top(X0)), (X1, top(X1)), (X1, top(X1) + THICK), (X0, top(X0) + THICK)])

# --- Texte vectorisé ------------------------------------------------------------
def wordmark(tx):
    size = 25.5
    lsb1 = g.first_lsb(A800, 'A', size)
    base1 = 34
    d1, w1 = g.text_path(A800, 'ALPHANET', size, 0.02, tx - lsb1, base1)
    w1v = w1 - lsb1
    ssize = 12
    lsb2 = g.first_lsb(A600, 'G', ssize)
    base2 = base1 + 8.5 + ssize * .74
    d2, w2 = g.text_path(A600, 'GROUP', ssize, 0.3, tx - lsb2, base2)
    x_rule = tx + (w2 - lsb2) + 6
    rule = (x_rule, base2 - ssize * .74 / 2 - .65, tx + w1v - x_rule, 1.3)
    return d1, d2, rule, tx + w1v

TX = 64 + 16
D1, D2, RULE, RIGHT_EDGE = wordmark(TX)
W = round(RIGHT_EDGE + 1, 1)

COLORS = {
    'couleur': dict(ink='#0b1f3a', blue='#1f5ad6', sub='#1f5ad6'),
    'blanc':   dict(ink='#ffffff', blue='#7aa7ff', sub='#a9c6ff'),
    'noir':    dict(ink='#000000', blue='#000000', sub='#000000'),
}

def lockup_svg(c):
    rx, ry, rw, rh = RULE
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 64" role="img" aria-labelledby="t">\n'
            f'<title id="t">Alphanet Group</title>\n'
            f'<path fill="{c["ink"]}" d="{A_D}"/>\n<path fill="{c["blue"]}" d="{BAND_D}"/>\n'
            f'<path fill="{c["ink"]}" d="{D1}"/>\n<path fill="{c["sub"]}" d="{D2}"/>\n'
            f'<rect fill="{c["sub"]}" x="{rx:.2f}" y="{ry:.2f}" width="{rw:.2f}" height="{rh}"/>\n</svg>\n')

def icon_svg(c):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-labelledby="t">\n'
            f'<title id="t">Alphanet Group</title>\n'
            f'<path fill="{c["ink"]}" d="{A_D}"/>\n<path fill="{c["blue"]}" d="{BAND_D}"/>\n</svg>\n')

# Icône d'onglet / d'appli : carré bleu marine, « A » blanc, trait bleu clair.
TILE = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">\n'
        f'<rect width="64" height="64" rx="14" fill="#0b1f3a"/>\n'
        f'<g transform="translate(32 32.5) scale(.72) translate(-32 -32)">'
        f'<path fill="#ffffff" d="{A_D}"/><path fill="#6f9dff" d="{BAND_D}"/></g>\n</svg>\n')

for name, c in COLORS.items():
    open(f'{OUT}/logo-{name}.svg', 'w').write(lockup_svg(c))
    open(f'{OUT}/logo-icone-{name}.svg', 'w').write(icon_svg(c))
open(f'{OUT}/favicon.svg', 'w').write(TILE)

# Symbole pour le site : couleurs prises dans les variables CSS (thème clair / sombre).
rx, ry, rw, rh = RULE
SITE = (f'      <symbol id="logo" viewBox="0 0 {W} 64">\n'
        f'        <path class="logo-ink" d="{A_D}"/>\n        <path class="logo-blue" d="{BAND_D}"/>\n'
        f'        <path class="logo-ink" d="{D1}"/>\n        <path class="logo-sub" d="{D2}"/>\n'
        f'        <rect class="logo-sub" x="{rx:.2f}" y="{ry:.2f}" width="{rw:.2f}" height="{rh}"/>\n'
        f'      </symbol>\n')
open(f'{OUT}/site-symbol.html', 'w').write(SITE)
print('largeur', W)
