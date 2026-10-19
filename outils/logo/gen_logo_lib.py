"""Génère les fichiers du logo Alphanet Group (texte vectorisé)."""
import io, sys
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

SRC = '../fonts/pjs.woff2'

def instance(wght):
    f = TTFont(SRC)
    return instancer.instantiateVariableFont(f, {'wght': wght})

def kern_pairs(font):
    """Lit les paires de crénage simples (GPOS PairPos format 1 et 2)."""
    pairs = {}
    if 'GPOS' not in font: return pairs
    gpos = font['GPOS'].table
    for lookup in gpos.LookupList.Lookup:
        subs = lookup.SubTable
        for st in subs:
            if lookup.LookupType == 9: st = st.ExtSubTable
            if getattr(st, 'LookupType', lookup.LookupType) != 2 and lookup.LookupType not in (2, 9): continue
            if not hasattr(st, 'Format'): continue
            cov = st.Coverage.glyphs
            if st.Format == 1:
                for i, g1 in enumerate(cov):
                    for pvr in st.PairSet[i].PairValueRecord:
                        v = pvr.Value1.XAdvance if pvr.Value1 and hasattr(pvr.Value1, 'XAdvance') else 0
                        if v: pairs.setdefault((g1, pvr.SecondGlyph), v)
            elif st.Format == 2:
                cd1 = st.ClassDef1.classDefs; cd2 = st.ClassDef2.classDefs
                for g1 in cov:
                    c1 = cd1.get(g1, 0)
                    rec = st.Class1Record[c1]
                    for g2, c2 in list(cd2.items()):
                        r = rec.Class2Record[c2]
                        v = r.Value1.XAdvance if r.Value1 and hasattr(r.Value1, 'XAdvance') else 0
                        if v: pairs.setdefault((g1, g2), v)
    return pairs

def text_path(font, text, size, tracking_em, x0, baseline, kern=True):
    """Renvoie (d, largeur) du texte vectorisé, en unités SVG."""
    gs = font.getGlyphSet(); cmap = font.getBestCmap(); upm = font['head'].unitsPerEm
    scale = size / upm
    pairs = kern_pairs(font) if kern else {}
    names = [cmap[ord(c)] for c in text]
    x = 0.0; ds = []
    for i, n in enumerate(names):
        pen = SVGPathPen(gs)
        tpen = TransformPen(pen, (scale, 0, 0, -scale, x0 + x * scale, baseline))
        gs[n].draw(tpen)
        ds.append(pen.getCommands())
        adv = gs[n].width
        if i + 1 < len(names):
            adv += pairs.get((n, names[i + 1]), 0)
            adv += tracking_em * upm
        x += adv
    # largeur visuelle réelle (de l'origine au bord du dernier glyphe)
    bp = BoundsPen(gs); last = names[-1]
    gs[last].draw(bp)
    width = (x - gs[last].width + (bp.bounds[2] if bp.bounds else gs[last].width)) * scale
    return ' '.join(ds), width

def first_lsb(font, ch, size):
    gs = font.getGlyphSet(); cmap = font.getBestCmap(); upm = font['head'].unitsPerEm
    bp = BoundsPen(gs); gs[cmap[ord(ch)]].draw(bp)
    return bp.bounds[0] * size / upm


capH = 745 / 1000
