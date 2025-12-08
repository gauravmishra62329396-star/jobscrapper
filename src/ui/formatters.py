#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: formatters.py
Descripción: Formateadores para presentar datos de trabajos y salarios en tablas
             y paneles Rich, proporcionando visualización clara y estructurada.

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
from typing import List
from rich.table import Table
from rich.panel import Panel
from src.models.job import Job
from src.models.salary import SalaryInfo


class JobFormatter:
    """Formateador para trabajos"""

    @staticmethod
    def format_job_table(jobs: List[Job]) -> Table:
        """
        Crea tabla Rich de trabajos

        Args:
            jobs: Lista de trabajos

        Returns:
            Tabla Rich formateada
        """
        table = Table(title=f"[bold]Trabajos Encontrados: {len(jobs)}[/bold]", show_lines=True)

        # Columnas
        table.add_column("ID", style="cyan", no_wrap=True, width=10)
        table.add_column("Título", style="magenta", width=30)
        table.add_column("Empresa", style="green", width=25)
        table.add_column("Ubicación", width=20)
        table.add_column("Salario", style="yellow", width=20)
        table.add_column("Tipo", style="blue", width=12)

        for job in jobs:
            # Truncar textos largos
            job_id_short = job.job_id[:8] + "..." if len(job.job_id) > 8 else job.job_id
            title_short = (job.title[:27] + "...") if job.title and len(job.title) > 30 else (job.title or "N/A")
            employer_short = (job.employer_name[:22] + "...") if job.employer_name and len(job.employer_name) > 25 else (job.employer_name or "N/A")

            table.add_row(
                job_id_short,
                title_short,
                employer_short,
                job.get_location(),
                job.get_salary_range() or "No especificado",
                job.employment_type or "N/A"
            )

        return table

    @staticmethod
    def format_job_details(job: Job) -> Panel:
        """
        Formatea detalles de un trabajo en panel Rich

        Args:
            job: Trabajo

        Returns:
            Panel Rich con detalles
        """
        content = f"""
[bold cyan]Título:[/bold cyan] {job.title or 'N/A'}
[bold green]Empresa:[/bold green] {job.employer_name or 'N/A'}
[bold]Ubicación:[/bold] {job.get_location()}
[bold yellow]Salario:[/bold yellow] {job.get_salary_range() or 'No especificado'}
[bold]Tipo de Empleo:[/bold] {job.employment_type or 'N/A'}
[bold]Remoto:[/bold] {'Sí' if job.is_remote else 'No'}
[bold]Publicado:[/bold] {job.posted_at_datetime or 'N/A'}

[bold]Descripción:[/bold]
{job.get_short_description(300)}

[bold]Requisitos:[/bold]
  • Experiencia: {job.required_experience or 'No especificado'}
  • Educación: {job.required_education or 'No especificado'}

[bold cyan]Link para aplicar:[/bold cyan] {job.apply_link or 'N/A'}
        """
        return Panel(
            content.strip(),
            title=f"[bold]Detalles del Trabajo: {job.job_id[:12]}[/bold]",
            border_style="blue"
        )

    @staticmethod
    def format_job_summary(jobs: List[Job]) -> str:
        """
        Formatea resumen de trabajos en texto simple

        Args:
            jobs: Lista de trabajos

        Returns:
            Resumen en texto
        """
        lines = ["\n" + "=" * 80]
        lines.append(f"RESUMEN DE BÚSQUEDA - {len(jobs)} trabajos encontrados")
        lines.append("=" * 80 + "\n")

        for i, job in enumerate(jobs, 1):
            lines.append(f"[{i}] {job.title or 'N/A'}")
            lines.append(f"    Empresa: {job.employer_name or 'N/A'}")
            lines.append(f"    Ubicación: {job.get_location()}")
            lines.append(f"    Salario: {job.get_salary_range() or 'No especificado'}")
            lines.append(f"    Link: {job.apply_link or 'N/A'}")
            lines.append("-" * 40)

        lines.append("=" * 80 + "\n")
        return "\n".join(lines)


class SalaryFormatter:
    """Formateador para información salarial"""

    @staticmethod
    def format_salary_table(salaries: List[SalaryInfo]) -> Table:
        """
        Crea tabla Rich de salarios

        Args:
            salaries: Lista de información salarial

        Returns:
            Tabla Rich formateada
        """
        table = Table(title="[bold]Información Salarial[/bold]", show_lines=True)

        # Columnas
        table.add_column("Puesto", style="magenta", width=25)
        table.add_column("Ubicación", style="cyan", width=20)
        table.add_column("Mediana", style="green", justify="right", width=15)
        table.add_column("Rango", style="yellow", justify="right", width=20)
        table.add_column("Fuente", style="dim", width=15)

        for salary in salaries:
            # Formatear valores
            title_short = (salary.job_title[:22] + "...") if salary.job_title and len(salary.job_title) > 25 else (salary.job_title or "N/A")
            location_short = (salary.location[:17] + "...") if salary.location and len(salary.location) > 20 else (salary.location or "N/A")

            median = salary.get_formatted_median() if salary.median_salary else "N/A"
            salary_range = salary.get_formatted_range()

            table.add_row(
                title_short,
                location_short,
                median,
                salary_range,
                salary.publisher_name or "N/A"
            )

        return table

    @staticmethod
    def format_salary_details(salaries: List[SalaryInfo]) -> str:
        """
        Formatea detalles de salarios en texto simple

        Args:
            salaries: Lista de información salarial

        Returns:
            Detalles en texto
        """
        lines = ["\n" + "=" * 80]
        lines.append(f"INFORMACIÓN DE SALARIOS - {len(salaries)} resultados")
        lines.append("=" * 80 + "\n")

        for i, salary in enumerate(salaries, 1):
            lines.append(f"[{i}] {salary.job_title or 'N/A'}")
            lines.append(f"    Ubicación: {salary.location or 'N/A'}")

            if salary.median_salary:
                lines.append(f"    Salario Mediano: {salary.get_formatted_median()}")
            if salary.min_salary and salary.max_salary:
                lines.append(f"    Rango: {salary.get_formatted_range()}")
            if salary.additional_pay:
                lines.append(f"    Pago Adicional: {salary.additional_pay}")

            lines.append(f"    Fuente: {salary.publisher_name or 'N/A'}")
            lines.append("-" * 40)

        lines.append("=" * 80 + "\n")
        return "\n".join(lines)
