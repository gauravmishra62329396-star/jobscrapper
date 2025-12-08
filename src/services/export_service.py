#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: export_service.py
Descripción: Servicio para exportar datos de trabajos y salarios a formatos CSV y JSON.
             Gestiona la creación de archivos con nombres generados automáticamente.

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
import csv
import json
import logging
from pathlib import Path
from typing import List, Union
from src.models.job import Job
from src.models.salary import SalaryInfo
from src.utils.file_utils import generate_filename, ensure_dir_exists

logger = logging.getLogger(__name__)


class ExportService:
    """Servicio para exportar datos a diferentes formatos"""

    def __init__(self, output_dir: Union[str, Path] = "output"):
        """
        Args:
            output_dir: Directorio de salida
        """
        self.output_dir = ensure_dir_exists(output_dir)
        logger.debug(f"ExportService inicializado: {self.output_dir}")

    def export_jobs_to_csv(self, jobs: List[Job], base_name: str) -> Path:
        """
        Exporta trabajos a CSV

        Args:
            jobs: Lista de trabajos
            base_name: Nombre base del archivo

        Returns:
            Path del archivo creado

        Raises:
            Exception: Si hay error al escribir
        """
        filename = generate_filename(base_name, "csv")
        filepath = self.output_dir / filename

        logger.info(f"Exportando {len(jobs)} trabajos a CSV: {filepath}")

        try:
            # Definir columnas
            fieldnames = [
                'job_id', 'title', 'employer_name', 'city', 'state', 'country',
                'is_remote', 'employment_type', 'min_salary', 'max_salary',
                'salary_currency', 'salary_period', 'description', 'apply_link',
                'posted_at_datetime', 'job_publisher', 'required_experience',
                'required_skills', 'required_education', 'benefits', 'google_link',
                'expiration_datetime'
            ]

            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
                writer.writeheader()

                for job in jobs:
                    # Convertir job a dict
                    job_dict = job.model_dump()

                    # Limpiar descripción
                    if job_dict.get('description'):
                        job_dict['description'] = job.get_short_description(500)

                    # Convertir listas a strings
                    if job_dict.get('required_skills') and isinstance(job_dict['required_skills'], list):
                        job_dict['required_skills'] = ', '.join(job_dict['required_skills'])

                    if job_dict.get('benefits') and isinstance(job_dict['benefits'], list):
                        job_dict['benefits'] = ', '.join(job_dict['benefits'])

                    writer.writerow(job_dict)

            logger.info(f"CSV creado exitosamente: {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"Error exportando a CSV: {e}")
            raise

    def export_jobs_to_json(self, jobs: List[Job], base_name: str) -> Path:
        """
        Exporta trabajos a JSON

        Args:
            jobs: Lista de trabajos
            base_name: Nombre base del archivo

        Returns:
            Path del archivo creado

        Raises:
            Exception: Si hay error al escribir
        """
        filename = generate_filename(base_name, "json")
        filepath = self.output_dir / filename

        logger.info(f"Exportando {len(jobs)} trabajos a JSON: {filepath}")

        try:
            # Convertir jobs a dicts
            jobs_data = [job.model_dump() for job in jobs]

            with open(filepath, 'w', encoding='utf-8') as jsonfile:
                json.dump(jobs_data, jsonfile, ensure_ascii=False, indent=2)

            logger.info(f"JSON creado exitosamente: {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"Error exportando a JSON: {e}")
            raise

    def export_salaries_to_json(self, salaries: List[SalaryInfo], base_name: str) -> Path:
        """
        Exporta información salarial a JSON

        Args:
            salaries: Lista de información salarial
            base_name: Nombre base del archivo

        Returns:
            Path del archivo creado

        Raises:
            Exception: Si hay error al escribir
        """
        filename = generate_filename(base_name, "json")
        filepath = self.output_dir / filename

        logger.info(f"Exportando {len(salaries)} datos salariales a JSON: {filepath}")

        try:
            # Convertir salaries a dicts
            salaries_data = [salary.model_dump() for salary in salaries]

            with open(filepath, 'w', encoding='utf-8') as jsonfile:
                json.dump(salaries_data, jsonfile, ensure_ascii=False, indent=2)

            logger.info(f"JSON salarial creado exitosamente: {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"Error exportando salarios a JSON: {e}")
            raise

    def export_salaries_to_csv(self, salaries: List[SalaryInfo], base_name: str) -> Path:
        """
        Exporta información salarial a CSV

        Args:
            salaries: Lista de información salarial
            base_name: Nombre base del archivo

        Returns:
            Path del archivo creado
        """
        filename = generate_filename(base_name, "csv")
        filepath = self.output_dir / filename

        logger.info(f"Exportando {len(salaries)} datos salariales a CSV: {filepath}")

        try:
            fieldnames = [
                'job_title', 'location', 'publisher_name', 'min_salary',
                'max_salary', 'median_salary', 'salary_currency',
                'salary_period', 'additional_pay'
            ]

            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for salary in salaries:
                    writer.writerow(salary.model_dump())

            logger.info(f"CSV salarial creado exitosamente: {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"Error exportando salarios a CSV: {e}")
            raise
