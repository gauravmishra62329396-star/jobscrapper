#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: test_console.py
Descripción: Tests para Console wrapper

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.ui.console import Console


class TestConsole:
    """Tests para Console"""

    def test_console_initialization(self):
        """Test inicialización de Console"""
        console = Console()

        assert console.console is not None

    @patch('src.ui.console.RichConsole')
    def test_print_success(self, mock_rich_console):
        """Test print_success"""
        mock_console_instance = Mock()
        mock_rich_console.return_value = mock_console_instance

        console = Console()
        console.print_success("Test message")

        mock_console_instance.print.assert_called_once()
        call_args = mock_console_instance.print.call_args[0][0]
        assert "[success]" in call_args
        assert "Test message" in call_args

    @patch('src.ui.console.RichConsole')
    def test_print_error(self, mock_rich_console):
        """Test print_error"""
        mock_console_instance = Mock()
        mock_rich_console.return_value = mock_console_instance

        console = Console()
        console.print_error("Error message")

        mock_console_instance.print.assert_called_once()
        call_args = mock_console_instance.print.call_args[0][0]
        assert "[error]" in call_args
        assert "Error message" in call_args

    @patch('src.ui.console.RichConsole')
    def test_print_warning(self, mock_rich_console):
        """Test print_warning"""
        mock_console_instance = Mock()
        mock_rich_console.return_value = mock_console_instance

        console = Console()
        console.print_warning("Warning message")

        mock_console_instance.print.assert_called_once()
        call_args = mock_console_instance.print.call_args[0][0]
        assert "[warning]" in call_args
        assert "Warning message" in call_args

    @patch('src.ui.console.RichConsole')
    def test_print_info(self, mock_rich_console):
        """Test print_info"""
        mock_console_instance = Mock()
        mock_rich_console.return_value = mock_console_instance

        console = Console()
        console.print_info("Info message")

        mock_console_instance.print.assert_called_once()
        call_args = mock_console_instance.print.call_args[0][0]
        assert "[info]" in call_args
        assert "Info message" in call_args

    @patch('src.ui.console.RichConsole')
    def test_print_header(self, mock_rich_console):
        """Test print_header"""
        mock_console_instance = Mock()
        mock_rich_console.return_value = mock_console_instance

        console = Console()
        console.print_header("Test Header")

        mock_console_instance.rule.assert_called_once()

    @patch('src.ui.console.RichConsole')
    def test_print_separator(self, mock_rich_console):
        """Test print_separator"""
        mock_console_instance = Mock()
        mock_rich_console.return_value = mock_console_instance

        console = Console()
        console.print_separator()

        mock_console_instance.print.assert_called_once()
        call_args = mock_console_instance.print.call_args[0][0]
        assert "─" in call_args

    @patch('src.ui.console.RichConsole')
    def test_print(self, mock_rich_console):
        """Test print genérico"""
        mock_console_instance = Mock()
        mock_rich_console.return_value = mock_console_instance

        console = Console()
        console.print("Test message", style="bold")

        mock_console_instance.print.assert_called_once_with("Test message", style="bold")

    @patch('src.ui.console.RichConsole')
    def test_clear(self, mock_rich_console):
        """Test clear console"""
        mock_console_instance = Mock()
        mock_rich_console.return_value = mock_console_instance

        console = Console()
        console.clear()

        mock_console_instance.clear.assert_called_once()
