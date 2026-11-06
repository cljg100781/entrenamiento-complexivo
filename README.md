# Simulador Complexivo UTE · v3.0

App web instalable (PWA) que funciona sin internet y descarga paquetes de preguntas nuevos cada vez que hay conexión.

## Publicar (GitHub Pages)
1. Crea un repositorio público `complexivo` y sube todo el contenido de esta carpeta.
2. Settings › Pages › Branch: `main` / root.
3. Abre `https://TU_USUARIO.github.io/complexivo/` en Chrome del teléfono › menú › «Instalar app».

## Añadir preguntas
1. Crea `banco/pack-003.json` con el formato de `pack-002.json` (ids únicos; `dificultad` 1–5 opcional).
2. Agrégalo a `banco/manifest.json` en `paquetes`.
3. Sube los cambios: los teléfonos lo descargan solos al tener internet.
Para corregir un paquete publicado, edítalo y sube su `version` en el manifiesto.

Un paquete puede incluir `articulos` (síntesis de artículos clave, clave `"COIP 454"`, `"CC 1461"`, etc.).

## Aportes de compañeros
Desde la app (Proponer pregunta › Compartir) llega una pregunta en JSON. Revísala, verifica la vigencia de la norma y agrégala al siguiente paquete.
