#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: menu.py
Description: Interactive menu system using Rich to display search options
             and scraper functionality for LinkedIn.

Author: Hex686f6c61
Repository: https://github.com/Hex686f6c61/linkedIN-Scraper
Version: 3.0.0
Date: 2025-12-08
"""
from rich.prompt import Prompt
from rich.panel import Panel
from src.ui.console import Console


class MenuSystem:
    """Interactive menu system"""

    def __init__(self, console: Console):
        """
        Args:
            console: Rich Console
        """
        self.console = console

    def show_main_menu(self) -> str:
        """
        Display main menu and return selected option

        Returns:
            Selected option as string
        """
        self.console.print_header("LINKEDIN JOB SCRAPER v3.0.0 - MAIN MENU")

        menu_text = """
[bold cyan]PREDEFINED SEARCHES:[/bold cyan]
  [1]  Custom Search
  [2]  Project Manager - Spain
  [3]  Software Engineer - Spain
  [4]  Data Scientist - Spain
  [5]  Frontend Developer - Spain
  [6]  Backend Developer - United States
  [7]  Machine Learning Engineer - United States
  [8]  Full Stack Developer - United States
  [9]  DevOps Engineer - United Kingdom
  [10] Senior Software Engineer - Global Remote

[bold magenta]ADDITIONAL FEATURES:[/bold magenta]
  [11] Get Job Details (by ID)
  [12] View Estimated Salaries
  [13] View Company Salaries

[bold red][0] Exit[/bold red]
        """

        panel = Panel(menu_text.strip(), border_style="green", padding=(1, 2))
        self.console.console.print(panel)

        # Get user choice
        choice = Prompt.ask(
            "\n[bold]Select an option[/bold]",
            choices=[str(i) for i in range(14)],
            default="0"
        )

        return choice

    def confirm_save(self, prompt_text: str = "Save results?") -> bool:
        """
        Ask user if they want to save

        Args:
            prompt_text: Prompt text

        Returns:
            True if user confirms
        """
        from rich.prompt import Confirm
        return Confirm.ask(f"[yellow]{prompt_text}[/yellow]", default=True)

    def wait_for_enter(self):
        """Wait for user to press ENTER"""
        self.console.console.input("\n[dim]Press ENTER to continue...[/dim]")
