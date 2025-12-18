#!/bin/bash
# Clean build script for LaTeX papers
# Compiles PDF and automatically cleans up auxiliary files
# Usage: ./build_clean.sh [paper_name_without_extension]

set -euo pipefail

# Auto-detect paper name if not provided
if [ -z "${1:-}" ]; then
    PAPER="$(ls *.tex 2>/dev/null | head -1 | sed 's/\.tex$//')"
    if [ -z "${PAPER}" ]; then
        echo "ERROR: No .tex file found in current directory"
        exit 1
    fi
else
    PAPER="$1"
fi

echo "Building ${PAPER}.pdf..."

LOG="/tmp/${PAPER}_build.log"
rm -f "${LOG}"

# First pass
pdflatex -interaction=nonstopmode "${PAPER}.tex" > "${LOG}" 2>&1 || true

# BibTeX pass
bibtex "${PAPER}" >> "${LOG}" 2>&1 || true

# Second pass for references
pdflatex -interaction=nonstopmode "${PAPER}.tex" >> "${LOG}" 2>&1 || true

# Third pass for cross-references
pdflatex -interaction=nonstopmode "${PAPER}.tex" >> "${LOG}" 2>&1 || true

# Check PDF was created (primary indicator of success)
if [ ! -f "${PAPER}.pdf" ]; then
    echo "ERROR: PDF was not generated. See ${LOG}"
    tail -30 "${LOG}"
    exit 1
fi

# Check for fatal errors (excluding missing figure warnings)
if grep "^!" "${LOG}" | grep -v "File.*not found" | grep -q "^!"; then
    echo "WARNING: Non-fatal LaTeX errors detected:"
    grep "^!" "${LOG}" | grep -v "File.*not found" | head -5
    echo "See ${LOG} for details"
fi

# Get page count if pdfinfo is available
PAGES="$(pdfinfo "${PAPER}.pdf" 2>/dev/null | awk '/Pages:/ {print $2}' || true)"

# Clean up auxiliary files
echo "Cleaning up auxiliary files..."
rm -f "${PAPER}.aux" "${PAPER}.log" "${PAPER}.out" "${PAPER}.bbl" "${PAPER}.blg" "${PAPER}.toc" "${PAPER}.lof" "${PAPER}.lot"

echo "✓ Build complete: ${PAPER}.pdf ${PAGES:+(${PAGES} pages)}"
echo "  Build log: ${LOG}"

