#!/usr/bin/env python3
"""Génère les pages HTML du site Alphanet Group (en-tête, pied de page et menu identiques partout)."""
import os, re, sys

GEN = os.path.dirname(os.path.abspath(__file__))
# Usage : python3 outils/generer/build.py [racine du dépôt] <version ?v=>
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(GEN, '..', '..'))
VERSION = sys.argv[2] if len(sys.argv) > 2 else '20261014-1'
BASE = 'https://alphanet-group.fr/'
PHONE_HTML = '07&nbsp;58&nbsp;34&nbsp;04&nbsp;07'
TEL = 'tel:+33758340407'

CSP = open(os.path.join(GEN, 'csp.html'), encoding='utf-8').read()
JSONLD = open(os.path.join(GEN, 'jsonld.html'), encoding='utf-8').read()
LEGAL_MAIN = open(os.path.join(GEN, 'legal-main.html'), encoding='utf-8').read()

NAV = [
    ('index.html', 'Accueil'),
    ('entreprise.html', 'Entreprise'),
    ('services.html', 'Services'),
    ('engagements.html', 'Engagements'),
    ('contact.html', 'Contact'),
]


def ico(name, cls='ico', extra=''):
    return f'<svg class="{cls}" aria-hidden="true"{extra}><use href="#{name}"/></svg>'


def chip(name):
    return f'<span class="chip-drop" aria-hidden="true">{ico(name)}</span>'


