#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: config.py
Descripción: Configuración centralizada de la aplicación cargada desde archivo .env.
             Gestiona API keys, timeouts, directorios y configuración de logging.

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Config(BaseSettings):
    """Configuración de la aplicación cargada desde .env"""

    # API Settings
    api_key: str = Field(..., description="API Key de OpenWeb Ninja")
    api_host: str = Field(default="api.openwebninja.com", description="Host de la API")

    # Request Settings
    max_retries: int = Field(default=3, ge=1, le=10, description="Número máximo de reintentos")
    retry_delay: int = Field(default=2, ge=1, le=10, description="Delay entre reintentos (segundos)")
    request_timeout: int = Field(default=30, ge=10, le=120, description="Timeout de requests (segundos)")
    rate_limit_delay: float = Field(default=1.0, ge=0.1, le=5.0, description="Delay entre requests (segundos)")

    # Paths
    output_dir: Path = Field(default=Path("output"), description="Directorio de salida")
    log_dir: Path = Field(default=Path("logs"), description="Directorio de logs")

    # Logging
    log_level: str = Field(default="INFO", description="Nivel de logging")
    log_to_file: bool = Field(default=True, description="Guardar logs en archivo")
    log_to_console: bool = Field(default=True, description="Mostrar logs en consola")

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False
    )

    def validate_and_setup(self) -> None:
        """Valida configuración y crea directorios necesarios"""
        if not self.api_key or self.api_key == "TU_API_KEY_AQUI":
            raise ValueError(
                "API_KEY no configurada. "
                "Por favor configura tu API key en el archivo .env"
            )

        # Crear directorios si no existen
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def load(cls) -> "Config":
        """Carga y valida la configuración"""
        config = cls()
        config.validate_and_setup()
        return config
