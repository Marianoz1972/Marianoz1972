# Maya Console App (Python)

Aplicación base para ejecutar operaciones en Autodesk Maya desde consola usando `mayapy`.

## Requisitos

- Autodesk Maya instalado.
- Usar `mayapy` (incluido con Maya) o ejecutar dentro de Maya Python.

## Uso rápido

```bash
mayapy maya_console_app.py --op new_scene
mayapy maya_console_app.py --op import_fbx --path /ruta/modelo.fbx
mayapy maya_console_app.py --op list_transforms --limit 20 --json
```

## Operaciones disponibles

- `new_scene`: crea una escena nueva.
- `import_fbx`: importa un archivo FBX (`--path` obligatorio).
- `list_transforms`: lista nodos transform de la escena.

## Nota

Si ejecutas con `python` normal (sin Maya), verás un error indicando que faltan `maya.standalone` y `maya.cmds`.