SPRITE = '''  <!-- Logo et pictogrammes partagés -->
  <svg class="svg-sprite" aria-hidden="true" focusable="false">
    <defs>
      <symbol id="logo" viewBox="0 0 260.0 64">
        <path class="logo-ink" d="M28.30 0L56.60 7.5V31.5C56.60 46 42.30 57 28.30 64C14.30 57 0.00 46 0.00 31.5V7.5Z"/>
        <path class="logo-paper" d="M24.60 12.30 32.00 12.30 45.55 51.60 37.30 51.60 28.30 25.30 19.30 51.60 11.05 51.60Z"/>
        <path class="logo-blue" d="M7.30 40.52 7.76 40.33 8.22 40.12 8.70 39.90 9.20 39.67 9.71 39.44 10.23 39.20 10.76 38.96 11.31 38.72 11.88 38.49 12.46 38.27 13.05 38.06 13.65 37.87 14.28 37.70 14.91 37.56 15.55 37.45 16.21 37.36 16.87 37.31 17.53 37.30 18.19 37.32 18.85 37.38 19.50 37.46 20.15 37.58 20.78 37.73 21.40 37.90 22.00 38.09 22.59 38.30 23.17 38.53 23.73 38.76 24.28 39.00 24.81 39.24 25.33 39.48 25.84 39.71 26.33 39.94 26.81 40.16 27.27 40.36 27.72 40.55 28.16 40.72 28.58 40.88 28.99 41.01 29.38 41.13 29.76 41.22 30.13 41.29 30.48 41.35 30.83 41.38 31.18 41.40 31.52 41.40 31.87 41.38 32.22 41.34 32.58 41.28 32.95 41.20 33.34 41.10 33.73 40.98 34.14 40.84 34.57 40.69 35.01 40.51 35.46 40.32 35.93 40.11 36.41 39.89 36.91 39.66 37.41 39.42 37.94 39.18 38.47 38.94 39.02 38.70 39.59 38.47 40.17 38.25 40.76 38.05 41.37 37.86 41.99 37.69 42.62 37.55 43.27 37.44 43.92 37.36 44.58 37.31 45.25 37.30 45.91 37.32 46.57 37.38 47.22 37.47 47.86 37.59 48.49 37.74 49.11 37.91 49.72 38.11 50.42 38.45 51.01 38.97 51.44 39.62 51.69 40.36 51.74 41.15 51.59 41.91 51.24 42.62 50.73 43.20 50.08 43.64 49.33 43.89 48.55 43.94 47.78 43.79 47.38 43.66 46.99 43.55 46.61 43.46 46.25 43.39 45.89 43.34 45.54 43.31 45.20 43.30 44.86 43.31 44.51 43.33 44.15 43.38 43.79 43.44 43.42 43.52 43.03 43.62 42.63 43.75 42.22 43.89 41.79 44.05 41.35 44.23 40.89 44.43 40.42 44.64 39.94 44.87 39.44 45.10 38.93 45.33 38.40 45.58 37.86 45.82 37.31 46.05 36.74 46.28 36.16 46.50 35.56 46.70 34.95 46.88 34.32 47.04 33.69 47.18 33.04 47.28 32.38 47.35 31.72 47.39 31.06 47.40 30.40 47.37 29.74 47.30 29.09 47.20 28.45 47.08 27.82 46.92 27.21 46.74 26.61 46.54 26.02 46.33 25.45 46.10 24.89 45.87 24.35 45.63 23.82 45.39 23.30 45.15 22.80 44.92 22.32 44.69 21.84 44.48 21.38 44.28 20.93 44.09 20.50 43.93 20.09 43.78 19.68 43.65 19.29 43.54 18.92 43.46 18.55 43.39 18.20 43.34 17.85 43.31 17.50 43.30 17.16 43.31 16.81 43.33 16.46 43.38 16.10 43.44 15.72 43.53 15.34 43.63 14.93 43.76 14.52 43.90 14.09 44.07 13.65 44.25 13.19 44.45 12.72 44.66 12.23 44.88 11.73 45.11 11.22 45.35 10.69 45.59 10.15 45.83 9.60 46.07 8.84 46.27 8.06 46.27 7.30 46.07 6.62 45.67 6.07 45.12 5.68 44.44 5.48 43.68 5.48 42.90 5.68 42.14 6.07 41.47 6.63 40.91Z"/>
        <path class="logo-ink" d="M73.6 34.0 82.21956030273437 16.467641845703128H87.99137573242187L96.61093603515624 34.0H90.9943369140625L89.6694326171875 31.19054248046875H80.26100341796875L78.94995727539062 34.0ZM81.99887573242187 27.38885107421875H87.93156030273437L86.33502124023437 23.825475097656252Q86.23523754882812 23.586549560546878 86.05534924316406 23.149164794921877Q85.8754609375 22.711780029296875 85.68171447753906 22.21424987792969Q85.48796801757813 21.716719726562502 85.32443432617188 21.289040649414062Q85.16090063476562 20.861361572265626 85.07996801757812 20.65570556640625H84.889826171875Q84.70190063476562 21.124131103515627 84.45715417480469 21.731698486328128Q84.21240771484375 22.339265869140625 83.98623217773437 22.90969140625Q83.760056640625 23.480116943359377 83.59541479492187 23.837116943359376Z M99.66599291992188 34.0V16.467641845703128H104.858517578125V29.820801513671874H116.11509912109375V34.0Z M119.40299291992187 34.0V16.467641845703128H132.93404248046875Q134.65640063476562 16.467641845703128 135.95329602050782 17.22792907714844Q137.25019140625 17.988216308593753 137.9722286376953 19.33139892578125Q138.69426586914062 20.674581542968753 138.69426586914062 22.42649453667535Q138.69426586914062 24.195237548828125 137.95947863769533 25.556991088867186Q137.22469140625 26.91874462890625 135.9161541748047 27.672102783203123Q134.60761694335937 28.4254609375 132.88747509765625 28.4254609375H124.595517578125V34.0ZM124.595517578125 24.5772021484375H131.44230493164062Q132.5944326171875 24.5772021484375 133.18999291992185 24.02340813623716Q133.78555322265623 23.469614124036816 133.78555322265623 22.450451081576414Q133.78555322265623 21.75887939453125 133.5156863455636 21.28657901908256Q133.24581946847098 20.81427864363387 132.726842351423 20.565089639199748Q132.207865234375 20.315900634765626 131.44230493164062 20.315900634765626H124.595517578125Z M141.86849291992186 34.0V16.467641845703128H147.061017578125V22.99232983398438H157.58370214843748V16.467641845703128H162.7762268066406V34.0H157.58370214843748V27.1715283203125H147.061017578125V34.0Z M165.8335 34.0 174.45306030273437 16.467641845703128H180.22487573242185L188.84443603515624 34.0H183.2278369140625L181.9029326171875 31.19054248046875H172.49450341796873L171.18345727539062 34.0ZM174.23237573242187 27.38885107421875H180.16506030273436L178.56852124023436 23.825475097656252Q178.4687375488281 23.586549560546878 178.28884924316407 23.149164794921877Q178.1089609375 22.711780029296875 177.91521447753905 22.21424987792969Q177.7214680175781 21.716719726562502 177.55793432617185 21.289040649414062Q177.39440063476562 20.861361572265626 177.31346801757812 20.65570556640625H177.123326171875Q176.9354006347656 21.124131103515627 176.69065417480468 21.731698486328128Q176.44590771484374 22.339265869140625 176.2197321777344 22.90969140625Q175.993556640625 23.480116943359377 175.82891479492187 23.837116943359376Z M191.89949291992187 34.0V16.467641845703128H196.54378002929687L205.63288647460936 24.647638427734375Q205.86737939453124 24.844989501953126 206.22937231445312 25.204766113281252Q206.591365234375 25.564542724609375 206.98467907714843 25.949819335937498Q207.37799291992187 26.335095947265625 207.67956030273436 26.6460888671875H207.9112766113281Q207.899634765625 26.1959541015625 207.88217199707032 25.5035693359375Q207.8647092285156 24.8111845703125 207.8647092285156 24.27346826171875V16.467641845703128H212.77951049804688V34.0H208.197865234375L199.33270556640625 25.99516650390625Q198.7273544921875 25.456889892578126 198.05825341796873 24.799150512695313Q197.38915234375 24.1414111328125 196.9855849609375 23.74006005859375H196.77936865234375Q196.79101049804686 24.085418212890623 196.80265234374997 24.8171611328125Q196.8142941894531 25.548904052734375 196.8142941894531 26.398173583984374V34.0Z M217.60349291992188 34.0V16.467641845703128H235.88031909179688V20.315900634765626H222.8098757324219V23.260627685546876H234.25331201171875V26.9841630859375H222.8098757324219V30.1517412109375H236.08431909179689V34.0Z M246.18399999999997 34.0V20.646840332031253H238.58665600585937V16.467641845703128H258.97386865234375V20.646840332031253H251.3765246582031V34.0Z"/>
        <path class="logo-sub" d="M78.592 51.523999999999994Q76.09599999999999 51.523999999999994 74.84799999999998 50.46799999999999Q73.6 49.41199999999999 73.6 47.263999999999996Q73.6 45.85999999999999 74.23599999999999 44.90599999999999Q74.87199999999999 43.952 76.07799999999999 43.471999999999994Q77.28399999999999 42.992 78.964 42.992Q80.056 42.992 80.95599999999999 43.178Q81.856 43.364 82.50999999999999 43.742Q83.16399999999999 44.12 83.51799999999999 44.696Q83.87199999999999 45.27199999999999 83.87199999999999 46.05199999999999H82.09599999999999Q82.09599999999999 45.62 81.844 45.31999999999999Q81.59199999999998 45.019999999999996 81.16 44.846Q80.728 44.672 80.18199999999999 44.593999999999994Q79.636 44.516 79.03599999999999 44.516Q78.26799999999999 44.516 77.61399999999999 44.666Q76.96 44.815999999999995 76.47999999999999 45.134Q75.99999999999999 45.452 75.73599999999999 45.943999999999996Q75.472 46.43599999999999 75.472 47.108V47.395999999999994Q75.472 48.331999999999994 75.88 48.901999999999994Q76.288 49.471999999999994 77.038 49.73599999999999Q77.788 49.99999999999999 78.80799999999999 49.99999999999999Q79.93599999999999 49.99999999999999 80.66199999999999 49.79599999999999Q81.38799999999999 49.592 81.74199999999999 49.208Q82.09599999999999 48.824 82.09599999999999 48.30799999999999V48.211999999999996H78.75999999999999V46.77199999999999H83.88399999999999V51.379999999999995H82.756L82.564 50.3Q82.11999999999999 50.73199999999999 81.50199999999998 51.001999999999995Q80.88399999999999 51.272 80.14599999999999 51.397999999999996Q79.40799999999999 51.523999999999994 78.592 51.523999999999994Z M89.716 51.379999999999995V43.135999999999996H96.244Q97.11999999999999 43.135999999999996 97.678 43.489999999999995Q98.23599999999999 43.843999999999994 98.512 44.425999999999995Q98.788 45.007999999999996 98.788 45.715999999999994Q98.788 46.44799999999999 98.41 47.08999999999999Q98.032 47.73199999999999 97.24 48.092L98.99199999999999 51.379999999999995H96.94L95.428 48.44H91.53999999999999V51.379999999999995ZM91.53999999999999 46.928H95.74Q96.30399999999999 46.928 96.60999999999999 46.598Q96.916 46.267999999999994 96.916 45.751999999999995Q96.916 45.403999999999996 96.78399999999999 45.157999999999994Q96.65199999999999 44.91199999999999 96.38799999999999 44.785999999999994Q96.124 44.66 95.74 44.66H91.53999999999999Z M109.29518059299191 51.523999999999994Q107.661628032345 51.523999999999994 106.4708140161725 51.025999999999996Q105.27999999999999 50.528 104.63799999999999 49.574Q103.996 48.62 103.996 47.25767634854771Q103.996 45.88399999999999 104.63799999999999 44.93599999999999Q105.27999999999999 43.98799999999999 106.4708140161725 43.489999999999995Q107.661628032345 42.992 109.29518059299191 42.992Q110.94399999999999 42.992 112.13199999999999 43.489999999999995Q113.32 43.98799999999999 113.96199999999999 44.93599999999999Q114.604 45.88399999999999 114.604 47.25767634854771Q114.604 48.62 113.96199999999999 49.574Q113.32 50.528 112.13199999999999 51.025999999999996Q110.94399999999999 51.523999999999994 109.29518059299191 51.523999999999994ZM109.3 49.99999999999999Q110.044 49.99999999999999 110.66799999999999 49.831999999999994Q111.29199999999999 49.663999999999994 111.75399999999999 49.339999999999996Q112.216 49.016 112.47399999999999 48.522999999999996Q112.732 48.029999999999994 112.732 47.38399999999999V47.108Q112.732 46.46443835616438 112.47399999999999 45.97621917808219Q112.216 45.48799999999999 111.75399999999999 45.163999999999994Q111.29199999999999 44.839999999999996 110.66799999999999 44.678Q110.044 44.516 109.3 44.516Q108.556 44.516 107.93199999999999 44.678Q107.30799999999999 44.839999999999996 106.84599999999999 45.163999999999994Q106.38399999999999 45.48799999999999 106.13199999999999 45.97621917808219Q105.88 46.46443835616438 105.88 47.108V47.38399999999999Q105.88 48.029999999999994 106.13199999999999 48.522999999999996Q106.38399999999999 49.016 106.84599999999999 49.339999999999996Q107.30799999999999 49.663999999999994 107.93199999999999 49.831999999999994Q108.556 49.99999999999999 109.3 49.99999999999999Z M124.672 51.523999999999994Q123.124 51.523999999999994 122.10999999999999 51.044Q121.09599999999999 50.56399999999999 120.59799999999998 49.681999999999995Q120.1 48.8 120.1 47.599999999999994V43.135999999999996H121.92399999999999V47.516Q121.92399999999999 48.70399999999999 122.63799999999999 49.35199999999999Q123.35199999999999 49.99999999999999 124.672 49.99999999999999Q125.99199999999999 49.99999999999999 126.70599999999999 49.35199999999999Q127.42 48.70399999999999 127.42 47.516V43.135999999999996H129.244V47.599999999999994Q129.244 48.8 128.74599999999998 49.681999999999995Q128.248 50.56399999999999 127.24 51.044Q126.232 51.523999999999994 124.672 51.523999999999994Z M135.09999999999997 51.379999999999995V43.135999999999996H141.14799999999997Q141.95199999999997 43.135999999999996 142.546 43.483999999999995Q143.14 43.831999999999994 143.46999999999997 44.437999999999995Q143.79999999999998 45.044 143.79999999999998 45.83582222222222Q143.79999999999998 46.61599999999999 143.464 47.233999999999995Q143.128 47.852 142.522 48.199999999999996Q141.91599999999997 48.547999999999995 141.09999999999997 48.547999999999995H136.92399999999998V51.379999999999995ZM136.92399999999998 47.023999999999994H140.59599999999998Q141.236 47.023999999999994 141.58799999999997 46.71121917808219Q141.93999999999997 46.39843835616438 141.93999999999997 45.847095890410955Q141.93999999999997 45.476 141.78365714285712 45.21135135135135Q141.62731428571428 44.946702702702694 141.32765714285713 44.803351351351345Q141.028 44.66 140.59599999999998 44.66H136.92399999999998Z"/>
        <rect class="logo-sub" x="149.80" y="46.29" width="109.17" height="1.3"/>
      </symbol>
      <symbol id="i-arrow" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></symbol>
      <symbol id="i-phone" viewBox="0 0 24 24"><path d="M6.6 3.5h2.9l1.6 4.1-2.1 1.4a11 11 0 0 0 6 6l1.4-2.1 4.1 1.6v2.9a2 2 0 0 1-2.2 2A16 16 0 0 1 4.6 5.7a2 2 0 0 1 2-2.2z"/></symbol>
      <symbol id="i-check" viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></symbol>
      <symbol id="i-pin" viewBox="0 0 24 24"><path d="M12 21s-7-6.1-7-11.4a7 7 0 0 1 14 0C19 14.9 12 21 12 21z"/><circle cx="12" cy="9.6" r="2.6"/></symbol>
      <symbol id="i-sun" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2.5v2M12 19.5v2M4.6 4.6 6 6M18 18l1.4 1.4M2.5 12h2M19.5 12h2M4.6 19.4 6 18M18 6l1.4-1.4"/></symbol>
      <symbol id="i-moon" viewBox="0 0 24 24"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/></symbol>
      <symbol id="i-menu" viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></symbol>
      <symbol id="i-close" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18"/></symbol>
      <symbol id="i-lock" viewBox="0 0 24 24"><rect x="5" y="10.5" width="14" height="10" rx="2"/><path d="M8.5 10.5V8a3.5 3.5 0 0 1 7 0v2.5"/></symbol>
      <symbol id="i-shield" viewBox="0 0 24 24"><path d="M12 3 4.5 6v5.5c0 4.6 3.1 8 7.5 9.5 4.4-1.5 7.5-4.9 7.5-9.5V6z"/><path d="M8.8 12l2.4 2.4 4-4.4"/></symbol>
      <symbol id="i-users" viewBox="0 0 24 24"><circle cx="9" cy="8.5" r="3.2"/><path d="M3.5 19c.5-3.2 2.7-5 5.5-5s5 1.8 5.5 5"/><circle cx="17" cy="9.5" r="2.5"/><path d="M16 14.2c2.7-.2 4.5 1.3 5 4.3"/></symbol>
      <symbol id="i-leaf" viewBox="0 0 24 24"><path d="M5 19c0-8 4.5-13 14-14 0 9.5-5 14-13 14"/><path d="M5 19c2-4 4.5-6.5 8-8.5"/></symbol>
      <symbol id="i-eye" viewBox="0 0 24 24"><path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="2.8"/></symbol>
      <!-- Services -->
      <symbol id="i-office" viewBox="0 0 24 24"><rect x="4.5" y="3" width="15" height="18" rx="2"/><path d="M8.5 7h1.5M14 7h1.5M8.5 11h1.5M14 11h1.5M8.5 15h1.5M14 15h1.5M10 21v-2.5h4V21"/></symbol>
      <symbol id="i-copro" viewBox="0 0 24 24"><path d="M3 21h18M5 21V8.5l6-4V21M11 21V10l8 3v8M7.8 9.5v.01M7.8 13v.01M7.8 16.5v.01M15 15.5v.01M15 18.5v.01"/></symbol>
      <symbol id="i-store" viewBox="0 0 24 24"><path d="M4.5 10.5V20h15v-9.5M3 9.5 4.6 4h14.8L21 9.5a3 3 0 0 1-6 0 3 3 0 0 1-6 0 3 3 0 0 1-6 0zM10 20v-4.5h4V20"/></symbol>
      <symbol id="i-window" viewBox="0 0 24 24"><rect x="4" y="3" width="16" height="18" rx="1.5"/><path d="M12 3v18M4 12h16M7 8.5l2-2M15 17.5l2-2"/></symbol>
      <symbol id="i-sparkle" viewBox="0 0 24 24"><path d="M10.5 3.5 12.3 8.2 17 10l-4.7 1.8-1.8 4.7-1.8-4.7L4 10l4.7-1.8zM18 14.5l.9 2.1 2.1.9-2.1.9-.9 2.1-.9-2.1-2.1-.9 2.1-.9z"/></symbol>
      <symbol id="i-hotel" viewBox="0 0 24 24"><path d="M3 19V6M3 15h18M21 19v-5.5a3 3 0 0 0-3-3h-7.5V15"/><circle cx="6.6" cy="11.6" r="1.9"/></symbol>
      <symbol id="i-drop" viewBox="0 0 24 24"><path d="M12 3s-6 6.6-6 11a6 6 0 0 0 12 0c0-4.4-6-11-6-11z"/><path d="M9.2 14.6a2.9 2.9 0 0 0 2.8 2.7"/></symbol>
    </defs>
  </svg>
'''

