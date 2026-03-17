#!/bin/bash
#
# Build the Baptist Shorter Catechism (Greek) PDF using Pandoc.
#
# Usage: ./build.sh
#
# Requires: Python 3.11+, Pandoc, XeLaTeX
#

set -euo pipefail
cd "$(dirname "$0")"

mkdir -p dist

echo "Converting TOML to Markdown..."
python3 toml_to_markdown.py -s src -o dist/baptist-shorter-catechism-greek.md

echo "Running Pandoc (Markdown -> PDF via XeLaTeX)..."
pandoc dist/baptist-shorter-catechism-greek.md \
    --template=templates/catechism.latex \
    --pdf-engine=xelatex \
    -o dist/baptist-shorter-catechism-greek.pdf

echo "Done: dist/baptist-shorter-catechism-greek.pdf"
