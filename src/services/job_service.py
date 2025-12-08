#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: job_service.py
Descripción: Servicio de lógica de negocio para búsqueda y gestión de trabajos.
             Incluye búsqueda, obtención de detalles, filtrado y ordenamiento de ofertas.

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
import logging
from typing import List
from pydantic import ValidationError
from src.api.jsearch_client import JSearchClient
from src.models.job import Job
from src.models.search_params import SearchParameters

logger = logging.getLogger(__name__)


class JobService:
    """Servicio para búsqueda y gestión de trabajos"""

    def __init__(self, api_client: JSearchClient):
        """
        Args:
            api_client: Cliente de JSearch API
        """
        self.api_client = api_client
        logger.debug("JobService inicializado")

    def search_jobs(self, params: SearchParameters) -> List[Job]:
        """
        Busca trabajos y retorna objetos Job validados

        Args:
            params: Parámetros de búsqueda

        Returns:
            Lista de objetos Job

        Raises:
            Exception: Si hay error en la búsqueda
        """
        logger.info(f"Buscando trabajos: '{params.query}' en {params.country}")

        try:
            # Llamar a la API
            raw_results = self.api_client.search_jobs(params)

            # Parsear resultados a objetos Job
            jobs = []
            for i, job_data in enumerate(raw_results):
                try:
                    job = Job.model_validate(job_data)
                    jobs.append(job)
                except ValidationError as e:
                    logger.warning(f"Error parseando trabajo #{i+1}: {e}")
                    # Continuar con el resto de trabajos
                    continue

            logger.info(f"Parseados {len(jobs)} trabajos de {len(raw_results)} resultados")
            return jobs

        except Exception as e:
            logger.error(f"Error en búsqueda: {e}")
            raise

    def get_job_details(self, job_id: str, country: str = "us") -> Job:
        """
        Obtiene detalles completos de un trabajo

        Args:
            job_id: ID del trabajo
            country: Código de país

        Returns:
            Objeto Job con detalles completos

        Raises:
            Exception: Si hay error obteniendo detalles
        """
        logger.info(f"Obteniendo detalles del trabajo: {job_id}")

        try:
            raw_data = self.api_client.get_job_details(job_id, country)
            job = Job.model_validate(raw_data)

            logger.info(f"Detalles obtenidos: {job.title}")
            return job

        except ValidationError as e:
            logger.error(f"Error parseando detalles del trabajo: {e}")
            raise ValueError(f"Datos del trabajo inválidos: {e}")
        except Exception as e:
            logger.error(f"Error obteniendo detalles: {e}")
            raise

    def filter_remote_jobs(self, jobs: List[Job]) -> List[Job]:
        """
        Filtra solo trabajos remotos

        Args:
            jobs: Lista de trabajos

        Returns:
            Lista de trabajos remotos
        """
        remote_jobs = [job for job in jobs if job.is_remote]
        logger.debug(f"Filtrados {len(remote_jobs)} trabajos remotos de {len(jobs)}")
        return remote_jobs

    def filter_by_salary(
        self,
        jobs: List[Job],
        min_salary: float,
        currency: str = "USD"
    ) -> List[Job]:
        """
        Filtra trabajos por salario mínimo

        Args:
            jobs: Lista de trabajos
            min_salary: Salario mínimo
            currency: Moneda

        Returns:
            Lista de trabajos que cumplen el criterio
        """
        filtered = [
            job for job in jobs
            if job.min_salary and job.salary_currency == currency and job.min_salary >= min_salary
        ]
        logger.debug(f"Filtrados {len(filtered)} trabajos con salario >= {min_salary} {currency}")
        return filtered

    def sort_by_salary(self, jobs: List[Job], descending: bool = True) -> List[Job]:
        """
        Ordena trabajos por salario

        Args:
            jobs: Lista de trabajos
            descending: Si ordenar descendente

        Returns:
            Lista ordenada
        """
        def get_salary_key(job: Job) -> float:
            if job.max_salary:
                return job.max_salary
            elif job.min_salary:
                return job.min_salary
            return 0

        sorted_jobs = sorted(jobs, key=get_salary_key, reverse=descending)
        logger.debug(f"Trabajos ordenados por salario")
        return sorted_jobs
