#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: main.py
Descripción: Punto de entrada principal de la aplicación LinkedIn Job Scraper.
             Gestiona la interfaz de usuario, servicios de búsqueda de empleos
             y coordinación de todas las funcionalidades del scraper.

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
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
    Maneja búsqueda personalizada del usuario

    Args:
        job_service: Servicio de trabajos
        export_service: Servicio de exportación
        prompts: Manejador de prompts
        console: Console de Rich
    """
    try:
        # Obtener parámetros
        params = prompts.get_custom_search_params()

        # Buscar trabajos con spinner
        with console.console.status("[bold green]Buscando trabajos...", spinner="dots"):
            jobs = job_service.search_jobs(params)

        if jobs:
            # Mostrar tabla con Rich
            table = JobFormatter.format_job_table(jobs)
            console.console.print("\n")
            console.console.print(table)

            console.print_success(f"Se encontraron {len(jobs)} trabajos")

            # Guardar resultados
            if prompts.confirm_save("¿Guardar resultados a archivos?"):
                csv_path = export_service.export_jobs_to_csv(jobs, params.query)
                json_path = export_service.export_jobs_to_json(jobs, params.query)
                console.print_success(f"CSV: {csv_path.name}")
                console.print_success(f"JSON: {json_path.name}")
        else:
            console.print_warning("No se encontraron trabajos con estos criterios")

    except Exception as e:
        console.print_error(f"Error en búsqueda: {e}")


def handle_predefined_search(choice, job_service, export_service, console):
    """
    Maneja búsquedas predefinidas

    Args:
        choice: Opción seleccionada
        job_service: Servicio de trabajos
        export_service: Servicio de exportación
        console: Console de Rich
    """
    try:
        params = PREDEFINED_SEARCHES[choice]
        title = SEARCH_TITLES[choice]

        console.print_info(f"Ejecutando búsqueda: {title}")

        # Buscar trabajos con spinner
        with console.console.status("[bold green]Buscando...", spinner="dots"):
            jobs = job_service.search_jobs(params)

        if jobs:
            # Mostrar tabla
            table = JobFormatter.format_job_table(jobs)
            console.console.print("\n")
            console.console.print(table)

            # Guardar automáticamente
            csv_path = export_service.export_jobs_to_csv(jobs, params.query)
            console.print_success(f"Guardado en: {csv_path.name}")
        else:
            console.print_warning("No se encontraron trabajos")

    except Exception as e:
        console.print_error(f"Error en búsqueda: {e}")


def handle_job_details(job_service, export_service, prompts, console):
    """
    Maneja obtención de detalles de trabajo

    Args:
        job_service: Servicio de trabajos
        export_service: Servicio de exportación
        prompts: Manejador de prompts
        console: Console de Rich
    """
    try:
        # Obtener job_id
        job_id, country = prompts.get_job_id_input()

        # Obtener detalles con spinner
        with console.console.status("[bold green]Obteniendo detalles...", spinner="dots"):
            job = job_service.get_job_details(job_id, country)

        # Mostrar panel con detalles
        panel = JobFormatter.format_job_details(job)
        console.console.print("\n")
        console.console.print(panel)

        # Guardar si el usuario quiere
        if prompts.confirm_save("¿Guardar detalles?"):
            csv_path = export_service.export_jobs_to_csv([job], f"job_details_{job_id[:8]}")
            console.print_success(f"Guardado en: {csv_path.name}")

    except Exception as e:
        console.print_error(f"Error obteniendo detalles: {e}")


def handle_salary_estimate(salary_service, export_service, prompts, console):
    """
    Maneja estimación de salarios

    Args:
        salary_service: Servicio de salarios
        export_service: Servicio de exportación
        prompts: Manejador de prompts
        console: Console de Rich
    """
    try:
        # Obtener parámetros
        params = prompts.get_salary_estimate_params()

        # Consultar salarios con spinner
        with console.console.status("[bold green]Consultando salarios...", spinner="dots"):
            salaries = salary_service.get_estimated_salary(**params)

        if salaries:
            # Mostrar tabla
            table = SalaryFormatter.format_salary_table(salaries)
            console.console.print("\n")
            console.console.print(table)

            console.print_success(f"Encontrados {len(salaries)} datos salariales")

            # Guardar si el usuario quiere
            if prompts.confirm_save("¿Guardar información salarial?"):
                json_path = export_service.export_salaries_to_json(
                    salaries,
                    f"salary_{params['job_title']}"
                )
                console.print_success(f"Guardado en: {json_path.name}")
        else:
            console.print_warning("No se encontró información de salarios")

    except Exception as e:
        console.print_error(f"Error consultando salarios: {e}")


def handle_company_salary(salary_service, export_service, prompts, console):
    """
    Maneja consulta de salarios de empresa

    Args:
        salary_service: Servicio de salarios
        export_service: Servicio de exportación
        prompts: Manejador de prompts
        console: Console de Rich
    """
    try:
        # Obtener parámetros
        params = prompts.get_company_salary_params()

        # Consultar salarios con spinner
        company_name = params['company']
        with console.console.status(
            f"[bold green]Consultando salarios de {company_name}...",
            spinner="dots"
        ):
            salaries = salary_service.get_company_salary(**params)

        if salaries:
            # Mostrar tabla
            table = SalaryFormatter.format_salary_table(salaries)
            console.console.print("\n")
            console.console.print(table)

            console.print_success(f"Encontrados {len(salaries)} datos salariales")

            # Guardar si el usuario quiere
            if prompts.confirm_save("¿Guardar información salarial?"):
                json_path = export_service.export_salaries_to_json(
                    salaries,
                    f"company_salary_{company_name}"
                )
                console.print_success(f"Guardado en: {json_path.name}")
        else:
            console.print_warning(f"No se encontró información de salarios para {company_name}")

    except Exception as e:
        console.print_error(f"Error consultando salarios: {e}")


def main():
    """Función principal de la aplicación"""
    console = Console()

    # Banner
    console.console.print("\n[bold cyan]═══════════════════════════════════════════════════════════════════════[/bold cyan]")
    console.console.print("[bold magenta]                   LINKEDIN JOB SCRAPER v3.0.0                         [/bold magenta]")
    console.console.print("[bold cyan]═══════════════════════════════════════════════════════════════════════[/bold cyan]\n")

    # Cargar configuración
    try:
        config = Config.load()
        logger = setup_logger(
            level=config.log_level,
            log_dir=config.log_dir,
            log_to_file=config.log_to_file,
            log_to_console=False  # Evitar duplicados con Rich
        )
        logger.info("LinkedIn Job Scraper v3.0.0 iniciado")

    except Exception as e:
        console.print_error(f"Error en configuración: {e}")
        console.console.print("\n[yellow]Verifica tu archivo .env[/yellow]")
        console.console.print("[dim]Copia .env.example a .env y configura tu API_KEY[/dim]\n")
        return

    # Inicializar servicios
    try:
        api_client = JSearchClient(config.api_key, config.api_host, config)
        job_service = JobService(api_client)
        salary_service = SalaryService(api_client)
        export_service = ExportService(config.output_dir)

        console.print_success("Servicios inicializados correctamente")
        console.print_info(f"Conectado a: {config.api_host}")

    except Exception as e:
        console.print_error(f"Error inicializando servicios: {e}")
        logger.error(f"Error fatal: {e}", exc_info=True)
        return

    # Inicializar UI
    menu = MenuSystem(console)
    prompts = Prompts(console)

    # Loop principal
    while True:
        try:
            choice = menu.show_main_menu()

            if choice == "0":
                console.print_info("¡Hasta luego! Gracias por usar LinkedIn Job Scraper")
                logger.info("Aplicación finalizada por el usuario")
                break

            elif choice == "1":
                # Búsqueda personalizada
                handle_custom_search(job_service, export_service, prompts, console)

            elif choice in PREDEFINED_SEARCHES:
                # Búsquedas predefinidas
                handle_predefined_search(choice, job_service, export_service, console)

            elif choice == "11":
                # Obtener detalles de trabajo
                handle_job_details(job_service, export_service, prompts, console)

            elif choice == "12":
                # Consultar salarios estimados
                handle_salary_estimate(salary_service, export_service, prompts, console)

            elif choice == "13":
                # Consultar salarios de empresa
                handle_company_salary(salary_service, export_service, prompts, console)

            # Pausa antes de mostrar menú de nuevo
            menu.wait_for_enter()

        except KeyboardInterrupt:
            console.print_warning("\nOperación cancelada por el usuario")
            continue
        except Exception as e:
            console.print_error(f"Error inesperado: {e}")
            logger.error(f"Error en loop principal: {e}", exc_info=True)
            menu.wait_for_enter()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[AVISO] Programa interrumpido por el usuario")
        print("Hasta luego")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Error fatal: {e}")
        print("Por favor verifica tu configuración y conexión a internet")
        sys.exit(1)