BUBBLES = '<div class="hero-bubbles" aria-hidden="true"><span></span><span class="b-m"></span><span class="b-m"></span><span class="b-s"></span><span class="b-s"></span><span class="b-m"></span><span class="b-s"></span><span class="b-s"></span><span class="b-m"></span><span class="b-s"></span><span class="b-s"></span><span></span></div>'

WAVE = '<svg class="wave" viewBox="0 0 1440 80" preserveAspectRatio="none" aria-hidden="true" focusable="false"><path d="M0 50C200 82 420 82 620 52S1040 6 1240 30s160 22 200 16V80H0Z"/></svg>'


def head(title, desc, page, extra='', robots=None, jsonld=''):
    url = BASE + ('' if page == 'index.html' else page)
    og = f'''  <meta property="og:type" content="website">
  <meta property="og:locale" content="fr_FR">
  <meta property="og:site_name" content="Alphanet Group">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{BASE}assets/img/og-image.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Logo Alphanet Group, nettoyage professionnel dans l’Hérault (34) et en Occitanie">
  <meta name="twitter:card" content="summary_large_image">
''' if not robots else ''
    rb = f'  <meta name="robots" content="{robots}">\n' if robots else ''
    # Fil d'Ariane lisible par les moteurs de recherche (pages autres que l'accueil)
    if page != 'index.html' and not jsonld:
        crumb = {'entreprise.html': 'Entreprise', 'services.html': 'Services', 'engagements.html': 'Engagements', 'contact.html': 'Contact', 'mentions-legales.html': 'Mentions légales'}[page]
        jsonld = f'''  <script type="application/ld+json">
  {{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
    {{"@type": "ListItem", "position": 1, "name": "Accueil", "item": "{BASE}"}},
    {{"@type": "ListItem", "position": 2, "name": "{crumb}", "item": "{url}"}}
  ]}}
  </script>
'''
    return f'''<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <!-- Sécurité : la page ne peut charger que les fichiers du site lui-même (aucun service tiers, aucun script extérieur) -->
{CSP}  <meta name="referrer" content="strict-origin-when-cross-origin">

  <title>{title}</title>
  <meta name="description" content="{desc}">
{rb}  <link rel="canonical" href="{url}">
  <meta name="color-scheme" content="light dark">
  <meta name="theme-color" content="#e8f3fd" data-theme-color>

{og}
  <link rel="icon" href="assets/img/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
  <link rel="preload" href="assets/fonts/plus-jakarta-sans-latin.woff2" as="font" type="font/woff2" crossorigin>
  <!-- Le numéro ?v= force le rechargement après chaque mise à jour : à augmenter quand le CSS ou le JS change -->
  <link rel="stylesheet" href="assets/css/styles.css?v={VERSION}">
  <script src="assets/js/theme.js?v={VERSION}"></script>
  <script src="assets/js/main.js?v={VERSION}" defer></script>
{jsonld}</head>
<body>
  <a class="skip-link" href="#contenu">Aller au contenu</a>

{SPRITE}'''.replace('\n\n\n', '\n\n')


