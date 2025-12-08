#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: console.py
Descripción: Wrapper personalizado de Rich Console para proporcionar salida
             coloreada y formateada en la terminal con temas y métodos de conveniencia.

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
from rich.console import Console as RichConsole
from rich.theme import Theme


# Tema personalizado
custom_theme = Theme({
    "success": "bold green",
    "error": "bold red",
    "warning": "bold yellow",
    "info": "bold cyan",
    "highlight": "bold magenta",
    "dim": "dim"
})


class Console:
    """Wrapper de Rich Console con métodos de conveniencia"""

    def __init__(self):
        self.console = RichConsole(theme=custom_theme)

    def print_success(self, message: str):
        """Imprime mensaje de éxito"""
        self.console.print(f"[success][OK][/success] {message}")

    def print_error(self, message: str):
        """Imprime mensaje de error"""
        self.console.print(f"[error][ERROR][/error] {message}")

    def print_warning(self, message: str):
        """Imprime mensaje de advertencia"""
        self.console.print(f"[warning][AVISO][/warning] {message}")

    def print_info(self, message: str):
        """Imprime mensaje informativo"""
        self.console.print(f"[info][INFO][/info] {message}")

    def print_header(self, title: str):
        """Imprime encabezado con línea decorativa"""
        self.console.rule(f"[bold]{title}[/bold]")

    def print_separator(self):
        """Imprime línea separadora"""
        self.console.print("─" * 80, style="dim")

    def print(self, *args, **kwargs):
        """Wrapper para print de Rich Console"""
        self.console.print(*args, **kwargs)

    def clear(self):
        """Limpia la consola"""
        self.console.clear()
