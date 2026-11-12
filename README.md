# Simulador Complexivo UTE · v3.7

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

## Seminario de Integración Curricular (v3.7)
`banco/pack-008.json` reúne 145 preguntas de las semanas 1 a 6 del seminario INTC-02004-J (identificadores `SIC<semana>-<n>`).
La app las muestra en «Seminario de Integración Curricular»: práctica por semana, con cronómetro o mini simulacro de 30 preguntas.
Para una semana nueva, agrega preguntas con identificador `SIC7-01`, `SIC8-01`, etc. en un paquete nuevo (`pack-009.json`) y súbelo al manifiesto: la app crea sola la tarjeta de esa semana.
