#!/usr/bin/env sh

PROGRAM_DIR="$HOME/.local/share/blasmodcli"

echo "=> Removing the virtual environment..."
rm -r "$PROGRAM_DIR/venv"

echo "=> Removing installed mods..."
rm -r "$PROGRAM_DIR/mods"

echo "=> Removing scripts directory..."
rm -r "$PROGRAM_DIR/scripts"

echo "=> Uninstallation complete!"
