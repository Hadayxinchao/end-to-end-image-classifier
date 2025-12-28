#!/bin/bash
# Security scanning script using Bandit and Safety
# This script checks for security vulnerabilities in code and dependencies

set -e

echo "🔒 Running security scans..."

# Check if bandit is installed
if ! command -v bandit &> /dev/null; then
    echo "Installing bandit..."
    pip install bandit[toml]
fi

# Check if safety is installed
if ! command -v safety &> /dev/null; then
    echo "Installing safety..."
    pip install safety
fi

# Run Bandit for code security
echo ""
echo "📊 Scanning Python code with Bandit..."
bandit -r src/ -c pyproject.toml -f json -o reports/bandit-report.json || true
bandit -r src/ -c pyproject.toml

# Run Safety for dependency vulnerabilities
echo ""
echo "🔍 Checking dependencies for known vulnerabilities..."
safety check --json --output reports/safety-report.json || true
safety check

# Check for outdated packages
echo ""
echo "📦 Checking for outdated packages..."
pip list --outdated

echo ""
echo "✅ Security scans complete!"
echo "Reports saved in reports/ directory"
