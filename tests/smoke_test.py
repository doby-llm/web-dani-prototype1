from html.parser import HTMLParser
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = 'https://doby-llm.github.io/web-dani-prototype1/'

PAGES = [
    'index.html',
    'servicios.html',
    'perdida-de-peso.html',
    'perdida-de-peso-con-apoyo-medico.html',
    'nutricion-deportiva.html',
    'nutricion-clinica.html',
    'como-funciona.html',
    'programas.html',
    'sobre-mi.html',
    'preguntas-frecuentes.html',
    'blog.html',
    'contacto.html',
    'aviso-legal.html',
    'privacidad.html',
    'cookies.html',
]

REQUIRED_ASSETS = [
    'styles.css',
    'script.js',
    'favicon.svg',
    'assets/hero-editorial.png',
    'assets/daniel-about.png',
    'assets/Manrope-Variable.ttf',
    'assets/og-image.svg',
    'robots.txt',
    'sitemap.xml',
    'README.md',
]

NAV_TARGETS = {
    'index.html',
    'perdida-de-peso.html',
    'nutricion-deportiva.html',
    'nutricion-clinica.html',
    'sobre-mi.html',
    'programas.html',
    'contacto.html',
}


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.start_tags = []
        self.h1_count = 0
        self.links = []
        self.sources = []
        self.forms = []
        self.meta_names = set()
        self.meta_props = set()
        self.canonicals = []
        self.imgs = []
        self.body_page = None
        self.text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.start_tags.append((tag, attrs))
        if tag == 'h1':
            self.h1_count += 1
        if tag == 'a' and 'href' in attrs:
            self.links.append(attrs['href'])
        if tag in {'img', 'script'} and 'src' in attrs:
            self.sources.append(attrs['src'])
        if tag == 'form':
            self.forms.append(attrs)
        if tag == 'meta':
            if 'name' in attrs:
                self.meta_names.add(attrs['name'])
            if 'property' in attrs:
                self.meta_props.add(attrs['property'])
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonicals.append(attrs.get('href', ''))
        if tag == 'img':
            self.imgs.append(attrs)
        if tag == 'body':
            self.body_page = attrs.get('data-page')

    def handle_data(self, data):
        self.text.append(data)


def parse(page):
    parser = Parser()
    parser.feed((ROOT / page).read_text(encoding='utf-8'))
    return parser


def local_target(path):
    clean = path.split('#', 1)[0]
    if clean in {'', './'}:
        return None
    if clean.startswith('./'):
        clean = clean[2:]
    return clean


for relative in REQUIRED_ASSETS + PAGES:
    assert (ROOT / relative).exists(), f'missing {relative}'

for page in PAGES:
    html = (ROOT / page).read_text(encoding='utf-8')
    parser = parse(page)
    visible_text = ' '.join(parser.text)

    assert parser.h1_count == 1, f'{page}: expected one h1, found {parser.h1_count}'
    assert parser.body_page == page, f'{page}: missing body data-page'
    assert '#contenido' in parser.links, f'{page}: missing skip link'
    assert parser.canonicals == [BASE_URL if page == 'index.html' else BASE_URL + page], f'{page}: bad canonical'

    for token in ['description', 'twitter:card', 'twitter:title', 'twitter:description', 'twitter:image']:
        assert token in parser.meta_names, f'{page}: missing meta {token}'
    for token in ['og:title', 'og:description', 'og:image', 'og:url', 'og:type', 'og:locale']:
        assert token in parser.meta_props, f'{page}: missing {token}'

    assert 'Prototipo 01' not in visible_text, f'{page}: visible prototype wording'
    assert 'Web en preparación comercial' in visible_text, f'{page}: missing preparation notice'
    assert 'Contenido pendiente de validación' in visible_text, f'{page}: missing validation notice'

    for href in parser.links:
        assert not href.startswith('/'), f'{page}: absolute-root href {href}'
        assert not href.startswith('http://'), f'{page}: non-https external href {href}'
        assert not href.startswith('https://wa.me'), f'{page}: wa.me link found'
        assert not href.startswith('mailto:'), f'{page}: mailto link found'
        target = local_target(href)
        if target and not target.startswith('https://'):
            assert (ROOT / target).exists(), f'{page}: broken href {href}'

    for src in parser.sources:
        assert not src.startswith('/'), f'{page}: absolute-root src {src}'
        assert not src.startswith('http'), f'{page}: remote source {src}'
        assert (ROOT / local_target(src)).exists(), f'{page}: missing src {src}'

    for img in parser.imgs:
        assert img.get('alt', '').strip(), f'{page}: image without alt'

    nav_links = {local_target(href) for href in parser.links if local_target(href) in NAV_TARGETS}
    assert NAV_TARGETS.issubset(nav_links), f'{page}: incomplete main/footer navigation'

assert parse('contacto.html').forms, 'contact page must include a form'
for page in set(PAGES) - {'contacto.html'}:
    assert not parse(page).forms, f'{page}: form should only exist on contacto.html'

