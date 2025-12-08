#!/bin/bash
# Script para ejecutar tests y verificar cobertura

echo "=========================================="
echo "LinkedIn Job Scraper - Test Suite"
echo "=========================================="
echo ""

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "Ejecutando tests con pytest..."
echo ""

# Ejecutar pytest con cobertura
python -m pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html

echo ""
echo "=========================================="
echo "Tests completados!"
echo "Reporte HTML generado en: htmlcov/index.html"
echo "=========================================="
