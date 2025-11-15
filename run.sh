#!/usr/bin/env bash
set -euo pipefail

# složka pro virtuální prostředí (lokálně v projektu)
VENV_DIR=".venv"

# vytvoření venv, pokud neexistuje
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    # aktualizace pip a instalace závislostí
    "$VENV_DIR/bin/pip" install --upgrade pip setuptools wheel
    "$VENV_DIR/bin/pip" install -r requirements.txt
fi

# aktivace venv
# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"

# spustit hlavní skript
python main.py
