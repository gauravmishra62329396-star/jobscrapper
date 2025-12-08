#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: prompts.py
Descripción: Prompts interactivos para capturar entrada del usuario mediante Rich,
             incluyendo parámetros de búsqueda, consultas salariales y confirmaciones.

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
from typing import Tuple, Dict
from rich.prompt import Prompt, Confirm, IntPrompt
from src.ui.console import Console
from src.models.search_params import SearchParameters


class Prompts:
    """Manejadores de input interactivos"""

    def __init__(self, console: Console):
        """
        Args:
            console: Console de Rich
        """
        self.console = console

    def get_custom_search_params(self) -> SearchParameters:
        """
        Obtiene parámetros de búsqueda personalizados del usuario

        Returns:
            SearchParameters validado
        """
        self.console.print_header("CONFIGURACIÓN DE BÚSQUEDA PERSONALIZADA")

        # Query de búsqueda
        query = Prompt.ask("\n[cyan]Búsqueda[/cyan] (ej: 'python developer madrid')")

        # País
        country = Prompt.ask(
            "[cyan]Código de país[/cyan] (ej: es, us, mx)",
            default="us",
            show_default=True
        )

        # Período de publicación
        self.console.console.print("\n[bold]Período de publicación:[/bold]")
        self.console.console.print("  1. Todos")
        self.console.console.print("  2. Hoy")
        self.console.console.print("  3. Últimos 3 días")
        self.console.console.print("  4. Última semana")
        self.console.console.print("  5. Último mes")

        periodo_choice = Prompt.ask(
            "[cyan]Selecciona período[/cyan]",
            choices=["1", "2", "3", "4", "5"],
            default="1"
        )

        periodos = {
            "1": "all", "2": "today", "3": "3days",
            "4": "week", "5": "month"
        }
        date_posted = periodos[periodo_choice]

        # Trabajo remoto
        work_from_home = Confirm.ask("\n[cyan]¿Solo trabajos remotos?[/cyan]", default=False)

        # Tipo de empleo
        self.console.console.print("\n[dim]Tipos de empleo (opcional): FULLTIME, PARTTIME, CONTRACTOR, INTERN[/dim]")
        employment_types = Prompt.ask(
            "[cyan]Tipo de empleo[/cyan] (deja vacío para todos)",
            default="",
            show_default=False
        )
        employment_types = employment_types.strip() if employment_types else None

        # Número de páginas
        num_pages = IntPrompt.ask(
            "\n[cyan]Número de páginas[/cyan] (1-10)",
            default=1,
            show_default=True
        )
        num_pages = max(1, min(10, num_pages))  # Limitar entre 1 y 10

        # Crear y validar parámetros
        try:
            params = SearchParameters(
                query=query,
                country=country,
                date_posted=date_posted,
                work_from_home=work_from_home,
                employment_types=employment_types,
                num_pages=num_pages
            )
            return params
        except Exception as e:
            self.console.print_error(f"Error en parámetros: {e}")
            raise

    def get_job_id_input(self) -> Tuple[str, str]:
        """
        Solicita Job ID y país al usuario

        Returns:
            Tupla (job_id, country)
        """
        self.console.print_header("OBTENER DETALLES DE TRABAJO")

        job_id = Prompt.ask("\n[cyan]Job ID[/cyan]")
        country = Prompt.ask(
            "[cyan]Código de país[/cyan]",
            default="us",
            show_default=True
        )

        return job_id, country

    def get_salary_estimate_params(self) -> Dict[str, str]:
        """
        Obtiene parámetros para estimación salarial

        Returns:
            Diccionario con parámetros
        """
        self.console.print_header("CONSULTAR SALARIOS ESTIMADOS")

        job_title = Prompt.ask("\n[cyan]Título del puesto[/cyan] (ej: 'Software Engineer')")
        location = Prompt.ask("[cyan]Ubicación[/cyan] (ej: 'Madrid, Spain' o 'New York, NY')")

        # Menú de experiencia
        years_of_experience = self._get_experience_level()

        return {
            "job_title": job_title,
            "location": location,
            "years_of_experience": years_of_experience
        }

    def get_company_salary_params(self) -> Dict[str, str]:
        """
        Obtiene parámetros para salarios de empresa

        Returns:
            Diccionario con parámetros
        """
        self.console.print_header("CONSULTAR SALARIOS DE EMPRESA")

        company = Prompt.ask("\n[cyan]Empresa[/cyan] (ej: 'Google', 'Amazon')")
        job_title = Prompt.ask("[cyan]Título del puesto[/cyan] (ej: 'Software Engineer')")

        location = Prompt.ask(
            "[cyan]Ubicación[/cyan] (opcional, presiona ENTER para omitir)",
            default="",
            show_default=False
        )
        location = location.strip() if location else None

        # Menú de experiencia
        years_of_experience = self._get_experience_level()

        return {
            "company": company,
            "job_title": job_title,
            "location": location,
            "years_of_experience": years_of_experience
        }

    def _get_experience_level(self) -> str:
        """
        Muestra menú de nivel de experiencia

        Returns:
            Código de experiencia
        """
        self.console.console.print("\n[bold]Años de experiencia:[/bold]")
        self.console.console.print("  1. Todos (ALL)")
        self.console.console.print("  2. Menos de 1 año")
        self.console.console.print("  3. 1-3 años")
        self.console.console.print("  4. 4-6 años")
        self.console.console.print("  5. 7-9 años")
        self.console.console.print("  6. 10+ años")

        exp_choice = Prompt.ask(
            "[cyan]Selecciona nivel[/cyan]",
            choices=["1", "2", "3", "4", "5", "6"],
            default="1"
        )

        experience_map = {
            "1": "ALL",
            "2": "LESS_THAN_ONE",
            "3": "ONE_TO_THREE",
            "4": "FOUR_TO_SIX",
            "5": "SEVEN_TO_NINE",
            "6": "TEN_AND_ABOVE"
        }

        return experience_map[exp_choice]

    def confirm_save(self, prompt_text: str = "¿Guardar resultados?") -> bool:
        """
        Pregunta al usuario si desea guardar

        Args:
            prompt_text: Texto del prompt

        Returns:
            True si el usuario confirma
        """
        return Confirm.ask(f"[yellow]{prompt_text}[/yellow]", default=True)
