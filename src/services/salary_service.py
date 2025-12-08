#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: salary_service.py
Descripción: Servicio de lógica de negocio para consultas salariales.
             Proporciona estimaciones salariales, salarios por empresa y comparaciones.

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
import logging
from typing import List, Optional
from pydantic import ValidationError
from src.api.jsearch_client import JSearchClient
from src.models.salary import SalaryInfo

logger = logging.getLogger(__name__)


class SalaryService:
    """Servicio para consultas salariales"""

    def __init__(self, api_client: JSearchClient):
        """
        Args:
            api_client: Cliente de JSearch API
        """
        self.api_client = api_client
        logger.debug("SalaryService inicializado")

    def get_estimated_salary(
        self,
        job_title: str,
        location: str,
        years_of_experience: str = "ALL"
    ) -> List[SalaryInfo]:
        """
        Obtiene estimación de salarios

        Args:
            job_title: Título del puesto
            location: Ubicación
            years_of_experience: Nivel de experiencia

        Returns:
            Lista de SalaryInfo

        Raises:
            Exception: Si hay error en la consulta
        """
        logger.info(f"Consultando salarios: {job_title} en {location} ({years_of_experience})")

        try:
            raw_results = self.api_client.get_estimated_salary(
                job_title=job_title,
                location=location,
                years_of_experience=years_of_experience
            )

            # Parsear resultados
            salaries = []
            for i, salary_data in enumerate(raw_results):
                try:
                    salary = SalaryInfo.model_validate(salary_data)
                    if salary.has_salary_data():  # Solo incluir si tiene datos
                        salaries.append(salary)
                except ValidationError as e:
                    logger.warning(f"Error parseando salario #{i+1}: {e}")
                    continue

            logger.info(f"Obtenidos {len(salaries)} datos salariales")
            return salaries

        except Exception as e:
            logger.error(f"Error consultando salarios: {e}")
            raise

    def get_company_salary(
        self,
        company: str,
        job_title: str,
        location: Optional[str] = None,
        years_of_experience: str = "ALL"
    ) -> List[SalaryInfo]:
        """
        Obtiene salarios de una empresa específica

        Args:
            company: Nombre de la empresa
            job_title: Título del puesto
            location: Ubicación (opcional)
            years_of_experience: Nivel de experiencia

        Returns:
            Lista de SalaryInfo

        Raises:
            Exception: Si hay error en la consulta
        """
        logger.info(f"Consultando salarios de {company} para {job_title}")

        try:
            raw_results = self.api_client.get_company_salary(
                company=company,
                job_title=job_title,
                location=location,
                years_of_experience=years_of_experience
            )

            # Parsear resultados
            salaries = []
            for i, salary_data in enumerate(raw_results):
                try:
                    salary = SalaryInfo.model_validate(salary_data)
                    if salary.has_salary_data():
                        salaries.append(salary)
                except ValidationError as e:
                    logger.warning(f"Error parseando salario de empresa #{i+1}: {e}")
                    continue

            logger.info(f"Obtenidos {len(salaries)} datos salariales de {company}")
            return salaries

        except Exception as e:
            logger.error(f"Error consultando salarios de empresa: {e}")
            raise

    def compare_locations(
        self,
        job_title: str,
        locations: List[str],
        years_of_experience: str = "ALL"
    ) -> dict:
        """
        Compara salarios entre diferentes ubicaciones

        Args:
            job_title: Título del puesto
            locations: Lista de ubicaciones
            years_of_experience: Nivel de experiencia

        Returns:
            Diccionario con comparación por ubicación
        """
        logger.info(f"Comparando salarios para {job_title} en {len(locations)} ubicaciones")

        comparison = {}
        for location in locations:
            try:
                salaries = self.get_estimated_salary(job_title, location, years_of_experience)
                if salaries:
                    # Calcular promedio de medianas
                    medians = [s.median_salary for s in salaries if s.median_salary]
                    avg_median = sum(medians) / len(medians) if medians else None
                    comparison[location] = {
                        'count': len(salaries),
                        'average_median': avg_median,
                        'salaries': salaries
                    }
            except Exception as e:
                logger.warning(f"Error comparando {location}: {e}")
                continue

        return comparison
