#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: rate_limiter.py
Descripción: Implementa control de tasa de peticiones (rate limiting) y sistema
             de reintentos con backoff exponencial para evitar saturar la API.

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
import time
import logging
from functools import wraps
from typing import Callable, TypeVar, Any

logger = logging.getLogger(__name__)

T = TypeVar('T')


class RateLimiter:
    """Implementa rate limiting para requests a la API"""

    def __init__(self, delay: float = 1.0, max_retries: int = 3, retry_delay: int = 2):
        """
        Args:
            delay: Tiempo mínimo entre requests (segundos)
            max_retries: Número máximo de reintentos
            retry_delay: Delay base entre reintentos (segundos)
        """
        self.delay = delay
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.last_request_time = 0.0
        self.request_count = 0

    def wait(self) -> None:
        """Espera el tiempo necesario para respetar rate limiting"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time

        if time_since_last_request < self.delay:
            sleep_time = self.delay - time_since_last_request
            logger.debug(f"Rate limiting: esperando {sleep_time:.2f}s")
            time.sleep(sleep_time)

        self.last_request_time = time.time()
        self.request_count += 1
        logger.debug(f"Request #{self.request_count}")

    def with_retry(self, func: Callable[..., T]) -> Callable[..., T]:
        """
        Decorator para agregar lógica de reintentos a una función

        Args:
            func: Función a decorar

        Returns:
            Función decorada con reintentos
        """
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception = None

            for attempt in range(self.max_retries):
                try:
                    # Rate limiting antes de cada intento
                    self.wait()

                    # Ejecutar función
                    result = func(*args, **kwargs)
                    return result

                except Exception as e:
                    last_exception = e
                    logger.warning(f"Intento {attempt + 1}/{self.max_retries} falló: {e}")

                    # Si no es el último intento, esperar con backoff exponencial
                    if attempt < self.max_retries - 1:
                        sleep_time = self.retry_delay * (2 ** attempt)  # Exponential backoff
                        logger.info(f"Reintentando en {sleep_time}s...")
                        time.sleep(sleep_time)
                    else:
                        logger.error(f"Máximo de reintentos alcanzado")

            # Si llegamos aquí, todos los intentos fallaron
            raise last_exception or Exception("Máximo de reintentos alcanzado")

        return wrapper


def retry_on_http_error(max_retries: int = 3, retry_delay: int = 2):
    """
    Decorator para reintentar en caso de errores HTTP específicos

    Args:
        max_retries: Número máximo de reintentos
        retry_delay: Delay base entre reintentos

    Returns:
        Decorator
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    error_str = str(e).lower()

                    # Errores que justifican reintentos
                    retryable_errors = ['429', 'timeout', 'connection', 'temporary']
                    is_retryable = any(err in error_str for err in retryable_errors)

                    if not is_retryable or attempt == max_retries - 1:
                        raise

                    sleep_time = retry_delay * (attempt + 1)
                    logger.warning(f"Error retryable: {e}. Reintentando en {sleep_time}s...")
                    time.sleep(sleep_time)

            raise Exception("Máximo de reintentos alcanzado")

        return wrapper
    return decorator
