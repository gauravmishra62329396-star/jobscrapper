#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: test_config.py
Descripción: Tests para Config

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from pydantic import ValidationError
from src.utils.config import Config


class TestConfig:
    """Tests para Config"""

    @patch.dict('os.environ', {'API_KEY': 'test_api_key_123'})
    def test_config_loading_from_env(self):
        """Test cargar configuración desde variables de entorno"""
        config = Config()

        assert config.api_key == 'test_api_key_123'

    @patch.dict('os.environ', {
        'API_KEY': 'test_key',
        'API_HOST': 'custom.api.com',
        'MAX_RETRIES': '5',
        'RETRY_DELAY': '3',
        'REQUEST_TIMEOUT': '60',
        'RATE_LIMIT_DELAY': '2.5'
    })
    def test_config_custom_values(self):
        """Test configuración con valores personalizados"""
        config = Config()

        assert config.api_key == 'test_key'
        assert config.api_host == 'custom.api.com'
        assert config.max_retries == 5
        assert config.retry_delay == 3
        assert config.request_timeout == 60
        assert config.rate_limit_delay == 2.5

    @patch.dict('os.environ', {'API_KEY': 'test_key'})
    def test_config_default_values(self):
        """Test valores por defecto de configuración"""
        config = Config()

        assert config.api_host == "api.openwebninja.com"
        assert config.max_retries == 3
        assert config.retry_delay == 2
        assert config.request_timeout == 30
        assert config.rate_limit_delay == 1.0
        assert config.log_level == "INFO"
        assert config.log_to_file is True
        assert config.log_to_console is True

    @patch.dict('os.environ', {'API_KEY': 'test_key'})
    def test_config_path_defaults(self):
        """Test valores por defecto de paths"""
        config = Config()

        assert config.output_dir == Path("output")
        assert config.log_dir == Path("logs")

    @patch.dict('os.environ', {
        'API_KEY': 'test_key',
        'OUTPUT_DIR': 'custom_output',
        'LOG_DIR': 'custom_logs'
    })
    def test_config_custom_paths(self):
        """Test paths personalizados"""
        config = Config()

        assert config.output_dir == Path("custom_output")
        assert config.log_dir == Path("custom_logs")

    @patch.dict('os.environ', {
        'API_KEY': 'test_key',
        'LOG_LEVEL': 'DEBUG',
        'LOG_TO_FILE': 'false',
        'LOG_TO_CONSOLE': 'false'
    })
    def test_config_logging_settings(self):
        """Test configuración de logging"""
        config = Config()

        assert config.log_level == "DEBUG"
        assert config.log_to_file is False
        assert config.log_to_console is False

    def test_config_missing_api_key(self, monkeypatch):
        """Test configuración sin API key"""
        # Limpiar entorno y evitar que lea .env
        monkeypatch.delenv('API_KEY', raising=False)

        # Mock el archivo .env para que no exista
        with patch.dict('os.environ', {}, clear=True):
            # Necesitamos usar _env_file=None para evitar que lea .env
            with pytest.raises(ValidationError) as exc_info:
                Config(_env_file=None)

            # Verificar que el error es por API_KEY
            assert 'api_key' in str(exc_info.value).lower()

    @patch.dict('os.environ', {'API_KEY': 'test_key'})
    def test_validate_and_setup_creates_directories(self, tmp_path):
        """Test validate_and_setup crea directorios"""
        config = Config()
        config.output_dir = tmp_path / "output"
        config.log_dir = tmp_path / "logs"

        config.validate_and_setup()

        assert config.output_dir.exists()
        assert config.log_dir.exists()

    @patch.dict('os.environ', {'API_KEY': 'TU_API_KEY_AQUI'})
    def test_validate_and_setup_invalid_api_key(self):
        """Test validate_and_setup con API key placeholder"""
        config = Config()

        with pytest.raises(ValueError) as exc_info:
            config.validate_and_setup()

        assert "API_KEY no configurada" in str(exc_info.value)

    @patch.dict('os.environ', {'API_KEY': ''})
    def test_validate_and_setup_empty_api_key(self):
        """Test validate_and_setup con API key vacía"""
        config = Config()

        with pytest.raises(ValueError):
            config.validate_and_setup()

    @patch.dict('os.environ', {'API_KEY': 'valid_key'})
    def test_config_load_method(self, tmp_path):
        """Test método load de Config"""
        # Crear un config temporal con directorios en tmp_path
        with patch.dict('os.environ', {
            'API_KEY': 'valid_key',
            'OUTPUT_DIR': str(tmp_path / "output"),
            'LOG_DIR': str(tmp_path / "logs")
        }):
            config = Config.load()

            assert config is not None
            assert isinstance(config, Config)
            assert config.output_dir.exists()
            assert config.log_dir.exists()

    @patch.dict('os.environ', {
        'API_KEY': 'test_key',
        'MAX_RETRIES': '0'  # Fuera de rango (ge=1)
    })
    def test_config_validation_max_retries_min(self):
        """Test validación de max_retries mínimo"""
        with pytest.raises(ValidationError):
            Config()

    @patch.dict('os.environ', {
        'API_KEY': 'test_key',
        'MAX_RETRIES': '11'  # Fuera de rango (le=10)
    })
    def test_config_validation_max_retries_max(self):
        """Test validación de max_retries máximo"""
        with pytest.raises(ValidationError):
            Config()

    @patch.dict('os.environ', {
        'API_KEY': 'test_key',
        'RETRY_DELAY': '0'  # Fuera de rango (ge=1)
    })
    def test_config_validation_retry_delay_min(self):
        """Test validación de retry_delay mínimo"""
        with pytest.raises(ValidationError):
            Config()

    @patch.dict('os.environ', {
        'API_KEY': 'test_key',
        'REQUEST_TIMEOUT': '5'  # Fuera de rango (ge=10)
    })
    def test_config_validation_request_timeout_min(self):
        """Test validación de request_timeout mínimo"""
        with pytest.raises(ValidationError):
            Config()

    @patch.dict('os.environ', {
        'API_KEY': 'test_key',
        'REQUEST_TIMEOUT': '200'  # Fuera de rango (le=120)
    })
    def test_config_validation_request_timeout_max(self):
        """Test validación de request_timeout máximo"""
        with pytest.raises(ValidationError):
            Config()

    @patch.dict('os.environ', {
        'API_KEY': 'test_key',
        'RATE_LIMIT_DELAY': '0.05'  # Fuera de rango (ge=0.1)
    })
    def test_config_validation_rate_limit_delay_min(self):
        """Test validación de rate_limit_delay mínimo"""
        with pytest.raises(ValidationError):
            Config()

    @patch.dict('os.environ', {
        'API_KEY': 'test_key',
        'RATE_LIMIT_DELAY': '6.0'  # Fuera de rango (le=5.0)
    })
    def test_config_validation_rate_limit_delay_max(self):
        """Test validación de rate_limit_delay máximo"""
        with pytest.raises(ValidationError):
            Config()

    @patch.dict('os.environ', {'API_KEY': 'test_key'})
    def test_config_case_insensitive(self):
        """Test que config es case insensitive"""
        with patch.dict('os.environ', {'api_key': 'lowercase_key'}):
            config = Config()
            # Debería aceptar tanto mayúsculas como minúsculas
            assert config.api_key in ['lowercase_key', 'test_key']

    @patch.dict('os.environ', {'API_KEY': 'test_key'})
    def test_config_directories_already_exist(self, tmp_path):
        """Test validate_and_setup cuando directorios ya existen"""
        output_dir = tmp_path / "output"
        log_dir = tmp_path / "logs"

        # Crear directorios previamente
        output_dir.mkdir(parents=True)
        log_dir.mkdir(parents=True)

        config = Config()
        config.output_dir = output_dir
        config.log_dir = log_dir

        # No debería fallar si ya existen
        config.validate_and_setup()

        assert output_dir.exists()
        assert log_dir.exists()
