# Master Metrics Docs

Documentación pública: https://docs.mastermetrics.com

Las páginas se generan con un script que lee el catálogo del API. No se editan a mano. Cada push a `main` publica solo.

## Regenerar

Requiere Python 3 y el `SERVER_AUTHORIZATION_SECRET_KEY` del API.

```sh
git pull
DOCS_API_URL=https://<host-del-api>/api/v2/docs DOCS_API_SECRET=<secret> python3 scripts/generate.py .
```

Correrlo siempre desde la raíz del repo. Sin `DOCS_API_URL` usa el API local (`http://localhost:3001/api/v2/docs`).

## Publicar

```sh
git diff --stat
git add -A
git commit -m "docs: regenerar catalogo"
git push
```

## Agregar descripciones

Para campos sin descripción en el API, crear `scripts/descriptions/<slug>.json` y regenerar:

```json
{ "<nombre_del_campo>": { "es": "...", "en": "...", "pt": "..." } }
```

## No editar a mano

Los `.mdx` y el bloque `navigation` de `docs.json`: el script los pisa.

## Errores

| Error | Causa |
|---|---|
| `DOCS_API_SECRET is required` | Falta la variable |
| `HTTP Error 400` | Secret incorrecto |
| `HTTP Error 404` | El API no tiene el endpoint de docs |
| `Connection refused` | No hay API en esa URL |

Más detalle en `apps/api/src/services/DocsService/README.md` del repo `smart-reporting-api`.
