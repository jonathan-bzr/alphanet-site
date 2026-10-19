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
      <symbol id="logo" viewBox="0 0 266.4 64">
        <path class="logo-ink" d="M26.20 4.00 32.40 4.00 32.40 20.45 26.39 36.30 12.69 38.07ZM37.09 34.92 31.60 20.45 31.60 4.00 37.80 4.00 49.43 33.33ZM21.47 49.28 17.40 60.00 4.00 60.00 7.54 51.08ZM60.00 60.00 46.60 60.00 41.55 46.69 54.08 45.07Z"/>
        <path class="logo-blue" d="M1.00 42.00 63.00 34.00 63.00 41.50 1.00 49.50Z"/>
        <path class="logo-ink" d="M80.0 34.0 88.61956030273437 16.467641845703128H94.39137573242188L103.01093603515625 34.0H97.3943369140625L96.0694326171875 31.19054248046875H86.66100341796876L85.34995727539062 34.0ZM88.39887573242187 27.38885107421875H94.33156030273437L92.73502124023437 23.825475097656252Q92.63523754882813 23.586549560546878 92.45534924316406 23.149164794921877Q92.2754609375 22.711780029296875 92.08171447753907 22.21424987792969Q91.88796801757813 21.716719726562502 91.72443432617189 21.289040649414062Q91.56090063476563 20.861361572265626 91.47996801757813 20.65570556640625H91.289826171875Q91.10190063476563 21.124131103515627 90.85715417480469 21.731698486328128Q90.61240771484376 22.339265869140625 90.38623217773437 22.90969140625Q90.160056640625 23.480116943359377 89.99541479492187 23.837116943359376Z M106.06599291992188 34.0V16.467641845703128H111.25851757812501V29.820801513671874H122.51509912109375V34.0Z M125.80299291992188 34.0V16.467641845703128H139.33404248046875Q141.05640063476562 16.467641845703128 142.3532960205078 17.22792907714844Q143.65019140625 17.988216308593753 144.37222863769532 19.33139892578125Q145.09426586914063 20.674581542968753 145.09426586914063 22.42649453667535Q145.09426586914063 24.195237548828125 144.3594786376953 25.556991088867186Q143.62469140625 26.91874462890625 142.3161541748047 27.672102783203123Q141.00761694335938 28.4254609375 139.28747509765626 28.4254609375H130.995517578125V34.0ZM130.995517578125 24.5772021484375H137.84230493164063Q138.9944326171875 24.5772021484375 139.58999291992188 24.02340813623716Q140.18555322265624 23.469614124036816 140.18555322265624 22.450451081576414Q140.18555322265624 21.75887939453125 139.9156863455636 21.28657901908256Q139.645819468471 20.81427864363387 139.126842351423 20.565089639199748Q138.607865234375 20.315900634765626 137.84230493164063 20.315900634765626H130.995517578125Z M148.26849291992187 34.0V16.467641845703128H153.461017578125V22.99232983398438H163.9837021484375V16.467641845703128H169.1762268066406V34.0H163.9837021484375V27.1715283203125H153.461017578125V34.0Z M172.2335 34.0 180.85306030273438 16.467641845703128H186.62487573242186L195.24443603515624 34.0H189.6278369140625L188.30293261718748 31.19054248046875H178.89450341796874L177.58345727539063 34.0ZM180.63237573242188 27.38885107421875H186.56506030273437L184.96852124023437 23.825475097656252Q184.8687375488281 23.586549560546878 184.68884924316404 23.149164794921877Q184.50896093749998 22.711780029296875 184.31521447753903 22.21424987792969Q184.1214680175781 21.716719726562502 183.95793432617188 21.289040649414062Q183.79440063476562 20.861361572265626 183.71346801757812 20.65570556640625H183.523326171875Q183.33540063476562 21.124131103515627 183.09065417480468 21.731698486328128Q182.84590771484375 22.339265869140625 182.61973217773436 22.90969140625Q182.39355664062498 23.480116943359377 182.22891479492188 23.837116943359376Z M198.29949291992187 34.0V16.467641845703128H202.94378002929687L212.03288647460937 24.647638427734375Q212.26737939453125 24.844989501953126 212.62937231445312 25.204766113281252Q212.991365234375 25.564542724609375 213.38467907714843 25.949819335937498Q213.77799291992187 26.335095947265625 214.07956030273436 26.6460888671875H214.3112766113281Q214.299634765625 26.1959541015625 214.2821719970703 25.5035693359375Q214.2647092285156 24.8111845703125 214.2647092285156 24.27346826171875V16.467641845703128H219.17951049804688V34.0H214.597865234375L205.73270556640625 25.99516650390625Q205.1273544921875 25.456889892578126 204.45825341796876 24.799150512695313Q203.78915234375 24.1414111328125 203.3855849609375 23.74006005859375H203.17936865234375Q203.19101049804686 24.085418212890623 203.20265234375 24.8171611328125Q203.2142941894531 25.548904052734375 203.2142941894531 26.398173583984374V34.0Z M224.00349291992188 34.0V16.467641845703128H242.28031909179688V20.315900634765626H229.2098757324219V23.260627685546876H240.65331201171875V26.9841630859375H229.2098757324219V30.1517412109375H242.4843190917969V34.0Z M252.58399999999997 34.0V20.646840332031253H244.98665600585937V16.467641845703128H265.37386865234373V20.646840332031253H257.77652465820313V34.0Z"/>
        <path class="logo-sub" d="M84.992 51.523999999999994Q82.496 51.523999999999994 81.24799999999999 50.46799999999999Q80.0 49.41199999999999 80.0 47.263999999999996Q80.0 45.85999999999999 80.636 44.90599999999999Q81.27199999999999 43.952 82.478 43.471999999999994Q83.684 42.992 85.364 42.992Q86.456 42.992 87.356 43.178Q88.256 43.364 88.91 43.742Q89.564 44.12 89.91799999999999 44.696Q90.27199999999999 45.27199999999999 90.27199999999999 46.05199999999999H88.496Q88.496 45.62 88.244 45.31999999999999Q87.99199999999999 45.019999999999996 87.56 44.846Q87.128 44.672 86.582 44.593999999999994Q86.036 44.516 85.43599999999999 44.516Q84.66799999999999 44.516 84.014 44.666Q83.36 44.815999999999995 82.88 45.134Q82.39999999999999 45.452 82.136 45.943999999999996Q81.872 46.43599999999999 81.872 47.108V47.395999999999994Q81.872 48.331999999999994 82.28 48.901999999999994Q82.688 49.471999999999994 83.438 49.73599999999999Q84.188 49.99999999999999 85.208 49.99999999999999Q86.336 49.99999999999999 87.062 49.79599999999999Q87.788 49.592 88.142 49.208Q88.496 48.824 88.496 48.30799999999999V48.211999999999996H85.16V46.77199999999999H90.28399999999999V51.379999999999995H89.156L88.964 50.3Q88.52 50.73199999999999 87.90199999999999 51.001999999999995Q87.28399999999999 51.272 86.54599999999999 51.397999999999996Q85.80799999999999 51.523999999999994 84.992 51.523999999999994Z M96.116 51.379999999999995V43.135999999999996H102.644Q103.52 43.135999999999996 104.078 43.489999999999995Q104.636 43.843999999999994 104.912 44.425999999999995Q105.188 45.007999999999996 105.188 45.715999999999994Q105.188 46.44799999999999 104.81 47.08999999999999Q104.432 47.73199999999999 103.64 48.092L105.392 51.379999999999995H103.34L101.828 48.44H97.94V51.379999999999995ZM97.94 46.928H102.14Q102.704 46.928 103.00999999999999 46.598Q103.316 46.267999999999994 103.316 45.751999999999995Q103.316 45.403999999999996 103.184 45.157999999999994Q103.05199999999999 44.91199999999999 102.788 44.785999999999994Q102.524 44.66 102.14 44.66H97.94Z M115.69518059299192 51.523999999999994Q114.06162803234501 51.523999999999994 112.8708140161725 51.025999999999996Q111.67999999999999 50.528 111.038 49.574Q110.396 48.62 110.396 47.25767634854771Q110.396 45.88399999999999 111.038 44.93599999999999Q111.67999999999999 43.98799999999999 112.8708140161725 43.489999999999995Q114.06162803234501 42.992 115.69518059299192 42.992Q117.344 42.992 118.532 43.489999999999995Q119.72 43.98799999999999 120.362 44.93599999999999Q121.004 45.88399999999999 121.004 47.25767634854771Q121.004 48.62 120.362 49.574Q119.72 50.528 118.532 51.025999999999996Q117.344 51.523999999999994 115.69518059299192 51.523999999999994ZM115.7 49.99999999999999Q116.444 49.99999999999999 117.068 49.831999999999994Q117.692 49.663999999999994 118.154 49.339999999999996Q118.616 49.016 118.874 48.522999999999996Q119.132 48.029999999999994 119.132 47.38399999999999V47.108Q119.132 46.46443835616438 118.874 45.97621917808219Q118.616 45.48799999999999 118.154 45.163999999999994Q117.692 44.839999999999996 117.068 44.678Q116.444 44.516 115.7 44.516Q114.956 44.516 114.332 44.678Q113.708 44.839999999999996 113.246 45.163999999999994Q112.78399999999999 45.48799999999999 112.532 45.97621917808219Q112.28 46.46443835616438 112.28 47.108V47.38399999999999Q112.28 48.029999999999994 112.532 48.522999999999996Q112.78399999999999 49.016 113.246 49.339999999999996Q113.708 49.663999999999994 114.332 49.831999999999994Q114.956 49.99999999999999 115.7 49.99999999999999Z M131.072 51.523999999999994Q129.524 51.523999999999994 128.51 51.044Q127.496 50.56399999999999 126.99799999999999 49.681999999999995Q126.5 48.8 126.5 47.599999999999994V43.135999999999996H128.324V47.516Q128.324 48.70399999999999 129.038 49.35199999999999Q129.752 49.99999999999999 131.072 49.99999999999999Q132.392 49.99999999999999 133.106 49.35199999999999Q133.82 48.70399999999999 133.82 47.516V43.135999999999996H135.644V47.599999999999994Q135.644 48.8 135.14600000000002 49.681999999999995Q134.648 50.56399999999999 133.64 51.044Q132.632 51.523999999999994 131.072 51.523999999999994Z M141.5 51.379999999999995V43.135999999999996H147.548Q148.352 43.135999999999996 148.94600000000003 43.483999999999995Q149.54000000000002 43.831999999999994 149.87 44.437999999999995Q150.20000000000002 45.044 150.20000000000002 45.83582222222222Q150.20000000000002 46.61599999999999 149.86400000000003 47.233999999999995Q149.52800000000002 47.852 148.92200000000003 48.199999999999996Q148.316 48.547999999999995 147.5 48.547999999999995H143.324V51.379999999999995ZM143.324 47.023999999999994H146.996Q147.63600000000002 47.023999999999994 147.988 46.71121917808219Q148.34 46.39843835616438 148.34 45.847095890410955Q148.34 45.476 148.18365714285716 45.21135135135135Q148.0273142857143 44.946702702702694 147.72765714285717 44.803351351351345Q147.42800000000003 44.66 146.996 44.66H143.324Z"/>
        <rect class="logo-sub" x="156.20" y="46.29" width="109.17" height="1.3"/>
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
