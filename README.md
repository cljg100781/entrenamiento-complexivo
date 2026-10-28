# Simulador Complexivo UTE

App web instalable (PWA) que funciona sin internet y descarga paquetes de preguntas nuevos cada vez que hay conexión.

## Añadir más preguntas
1. Crea `banco/pack-002.json` con el mismo formato de `pack-001.json` (ids únicos, p. ej. `P2-...`).
2. Agrega el paquete a `banco/manifest.json` en la lista `paquetes`.
3. Sube los cambios. Los teléfonos lo descargarán automáticamente la próxima vez que tengan internet.

Para corregir un paquete ya publicado, edítalo y sube su `version` en el manifiesto (1 → 2): la app lo reemplaza.
