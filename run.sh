#!/bin/bash
# Script de ejecución rápida para LinkedIn Job Scraper v3.0

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Detectar OS para activación correcta de venv
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    VENV_ACTIVATE="venv/Scripts/activate"
else
    VENV_ACTIVATE="venv/bin/activate"
fi

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}[AVISO] Entorno virtual no encontrado${NC}"
    echo -e "${GREEN}[→] Creando entorno virtual...${NC}"
    python3 -m venv venv || python -m venv venv

    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR] No se pudo crear el entorno virtual${NC}"
        exit 1
    fi

    # Activar y instalar dependencias
    source $VENV_ACTIVATE
    echo -e "${GREEN}[→] Instalando dependencias...${NC}"
    pip install --upgrade pip -q
    pip install -r requirements.txt -q
    echo -e "${GREEN}[OK] Entorno configurado${NC}"
else
    # Activar entorno virtual existente
    source $VENV_ACTIVATE
fi

# Verificar .env
if [ ! -f ".env" ]; then
    echo -e "${RED}[ERROR] Archivo .env no encontrado${NC}"
    echo -e "${YELLOW}Copia .env.example a .env y configura tu API_KEY${NC}"
    exit 1
fi

# Ejecutar la aplicación
echo -e "${GREEN}[→] Iniciando LinkedIn Job Scraper v3.0...${NC}"
echo ""
python -m src.main

# Desactivar entorno virtual al salir
deactivate
