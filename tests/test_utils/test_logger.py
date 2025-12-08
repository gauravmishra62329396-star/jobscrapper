#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: test_logger.py
Descripción: Tests para logger utilities

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
import pytest
import logging
from pathlib import Path
from src.utils.logger import setup_logger, get_logger


class TestLogger:
    """Tests para funciones de logging"""

    def test_setup_logger_default(self):
        """Test setup_logger con valores por defecto"""
        logger = setup_logger(name="test_logger_default")

        assert logger is not None
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_logger_default"
        assert logger.level == logging.INFO

        # Limpiar handlers
        logger.handlers.clear()

    def test_setup_logger_custom_level(self):
        """Test setup_logger con nivel personalizado"""
        logger = setup_logger(name="test_logger_debug", level="DEBUG")

        assert logger.level == logging.DEBUG

        logger.handlers.clear()

    def test_setup_logger_critical_level(self):
        """Test setup_logger con nivel CRITICAL"""
        logger = setup_logger(name="test_logger_critical", level="CRITICAL")

        assert logger.level == logging.CRITICAL

        logger.handlers.clear()

    def test_setup_logger_with_file(self, tmp_path):
        """Test setup_logger con archivo de log"""
        log_dir = tmp_path / "logs"
        logger = setup_logger(
            name="test_logger_file",
            log_dir=log_dir,
            log_to_file=True,
            log_to_console=False
        )

        # Verificar que se creó el directorio
        assert log_dir.exists()

        # Verificar que tiene handler de archivo
        file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
        assert len(file_handlers) > 0

        logger.handlers.clear()

    def test_setup_logger_without_file(self):
        """Test setup_logger sin archivo de log"""
        logger = setup_logger(
            name="test_logger_no_file",
            log_to_file=False,
            log_to_console=True
        )

        # No debería tener FileHandler
        file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
        assert len(file_handlers) == 0

        logger.handlers.clear()

    def test_setup_logger_with_console(self):
        """Test setup_logger con salida a consola"""
        logger = setup_logger(
            name="test_logger_console",
            log_to_console=True,
            log_to_file=False
        )

        # Debería tener StreamHandler
        stream_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
        assert len(stream_handlers) > 0

        logger.handlers.clear()

    def test_setup_logger_without_console(self, tmp_path):
        """Test setup_logger sin salida a consola"""
        logger = setup_logger(
            name="test_logger_no_console",
            log_dir=tmp_path,
            log_to_console=False,
            log_to_file=True
        )

        # No debería tener StreamHandler (excepto FileHandler que también hereda de StreamHandler)
        # Verificar que no hay StreamHandler que no sea FileHandler
        stream_handlers = [
            h for h in logger.handlers
            if isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler)
        ]
        assert len(stream_handlers) == 0

        logger.handlers.clear()

    def test_setup_logger_both_outputs(self, tmp_path):
        """Test setup_logger con archivo y consola"""
        logger = setup_logger(
            name="test_logger_both",
            log_dir=tmp_path,
            log_to_file=True,
            log_to_console=True
        )

        assert len(logger.handlers) == 2

        logger.handlers.clear()

    def test_setup_logger_no_duplicate_handlers(self):
        """Test que setup_logger no duplica handlers"""
        logger_name = "test_logger_no_dup"

        logger1 = setup_logger(name=logger_name, log_to_console=True, log_to_file=False)
        handler_count_1 = len(logger1.handlers)

        # Llamar de nuevo con el mismo nombre
        logger2 = setup_logger(name=logger_name, log_to_console=True, log_to_file=False)
        handler_count_2 = len(logger2.handlers)

        # No deberían haberse agregado nuevos handlers
        assert handler_count_1 == handler_count_2
        assert logger1 is logger2

        logger1.handlers.clear()

    def test_setup_logger_creates_log_directory(self, tmp_path):
        """Test que setup_logger crea el directorio de logs"""
        log_dir = tmp_path / "new_log_dir"

        assert not log_dir.exists()

        logger = setup_logger(
            name="test_logger_create_dir",
            log_dir=log_dir,
            log_to_file=True
        )

        assert log_dir.exists()

        logger.handlers.clear()

    def test_setup_logger_file_encoding(self, tmp_path):
        """Test que el archivo de log usa UTF-8"""
        log_dir = tmp_path / "logs"
        logger = setup_logger(
            name="test_logger_encoding",
            log_dir=log_dir,
            log_to_file=True,
            log_to_console=False
        )

        # Escribir mensaje con caracteres especiales
        logger.info("Test con caracteres especiales: ñáéíóú")

        # Verificar que el archivo existe y es legible con UTF-8
        log_files = list(log_dir.glob("*.log"))
        assert len(log_files) > 0

        with open(log_files[0], 'r', encoding='utf-8') as f:
            content = f.read()
            assert "ñáéíóú" in content

        logger.handlers.clear()

    def test_get_logger(self):
        """Test get_logger obtiene logger existente"""
        # Primero crear un logger
        setup_logger(name="test_get_logger", log_to_console=True, log_to_file=False)

        # Obtenerlo con get_logger
        logger = get_logger("test_get_logger")

        assert logger is not None
        assert logger.name == "test_get_logger"

        logger.handlers.clear()

    def test_get_logger_nonexistent(self):
        """Test get_logger con logger que no existe"""
        logger = get_logger("nonexistent_logger_xyz")

        # Debería crear un logger básico
        assert logger is not None
        assert logger.name == "nonexistent_logger_xyz"

    def test_setup_logger_file_format(self, tmp_path):
        """Test formato de mensajes en archivo"""
        log_dir = tmp_path / "logs"
        logger = setup_logger(
            name="test_logger_format",
            log_dir=log_dir,
            log_to_file=True,
            log_to_console=False,
            level="INFO"
        )

        logger.info("Test message")

        log_files = list(log_dir.glob("*.log"))
        with open(log_files[0], 'r') as f:
            content = f.read()

            # Verificar formato: timestamp - name - level - message
            assert "test_logger_format" in content
            assert "INFO" in content
            assert "Test message" in content

        logger.handlers.clear()

    def test_setup_logger_filename_contains_date(self, tmp_path):
        """Test que el nombre de archivo de log contiene la fecha"""
        from datetime import datetime

        log_dir = tmp_path / "logs"
        logger = setup_logger(
            name="test_logger_date",
            log_dir=log_dir,
            log_to_file=True,
            log_to_console=False
        )

        log_files = list(log_dir.glob("*.log"))
        assert len(log_files) > 0

        # El nombre del archivo debería contener la fecha de hoy
        today = datetime.now().strftime('%Y%m%d')
        assert any(today in str(f.name) for f in log_files)

        logger.handlers.clear()

    def test_setup_logger_different_levels(self):
        """Test setup_logger con diferentes niveles de logging"""
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        expected_levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]

        for level_str, expected_level in zip(levels, expected_levels):
            logger = setup_logger(
                name=f"test_logger_{level_str.lower()}",
                level=level_str,
                log_to_console=True,
                log_to_file=False
            )

            assert logger.level == expected_level

            logger.handlers.clear()

    def test_setup_logger_console_level_is_info(self):
        """Test que el handler de consola usa nivel INFO"""
        logger = setup_logger(
            name="test_logger_console_level",
            level="DEBUG",
            log_to_console=True,
            log_to_file=False
        )

        # Buscar el StreamHandler
        stream_handlers = [
            h for h in logger.handlers
            if isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler)
        ]

        assert len(stream_handlers) > 0
        assert stream_handlers[0].level == logging.INFO

        logger.handlers.clear()

    def test_setup_logger_file_level_is_debug(self, tmp_path):
        """Test que el handler de archivo usa nivel DEBUG"""
        logger = setup_logger(
            name="test_logger_file_level",
            level="INFO",
            log_dir=tmp_path,
            log_to_file=True,
            log_to_console=False
        )

        # Buscar el FileHandler
        file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]

        assert len(file_handlers) > 0
        assert file_handlers[0].level == logging.DEBUG

        logger.handlers.clear()