contact = (ROOT / 'contacto.html').read_text(encoding='utf-8').lower()
for token in ['preventdefault', 'no se envía ni se almacena', 'no introduzcas', 'datos sanitarios']:
    assert token in contact or token in (ROOT / 'script.js').read_text(encoding='utf-8').lower(), f'missing honest form marker {token}'
for forbidden in ['name="patologia"', 'name="medicacion"', 'name="diagnostico"', 'name="analitica"', 'medicación actual']:
    assert forbidden not in contact, f'contact form asks sensitive health data: {forbidden}'

all_text = '\n'.join(path.read_text(encoding='utf-8', errors='ignore') for path in [*(ROOT / p for p in PAGES), ROOT / 'styles.css', ROOT / 'script.js'])
for forbidden in ['https://fonts.googleapis.com', 'cdn.tailwindcss.com', 'kit.fontawesome.com', 'mailto:', 'https://wa.me/', 'info@danielclemente.com']:
    assert forbidden not in all_text, f'forbidden external/placeholder token: {forbidden}'
for secret_pattern in [r'sk-[A-Za-z0-9]{20,}', r'ghp_[A-Za-z0-9]{20,}', r'AKIA[0-9A-Z]{16}']:
    assert not re.search(secret_pattern, all_text), f'possible secret matched {secret_pattern}'

css = (ROOT / 'styles.css').read_text(encoding='utf-8')
js = (ROOT / 'script.js').read_text(encoding='utf-8')
for token in ['@font-face', 'assets/Manrope-Variable.ttf', 'prefers-reduced-motion', ':focus-visible']:
    assert token in css, f'missing CSS requirement {token}'
for token in ['menu-toggle', 'Escape', 'resize', 'aria-current', 'preventDefault', 'IntersectionObserver', 'mobile-contact-bar', 'scroll', 'is-visible']:
    assert token in js, f'missing JS behavior {token}'

sitemap = ET.parse(ROOT / 'sitemap.xml')
ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
locs = [node.text for node in sitemap.findall('.//sm:loc', ns)]
expected_locs = [BASE_URL] + [BASE_URL + page for page in PAGES if page != 'index.html']
assert locs == expected_locs, f'sitemap mismatch: {locs}'

medical_page = (ROOT / 'perdida-de-peso-con-apoyo-medico.html').read_text(encoding='utf-8')
for token in ['Pérdida de peso con tratamiento médico', 'tratamiento farmacológico', 'GLP-1', 'seguimiento nutricional y de hábitos', 'no vende ni dispensa medicamentos', 'solución aislada', 'no se recomienda un medicamento concreto', 'no sustituye una consulta médica']:
    assert token.lower() in medical_page.lower(), f'medical page missing required wording: {token}'
for page in ['index.html', 'programas.html']:
    page_text = (ROOT / page).read_text(encoding='utf-8').lower()
    assert 'pérdida de peso con tratamiento médico' in page_text or 'nutrición + tratamiento médico' in page_text, f'{page}: missing treatment medical wording'
assert 'no es una solución aislada' in (ROOT / 'index.html').read_text(encoding='utf-8').lower(), 'home missing integrated-treatment safeguard'
assert 'casos seleccionados' in (ROOT / 'programas.html').read_text(encoding='utf-8').lower(), 'programs missing individual-selection safeguard'
assert 'cóctel' not in all_text.lower(), 'informal/undefined cocktail wording found'
clinical_page = (ROOT / 'nutricion-clinica.html').read_text(encoding='utf-8').lower()
for token in ['tratamiento y seguimiento nutricional', 'patologías digestivas', 'alergias e intolerancias', 'dislipemias', 'hipertensión arterial', 'seguimiento práctico', 'seguimiento de hábitos']:
    assert token in clinical_page, f'clinical page missing required wording: {token}'
assert 'diabetes' in clinical_page and 'hígado graso' in clinical_page, 'clinical page missing additional metabolic areas'

for forbidden_clinical in ['profesional médica', 'seguimiento médico', 'coordinación necesaria', 'no se modifican medicamentos', 'no constituye un diagnóstico']:
    assert forbidden_clinical not in clinical_page, f'clinical page contains medical-coordination wording: {forbidden_clinical}'

sports_page = (ROOT / 'nutricion-deportiva.html').read_text(encoding='utf-8').lower()
for token in ['seguimiento nutricional', 'deportistas de fuerza', 'deportes de resistencia', 'otras modalidades deportivas', 'ganancia de masa muscular', 'rendimiento', 'recuperación', 'excel 365', 'seguimiento semanal']:
    assert token in sports_page, f'sports page missing required wording: {token}'
for forbidden_sports in ['profesional médica', 'seguimiento médico', 'farmacología', 'prescripción', 'coordinación necesaria']:
    assert forbidden_sports not in sports_page, f'sports page contains medical-coordination wording: {forbidden_sports}'

print(f'PASS: {len(PAGES)} pages, metadata, links, form safeguards, assets and sitemap verified')
