#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: menu.py
Descripción: Sistema de menús interactivos utilizando Rich para mostrar opciones
             de búsqueda predefinidas y funcionalidades del scraper de LinkedIn.

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
from rich.prompt import Prompt
from rich.panel import Panel
from src.ui.console import Console


class MenuSystem:
    """Sistema de menús interactivos"""

    def __init__(self, console: Console):
        """
        Args:
            console: Console de Rich
        """
        self.console = console

    def show_main_menu(self) -> str:
        """
        Muestra menú principal y retorna opción seleccionada

        Returns:
            Opción seleccionada como string
        """
        self.console.print_header("LINKEDIN JOB SCRAPER v3.0.0 - MENÚ PRINCIPAL")

        menu_text = """
[bold cyan]BÚSQUEDAS PREDEFINIDAS:[/bold cyan]
  [1]  Búsqueda personalizada
  [2]  Project Manager - España
  [3]  Software Engineer - España
  [4]  Data Scientist - España
  [5]  Frontend Developer - España
  [6]  Backend Developer - Estados Unidos
  [7]  Machine Learning Engineer - Estados Unidos
  [8]  Full Stack Developer - Estados Unidos
  [9]  DevOps Engineer - Reino Unido
  [10] Senior Software Engineer - Remoto Global

[bold magenta]FUNCIONES ADICIONALES:[/bold magenta]
  [11] Obtener detalles de un trabajo (por ID)
  [12] Consultar salarios estimados por puesto
  [13] Consultar salarios de empresa específica

[bold red][0] Salir[/bold red]
        """

        panel = Panel(menu_text.strip(), border_style="green", padding=(1, 2))
        self.console.console.print(panel)

        # Obtener opción del usuario
        choice = Prompt.ask(
            "\n[bold]Selecciona una opción[/bold]",
            choices=[str(i) for i in range(14)],
            default="0"
        )

        return choice

    def confirm_save(self, prompt_text: str = "¿Guardar resultados?") -> bool:
        """
        Pregunta al usuario si desea guardar

        Args:
            prompt_text: Texto del prompt

        Returns:
            True si el usuario confirma
        """
        from rich.prompt import Confirm
        return Confirm.ask(f"[yellow]{prompt_text}[/yellow]", default=True)

    def wait_for_enter(self):
        """Espera a que el usuario presione ENTER"""
        self.console.console.input("\n[dim]Presiona ENTER para continuar...[/dim]")
