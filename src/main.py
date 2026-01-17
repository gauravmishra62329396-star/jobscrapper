#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: main.py
Description: Main entry point of the LinkedIn Job Scraper application.
             Manages the user interface, job search services
             and coordination of all scraper functionalities.

Author: Hex686f6c61
Repository: https://github.com/Hex686f6c61/linkedIN-Scraper
Version: 3.0.0
Date: 2025-12-08
"""
import sys
from src.utils.config import Config
from src.utils.logger import setup_logger
from src.api.jsearch_client import JSearchClient
from src.services.job_service import JobService
from src.services.salary_service import SalaryService
from src.services.export_service import ExportService
from src.ui.console import Console
from src.ui.menu import MenuSystem
from src.ui.prompts import Prompts
from src.ui.formatters import JobFormatter, SalaryFormatter
from config.predefined_searches import PREDEFINED_SEARCHES, SEARCH_TITLES


def handle_custom_search(job_service, export_service, prompts, console):
    """
    Handle custom job search from user

    Args:
        job_service: Job service
        export_service: Export service
        prompts: Prompts handler
        console: Rich console
    """
    try:
        # Get parameters
        params = prompts.get_custom_search_params()

        # Search for jobs with spinner
        with console.console.status("[bold green]Searching for jobs...", spinner="dots"):
            jobs = job_service.search_jobs(params)

        if jobs:
            # Display table with Rich
            table = JobFormatter.format_job_table(jobs)
            console.console.print("\n")
            console.console.print(table)

            console.print_success(f"Found {len(jobs)} jobs")

            # Save results
            if prompts.confirm_save("Save results to files?"):
                csv_path = export_service.export_jobs_to_csv(jobs, params.query)
                json_path = export_service.export_jobs_to_json(jobs, params.query)
                console.print_success(f"CSV: {csv_path.name}")
                console.print_success(f"JSON: {json_path.name}")
        else:
            console.print_warning("No jobs found with these criteria")

    except Exception as e:
        console.print_error(f"Search error: {e}")


def handle_predefined_search(choice, job_service, export_service, console):
    """
    Handle predefined searches

    Args:
        choice: Selected option
        job_service: Job service
        export_service: Export service
        console: Rich console
    """
    try:
        params = PREDEFINED_SEARCHES[choice]
        title = SEARCH_TITLES[choice]

        console.print_info(f"Running search: {title}")

        # Search for jobs with spinner
        with console.console.status("[bold green]Searching...", spinner="dots"):
            jobs = job_service.search_jobs(params)

        if jobs:
            # Display table
            table = JobFormatter.format_job_table(jobs)
            console.console.print("\n")
            console.console.print(table)

            # Auto save
            csv_path = export_service.export_jobs_to_csv(jobs, params.query)
            console.print_success(f"Saved to: {csv_path.name}")
        else:
            console.print_warning("No jobs found")

    except Exception as e:
        console.print_error(f"Search error: {e}")


def handle_job_details(job_service, export_service, prompts, console):
    """
    Handle job details retrieval

    Args:
        job_service: Job service
        export_service: Export service
        prompts: Prompts handler
        console: Rich console
    """
    try:
        # Get job_id
        job_id, country = prompts.get_job_id_input()

        # Get details with spinner
        with console.console.status("[bold green]Fetching details...", spinner="dots"):
            job = job_service.get_job_details(job_id, country)

        # Display panel with details
        panel = JobFormatter.format_job_details(job)
        console.console.print("\n")
        console.console.print(panel)

        # Save if user wants
        if prompts.confirm_save("Save details?"):
            csv_path = export_service.export_jobs_to_csv([job], f"job_details_{job_id[:8]}")
            console.print_success(f"Saved to: {csv_path.name}")

    except Exception as e:
        console.print_error(f"Error fetching details: {e}")


def handle_salary_estimate(salary_service, export_service, prompts, console):
    """
    Handle salary estimation

    Args:
        salary_service: Salary service
        export_service: Export service
        prompts: Prompts handler
        console: Rich console
    """
    try:
        # Get parameters
        params = prompts.get_salary_estimate_params()

        # Query salaries with spinner
        with console.console.status("[bold green]Querying salaries...", spinner="dots"):
            salaries = salary_service.get_estimated_salary(**params)

        if salaries:
            # Display table
            table = SalaryFormatter.format_salary_table(salaries)
            console.console.print("\n")
            console.console.print(table)

            console.print_success(f"Found {len(salaries)} salary records")

            # Save if user wants
            if prompts.confirm_save("Save salary information?"):
                json_path = export_service.export_salaries_to_json(
                    salaries,
                    f"salary_{params['job_title']}"
                )
                console.print_success(f"Saved to: {json_path.name}")
        else:
            console.print_warning("No salary information found")

    except Exception as e:
        console.print_error(f"Error querying salaries: {e}")


def handle_company_salary(salary_service, export_service, prompts, console):
    """
    Handle company salary query

    Args:
        salary_service: Salary service
        export_service: Export service
        prompts: Prompts handler
        console: Rich console
    """
    try:
        # Get parameters
        params = prompts.get_company_salary_params()

        # Query salaries with spinner
        company_name = params['company']
        with console.console.status(
            f"[bold green]Querying salaries for {company_name}...",
            spinner="dots"
        ):
            salaries = salary_service.get_company_salary(**params)

        if salaries:
            # Display table
            table = SalaryFormatter.format_salary_table(salaries)
            console.console.print("\n")
            console.console.print(table)

            console.print_success(f"Found {len(salaries)} salary records")

            # Save if user wants
            if prompts.confirm_save("Save salary information?"):
                json_path = export_service.export_salaries_to_json(
                    salaries,
                    f"company_salary_{company_name}"
                )
                console.print_success(f"Saved to: {json_path.name}")
        else:
            console.print_warning(f"No salary information found for {company_name}")

    except Exception as e:
        console.print_error(f"Error querying salaries: {e}")


def main():
    """Main application function"""
    console = Console()

    # Banner
    console.console.print("\n[bold cyan]═══════════════════════════════════════════════════════════════════════[/bold cyan]")
    console.console.print("[bold magenta]                   LINKEDIN JOB SCRAPER v3.0.0                         [/bold magenta]")
    console.console.print("[bold cyan]═══════════════════════════════════════════════════════════════════════[/bold cyan]\n")

    # Load configuration
    try:
        config = Config.load()
        logger = setup_logger(
            level=config.log_level,
            log_dir=config.log_dir,
            log_to_file=config.log_to_file,
            log_to_console=False  # Avoid duplicates with Rich
        )
        logger.info("LinkedIn Job Scraper v3.0.0 started")

    except Exception as e:
        console.print_error(f"Configuration error: {e}")
        console.console.print("\n[yellow]Verify your .env file[/yellow]")
        console.console.print("[dim]Copy .env.example to .env and configure your API_KEY[/dim]\n")
        return

    # Initialize services
    try:
        api_client = JSearchClient(config.api_key, config.api_host, config)
        job_service = JobService(api_client)
        salary_service = SalaryService(api_client)
        export_service = ExportService(config.output_dir)

        console.print_success("Services initialized successfully")
        console.print_info(f"Connected to: {config.api_host}")

    except Exception as e:
        console.print_error(f"Error initializing services: {e}")
        logger.error(f"Fatal error: {e}", exc_info=True)
        return

    # Initialize UI
    menu = MenuSystem(console)
    prompts = Prompts(console)

    # Main loop
    while True:
        try:
            choice = menu.show_main_menu()

            if choice == "0":
                console.print_info("Goodbye! Thank you for using LinkedIn Job Scraper")
                logger.info("Application closed by user")
                break

            elif choice == "1":
                # Custom search
                handle_custom_search(job_service, export_service, prompts, console)

            elif choice in PREDEFINED_SEARCHES:
                # Predefined searches
                handle_predefined_search(choice, job_service, export_service, console)

            elif choice == "11":
                # Get job details
                handle_job_details(job_service, export_service, prompts, console)

            elif choice == "12":
                # View estimated salaries
                handle_salary_estimate(salary_service, export_service, prompts, console)

            elif choice == "13":
                # View company salaries
                handle_company_salary(salary_service, export_service, prompts, console)

            # Pause before showing menu again
            menu.wait_for_enter()

        except KeyboardInterrupt:
            console.print_warning("\nOperation canceled by user")
            continue
        except Exception as e:
            console.print_error(f"Unexpected error: {e}")
            logger.error(f"Error in main loop: {e}", exc_info=True)
            menu.wait_for_enter()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Program interrupted by user")
        print("Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Fatal error: {e}")
        print("Please verify your configuration and internet connection")
        sys.exit(1)
