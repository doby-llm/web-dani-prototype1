# Daniel Clemente — web final multipágina estática

Web estática multipágina para Daniel Clemente, nutricionista. Sustituye la landing de prototipo por una arquitectura navegable preparada para GitHub Pages bajo `https://doby-llm.github.io/web-dani-prototype1/`.

## Ejecutar localmente

```bash
python3 -m http.server 4173
```

Abrir `http://localhost:4173/`. No hay build, dependencias externas, CDN, backend, analytics ni envío de formularios.

## Páginas

- `index.html` — inicio orientado a conversión.
- `servicios.html` — índice de servicios.
- `perdida-de-peso.html` — captación principal.
- `perdida-de-peso-con-apoyo-medico.html` — tratamiento médico con farmacología sujeta a indicación y prescripción profesional, acompañado de seguimiento nutricional y de hábitos; alcance provisional.
- `nutricion-deportiva.html` — seguimiento nutricional para deportistas de fuerza, resistencia y otras modalidades; masa muscular, rendimiento y recuperación; contenido provisional.
- `nutricion-clinica.html` — tratamiento y seguimiento nutricional en patologías digestivas, alergias e intolerancias, dislipemias, hipertensión y otras situaciones metabólicas; contenido provisional.
- `como-funciona.html` — proceso online en cinco pasos.
- `programas.html` — inclusiones y tarifas provisionales.
- `sobre-mi.html` — biografía, formación, experiencia, docencia y enfoque.
- `preguntas-frecuentes.html` — FAQ prudente.
- `blog.html` — ideas editoriales educativas provisionales.
- `contacto.html` — canales pendientes y formulario demo.
- `aviso-legal.html`, `privacidad.html`, `cookies.html` — placeholders legales honestos.

## Estado y pendientes

Contenido comercial, precios, colaboración médica, formulación farmacológica, condiciones, denominaciones oficiales, canales de contacto y textos legales están marcados como orientativos/provisionales o pendientes de validación. El formulario de contacto usa `preventDefault`, no solicita datos sanitarios y no envía ni almacena información.

## Verificación

`tests/smoke_test.py` comprueba archivos, metadata, un único H1 por página, enlaces internos, rutas relativas, sitemap, ausencia de `wa.me`, CDN, secretos, formulario honesto y soporte de `prefers-reduced-motion`.
