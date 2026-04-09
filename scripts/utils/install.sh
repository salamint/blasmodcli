#!/usr/bin/env sh

GIT_URL="https://github.com/salamint/blasmodcli.git"
PROGRAM_DIR="$HOME/.local/share/blasmodcli"
VENV_DIR="$PROGRAM_DIR/venv"
SCRIPTS_DIR="$PROGRAM_DIR/scripts"
TEMP_LOCATION="/tmp/blasmodcli"

echo "=> Cloning repository..."
git clone "$GIT_URL" "$TEMP_LOCATION"

echo "=> Creating the virtual environment..."
mkdir -p "$PROGRAM_DIR"
python -m venv "$VENV_DIR"

echo "=> Installing the python package locally..."
. "$VENV_DIR/bin/activate"
pip install "$TEMP_LOCATION"

CONFIG_DIR="$HOME/.config/blasmodcli"
echo "=> Copying the default configuration..."
mkdir -p "$CONFIG_DIR"
cp "$TEMP_LOCATION/docs/config/general.toml" "$CONFIG_DIR"
cp -r "$TEMP_LOCATION/docs/config/games" "$CONFIG_DIR"
cp -r "$TEMP_LOCATION/docs/config/sources" "$CONFIG_DIR"

echo "=> Cleaning up installation..."
mv "$TEMP_LOCATION/scripts" "$PROGRAM_DIR"
rm -rf "$TEMP_LOCATION"

echo "=> blasmodcli interface successfully installed!"
echo "TIP: The scripts can be found in the $SCRIPTS_DIR directory."
echo "TIP: Consider creating a shortcut in your /usr/bin directory or any directory in your \$PATH variable, or add the scripts directory to the \$PATH."
