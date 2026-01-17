#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: prompts.py
Description: Interactive prompts to capture user input via Rich,
             including search parameters, salary queries, and confirmations.

Author: Hex686f6c61
Repository: https://github.com/Hex686f6c61/linkedIN-Scraper
Version: 3.0.0
Date: 2025-12-08
"""
from typing import Tuple, Dict
from rich.prompt import Prompt, Confirm, IntPrompt
from src.ui.console import Console
from src.models.search_params import SearchParameters


class Prompts:
    """Interactive input handlers"""

    def __init__(self, console: Console):
        """
        Args:
            console: Rich Console
        """
        self.console = console

    def get_custom_search_params(self) -> SearchParameters:
        """
        Get custom search parameters from user

        Returns:
            Validated SearchParameters
        """
        self.console.print_header("CUSTOM SEARCH CONFIGURATION")

        # Search query
        query = Prompt.ask("\n[cyan]Search Query[/cyan] (e.g., 'python developer madrid')")

        # Country
        country = Prompt.ask(
            "[cyan]Country Code[/cyan] (e.g., es, us, mx)",
            default="us",
            show_default=True
        )

        # Publication period
        self.console.console.print("\n[bold]Publication Period:[/bold]")
        self.console.console.print("  1. All")
        self.console.console.print("  2. Today")
        self.console.console.print("  3. Last 3 Days")
        self.console.console.print("  4. Last Week")
        self.console.console.print("  5. Last Month")

        periodo_choice = Prompt.ask(
            "[cyan]Select Period[/cyan]",
            choices=["1", "2", "3", "4", "5"],
            default="1"
        )

        periodos = {
            "1": "all", "2": "today", "3": "3days",
            "4": "week", "5": "month"
        }
        date_posted = periodos[periodo_choice]

        # Remote work only
        work_from_home = Confirm.ask("\n[cyan]Remote jobs only?[/cyan]", default=False)

        # Employment type
        self.console.console.print("\n[dim]Employment Types (optional): FULLTIME, PARTTIME, CONTRACTOR, INTERN[/dim]")
        employment_types = Prompt.ask(
            "[cyan]Employment Type[/cyan] (leave empty for all)",
            default="",
            show_default=False
        )
        employment_types = employment_types.strip() if employment_types else None

        # Number of pages
        num_pages = IntPrompt.ask(
            "\n[cyan]Number of Pages[/cyan] (1-10)",
            default=1,
            show_default=True
        )
        num_pages = max(1, min(10, num_pages))  # Limit between 1 and 10

        # Create and validate parameters
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
            self.console.print_error(f"Error in parameters: {e}")
            raise

    def get_job_id_input(self) -> Tuple[str, str]:
        """
        Request Job ID and country from user

        Returns:
            Tuple (job_id, country)
        """
        self.console.print_header("GET JOB DETAILS")

        job_id = Prompt.ask("\n[cyan]Job ID[/cyan]")
        country = Prompt.ask(
            "[cyan]Country Code[/cyan]",
            default="us",
            show_default=True
        )

        return job_id, country

    def get_salary_estimate_params(self) -> Dict[str, str]:
        """
        Get parameters for salary estimation

        Returns:
            Dictionary with parameters
        """
        self.console.print_header("VIEW ESTIMATED SALARIES")

        job_title = Prompt.ask("\n[cyan]Job Title[/cyan] (e.g., 'Software Engineer')")
        location = Prompt.ask("[cyan]Location[/cyan] (e.g., 'Madrid, Spain' or 'New York, NY')")

        # Experience menu
        years_of_experience = self._get_experience_level()

        return {
            "job_title": job_title,
            "location": location,
            "years_of_experience": years_of_experience
        }

    def get_company_salary_params(self) -> Dict[str, str]:
        """
        Get parameters for company salaries

        Returns:
            Dictionary with parameters
        """
        self.console.print_header("VIEW COMPANY SALARIES")

        company = Prompt.ask("\n[cyan]Company[/cyan] (e.g., 'Google', 'Amazon')")
        job_title = Prompt.ask("[cyan]Job Title[/cyan] (e.g., 'Software Engineer')")

        location = Prompt.ask(
            "[cyan]Location[/cyan] (optional, press ENTER to skip)",
            default="",
            show_default=False
        )
        location = location.strip() if location else None

        # Experience menu
        years_of_experience = self._get_experience_level()

        return {
            "company": company,
            "job_title": job_title,
            "location": location,
            "years_of_experience": years_of_experience
        }

    def _get_experience_level(self) -> str:
        """
        Display experience level menu

        Returns:
            Experience code
        """
        self.console.console.print("\n[bold]Years of Experience:[/bold]")
        self.console.console.print("  1. All (ALL)")
        self.console.console.print("  2. Less than 1 year")
        self.console.console.print("  3. 1-3 years")
        self.console.console.print("  4. 4-6 years")
        self.console.console.print("  5. 7-9 years")
        self.console.console.print("  6. 10+ years")

        exp_choice = Prompt.ask(
            "[cyan]Select Level[/cyan]",
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

    def confirm_save(self, prompt_text: str = "Save results?") -> bool:
        """
        Ask user if they want to save

        Args:
            prompt_text: Prompt text

        Returns:
            True if user confirms
        """
        return Confirm.ask(f"[yellow]{prompt_text}[/yellow]", default=True)
