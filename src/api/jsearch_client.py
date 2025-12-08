#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: jsearch_client.py
Descripción: Cliente especializado para la API JSearch de OpenWeb Ninja.
             Proporciona métodos para buscar trabajos, obtener detalles y consultar salarios.

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
import logging
from typing import List, Dict, Any, Optional
from src.api.client import HTTPClient, HTTPError
from src.api.rate_limiter import RateLimiter
from src.models.search_params import SearchParameters

logger = logging.getLogger(__name__)


class JSearchClient:
    """Cliente para interactuar con JSearch API de OpenWeb Ninja"""

    def __init__(self, api_key: str, api_host: str = "api.openwebninja.com", config: Any = None):
        """
        Args:
            api_key: API key de OpenWeb Ninja
            api_host: Host de la API
            config: Objeto Config opcional con configuración
        """
        self.api_key = api_key
        self.api_host = api_host

        # Crear cliente HTTP
        self.client = HTTPClient(
            host=api_host,
            headers={'x-api-key': api_key},
            timeout=config.request_timeout if config else 30
        )

        # Configurar rate limiter
        self.rate_limiter = RateLimiter(
            delay=config.rate_limit_delay if config else 1.0,
            max_retries=config.max_retries if config else 3,
            retry_delay=config.retry_delay if config else 2
        )

        logger.info(f"JSearchClient inicializado para {api_host}")

    def search_jobs(self, params: SearchParameters) -> List[Dict[str, Any]]:
        """
        Busca trabajos usando JSearch API

        Args:
            params: Parámetros de búsqueda validados

        Returns:
            Lista de trabajos encontrados

        Raises:
            HTTPError: Si hay error en la petición
        """
        endpoint = "/jsearch/search"
        api_params = params.to_api_params()

        logger.info(f"Buscando trabajos: {params.query} en {params.country}")

        # Usar rate limiter con reintentos
        @self.rate_limiter.with_retry
        def _make_request():
            response = self.client.get(endpoint, api_params)

            # Verificar si hay error en la respuesta
            if "error" in response:
                raise HTTPError(400, response.get("error"))

            return response.get("data", [])

        try:
            jobs = _make_request()
            logger.info(f"Encontrados {len(jobs)} trabajos")
            return jobs
        except HTTPError as e:
            if e.status_code == 429:
                logger.error("Rate limit excedido")
                raise HTTPError(429, "Rate limit excedido. Intenta más tarde.")
            raise

    def get_job_details(
        self,
        job_id: str,
        country: str = "us",
        language: Optional[str] = None,
        fields: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Obtiene detalles de un trabajo específico

        Args:
            job_id: ID del trabajo
            country: Código de país
            language: Código de idioma (opcional)
            fields: Campos específicos a incluir (opcional)

        Returns:
            Detalles del trabajo

        Raises:
            HTTPError: Si hay error en la petición
        """
        endpoint = "/jsearch/job-details"
        params = {
            'job_id': job_id,
            'country': country
        }

        if language:
            params['language'] = language
        if fields:
            params['fields'] = fields

        logger.info(f"Obteniendo detalles del trabajo: {job_id}")

        @self.rate_limiter.with_retry
        def _make_request():
            response = self.client.get(endpoint, params)

            if "error" in response:
                raise HTTPError(400, response.get("error"))

            data = response.get("data", [])
            if not data:
                raise HTTPError(404, "Trabajo no encontrado")

            return data[0]  # Retornar primer resultado

        return _make_request()

    def get_estimated_salary(
        self,
        job_title: str,
        location: str,
        location_type: str = "ANY",
        years_of_experience: str = "ALL",
        fields: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Obtiene estimación de salarios

        Args:
            job_title: Título del trabajo
            location: Ubicación
            location_type: Tipo de ubicación (ANY, CITY, STATE, COUNTRY)
            years_of_experience: Nivel de experiencia
            fields: Campos específicos (opcional)

        Returns:
            Lista con información salarial

        Raises:
            HTTPError: Si hay error en la petición
        """
        endpoint = "/jsearch/estimated-salary"
        params = {
            'job_title': job_title,
            'location': location,
            'location_type': location_type,
            'years_of_experience': years_of_experience
        }

        if fields:
            params['fields'] = fields

        logger.info(f"Obteniendo estimación salarial: {job_title} en {location}")

        @self.rate_limiter.with_retry
        def _make_request():
            response = self.client.get(endpoint, params)

            if "error" in response:
                raise HTTPError(400, response.get("error"))

            return response.get("data", [])

        return _make_request()

    def get_company_salary(
        self,
        company: str,
        job_title: str,
        location: Optional[str] = None,
        location_type: str = "ANY",
        years_of_experience: str = "ALL"
    ) -> List[Dict[str, Any]]:
        """
        Obtiene salarios de una empresa específica

        Args:
            company: Nombre de la empresa
            job_title: Título del trabajo
            location: Ubicación (opcional)
            location_type: Tipo de ubicación
            years_of_experience: Nivel de experiencia

        Returns:
            Lista con información salarial de la empresa

        Raises:
            HTTPError: Si hay error en la petición
        """
        endpoint = "/jsearch/company-job-salary"
        params = {
            'company': company,
            'job_title': job_title,
            'location_type': location_type,
            'years_of_experience': years_of_experience
        }

        if location:
            params['location'] = location

        logger.info(f"Obteniendo salarios de {company} para {job_title}")

        @self.rate_limiter.with_retry
        def _make_request():
            response = self.client.get(endpoint, params)

            if "error" in response:
                raise HTTPError(400, response.get("error"))

            return response.get("data", [])

        return _make_request()
