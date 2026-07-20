"""Genera un inventario del proyecto y detecta archivos inadecuados para GitHub."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


EXCLUDED_PARTS = {
    ".git",
    ".venv",
    "__pycache__",
    ".ipynb_checkpoints",
}

LARGE_FILE_MB = 20.0


def classify(path: Path) -> str:
    suffixes = "".join(path.suffixes).lower()

    if suffixes in {".nii", ".nii.gz"}:
        return "neuroimage"
    if path.suffix.lower() == ".ipynb":
        return "notebook"
    if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".svg", ".pdf"}:
        return "figure_or_document"
    if path.suffix.lower() in {".csv", ".json", ".yaml", ".yml"}:
        return "data_or_config"
    if path.suffix.lower() in {".py", ".tex", ".bib", ".md"}:
        return "source_or_text"
    if path.suffix.lower() in {".pt", ".pth", ".ckpt", ".h5"}:
        return "model_binary"

    return "other"


def audit(project_root: Path) -> pd.DataFrame:
    rows = []

    for path in project_root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in EXCLUDED_PARTS for part in path.parts):
            continue

        size_mb = path.stat().st_size / (1024 ** 2)
        relative = path.relative_to(project_root)

        suggested_action = "include"

        if "data/raw" in relative.as_posix():
            suggested_action = "exclude_raw_data"
        elif classify(path) in {"neuroimage", "model_binary"}:
            suggested_action = "exclude_large_binary"
        elif size_mb > LARGE_FILE_MB:
            suggested_action = "review_large_file"

        rows.append(
            {
                "relative_path": relative.as_posix(),
                "size_mb": round(size_mb, 3),
                "extension": "".join(path.suffixes).lower(),
                "category": classify(path),
                "suggested_action": suggested_action,
            }
        )

    return pd.DataFrame(rows).sort_values(
        ["suggested_action", "size_mb"],
        ascending=[True, False],
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "project_root",
        type=Path,
        nargs="?",
        default=Path.cwd(),
    )
    args = parser.parse_args()

    root = args.project_root.resolve()
    output_dir = root / "repository_audit"
    output_dir.mkdir(exist_ok=True)

    inventory = audit(root)
    inventory.to_csv(
        output_dir / "repository_inventory.csv",
        index=False,
    )

    large = inventory.loc[
        inventory["size_mb"] > LARGE_FILE_MB
    ]
    large.to_csv(
        output_dir / "large_files.csv",
        index=False,
    )

    print(f"Proyecto: {root}")
    print(f"Archivos inventariados: {len(inventory)}")
    print(f"Archivos mayores a {LARGE_FILE_MB:.0f} MB: {len(large)}")
    print(f"Resultados: {output_dir}")


if __name__ == "__main__":
    main()