def header(active):
    def link(href, label, menu=False):
        cur = ' aria-current="page"' if href == active else ''
        return f'<li><a href="{href}"{cur}>{label}</a></li>'
    desktop = '\n          '.join(link(h, l) for h, l in NAV)
    mobile = '\n          '.join(link(h, l) for h, l in NAV)
    return f'''
  <!-- ================================================================
       En-tête
       ================================================================ -->
  <header class="site-header" data-header>
    <div class="container header-inner">
      <a class="brand" href="index.html" aria-label="Alphanet Group, accueil">
        {ico('logo', 'brand-logo')}
      </a>
      <nav class="nav" aria-label="Navigation principale">
        <ul class="nav-list">
          {desktop}
        </ul>
      </nav>
      <div class="header-actions">
        <a class="btn btn-primary btn-sm header-cta" href="contact.html#formulaire">Devis gratuit</a>
        <button class="icon-btn nav-toggle" type="button" aria-expanded="false" aria-controls="menu" aria-label="Ouvrir le menu" data-nav-toggle>
          {ico('i-menu', 'ico ico-menu')}
          {ico('i-close', 'ico ico-close')}
        </button>
      </div>
    </div>
    <!-- Menu sur téléphone et tablette -->
    <div class="menu" id="menu" data-menu inert>
      <nav class="container" aria-label="Menu">
        <ul class="menu-list">
          {mobile}
        </ul>
        <div class="menu-actions">
          <a class="btn btn-primary btn-lg" href="contact.html#formulaire">Demander un devis gratuit</a>
          <a class="btn btn-ghost btn-lg" href="{TEL}">{ico('i-phone')}{PHONE_HTML}</a>
        </div>
      </nav>
    </div>
  </header>
'''


def footer(mobile_bar=True):
    links = '\n          '.join(f'<li><a href="{h}">{l}</a></li>' for h, l in NAV)
    bar = '''
  <!-- Barre d'action sur téléphone -->
  <div class="mobile-bar" data-mobile-bar inert>
    <a class="btn btn-ghost" href="%s">%s Appeler</a>
    <a class="btn btn-primary" href="contact.html#formulaire">Devis gratuit</a>
  </div>
''' % (TEL, ico('i-phone')) if mobile_bar else ''
    return f'''
  <!-- ================================================================
       Pied de page
       ================================================================ -->
  <footer class="site-footer">
    <div class="container footer-inner">
      <div class="footer-brand">
        <a class="brand" href="index.html" aria-label="Alphanet Group, accueil">
          {ico('logo', 'brand-logo')}
        </a>
        <p>Nettoyage professionnel de bureaux, hôtels, copropriétés et commerces depuis 2014. Principalement dans l’Hérault (34), partout en Occitanie et dans le Sud de la France.</p>
      </div>

      <nav class="footer-nav" aria-label="Plan du site">
        <p class="footer-title">Le site</p>
        <ul>
          {links}
        </ul>
      </nav>

      <div class="footer-contact">
        <p class="footer-title">Contact</p>
        <a href="{TEL}">{ico('i-phone')}{PHONE_HTML}</a>
        <p>{ico('i-pin')}Occitanie et Sud de la France</p>
        <a href="contact.html#formulaire">{ico('i-arrow')}Demander un devis gratuit</a>
      </div>
    </div>

    <div class="container footer-bottom">
      <p>© <span data-current-year>2026</span> Alphanet Group</p>
      <p><a href="mentions-legales.html">Mentions légales</a><span aria-hidden="true"> · </span><a href="mentions-legales.html#donnees">Données personnelles</a></p>
    </div>
  </footer>
{bar}
  <!-- Mode clair / sombre : bouton flottant en bas à droite, toujours accessible -->
  <button class="theme-fab" type="button" aria-label="Passer en mode sombre" title="Mode sombre" data-theme-toggle>
    {ico('i-moon', 'ico ico-moon')}{ico('i-sun', 'ico ico-sun')}
  </button>
</body>
</html>
'''


# ---------------------------------------------------------------------------
# Contenu partagé
# ---------------------------------------------------------------------------
STATS = f'''<div class="bulle hero-card reveal" role="group" aria-labelledby="stats-title">
          <p class="hero-card-title" id="stats-title">Alphanet en bref</p>
          <ul class="stats">
            <li class="stat"><strong class="stat-num"><span data-count="12" data-count-since="2014-04-10">12</span><span class="stat-unit">&nbsp;ans</span></strong><span class="stat-label">d’expérience à Montpellier</span></li>
            <li class="stat"><strong class="stat-num"><span data-count="6">6</span></strong><span class="stat-label">types de locaux et d’interventions</span></li>
            <li class="stat"><strong class="stat-num"><span data-count="1">1</span></strong><span class="stat-label">interlocuteur, du devis au suivi</span></li>
            <li class="stat"><strong class="stat-num"><span data-count="34">34</span></strong><span class="stat-label">l’Hérault, notre secteur principal</span></li>
          </ul>
        </div>'''

ZONE = '''<div class="zone">
            <p class="zone-title">%s Zone d’intervention</p>
            <p class="zone-text">Alphanet Group intervient principalement dans l’Hérault (34), mais aussi dans toute l’Occitanie et les autres régions du Sud. Pour toute question sur votre localisation, appelez-nous&nbsp;: nous étudions chaque demande.</p>
          </div>''' % ico('i-pin')

