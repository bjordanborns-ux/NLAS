#!/usr/bin/env bash

set -e

echo "🚀 Initializing NorthLight development environment..."

# Update Ubuntu package information.
sudo apt-get update

# Install useful Linux development tools.
sudo apt-get install -y \
    curl \
    git \
    htop \
    ripgrep \
    tree \
    python3-pip \
    unzip \
    nano

# Install Starship if it is not already installed.
if ! command -v starship >/dev/null 2>&1; then
    echo "⭐ Installing Starship..."
    curl -sS https://starship.rs/install.sh | sh -s -- --yes
else
    echo "⭐ Starship is already installed."
fi

# Create Starship configuration directory.
mkdir -p "${HOME}/.config"

# Copy the repository's Starship configuration.
cp .devcontainer/starship.toml "${HOME}/.config/starship.toml"

# Enable Starship in Bash without adding duplicate lines.
STARSHIP_INIT='eval "$(starship init bash)"'

if ! grep -Fxq "${STARSHIP_INIT}" "${HOME}/.bashrc"; then
    echo "" >> "${HOME}/.bashrc"
    echo "# NorthLight Starship prompt" >> "${HOME}/.bashrc"
    echo "${STARSHIP_INIT}" >> "${HOME}/.bashrc"
fi

# Give Python packaging tools a clean baseline.
python -m pip install --upgrade pip

echo ""
echo "✅ NorthLight development environment initialized."
echo "🛰️ Restart the terminal to activate Starship."