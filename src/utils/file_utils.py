#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: file_utils.py
Descripción: Utilidades para manejo de archivos incluyendo limpieza de nombres,
             generación de nombres con timestamp y gestión de directorios.

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
import re
from pathlib import Path
from datetime import datetime
from typing import Union


def clean_filename(filename: str) -> str:
    """
    Limpia un nombre de archivo removiendo caracteres inválidos

    Args:
        filename: Nombre de archivo a limpiar

    Returns:
        Nombre de archivo limpio
    """
    # Remover caracteres no alfanuméricos excepto espacios y guiones
    cleaned = re.sub(r'[^\w\s-]', '', filename)
    # Reemplazar espacios y múltiples guiones por un solo guion bajo
    cleaned = re.sub(r'[-\s]+', '_', cleaned)
    # Remover guiones al inicio y final
    cleaned = cleaned.strip('_-')
    return cleaned


def generate_filename(
    base_name: str,
    extension: str,
    include_timestamp: bool = True
) -> str:
    """
    Genera un nombre de archivo con timestamp opcional

    Args:
        base_name: Nombre base del archivo
        extension: Extensión del archivo (sin punto)
        include_timestamp: Si incluir timestamp

    Returns:
        Nombre de archivo generado
    """
    clean_base = clean_filename(base_name)

    if include_timestamp:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{clean_base}_{timestamp}.{extension}"

    return f"{clean_base}.{extension}"


def ensure_dir_exists(directory: Union[str, Path]) -> Path:
    """
    Asegura que un directorio existe, creándolo si es necesario

    Args:
        directory: Ruta del directorio

    Returns:
        Path del directorio
    """
    dir_path = Path(directory)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def get_file_size(file_path: Union[str, Path]) -> int:
    """
    Obtiene el tamaño de un archivo en bytes

    Args:
        file_path: Ruta del archivo

    Returns:
        Tamaño en bytes
    """
    return Path(file_path).stat().st_size


def format_file_size(size_bytes: int) -> str:
    """
    Formatea tamaño de archivo en formato legible

    Args:
        size_bytes: Tamaño en bytes

    Returns:
        Tamaño formateado (ej: "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"