SERVICES = [
    dict(id='bureaux', key='bureaux', icon='i-office', name='Bureaux et locaux professionnels', featured=True,
         short='Espaces de travail, salles de réunion, sanitaires et espaces de pause, à la fréquence qui vous convient.',
         intro='Un environnement de travail propre, c’est du confort pour vos équipes et une bonne image pour vos visiteurs. Nous intervenons à la fréquence qui vous convient : tous les jours, plusieurs fois par semaine ou ponctuellement.',
         more='Avant la première intervention, nous convenons avec vous des tâches, des horaires et des consignes d’accès, pour que chaque passage se déroule sans gêner votre activité.',
         checks=['Sols : aspiration et lavage adaptés à chaque revêtement',
                 'Bureaux, postes de travail et salles de réunion',
                 'Sanitaires nettoyés et désinfectés',
                 'Espaces de pause et cuisines',
                 'Vidage des corbeilles et évacuation des déchets courants',
                 'Points de contact (poignées, interrupteurs, rampes) désinfectés régulièrement']),
    dict(id='hotellerie', key='hotellerie', icon='i-hotel', name='Hôtellerie', featured=True,
         short='Chambres, réception et espaces communs : une propreté irréprochable pour l’expérience de vos clients.',
         intro='Dans un hôtel, la propreté se remarque dès l’arrivée et compte dans l’avis de chaque client. Nous entretenons vos chambres et vos espaces communs avec méthode, au rythme de vos arrivées et de vos départs.',
         more='Nous convenons avec vous des tâches, des horaires et des priorités (chambres à libérer, recouches, espaces communs), pour une organisation fluide avec vos équipes de réception.',
         checks=['Chambres et salles de bain',
                 'Hall d’accueil, réception et couloirs',
                 'Salles de petit-déjeuner, de réunion et de séminaire',
                 'Sanitaires des espaces communs',
                 'Vitres et parties vitrées',
                 'Interventions planifiées selon vos arrivées et vos départs']),
    dict(id='coproprietes', key='coproprietes', icon='i-copro', name='Copropriétés',
         short='Halls, escaliers et parties communes, en lien direct avec votre syndic.',
         intro='Des parties communes propres valorisent l’immeuble et le quotidien des résidents. Nous travaillons en lien direct avec votre syndic ou votre conseil syndical, avec un interlocuteur unique pour toute la copropriété.',
         more='Le cahier des charges est écrit : vous savez ce qui est fait, à quelle fréquence, et vous pouvez nous signaler la moindre remarque.',
         checks=['Halls d’entrée et paliers',
                 'Escaliers et cages d’escalier',
                 'Cabines d’ascenseur',
                 'Locaux poubelles et locaux à vélos',
                 'Vitres des parties communes',
                 'Passages réguliers selon le cahier des charges convenu']),
    dict(id='commerces', key='commerces', icon='i-store', name='Commerces',
         short='Un cadre impeccable pour vos clients, avant l’ouverture ou après la fermeture.',
         intro='Pour un commerce, la propreté fait partie de l’accueil. Nous intervenons avant l’ouverture ou après la fermeture pour que vos clients trouvent un lieu impeccable, sans gêner votre activité.',
         more='Boutique, restaurant, salon, agence : nous adaptons les produits et les méthodes à vos surfaces et à vos contraintes.',
         checks=['Surfaces de vente, réserves et arrière-boutiques',
                 'Vitrines et portes vitrées',
                 'Caisses, comptoirs et mobilier',
                 'Sanitaires clients et du personnel',
                 'Horaires décalés : avant l’ouverture, après la fermeture',
                 'Intervention régulière ou ponctuelle, selon vos besoins']),
    dict(id='vitrerie', key='vitrerie', icon='i-window', name='Vitrerie',
         short='Vitres, vitrines et cloisons vitrées, nettes et sans traces.',
         intro='Des vitres nettes laissent entrer la lumière et donnent une meilleure image de vos locaux. Nous nettoyons vos surfaces vitrées à l’intérieur comme à l’extérieur, à la fréquence de votre choix.',
         more='La vitrerie peut s’ajouter à un contrat d’entretien existant ou faire l’objet d’une intervention séparée.',
         checks=['Vitres et fenêtres, côté intérieur et côté extérieur',
                 'Vitrines et baies vitrées',
                 'Cloisons vitrées de bureaux',
                 'Portes vitrées et garde-corps vitrés',
                 'Châssis et rebords de fenêtres',
                 'Finition sans traces']),
    dict(id='remise-en-etat', key='remise-en-etat', icon='i-sparkle', name='Remise en état et après sinistre',
         short='Après travaux, déménagement, dégât des eaux ou incendie : des locaux propres et prêts à servir.',
         intro='Après des travaux, un déménagement ou une longue inoccupation, mais aussi après un dégât des eaux, un incendie ou une inondation, vos locaux doivent être remis en état avant de servir à nouveau. Nous intervenons pour les nettoyer, les désinfecter et vous permettre de reprendre votre activité au plus vite.',
         more='Une visite préalable nous permet d’évaluer l’état des lieux et de vous remettre un devis précis. En cas d’urgence après un sinistre, appelez-nous directement au 07&nbsp;58&nbsp;34&nbsp;04&nbsp;07 : nous évaluons la situation avec vous et organisons l’intervention.',
         checks=['Poussières de chantier, traces de peinture, de colle ou de plâtre',
                 'Sols, plinthes, menuiseries, sanitaires et cuisines',
                 'Vitres et vitrines',
                 'Traces de suie et de fumée après un incendie',
                 'Désinfection après un dégât des eaux ou une inondation',
                 'Évacuation des déchets liés aux travaux ou au sinistre',
                 'Intervention rapide en cas d’urgence']),
]


def cta_band(title='Parlons de vos locaux', text='Visite et devis gratuits, sans engagement. Nous vous répondons rapidement.'):
    return f'''
    <section class="cta-band" aria-labelledby="cta-title">
      <div class="container cta-inner">
        <div>
          <h2 class="h2" id="cta-title">{title}</h2>
          <p>{text}</p>
        </div>
        <div class="cta-actions">
          <a class="btn btn-white btn-lg" href="contact.html#formulaire">Demander un devis {ico('i-arrow', 'ico ico-arrow')}</a>
          <a class="btn btn-outline-white btn-lg" href="{TEL}">{ico('i-phone')}{PHONE_HTML}</a>
        </div>
      </div>
    </section>
'''


def page_hero(title, lead, crumb, extra='', soft=False):
    cls = 'page-hero page-hero--soft' if soft else 'page-hero'
    return f'''
    <section class="{cls}" aria-labelledby="page-title">
      <div class="hero-media" aria-hidden="true"></div>
      {BUBBLES}
      <div class="container">
        <nav class="breadcrumb" aria-label="Fil d’Ariane">
          <a href="index.html">Accueil</a><span aria-hidden="true">›</span><span aria-current="page">{crumb}</span>
        </nav>
        <h1 class="page-title" id="page-title">{title}</h1>
        <p class="lead">{lead}</p>{extra}
      </div>
      {WAVE}
    </section>
'''


def write(name, html):
    with open(os.path.join(ROOT, name), 'w', encoding='utf-8') as f:
        f.write(html)
    print('écrit', name, len(html))


