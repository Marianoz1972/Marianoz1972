#!/usr/bin/env python3
"""CLI utility to run simple scene operations in Autodesk Maya from console.

Usage examples:
  python maya_console_app.py --op new_scene
  mayapy maya_console_app.py --op import_fbx --path /tmp/asset.fbx
  mayapy maya_console_app.py --op list_transforms --limit 20
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, asdict
from typing import Any, Optional


@dataclass
class Result:
    ok: bool
    operation: str
    message: str
    data: Optional[dict[str, Any]] = None


def _ensure_maya_modules():
    try:
        import maya.standalone as standalone  # type: ignore
        import maya.cmds as cmds  # type: ignore

        return standalone, cmds
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(
            "No se pudo importar maya.standalone/maya.cmds. "
            "Ejecuta este script con mayapy o dentro de Maya."
        ) from exc


def init_maya(standalone_module) -> None:
    standalone_module.initialize(name="python")


def op_new_scene(cmds_module) -> Result:
    cmds_module.file(new=True, force=True)
    return Result(True, "new_scene", "Escena nueva creada.")


def op_import_fbx(cmds_module, path: str) -> Result:
    if not os.path.exists(path):
        return Result(False, "import_fbx", f"Archivo no encontrado: {path}")

    cmds_module.file(path, i=True, type="FBX", ignoreVersion=True, ra=True)
    return Result(True, "import_fbx", "FBX importado correctamente.", {"path": path})


def op_list_transforms(cmds_module, limit: int) -> Result:
    nodes = cmds_module.ls(type="transform") or []
    return Result(
        True,
        "list_transforms",
        f"Se encontraron {len(nodes)} transforms.",
        {"total": len(nodes), "nodes": nodes[:limit]},
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aplicación de consola para Maya (Python).")
    parser.add_argument(
        "--op",
        required=True,
        choices=["new_scene", "import_fbx", "list_transforms"],
        help="Operación a ejecutar.",
    )
    parser.add_argument("--path", default="", help="Ruta para operaciones de importación.")
    parser.add_argument("--limit", type=int, default=25, help="Límite de elementos listados.")
    parser.add_argument("--json", action="store_true", help="Salida JSON (útil para pipelines).")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    try:
        standalone, cmds = _ensure_maya_modules()
        init_maya(standalone)

        if args.op == "new_scene":
            result = op_new_scene(cmds)
        elif args.op == "import_fbx":
            result = op_import_fbx(cmds, args.path)
        else:
            result = op_list_transforms(cmds, args.limit)

    except Exception as exc:
        result = Result(False, args.op, f"Error: {exc}")

    if args.json:
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    else:
        status = "OK" if result.ok else "ERROR"
        print(f"[{status}] {result.operation}: {result.message}")
        if result.data:
            print(result.data)

    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
