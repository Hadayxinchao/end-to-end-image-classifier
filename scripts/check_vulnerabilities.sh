#!/bin/bash
# Dependency vulnerability check using multiple tools
# Checks both Python packages and Docker images

set -e

echo "🔍 Checking for dependency vulnerabilities..."

# Create reports directory if it doesn't exist
mkdir -p reports

# Check Python dependencies with Safety
echo ""
echo "1️⃣ Scanning Python dependencies with Safety..."
if command -v safety &> /dev/null; then
    safety check --file requirements.txt --json --output reports/safety-report.json || {
        echo "⚠️  Vulnerabilities found! Check reports/safety-report.json"
    }
    safety check --file requirements.txt || true
else
    echo "Safety not installed. Installing..."
    pip install safety
    safety check --file requirements.txt
fi

# Check with pip-audit (alternative vulnerability scanner)
echo ""
echo "2️⃣ Scanning with pip-audit..."
if command -v pip-audit &> /dev/null; then
    pip-audit --desc --format json --output reports/pip-audit-report.json || true
    pip-audit --desc || true
else
    echo "pip-audit not installed. Installing..."
    pip install pip-audit
    pip-audit --desc || true
fi

# Scan Dockerfile with Trivy if available
echo ""
echo "3️⃣ Scanning Dockerfile with Trivy (if available)..."
if command -v trivy &> /dev/null; then
    trivy config Dockerfile --format json --output reports/trivy-dockerfile.json || true
    trivy config Dockerfile || true
else
    echo "Trivy not installed. Skipping Docker scan."
    echo "Install with: curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin"
fi

# Check for known security issues in requirements
echo ""
echo "4️⃣ Checking for insecure package patterns..."
if grep -i -E "(pickle|yaml\.load[^_]|exec|eval)" requirements.txt 2>/dev/null; then
    echo "⚠️  Found potentially insecure packages"
else
    echo "✅ No obvious insecure patterns in requirements"
fi

echo ""
echo "✅ Vulnerability scan complete!"
echo "📊 Reports saved in reports/ directory"