# ---------------------------------------------------------------------------
# Accueil
# ---------------------------------------------------------------------------
def page_index():
    cards = ''
    for sv in SERVICES:
        feat = ' service--featured' if sv.get('featured') else ''
        cards += f'''
          <li class="service{feat} reveal">
            {chip(sv['icon'])}
            <h3 class="h3"><a href="services.html#{sv['id']}">{sv['name']}</a></h3>
            <p>{sv['short']}</p>
            <span class="service-more" aria-hidden="true">En savoir plus {ico('i-arrow')}</span>
          </li>'''
    html = head('Alphanet Group | Nettoyage professionnel à Montpellier, Hérault (34)',
                'Nettoyage de bureaux, hôtels, copropriétés et commerces depuis 2014, principalement dans l’Hérault (34), en Occitanie et dans le Sud. Devis gratuit au 07 58 34 04 07.',
                'index.html', jsonld=JSONLD)
    html += header('index.html')
    html += f'''
  <main id="contenu">
    <!-- ================================================================
         Accueil
         ================================================================ -->
    <section class="hero" id="top" aria-labelledby="hero-title">
      <div class="hero-media" aria-hidden="true"></div>
      {BUBBLES}
      <div class="container hero-grid">
        <div class="hero-content">
          <p class="hero-eyebrow"><span class="dot" aria-hidden="true"></span>Nettoyage professionnel · Occitanie</p>
          <h1 class="hero-title" id="hero-title">Des locaux impeccables, <span class="accent">en toute confiance.</span></h1>
          <p class="hero-lead">Bureaux, hôtels, copropriétés et commerces&nbsp;: nous entretenons vos locaux depuis 2014, principalement dans l’Hérault et partout dans le Sud, avec des équipes stables et un interlocuteur unique.</p>
          <div class="hero-actions" data-hero-actions>
            <a class="btn btn-primary btn-lg" href="contact.html#formulaire">Demander un devis gratuit {ico('i-arrow', 'ico ico-arrow')}</a>
            <a class="btn btn-ghost btn-lg" href="{TEL}">{ico('i-phone')}{PHONE_HTML}</a>
          </div>
          <ul class="hero-points">
            <li>{ico('i-check')}Devis gratuit et sans engagement</li>
            <li>{ico('i-check')}Horaires adaptés à votre activité</li>
          </ul>
        </div>
        <!-- Chiffres clés : le « 12 » est recalculé chaque année par le script à partir de la date de création (10 avril 2014) -->
        {STATS}
      </div>
      {WAVE}
    </section>

    <!-- ================================================================
         Notre mission
         ================================================================ -->
    <section class="section" id="mission" aria-labelledby="mission-title">
      <div class="container split split--text-wide">
        <div class="prose reveal">
          <p class="eyebrow">Notre mission</p>
          <h2 class="h2" id="mission-title">Des locaux propres, une équipe sur laquelle compter</h2>
          <p>Depuis 2014, Alphanet Group entretient les bureaux, les hôtels, les copropriétés et les commerces principalement dans l’Hérault (34), mais aussi partout en Occitanie et dans les autres régions du Sud. Notre objectif&nbsp;: que vos locaux soient accueillants chaque jour, sans que vous ayez à vous en occuper.</p>
          <p>Un seul interlocuteur, des équipes stables, des horaires adaptés à votre activité&nbsp;: nous faisons simple pour que vous puissiez vous concentrer sur votre métier.</p>
          <a class="link-more" href="entreprise.html">Découvrir l’entreprise {ico('i-arrow')}</a>
        </div>
        <ul class="values values--pairs">
          <li class="value reveal">
            {chip('i-pin')}
            <h3 class="h3">Proximité</h3>
            <p>Implantés dans l’Hérault (34), nous intervenons dans toute l’Occitanie et le Sud de la France.</p>
          </li>
          <li class="value reveal">
            {chip('i-shield')}
            <h3 class="h3">Fiabilité</h3>
            <p>Des équipes stables et des passages réguliers, aux horaires convenus.</p>
          </li>
          <li class="value reveal">
            {chip('i-lock')}
            <h3 class="h3">Discrétion</h3>
            <p>Le respect de vos locaux, de vos consignes d’accès et de votre confidentialité.</p>
          </li>
          <li class="value reveal">
            {chip('i-eye')}
            <h3 class="h3">Transparence</h3>
            <p>Un devis détaillé et un interlocuteur qui répond à vos questions.</p>
          </li>
        </ul>
      </div>
    </section>

    <!-- ================================================================
         Services
         ================================================================ -->
    <section class="section section--soft" id="services" aria-labelledby="services-title">
      <div class="container">
        <div class="section-head reveal">
          <p class="eyebrow">Nos services</p>
          <h2 class="h2" id="services-title">Un savoir-faire pour chaque type de locaux</h2>
          <p class="lead">Bureaux et hôtellerie en tête, et tout ce dont vos locaux ont besoin&nbsp;: interventions régulières ou ponctuelles, en journée ou en horaires décalés.</p>
        </div>
        <ul class="services">{cards}
        </ul>
        <div class="section-foot">
          <a class="btn btn-ghost btn-lg" href="services.html">Voir tous nos services {ico('i-arrow', 'ico ico-arrow')}</a>
        </div>
      </div>
    </section>

    <!-- ================================================================
         Engagements
         ================================================================ -->
    <section class="section" id="engagements" aria-labelledby="engagements-title">
      <div class="container">
        <div class="section-head reveal">
          <p class="eyebrow">Nos engagements</p>
          <h2 class="h2" id="engagements-title">Ce que vous pouvez attendre de nous</h2>
          <p class="lead">Un service suivi, des équipes stables et des méthodes respectueuses de l’environnement et de votre confidentialité.</p>
        </div>
        <ul class="values">
          <li class="value reveal">
            {chip('i-check')}
            <h3 class="h3">Un service suivi</h3>
            <p>Un cahier des charges clair et des contrôles réguliers sur site.</p>
          </li>
          <li class="value reveal">
            {chip('i-users')}
            <h3 class="h3">Des équipes stables</h3>
            <p>Des agents formés à vos consignes, remplacés en cas d’absence.</p>
          </li>
          <li class="value reveal">
            {chip('i-leaf')}
            <h3 class="h3">Respect de l’environnement</h3>
            <p>Du matériel professionnel et des produits respectueux de l’environnement.</p>
          </li>
          <li class="value reveal">
            {chip('i-lock')}
            <h3 class="h3">Confidentialité</h3>
            <p>Vos accès, vos documents et vos données restent protégés.</p>
          </li>
        </ul>
        <div class="section-foot">
          <a class="link-more" href="engagements.html">Découvrir tous nos engagements {ico('i-arrow')}</a>
        </div>
      </div>
    </section>
{cta_band()}  </main>
'''
    html += footer()
    write('index.html', html)


