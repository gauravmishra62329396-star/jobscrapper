#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: console.py
Description: Custom wrapper of Rich Console to provide colorful and formatted
             output in the terminal with themes and convenience methods.

Author: Hex686f6c61
Repository: https://github.com/Hex686f6c61/linkedIN-Scraper
Version: 3.0.0
Date: 2025-12-08
"""
from rich.console import Console as RichConsole
from rich.theme import Theme


# Custom theme
custom_theme = Theme({
    "success": "bold green",
    "error": "bold red",
    "warning": "bold yellow",
    "info": "bold cyan",
    "highlight": "bold magenta",
    "dim": "dim"
})


class Console:
    """Wrapper of Rich Console with convenience methods"""

    def __init__(self):
        self.console = RichConsole(theme=custom_theme)

    def print_success(self, message: str):
        """Print success message"""
        self.console.print(f"[success][✓][/success] {message}")

    def print_error(self, message: str):
        """Print error message"""
        self.console.print(f"[error][✗][/error] {message}")

    def print_warning(self, message: str):
        """Print warning message"""
        self.console.print(f"[warning][!][/warning] {message}")

    def print_info(self, message: str):
        """Print informational message"""
        self.console.print(f"[info][ℹ][/info] {message}")

    def print_header(self, title: str):
        """Print header with decorative line"""
        self.console.rule(f"[bold]{title}[/bold]")

    def print_separator(self):
        """Print separator line"""
        self.console.print("─" * 80, style="dim")

    def print(self, *args, **kwargs):
        """Wrapper for Rich Console print"""
        self.console.print(*args, **kwargs)

    def clear(self):
        """Clear console"""
        self.console.clear()
