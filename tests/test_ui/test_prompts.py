#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: test_prompts.py
Descripción: Tests para Prompts interactivos

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.ui.prompts import Prompts
from src.ui.console import Console
from src.models.search_params import SearchParameters


class TestPrompts:
    """Tests para Prompts"""

    def test_prompts_initialization(self):
        """Test inicialización de Prompts"""
        console = Console()
        prompts = Prompts(console)

        assert prompts.console == console

    @patch('rich.prompt.IntPrompt.ask')
    @patch('rich.prompt.Confirm.ask')
    @patch('rich.prompt.Prompt.ask')
    def test_get_custom_search_params(self, mock_prompt, mock_confirm, mock_int_prompt):
        """Test obtener parámetros personalizados"""
        mock_prompt.side_effect = ["python developer", "us", "1", ""]
        mock_confirm.return_value = False
        mock_int_prompt.return_value = 1

        console = Console()
        prompts = Prompts(console)

        params = prompts.get_custom_search_params()

        assert isinstance(params, SearchParameters)
        assert params.query == "python developer"
        assert params.country == "us"
        assert params.num_pages == 1

    @patch('rich.prompt.IntPrompt.ask')
    @patch('rich.prompt.Confirm.ask')
    @patch('rich.prompt.Prompt.ask')
    def test_get_custom_search_params_with_remote(self, mock_prompt, mock_confirm, mock_int_prompt):
        """Test parámetros con trabajo remoto"""
        mock_prompt.side_effect = ["developer", "es", "2", "FULLTIME"]
        mock_confirm.return_value = True
        mock_int_prompt.return_value = 2

        console = Console()
        prompts = Prompts(console)

        params = prompts.get_custom_search_params()

        assert params.work_from_home is True
        assert params.employment_types == "FULLTIME"

    @patch('rich.prompt.IntPrompt.ask')
    @patch('rich.prompt.Confirm.ask')
    @patch('rich.prompt.Prompt.ask')
    def test_get_custom_search_params_different_periods(self, mock_prompt, mock_confirm, mock_int_prompt):
        """Test diferentes períodos de publicación"""
        console = Console()
        prompts = Prompts(console)

        period_map = {
            "1": "all",
            "2": "today",
            "3": "3days",
            "4": "week",
            "5": "month"
        }

        for choice, expected_period in period_map.items():
            mock_prompt.side_effect = ["test", "us", choice, ""]
            mock_confirm.return_value = False
            mock_int_prompt.return_value = 1

            params = prompts.get_custom_search_params()
            assert params.date_posted == expected_period

    @patch('rich.prompt.IntPrompt.ask')
    @patch('rich.prompt.Confirm.ask')
    @patch('rich.prompt.Prompt.ask')
    def test_get_custom_search_params_max_pages(self, mock_prompt, mock_confirm, mock_int_prompt):
        """Test límite de páginas"""
        mock_prompt.side_effect = ["test", "us", "1", ""]
        mock_confirm.return_value = False
        mock_int_prompt.return_value = 15  # Más del máximo

        console = Console()
        prompts = Prompts(console)

        params = prompts.get_custom_search_params()

        # Debería limitarse a 10
        assert params.num_pages == 10

    @patch('rich.prompt.Prompt.ask')
    def test_get_job_id_input(self, mock_prompt):
        """Test obtener job ID"""
        mock_prompt.side_effect = ["abc123", "us"]

        console = Console()
        prompts = Prompts(console)

        job_id, country = prompts.get_job_id_input()

        assert job_id == "abc123"
        assert country == "us"

    @patch('rich.prompt.Prompt.ask')
    def test_get_job_id_input_default_country(self, mock_prompt):
        """Test job ID con país por defecto"""
        mock_prompt.side_effect = ["xyz789", "us"]

        console = Console()
        prompts = Prompts(console)

        job_id, country = prompts.get_job_id_input()

        assert country == "us"

    @patch('rich.prompt.Prompt.ask')
    def test_get_salary_estimate_params(self, mock_prompt):
        """Test obtener parámetros de estimación salarial"""
        mock_prompt.side_effect = ["Software Engineer", "Madrid, Spain", "1"]

        console = Console()
        prompts = Prompts(console)

        params = prompts.get_salary_estimate_params()

        assert params["job_title"] == "Software Engineer"
        assert params["location"] == "Madrid, Spain"
        assert params["years_of_experience"] == "ALL"

    @patch('rich.prompt.Prompt.ask')
    def test_get_salary_estimate_params_different_experience(self, mock_prompt):
        """Test estimación con diferentes niveles de experiencia"""
        console = Console()
        prompts = Prompts(console)

        experience_map = {
            "1": "ALL",
            "2": "LESS_THAN_ONE",
            "3": "ONE_TO_THREE",
            "4": "FOUR_TO_SIX",
            "5": "SEVEN_TO_NINE",
            "6": "TEN_AND_ABOVE"
        }

        for choice, expected in experience_map.items():
            mock_prompt.side_effect = ["Engineer", "Madrid", choice]
            params = prompts.get_salary_estimate_params()
            assert params["years_of_experience"] == expected

    @patch('rich.prompt.Prompt.ask')
    def test_get_company_salary_params(self, mock_prompt):
        """Test obtener parámetros de salario de empresa"""
        mock_prompt.side_effect = ["Google", "Engineer", "Mountain View", "1"]

        console = Console()
        prompts = Prompts(console)

        params = prompts.get_company_salary_params()

        assert params["company"] == "Google"
        assert params["job_title"] == "Engineer"
        assert params["location"] == "Mountain View"
        assert params["years_of_experience"] == "ALL"

    @patch('rich.prompt.Prompt.ask')
    def test_get_company_salary_params_without_location(self, mock_prompt):
        """Test salario de empresa sin ubicación"""
        mock_prompt.side_effect = ["Amazon", "Developer", "", "1"]

        console = Console()
        prompts = Prompts(console)

        params = prompts.get_company_salary_params()

        assert params["location"] is None

    @patch('rich.prompt.Confirm.ask')
    def test_confirm_save(self, mock_confirm):
        """Test confirmar guardar"""
        mock_confirm.return_value = True

        console = Console()
        prompts = Prompts(console)

        result = prompts.confirm_save()

        assert result is True

    @patch('rich.prompt.Confirm.ask')
    def test_confirm_save_custom_prompt(self, mock_confirm):
        """Test confirmar con prompt personalizado"""
        mock_confirm.return_value = False

        console = Console()
        prompts = Prompts(console)

        result = prompts.confirm_save("Custom question?")

        assert result is False
        call_args = mock_confirm.call_args[0][0]
        assert "Custom question?" in call_args

    @patch('rich.prompt.Prompt.ask')
    def test_get_experience_level(self, mock_prompt):
        """Test obtener nivel de experiencia"""
        mock_prompt.return_value = "3"

        console = Console()
        prompts = Prompts(console)

        # Método privado pero lo probamos indirectamente
        experience = prompts._get_experience_level()

        assert experience == "ONE_TO_THREE"

    @patch('rich.prompt.IntPrompt.ask')
    @patch('rich.prompt.Confirm.ask')
    @patch('rich.prompt.Prompt.ask')
    def test_get_custom_search_params_min_pages(self, mock_prompt, mock_confirm, mock_int_prompt):
        """Test límite mínimo de páginas"""
        mock_prompt.side_effect = ["test", "us", "1", ""]
        mock_confirm.return_value = False
        mock_int_prompt.return_value = 0  # Menos del mínimo

        console = Console()
        prompts = Prompts(console)

        params = prompts.get_custom_search_params()

        # Debería limitarse a 1
        assert params.num_pages == 1

    @patch('rich.prompt.IntPrompt.ask')
    @patch('rich.prompt.Confirm.ask')
    @patch('rich.prompt.Prompt.ask')
    def test_get_custom_search_params_empty_employment_types(self, mock_prompt, mock_confirm, mock_int_prompt):
        """Test sin tipos de empleo especificados"""
        mock_prompt.side_effect = ["test", "us", "1", ""]
        mock_confirm.return_value = False
        mock_int_prompt.return_value = 1

        console = Console()
        prompts = Prompts(console)

        params = prompts.get_custom_search_params()

        # employment_types vacío debería ser None
        assert params.employment_types is None


@patch('rich.prompt.IntPrompt.ask', return_value=1)
@patch('rich.prompt.Confirm.ask', return_value=False)
@patch('rich.prompt.Prompt.ask')
def test_get_custom_search_params_validation_error(mock_prompt, mock_confirm, mock_int_prompt):
    """Test get_custom_search_params con error de validación"""
    # Configurar mocks para que retornen un query inválido
    mock_prompt.side_effect = ["", "es", "1", ""]  # Query vacío debería fallar
    mock_int_prompt.return_value = 1

    console = Console()
    prompts = Prompts(console)

    # Debería lanzar ValidationError que se propaga
    with pytest.raises(Exception):  # ValidationError se propaga como Exception
        prompts.get_custom_search_params()