# ---------------------------------------------------------------------------
# L'entreprise
# ---------------------------------------------------------------------------
def page_entreprise():
    steps = [
        ('01', 'Visite gratuite', 'Nous venons voir vos locaux et comprendre vos besoins : surfaces, fréquence, horaires, consignes d’accès.'),
        ('02', 'Devis détaillé', 'Tâches, fréquences, horaires et tarif, présentés clairement. Vous savez exactement ce qui est prévu.'),
        ('03', 'Équipe dédiée', 'Des agents formés à vos consignes, remplacés en cas d’absence pour que le service ne s’interrompe pas.'),
        ('04', 'Suivi qualité', 'Des contrôles réguliers et un interlocuteur toujours joignable pour toute remarque.'),
    ]
    steps_html = ''.join(f'''
          <li class="step reveal">
            <span class="step-num" aria-hidden="true">{n}</span>
            <h3 class="h3">{t}</h3>
            <p>{p}</p>
          </li>''' for n, t, p in steps)
    html = head('Notre entreprise | Alphanet Group',
                'Alphanet Group, entreprise de nettoyage professionnel créée en 2014 à Montpellier, active dans l’Hérault (34), en Occitanie et dans le Sud : histoire, valeurs, méthode.',
                'entreprise.html')
    html += header('entreprise.html')
    html += f'''
  <main id="contenu">
{page_hero('Notre entreprise', 'Alphanet Group est une entreprise de nettoyage professionnel installée à Montpellier, au service des entreprises, des hôtels, des copropriétés et des commerces depuis 2014. Elle intervient principalement dans l’Hérault (34), mais aussi partout en Occitanie et dans les autres régions du Sud.', 'Entreprise')}
    <!-- Histoire -->
    <section class="section" id="histoire" aria-labelledby="histoire-title">
      <div class="container split split--text-wide">
        <div class="prose reveal">
          <p class="eyebrow">Notre histoire</p>
          <h2 class="h2" id="histoire-title">Une entreprise montpelliéraine, depuis 2014</h2>
          <p>Alphanet Group a été créée en 2014 à Montpellier. Depuis, nous accompagnons les professionnels de l’Hérault (34), puis de toute l’Occitanie et du Sud, dans l’entretien de leurs locaux, avec une même exigence&nbsp;: un travail soigné, régulier et sans mauvaise surprise.</p>
          <p>Nous intervenons aujourd’hui dans six domaines&nbsp;: l’entretien de bureaux et de locaux professionnels, l’hôtellerie, les copropriétés, les commerces, la vitrerie et la remise en état de locaux, y compris après un sinistre.</p>
          <p>Notre force&nbsp;: une organisation simple, avec un interlocuteur unique qui connaît vos locaux et vos attentes.</p>
        </div>
        {STATS}
      </div>
    </section>

    <!-- Mission -->
    <section class="section section--soft" id="mission" aria-labelledby="mission-title">
      <div class="container">
        <div class="bulle promise reveal">
          <p class="eyebrow">Notre mission</p>
          <p id="mission-title">Offrir à chaque client des locaux propres et accueillants, avec un service simple&nbsp;: <span>un interlocuteur unique, des équipes stables et des engagements tenus.</span></p>
        </div>
      </div>
    </section>

    <!-- Valeurs -->
    <section class="section" id="valeurs" aria-labelledby="valeurs-title">
      <div class="container">
        <div class="section-head reveal">
          <p class="eyebrow">Nos valeurs</p>
          <h2 class="h2" id="valeurs-title">Quatre principes que nous appliquons chaque jour</h2>
          <p class="lead">Ils guident la façon dont nous recrutons, dont nous organisons les passages et dont nous vous répondons.</p>
        </div>
        <ul class="values">
          <li class="value reveal">
            {chip('i-pin')}
            <h3 class="h3">Proximité</h3>
            <p>Une entreprise locale, joignable et disponible. Nous nous déplaçons pour comprendre vos locaux avant de vous proposer un devis.</p>
          </li>
          <li class="value reveal">
            {chip('i-shield')}
            <h3 class="h3">Fiabilité</h3>
            <p>Des passages réguliers, aux horaires convenus, par des équipes stables. Si un agent est absent, il est remplacé.</p>
          </li>
          <li class="value reveal">
            {chip('i-lock')}
            <h3 class="h3">Discrétion</h3>
            <p>Nous respectons vos locaux, vos consignes d’accès et la confidentialité de ce que nous pouvons voir en intervenant chez vous.</p>
          </li>
          <li class="value reveal">
            {chip('i-eye')}
            <h3 class="h3">Transparence</h3>
            <p>Un devis détaillé, des tâches clairement listées et un interlocuteur qui répond à vos questions.</p>
          </li>
        </ul>
      </div>
    </section>

    <!-- Méthode -->
    <section class="section section--soft" id="methode" aria-labelledby="methode-title">
      <div class="container">
        <div class="section-head reveal">
          <p class="eyebrow">Notre méthode</p>
          <h2 class="h2" id="methode-title">Une méthode simple, un seul interlocuteur</h2>
          <p class="lead">Du premier rendez-vous au suivi au quotidien, vous savez toujours à qui parler. Matériel professionnel et produits respectueux de l’environnement.</p>
        </div>
        <ol class="steps">{steps_html}
        </ol>
      </div>
    </section>

    <!-- Zone -->
    <section class="section" id="zone" aria-labelledby="zone-title">
      <div class="container split">
        <div class="prose reveal">
          <p class="eyebrow">Où nous intervenons</p>
          <h2 class="h2" id="zone-title">L’Hérault d’abord, tout le Sud ensuite</h2>
          <p>Depuis Montpellier, nos équipes interviennent principalement dans l’Hérault (34), notre secteur historique. Nous intervenons aussi partout en Occitanie et dans les autres régions du Sud de la France, auprès des entreprises, des hôtels, des copropriétés et des commerces.</p>
          <a class="link-more" href="contact.html#formulaire">Demander un devis {ico('i-arrow')}</a>
        </div>
        <div class="bulle reveal zone-card">
          {chip('i-pin')}
          <h3 class="h3">Une question sur votre localisation&nbsp;?</h3>
          <p>Appelez-nous&nbsp;: nous étudions chaque demande.</p>
          <a class="link-more" href="{TEL}">{PHONE_HTML} {ico('i-arrow')}</a>
        </div>
      </div>
    </section>
{cta_band()}  </main>
'''
    html += footer()
    write('entreprise.html', html)


# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------
def page_services():
    quick = ''.join(f'<li><a href="#{sv["id"]}">{sv["name"].replace("Bureaux et locaux professionnels", "Bureaux")}</a></li>' for sv in SERVICES)
    blocks = ''
    for i, sv in enumerate(SERVICES):
        flip = ' svc--flip' if i % 2 else ''
        checks = ''.join(f'\n            <li>{ico("i-check")}<span>{c}</span></li>' for c in sv['checks'])
        blocks += f'''
        <article class="svc{flip}" id="{sv['id']}" aria-labelledby="{sv['id']}-title">
          <div class="svc-text reveal">
            {chip(sv['icon'])}
            <h2 class="h2" id="{sv['id']}-title">{sv['name']}</h2>
            <p>{sv['intro']}</p>
            <p>{sv['more']}</p>
            <a class="btn btn-primary" href="contact.html?prestation={sv['key']}#formulaire">Demander un devis {ico('i-arrow', 'ico ico-arrow')}</a>
          </div>
          <div class="bulle reveal">
            <p class="bulle-title">Ce que nous faisons</p>
            <ul class="checks">{checks}
            </ul>
          </div>
        </article>'''
    quicknav = '\n        <nav aria-label="Aller à un service"><ul class="quicknav">' + quick + '</ul></nav>'
    hero = page_hero('Nos services', 'Des prestations de nettoyage pour les professionnels, principalement dans l’Hérault (34), mais aussi partout en Occitanie et dans les autres régions du Sud, en interventions régulières ou ponctuelles, en journée ou en horaires décalés.', 'Services', extra=quicknav)
    html = head('Nettoyage bureaux, hôtellerie, copropriétés | Alphanet Group',
                'Nettoyage de bureaux, hôtellerie, copropriétés, commerces, vitrerie, remise en état et après sinistre, dans l’Hérault (34), en Occitanie et dans le Sud.',
                'services.html')
    html += header('services.html')
    html += f'''
  <main id="contenu">
{hero}
    <section class="section" aria-label="Détail des services">
      <div class="container">{blocks}
      </div>
    </section>
{cta_band('Un besoin particulier ?', 'Votre situation ne correspond à aucune de ces prestations&nbsp;? Appelez-nous&nbsp;: nous étudions toute demande.')}  </main>
'''
    html += footer()
    write('services.html', html)


# ---------------------------------------------------------------------------
# Engagements
# ---------------------------------------------------------------------------
def page_engagements():
    items = [
        ('i-check', 'Un service suivi',
         'Chaque prestation est cadrée par un cahier des charges écrit : tâches, fréquences et horaires. Des contrôles réguliers permettent de vérifier que le résultat est à la hauteur de vos attentes.',
         ['Un cahier des charges clair, validé avec vous', 'Des contrôles réguliers sur site', 'Un interlocuteur joignable pour toute remarque', 'Une correction rapide si quelque chose ne vous convient pas']),
        ('i-users', 'Des équipes stables et formées',
         'Nous privilégions des équipes stables, qui connaissent vos locaux et vos habitudes. Les agents sont formés à vos consignes et remplacés en cas d’absence, pour que le service ne s’interrompe pas.',
         ['Les mêmes agents autant que possible', 'Une formation à vos consignes et à vos locaux', 'Un remplacement en cas d’absence', 'Une tenue et un comportement professionnels']),
        ('i-leaf', 'Le respect de l’environnement',
         'Nous utilisons du matériel professionnel adapté à chaque surface et des produits respectueux de l’environnement, dosés avec soin pour limiter les consommations.',
         ['Des produits respectueux de l’environnement', 'Un dosage maîtrisé', 'Du matériel professionnel adapté aux surfaces', 'Des gestes économes en eau']),
        ('i-lock', 'La confidentialité et la sécurité',
         'Nous intervenons chez vous, parfois en dehors des heures de travail : la confiance est essentielle. Nous respectons vos consignes d’accès et la confidentialité de ce que nous pouvons voir dans vos locaux.',
         ['Un respect strict de vos consignes d’accès (clés, badges, alarmes)', 'Une discrétion totale sur les documents et les informations', 'Des interventions aux horaires convenus', 'Vos données de contact protégées, sans cookie ni service tiers']),
    ]
    cards = ''
    for icon, title, text, checks in items:
        lis = ''.join(f'\n              <li>{ico("i-check")}<span>{c}</span></li>' for c in checks)
        cards += f'''
          <article class="engage reveal">
            {chip(icon)}
            <h2 class="h3">{title}</h2>
            <p>{text}</p>
            <ul class="checks">{lis}
            </ul>
          </article>'''
    html = head('Nos engagements | Alphanet Group',
                'Service suivi, équipes stables et formées, respect de l’environnement, confidentialité : les engagements d’Alphanet Group, entreprise de nettoyage dans l’Hérault (34).',
                'engagements.html')
    html += header('engagements.html')
    html += f'''
  <main id="contenu">
{page_hero('Nos engagements', 'Ce que nous vous promettons, et la façon dont nous le tenons au quotidien.', 'Engagements')}
    <section class="section" aria-label="Nos quatre engagements">
      <div class="container">
        <div class="engage-grid">{cards}
        </div>
      </div>
    </section>

    <section class="section section--soft" aria-labelledby="promesse-title">
      <div class="container">
        <div class="bulle promise reveal">
          <p class="eyebrow" id="promesse-title">Notre promesse</p>
          <p>Des locaux propres, <span>un service simple</span> et des engagements tenus, du premier rendez-vous au suivi au quotidien.</p>
          <a class="link-more" href="contact.html#formulaire">Demander un devis gratuit {ico('i-arrow')}</a>
        </div>
      </div>
    </section>
{cta_band('Un doute, une question ?', 'Posez-nous vos questions sur notre façon de travailler&nbsp;: nous vous répondons avec plaisir.')}  </main>
'''
    html += footer()
    write('engagements.html', html)


