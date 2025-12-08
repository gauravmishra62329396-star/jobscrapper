#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: test_menu.py
Descripción: Tests para MenuSystem

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.ui.menu import MenuSystem
from src.ui.console import Console


class TestMenuSystem:
    """Tests para MenuSystem"""

    def test_menu_system_initialization(self):
        """Test inicialización de MenuSystem"""
        console = Console()
        menu = MenuSystem(console)

        assert menu.console == console

    @patch('rich.prompt.Prompt.ask')
    def test_show_main_menu(self, mock_prompt_ask):
        """Test mostrar menú principal"""
        mock_prompt_ask.return_value = "1"
        console = Console()
        menu = MenuSystem(console)

        choice = menu.show_main_menu()

        assert choice == "1"
        mock_prompt_ask.assert_called_once()

    @patch('rich.prompt.Prompt.ask')
    def test_show_main_menu_different_choices(self, mock_prompt_ask):
        """Test diferentes opciones del menú"""
        console = Console()
        menu = MenuSystem(console)

        for choice in ["0", "1", "5", "10", "13"]:
            mock_prompt_ask.return_value = choice
            result = menu.show_main_menu()
            assert result == choice

    @patch('rich.prompt.Confirm.ask')
    def test_confirm_save_yes(self, mock_confirm_ask):
        """Test confirmar guardar (sí)"""
        mock_confirm_ask.return_value = True
        console = Console()
        menu = MenuSystem(console)

        result = menu.confirm_save()

        assert result is True

    @patch('rich.prompt.Confirm.ask')
    def test_confirm_save_no(self, mock_confirm_ask):
        """Test confirmar guardar (no)"""
        mock_confirm_ask.return_value = False
        console = Console()
        menu = MenuSystem(console)

        result = menu.confirm_save()

        assert result is False

    @patch('rich.prompt.Confirm.ask')
    def test_confirm_save_custom_prompt(self, mock_confirm_ask):
        """Test confirmar con prompt personalizado"""
        mock_confirm_ask.return_value = True
        console = Console()
        menu = MenuSystem(console)

        result = menu.confirm_save("Custom prompt?")

        assert result is True
        # Verificar que se pasó el prompt personalizado
        call_args = mock_confirm_ask.call_args[0][0]
        assert "Custom prompt?" in call_args

    def test_wait_for_enter(self):
        """Test esperar ENTER"""
        console = Mock()
        console.console = Mock()
        console.console.input = Mock(return_value="")

        menu = MenuSystem(console)
        menu.wait_for_enter()

        console.console.input.assert_called_once()
