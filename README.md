# Daniel Clemente — Prototipo 01

Landing estática para explorar la primera dirección visual de la web de Daniel Clemente.

## Estado

Este repositorio contiene un prototipo público. Los precios, datos de contacto, titulaciones y formulaciones médicas son provisionales hasta su validación.

## Ejecutar localmente

Desde la raíz del repositorio:

```bash
python3 -m http.server 4173
```

Abrir `http://localhost:4173/`.

## Estructura

- `index.html` — estructura y contenido.
- `styles.css` — tokens visuales, responsive y animaciones.
- `script.js` — menú móvil, reveal on scroll, navegación activa y formulario de demo.
- `assets/` — tipografía, imágenes y previsualización social locales.
- `tests/smoke_test.py` — comprobaciones estáticas básicas.

## GitHub Pages

El repositorio está preparado para GitHub Pages publicando la rama `main` desde la raíz. La página usa rutas relativas para funcionar bajo el subpath del repositorio.

El formulario muestra estados de demo y no envía datos. Antes de publicar como web comercial hay que conectar un proveedor y revisar privacidad, consentimiento y tratamiento de datos.
