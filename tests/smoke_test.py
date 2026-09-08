from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'index.html').read_text(encoding='utf-8')
CSS = (ROOT / 'styles.css').read_text(encoding='utf-8')
JS = (ROOT / 'script.js').read_text(encoding='utf-8')

required_files = [
    'index.html', 'styles.css', 'script.js', 'favicon.svg',
    'assets/hero-editorial.png', 'assets/daniel-about.png',
    'assets/Manrope-Variable.ttf', 'assets/og-image.svg',
    'robots.txt', 'sitemap.xml',
]
for relative in required_files:
    assert (ROOT / relative).exists(), f'missing {relative}'

required_ids = [
    'inicio', 'perdida-peso', 'nutricion-deportiva', 'nutricion-clinica',
    'seguimiento', 'tarifas', 'sobre-mi', 'blog', 'contacto', 'legal-notes',
]
for identifier in required_ids:
    assert f'id="{identifier}"' in HTML, f'missing section #{identifier}'

for token in ['og:title', 'og:description', 'og:image', 'twitter:card', 'twitter:image', 'theme-color']:
    assert token in HTML, f'missing metadata {token}'

for token in ['IntersectionObserver', 'prefers-reduced-motion', 'data-contact-form', 'menu-toggle']:
    assert token in JS or token in CSS, f'missing interaction {token}'

for color in ['#075C56', '#0B4745', '#DDEFE9', '#EEF7F4', '#FAFBFA', '#526260', '#DCE5E2']:
    assert color in CSS, f'missing design token {color}'

assert 'https://wa.me/' not in HTML
assert 'https://fonts.googleapis.com' not in HTML
assert 'cdn.tailwindcss.com' not in HTML
assert 'placeholder' in HTML.lower()
assert 'no se envía ni se almacena' in HTML.lower()

print(f'PASS: {len(required_files)} files, {len(required_ids)} section IDs, metadata, tokens and interaction guards verified')
