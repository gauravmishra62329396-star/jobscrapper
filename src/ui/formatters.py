#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: formatters.py
Description: Formatters to present job and salary data in tables
             and Rich panels, providing clear and structured visualization.

Author: Hex686f6c61
Repository: https://github.com/Hex686f6c61/linkedIN-Scraper
Version: 3.0.0
Date: 2025-12-08
"""
from typing import List
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from src.models.job import Job
from src.models.salary import SalaryInfo


class JobFormatter:
    """Formatter for jobs"""

    @staticmethod
    def format_job_table(jobs: List[Job]) -> Table:
        """
        Create Rich table of jobs with all details

        Args:
            jobs: List of jobs

        Returns:
            Formatted Rich table
        """
        table = Table(
            title=f"[bold green]📋 JOBS FOUND: {len(jobs)}[/bold green]",
            show_lines=True,
            expand=True
        )

        # Columns
        table.add_column("ID", style="bright_cyan", no_wrap=True, width=10)
        table.add_column("Job Title", style="bright_magenta", width=35)
        table.add_column("Company", style="bright_green", width=28)
        table.add_column("Location", style="bright_yellow", width=22)
        table.add_column("Salary Range", style="bright_white", width=18)
        table.add_column("Employment Type", style="bright_blue", width=15)
        table.add_column("Remote", style="bright_cyan", width=8)
        table.add_column("Posted", style="dim", width=12)

        for job in jobs:
            # Truncate long texts
            job_id_short = job.job_id[:8] + "..." if len(job.job_id) > 8 else job.job_id
            title_short = (job.title[:32] + "...") if job.title and len(job.title) > 35 else (job.title or "N/A")
            employer_short = (job.employer_name[:25] + "...") if job.employer_name and len(job.employer_name) > 28 else (job.employer_name or "N/A")
            location_short = (job.get_location()[:19] + "...") if job.get_location() and len(job.get_location()) > 22 else job.get_location()
            salary_display = job.get_salary_range() or "Not specified"
            remote_display = "🌍 Yes" if job.is_remote else "📍 No"
            posted_display = (job.posted_at_datetime[:10]) if job.posted_at_datetime else "N/A"

            table.add_row(
                job_id_short,
                title_short,
                employer_short,
                location_short,
                salary_display,
                job.employment_type or "N/A",
                remote_display,
                posted_display
            )

        return table

    @staticmethod
    def format_job_details(job: Job) -> Panel:
        """
        Format job details in Rich panel

        Args:
            job: Job object

        Returns:
            Rich Panel with details
        """
        # Build detailed content
        lines = []
        lines.append(f"[bold bright_cyan]📋 Job Title:[/bold bright_cyan] [yellow]{job.title or 'N/A'}[/yellow]")
        lines.append(f"[bold bright_green]🏢 Company:[/bold bright_green] [yellow]{job.employer_name or 'N/A'}[/yellow]")
        lines.append(f"[bold bright_yellow]📍 Location:[/bold bright_yellow] {job.get_location()}")
        lines.append(f"[bold bright_cyan]💰 Salary:[/bold bright_cyan] [green]{job.get_salary_range() or 'Not specified'}[/green]")
        lines.append(f"[bold]⏱️  Employment Type:[/bold] {job.employment_type or 'N/A'}")
        lines.append(f"[bold]🌍 Remote:[/bold] {'✓ Yes' if job.is_remote else '✗ No'}")
        lines.append(f"[bold]📅 Posted:[/bold] {job.posted_at_datetime or 'N/A'}")
        lines.append(f"[bold]👤 Experience Required:[/bold] {job.required_experience or 'Not specified'}")
        lines.append(f"[bold]🎓 Education Required:[/bold] {job.required_education or 'Not specified'}")
        
        lines.append("\n[bold bright_magenta]📝 Description:[/bold bright_magenta]")
        description = job.get_short_description(300)
        lines.append(description if description else "No description available")
        
        lines.append("\n[bold bright_cyan]🔗 Apply Link:[/bold bright_cyan]")
        lines.append(f"[blue underline]{job.apply_link or 'N/A'}[/blue underline]")

        content = "\n".join(lines)
        
        return Panel(
            content.strip(),
            title=f"[bold bright_yellow]JOB DETAILS: {job.job_id[:12]}[/bold bright_yellow]",
            border_style="bright_blue",
            padding=(1, 2)
        )

    @staticmethod
    def format_job_summary(jobs: List[Job]) -> str:
        """
        Format job summary in plain text

        Args:
            jobs: List of jobs

        Returns:
            Summary in text
        """
        lines = ["\n" + "=" * 100]
        lines.append(f"📊 SEARCH SUMMARY - {len(jobs)} jobs found")
        lines.append("=" * 100 + "\n")

        for i, job in enumerate(jobs, 1):
            lines.append(f"[{i}] 📋 {job.title or 'N/A'}")
            lines.append(f"    🏢 Company: {job.employer_name or 'N/A'}")
            lines.append(f"    📍 Location: {job.get_location()}")
            lines.append(f"    💰 Salary: {job.get_salary_range() or 'Not specified'}")
            lines.append(f"    ⏱️  Type: {job.employment_type or 'N/A'}")
            lines.append(f"    🌍 Remote: {'Yes' if job.is_remote else 'No'}")
            lines.append(f"    🔗 Apply: {job.apply_link or 'N/A'}")
            lines.append("-" * 40)

        lines.append("=" * 100 + "\n")
        return "\n".join(lines)


class SalaryFormatter:
    """Formatter for salary information"""

    @staticmethod
    def format_salary_table(salaries: List[SalaryInfo]) -> Table:
        """
        Create Rich table of salaries

        Args:
            salaries: List of salary information

        Returns:
            Formatted Rich table
        """
        table = Table(
            title="[bold green]💰 SALARY INFORMATION[/bold green]",
            show_lines=True,
            expand=True
        )

        # Columns
        table.add_column("Job Title", style="bright_magenta", width=30)
        table.add_column("Location", style="bright_cyan", width=25)
        table.add_column("Median Salary", style="bright_green", justify="right", width=18)
        table.add_column("Salary Range", style="bright_yellow", justify="right", width=25)
        table.add_column("Source", style="dim", width=20)

        for salary in salaries:
            # Format values
            title_short = (salary.job_title[:27] + "...") if salary.job_title and len(salary.job_title) > 30 else (salary.job_title or "N/A")
            location_short = (salary.location[:22] + "...") if salary.location and len(salary.location) > 25 else (salary.location or "N/A")

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
        Format salary details in plain text

        Args:
            salaries: List of salary information

        Returns:
            Details in text
        """
        lines = ["\n" + "=" * 100]
        lines.append(f"💰 SALARY INFORMATION - {len(salaries)} results")
        lines.append("=" * 100 + "\n")

        for i, salary in enumerate(salaries, 1):
            lines.append(f"[{i}] 📋 {salary.job_title or 'N/A'}")
            lines.append(f"    📍 Location: {salary.location or 'N/A'}")

            if salary.median_salary:
                lines.append(f"    💰 Median Salary: {salary.get_formatted_median()}")
            if salary.min_salary and salary.max_salary:
                lines.append(f"    💵 Range: {salary.get_formatted_range()}")
            if salary.additional_pay:
                lines.append(f"    ➕ Additional Pay: {salary.additional_pay}")

            lines.append(f"    📰 Source: {salary.publisher_name or 'N/A'}")
            lines.append("-" * 40)

        lines.append("=" * 100 + "\n")
        return "\n".join(lines)
