#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: client.py
Descripción: Cliente HTTP genérico para realizar peticiones HTTPS a APIs externas.
             Proporciona métodos GET y POST con manejo de errores y parsing JSON.

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
import http.client
import json
import urllib.parse
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class HTTPError(Exception):
    """Excepción para errores HTTP"""

    def __init__(self, status_code: int, message: str = ""):
        self.status_code = status_code
        self.message = message
        super().__init__(f"HTTP {status_code}: {message}")


class HTTPClient:
    """Cliente HTTP genérico para hacer requests HTTPS"""

    def __init__(
        self,
        host: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 30
    ):
        """
        Args:
            host: Hostname del servidor (sin https://)
            headers: Headers HTTP por defecto
            timeout: Timeout en segundos
        """
        self.host = host
        self.headers = headers or {}
        self.timeout = timeout
        logger.debug(f"HTTPClient inicializado para {host}")

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Realiza un GET request

        Args:
            endpoint: Endpoint de la API (ej: "/api/search")
            params: Parámetros de query

        Returns:
            Respuesta JSON parseada

        Raises:
            HTTPError: Si el status code no es 200
            json.JSONDecodeError: Si la respuesta no es JSON válido
        """
        params = params or {}

        # Construir URL con parámetros
        query_string = urllib.parse.urlencode(params)
        full_endpoint = f"{endpoint}?{query_string}" if query_string else endpoint

        logger.debug(f"GET {self.host}{full_endpoint}")

        # Crear conexión HTTPS
        conn = http.client.HTTPSConnection(self.host, timeout=self.timeout)

        try:
            # Realizar request
            conn.request("GET", full_endpoint, headers=self.headers)

            # Obtener respuesta
            response = conn.getresponse()
            status_code = response.status
            data = response.read()

            logger.debug(f"Response: {status_code}, {len(data)} bytes")

            # Verificar status code
            if status_code != 200:
                error_msg = data.decode('utf-8', errors='ignore')[:200]
                raise HTTPError(status_code, error_msg)

            # Parsear JSON
            result = json.loads(data.decode('utf-8'))
            return result

        finally:
            conn.close()

    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Realiza un POST request

        Args:
            endpoint: Endpoint de la API
            data: Datos para el body (se serializan a JSON)
            params: Parámetros de query

        Returns:
            Respuesta JSON parseada

        Raises:
            HTTPError: Si el status code no es 200-201
        """
        params = params or {}
        data = data or {}

        # Construir URL con parámetros
        query_string = urllib.parse.urlencode(params)
        full_endpoint = f"{endpoint}?{query_string}" if query_string else endpoint

        # Preparar body
        body = json.dumps(data).encode('utf-8')

        # Headers para JSON
        headers = self.headers.copy()
        headers['Content-Type'] = 'application/json'
        headers['Content-Length'] = str(len(body))

        logger.debug(f"POST {self.host}{full_endpoint}")

        # Crear conexión HTTPS
        conn = http.client.HTTPSConnection(self.host, timeout=self.timeout)

        try:
            # Realizar request
            conn.request("POST", full_endpoint, body=body, headers=headers)

            # Obtener respuesta
            response = conn.getresponse()
            status_code = response.status
            response_data = response.read()

            logger.debug(f"Response: {status_code}, {len(response_data)} bytes")

            # Verificar status code
            if status_code not in (200, 201):
                error_msg = response_data.decode('utf-8', errors='ignore')[:200]
                raise HTTPError(status_code, error_msg)

            # Parsear JSON
            result = json.loads(response_data.decode('utf-8'))
            return result

        finally:
            conn.close()
