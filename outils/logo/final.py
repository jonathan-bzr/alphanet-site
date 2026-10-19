"""Logo définitif Alphanet Group : écusson bleu marine, « A » blanc, vague bleue (raclette).
Formes calculées (pas de masque ni de trait SVG) pour rester lisibles partout : site, mails, logiciels.
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

# --- Géométrie du pictogramme (repère 64 x 64, centré sur x = 32) ----------------
SL, SR = 3.7, 60.3            # bords gauche et droit de l'écusson
CORNER, SIDE = 7.5, 31.5      # hauteur des coins du haut, fin de la partie droite des côtés
SHIELD_D = (f'M32 0L{SR} {CORNER}V{SIDE}C{SR} 46 46 57 32 64C18 57 {SL} 46 {SL} {SIDE}V{CORNER}Z')

# Le « A » : sommet plat, sans barre (la vague la remplace).
A_POLY = [(28.3, 12.3), (35.7, 12.3), (49.25, 51.6), (41, 51.6), (32, 25.3), (23, 51.6), (14.75, 51.6)]

# La vague : une période de sinusoïde, épaisse, bouts arrondis.
WX0, WX1 = 12.15, 52.45       # début et fin de la ligne médiane
WY, WAMP, WPER, WPH = 42.35, 2.05, 27.67, 14.26
WTHICK = 6.0

def wave_y(x): return WY - WAMP * math.sin(2 * math.pi * (x - WPH) / WPER)
def wave_dy(x): return -WAMP * 2 * math.pi / WPER * math.cos(2 * math.pi * (x - WPH) / WPER)

def wave_poly(n=80, cap=12):
    """Contour plein de la vague : bord haut, bout arrondi, bord bas, bout arrondi."""
    h = WTHICK / 2
    def normal(x):
        dx, dy = 1, wave_dy(x); l = math.hypot(dx, dy)
        return -dy / l, dx / l       # normale vers le bas (y croît vers le bas)
    xs = [WX0 + (WX1 - WX0) * i / n for i in range(n + 1)]
    upper = [(x - normal(x)[0] * h, wave_y(x) - normal(x)[1] * h) for x in xs]
    lower = [(x + normal(x)[0] * h, wave_y(x) + normal(x)[1] * h) for x in xs]
    def capf(x, sign):
        nx, ny = normal(x); a0 = math.atan2(-ny, -nx)   # part du bord haut
        return [(x + h * math.cos(a0 + sign * math.pi * k / cap), wave_y(x) + h * math.sin(a0 + sign * math.pi * k / cap))
                for k in range(1, cap)]
    return upper + capf(WX1, 1) + lower[::-1] + capf(WX0, -1)[::-1]

def d(poly, dx=0.0):
    return 'M' + ' '.join(f'{x + dx:.2f} {y:.2f}' for x, y in poly) + 'Z'

def shield_d(dx=0.0):
    if not dx: return SHIELD_D
    return (f'M{32 + dx:.2f} 0L{SR + dx:.2f} {CORNER}V{SIDE}C{SR + dx:.2f} 46 {46 + dx:.2f} 57 {32 + dx:.2f} 64'
            f'C{18 + dx:.2f} 57 {SL + dx:.2f} 46 {SL + dx:.2f} {SIDE}V{CORNER}Z')

WAVE = wave_poly()

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

DX = -SL                      # dans le logo complet, l'écusson touche le bord gauche
TX = round(SR - SL + 17, 1)
D1, D2, RULE, RIGHT_EDGE = wordmark(TX)
W = round(RIGHT_EDGE + 1, 1)

COLORS = {
    'couleur': dict(shield='#0b1f3a', a='#ffffff', wave='#1f5ad6', ink='#0b1f3a', sub='#1f5ad6'),
    'blanc':   dict(shield='#ffffff', a='#0b1f3a', wave='#7aa7ff', ink='#ffffff', sub='#a9c6ff'),
    # une seule encre : le blanc est le papier, la vague coupe le « A »
    'noir':    dict(shield='#000000', a='#ffffff', wave='#000000', ink='#000000', sub='#000000'),
}

def picto(c, dx=0.0):
    return (f'<path fill="{c["shield"]}" d="{shield_d(dx)}"/>\n<path fill="{c["a"]}" d="{d(A_POLY, dx)}"/>\n'
            f'<path fill="{c["wave"]}" d="{d(WAVE, dx)}"/>\n')

def lockup_svg(c):
    rx, ry, rw, rh = RULE
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 64" role="img" aria-labelledby="t">\n'
            f'<title id="t">Alphanet Group</title>\n' + picto(c, DX) +
            f'<path fill="{c["ink"]}" d="{D1}"/>\n<path fill="{c["sub"]}" d="{D2}"/>\n'
            f'<rect fill="{c["sub"]}" x="{rx:.2f}" y="{ry:.2f}" width="{rw:.2f}" height="{rh}"/>\n</svg>\n')

def icon_svg(c):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-labelledby="t">\n'
            f'<title id="t">Alphanet Group</title>\n' + picto(c) + '</svg>\n')

# Icône d'onglet / d'appli : carré bleu marine, écusson blanc, « A » bleu marine, vague bleu clair.
TILE = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">\n'
        f'<rect width="64" height="64" rx="14" fill="#0b1f3a"/>\n'
        f'<g transform="translate(32 32) scale(.78) translate(-32 -32)">'
        f'<path fill="#ffffff" d="{SHIELD_D}"/><path fill="#0b1f3a" d="{d(A_POLY)}"/>'
        f'<path fill="#5b8cf0" d="{d(WAVE)}"/></g>\n</svg>\n')

for name, c in COLORS.items():
    open(f'{OUT}/logo-{name}.svg', 'w').write(lockup_svg(c))
    open(f'{OUT}/logo-icone-{name}.svg', 'w').write(icon_svg(c))
open(f'{OUT}/favicon.svg', 'w').write(TILE)

# Symbole pour le site : couleurs prises dans les variables CSS (thème clair / sombre).
rx, ry, rw, rh = RULE
SITE = (f'      <symbol id="logo" viewBox="0 0 {W} 64">\n'
        f'        <path class="logo-ink" d="{shield_d(DX)}"/>\n'
        f'        <path class="logo-paper" d="{d(A_POLY, DX)}"/>\n'
        f'        <path class="logo-blue" d="{d(WAVE, DX)}"/>\n'
        f'        <path class="logo-ink" d="{D1}"/>\n        <path class="logo-sub" d="{D2}"/>\n'
        f'        <rect class="logo-sub" x="{rx:.2f}" y="{ry:.2f}" width="{rw:.2f}" height="{rh}"/>\n'
        f'      </symbol>\n')
open(f'{OUT}/site-symbol.html', 'w').write(SITE)
print('largeur', W)