# ---------------------------------------------------------------------------
# Contact
# ---------------------------------------------------------------------------
def page_contact():
    html = head('Contact et devis gratuit | Alphanet Group',
                'Devis gratuit pour le nettoyage de vos bureaux, hôtel, copropriété ou commerce, dans l’Hérault (34), en Occitanie et dans le Sud. Appelez le 07 58 34 04 07 ou écrivez-nous.',
                'contact.html')
    html += header('contact.html')
    html += f'''
  <main id="contenu">
{page_hero('Contact et devis gratuit', 'Décrivez votre besoin&nbsp;: nous organisons une visite et vous remettons un devis gratuit, sans engagement.', 'Contact', soft=True)}
    <section class="section section--form" id="formulaire" aria-label="Demande de devis">
      <div class="container contact-grid">
        <div class="contact-intro reveal">
          <a class="contact-phone" href="{TEL}">
            <span class="contact-phone-icon">{ico('i-phone')}</span>
            <span><span class="contact-label">Appelez-nous</span><strong>{PHONE_HTML}</strong></span>
          </a>

          <div class="contact-block">
            <p class="contact-block-title">Après votre demande</p>
            <ol class="mini-steps">
              <li>Nous vous rappelons pour préciser votre besoin.</li>
              <li>Nous visitons vos locaux, gratuitement.</li>
              <li>Vous recevez un devis détaillé, sans engagement.</li>
            </ol>
          </div>

          <div class="contact-block">
            {ZONE}
          </div>
        </div>

        <div class="form-card reveal">
          <h2 class="h3">Demande de devis</h2>
          <p class="form-intro">Les champs marqués d’un <span class="req">*</span> sont obligatoires.</p>
          <form class="form" data-quote-form novalidate>
            <div class="field">
              <label for="f-nom">Nom et prénom <span class="req" aria-hidden="true">*</span></label>
              <input id="f-nom" name="nom" type="text" autocomplete="name" maxlength="80" required aria-describedby="e-nom">
              <p class="field-error" id="e-nom"></p>
            </div>
            <div class="field">
              <label for="f-societe">Société / organisme</label>
              <input id="f-societe" name="societe" type="text" autocomplete="organization" maxlength="100">
            </div>
            <div class="field">
              <label for="f-telephone">Téléphone <span class="req" aria-hidden="true">*</span></label>
              <input id="f-telephone" name="telephone" type="tel" autocomplete="tel" inputmode="tel" maxlength="20" pattern="[0-9 +.\\-]{{10,20}}" required aria-describedby="e-telephone">
              <p class="field-error" id="e-telephone"></p>
            </div>
            <div class="field">
              <label for="f-email">E-mail <span class="req" aria-hidden="true">*</span></label>
              <input id="f-email" name="email" type="email" autocomplete="email" maxlength="120" required aria-describedby="e-email">
              <p class="field-error" id="e-email"></p>
            </div>
            <div class="field field--full">
              <label for="f-type">Prestation souhaitée <span class="req" aria-hidden="true">*</span></label>
              <div class="select">
                <select id="f-type" name="type" required aria-describedby="e-type">
                  <option value="">Choisir…</option>
                  <option value="Bureaux / locaux professionnels">Bureaux / locaux professionnels</option>
                  <option value="Hôtellerie">Hôtellerie</option>
                  <option value="Copropriété / parties communes">Copropriété / parties communes</option>
                  <option value="Commerce / lieu recevant du public">Commerce / lieu recevant du public</option>
                  <option value="Vitrerie">Vitrerie</option>
                  <option value="Remise en état / après sinistre">Remise en état / après sinistre</option>
                  <option value="Particulier (domicile)">Particulier (domicile)</option>
                  <option value="Autre demande">Autre demande</option>
                </select>
              </div>
              <p class="field-error" id="e-type"></p>
            </div>
            <div class="field field--full">
              <label for="f-message">Votre besoin</label>
              <textarea id="f-message" name="message" rows="4" maxlength="1500" placeholder="Type de locaux, surface, fréquence, commune, horaires… (pas de données sensibles)"></textarea>
            </div>
            <div class="form-hp" aria-hidden="true">
              <label for="f-site">Ne pas remplir ce champ</label>
              <input id="f-site" name="site_web" type="text" tabindex="-1" autocomplete="off">
            </div>
            <p class="form-privacy">{ico('i-lock')}<span>Vos informations servent uniquement à répondre à votre demande. Elles ne sont ni enregistrées sur ce site, ni transmises à des tiers. <a href="mentions-legales.html#donnees">Vos données et vos droits</a></span></p>
            <div class="form-submit">
              <button class="btn btn-primary btn-lg" type="submit">Envoyer ma demande {ico('i-arrow', 'ico ico-arrow')}</button>
            </div>
            <p class="form-status" role="status" data-form-status hidden></p>
          </form>
          <noscript><p class="form-noscript">Le formulaire a besoin de JavaScript. Appelez-nous au {PHONE_HTML}.</p></noscript>
        </div>
      </div>
    </section>
  </main>
'''
    html += footer(mobile_bar=False)
    write('contact.html', html)


# ---------------------------------------------------------------------------
# Mentions légales
# ---------------------------------------------------------------------------
def page_legal():
    main = LEGAL_MAIN
    # plus de partenaires cités sur le site
    main = main.replace(' Les noms et marques des partenaires appartiennent à leurs propriétaires respectifs.', '')
    # la vague sous le bandeau du haut
    marker = '      </div>\n    </section>\n'
    assert marker in main
    main = main.replace(marker, f'      </div>\n      {WAVE}\n    </section>\n', 1)
    html = head('Mentions légales et données personnelles | Alphanet Group',
                'Mentions légales, protection des données personnelles et cookies du site d’Alphanet Group, entreprise de nettoyage dans l’Hérault (34).',
                'mentions-legales.html', robots='noindex, follow')
    html += header('')
    html += f'''
  <main id="contenu">
{main}  </main>
'''
    html += footer(mobile_bar=False)
    write('mentions-legales.html', html)


if __name__ == '__main__':
    page_index()
    page_entreprise()
    page_services()
    page_engagements()
    page_contact()
    page_legal()
