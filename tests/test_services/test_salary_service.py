#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: test_salary_service.py
Descripción: Tests para SalaryService

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
import pytest
from unittest.mock import Mock, patch
from pydantic import ValidationError
from src.services.salary_service import SalaryService
from src.models.salary import SalaryInfo


class TestSalaryService:
    """Tests para SalaryService"""

    def test_salary_service_initialization(self):
        """Test inicialización del servicio"""
        mock_client = Mock()
        service = SalaryService(mock_client)

        assert service.api_client == mock_client

    def test_get_estimated_salary_success(self, sample_salary_data):
        """Test obtener estimación salarial exitosa"""
        mock_client = Mock()
        mock_client.get_estimated_salary.return_value = [
            sample_salary_data,
            sample_salary_data.copy()
        ]

        service = SalaryService(mock_client)
        salaries = service.get_estimated_salary("Software Engineer", "Madrid, Spain")

        assert len(salaries) == 2
        assert all(isinstance(sal, SalaryInfo) for sal in salaries)
        mock_client.get_estimated_salary.assert_called_once()

    def test_get_estimated_salary_with_experience(self, sample_salary_data):
        """Test estimación salarial con nivel de experiencia"""
        mock_client = Mock()
        mock_client.get_estimated_salary.return_value = [sample_salary_data]

        service = SalaryService(mock_client)
        salaries = service.get_estimated_salary(
            "Developer",
            "Madrid",
            years_of_experience="FIVE_TO_SEVEN"
        )

        call_args = mock_client.get_estimated_salary.call_args
        assert call_args[1]["years_of_experience"] == "FIVE_TO_SEVEN"

    def test_get_estimated_salary_empty_results(self):
        """Test estimación salarial sin resultados"""
        mock_client = Mock()
        mock_client.get_estimated_salary.return_value = []

        service = SalaryService(mock_client)
        salaries = service.get_estimated_salary("Rare Job", "Location")

        assert salaries == []

    def test_get_estimated_salary_filters_no_data(self, sample_salary_data):
        """Test estimación salarial filtra salarios sin datos"""
        # Salario con datos
        valid_salary = sample_salary_data.copy()

        # Salario sin datos
        invalid_salary = {
            "job_title": "Test",
            "location": "Test",
            "min_salary": None,
            "max_salary": None,
            "median_salary": None
        }

        mock_client = Mock()
        mock_client.get_estimated_salary.return_value = [
            valid_salary,
            invalid_salary,
            valid_salary.copy()
        ]

        service = SalaryService(mock_client)
        salaries = service.get_estimated_salary("Developer", "Madrid")

        # Solo deberían incluirse los 2 salarios válidos
        assert len(salaries) == 2

    @patch('src.services.salary_service.logger')
    def test_get_estimated_salary_with_invalid_data(self, mock_logger, sample_salary_data):
        """Test estimación salarial con datos inválidos (se ignoran)"""
        mock_client = Mock()
        mock_client.get_estimated_salary.return_value = [
            sample_salary_data,
            {"min_salary": "not_a_number"},  # Tipo incorrecto causa ValidationError
            sample_salary_data.copy()
        ]

        service = SalaryService(mock_client)
        salaries = service.get_estimated_salary("Developer", "Madrid")

        # Solo los 2 válidos deberían parsearse
        assert len(salaries) == 2
        # Verificar que se llamó logger.warning para el dato inválido
        assert mock_logger.warning.called

    def test_get_estimated_salary_api_error(self):
        """Test estimación salarial con error de API"""
        mock_client = Mock()
        mock_client.get_estimated_salary.side_effect = Exception("API Error")

        service = SalaryService(mock_client)

        with pytest.raises(Exception) as exc_info:
            service.get_estimated_salary("Developer", "Madrid")

        assert "API Error" in str(exc_info.value)

    def test_get_company_salary_success(self, sample_salary_data):
        """Test obtener salarios de empresa exitoso"""
        mock_client = Mock()
        mock_client.get_company_salary.return_value = [sample_salary_data]

        service = SalaryService(mock_client)
        salaries = service.get_company_salary("Google", "Software Engineer")

        assert len(salaries) == 1
        assert isinstance(salaries[0], SalaryInfo)
        mock_client.get_company_salary.assert_called_once()

    def test_get_company_salary_with_all_params(self, sample_salary_data):
        """Test salarios de empresa con todos los parámetros"""
        mock_client = Mock()
        mock_client.get_company_salary.return_value = [sample_salary_data]

        service = SalaryService(mock_client)
        salaries = service.get_company_salary(
            "Google",
            "Engineer",
            location="Mountain View",
            years_of_experience="FIVE_TO_SEVEN"
        )

        call_args = mock_client.get_company_salary.call_args
        assert call_args[1]["company"] == "Google"
        assert call_args[1]["location"] == "Mountain View"
        assert call_args[1]["years_of_experience"] == "FIVE_TO_SEVEN"

    def test_get_company_salary_without_location(self, sample_salary_data):
        """Test salarios de empresa sin ubicación"""
        mock_client = Mock()
        mock_client.get_company_salary.return_value = [sample_salary_data]

        service = SalaryService(mock_client)
        salaries = service.get_company_salary("Google", "Engineer", location=None)

        call_args = mock_client.get_company_salary.call_args
        assert call_args[1]["location"] is None

    def test_get_company_salary_filters_no_data(self, sample_salary_data):
        """Test salarios de empresa filtra salarios sin datos"""
        valid_salary = sample_salary_data.copy()
        invalid_salary = {
            "job_title": "Test",
            "min_salary": None,
            "max_salary": None,
            "median_salary": None
        }

        mock_client = Mock()
        mock_client.get_company_salary.return_value = [
            valid_salary,
            invalid_salary
        ]

        service = SalaryService(mock_client)
        salaries = service.get_company_salary("Google", "Engineer")

        assert len(salaries) == 1

    @patch('src.services.salary_service.logger')
    def test_get_company_salary_with_invalid_data(self, mock_logger, sample_salary_data):
        """Test salarios de empresa con datos inválidos"""
        mock_client = Mock()
        mock_client.get_company_salary.return_value = [
            sample_salary_data,
            {"median_salary": "invalid_string"},  # Tipo incorrecto causa ValidationError
            sample_salary_data.copy()
        ]

        service = SalaryService(mock_client)
        salaries = service.get_company_salary("Google", "Engineer")

        assert len(salaries) == 2
        # Verificar que se llamó logger.warning para el dato inválido
        assert mock_logger.warning.called

    def test_get_company_salary_empty_results(self):
        """Test salarios de empresa sin resultados"""
        mock_client = Mock()
        mock_client.get_company_salary.return_value = []

        service = SalaryService(mock_client)
        salaries = service.get_company_salary("Nonexistent", "Job")

        assert salaries == []

    def test_get_company_salary_api_error(self):
        """Test salarios de empresa con error de API"""
        mock_client = Mock()
        mock_client.get_company_salary.side_effect = Exception("Not found")

        service = SalaryService(mock_client)

        with pytest.raises(Exception) as exc_info:
            service.get_company_salary("Nonexistent", "Job")

        assert "Not found" in str(exc_info.value)

    def test_compare_locations_success(self, sample_salary_data):
        """Test comparar salarios entre ubicaciones"""
        madrid_salary = sample_salary_data.copy()
        madrid_salary["median_salary"] = 50000

        barcelona_salary = sample_salary_data.copy()
        barcelona_salary["median_salary"] = 55000

        mock_client = Mock()

        def mock_get_salary(job_title, location, years_of_experience):
            if "Madrid" in location:
                return [SalaryInfo.model_validate(madrid_salary)]
            elif "Barcelona" in location:
                return [SalaryInfo.model_validate(barcelona_salary)]
            return []

        service = SalaryService(mock_client)
        service.get_estimated_salary = mock_get_salary

        comparison = service.compare_locations(
            "Developer",
            ["Madrid", "Barcelona"],
            "ALL"
        )

        assert len(comparison) == 2
        assert "Madrid" in comparison
        assert "Barcelona" in comparison
        assert comparison["Madrid"]["count"] == 1
        assert comparison["Madrid"]["average_median"] == 50000
        assert comparison["Barcelona"]["average_median"] == 55000

    def test_compare_locations_with_multiple_salaries(self, sample_salary_data):
        """Test comparar ubicaciones con múltiples salarios por ubicación"""
        salary1 = sample_salary_data.copy()
        salary1["median_salary"] = 40000

        salary2 = sample_salary_data.copy()
        salary2["median_salary"] = 60000

        mock_client = Mock()

        def mock_get_salary(job_title, location, years_of_experience):
            return [
                SalaryInfo.model_validate(salary1),
                SalaryInfo.model_validate(salary2)
            ]

        service = SalaryService(mock_client)
        service.get_estimated_salary = mock_get_salary

        comparison = service.compare_locations("Developer", ["Madrid"], "ALL")

        assert comparison["Madrid"]["count"] == 2
        assert comparison["Madrid"]["average_median"] == 50000  # (40000 + 60000) / 2

    def test_compare_locations_empty_results(self):
        """Test comparar ubicaciones sin resultados"""
        mock_client = Mock()

        service = SalaryService(mock_client)
        service.get_estimated_salary = Mock(return_value=[])

        comparison = service.compare_locations("Developer", ["Location"], "ALL")

        assert comparison == {}

    def test_compare_locations_with_no_median(self, sample_salary_data):
        """Test comparar ubicaciones cuando salarios no tienen mediana"""
        no_median_salary = sample_salary_data.copy()
        no_median_salary["median_salary"] = None

        mock_client = Mock()

        service = SalaryService(mock_client)
        service.get_estimated_salary = Mock(
            return_value=[SalaryInfo.model_validate(no_median_salary)]
        )

        comparison = service.compare_locations("Developer", ["Madrid"], "ALL")

        assert comparison["Madrid"]["count"] == 1
        assert comparison["Madrid"]["average_median"] is None

    def test_compare_locations_handles_errors(self, sample_salary_data):
        """Test comparar ubicaciones maneja errores individualmente"""
        mock_client = Mock()

        def mock_get_salary(job_title, location, years_of_experience):
            if "Madrid" in location:
                return [SalaryInfo.model_validate(sample_salary_data)]
            elif "Error" in location:
                raise Exception("API Error")
            return []

        service = SalaryService(mock_client)
        service.get_estimated_salary = mock_get_salary

        comparison = service.compare_locations(
            "Developer",
            ["Madrid", "Error Location", "No Results"],
            "ALL"
        )

        # Solo Madrid debería estar en el resultado
        assert len(comparison) == 1
        assert "Madrid" in comparison

    def test_compare_locations_empty_location_list(self):
        """Test comparar con lista vacía de ubicaciones"""
        mock_client = Mock()
        service = SalaryService(mock_client)

        comparison = service.compare_locations("Developer", [], "ALL")

        assert comparison == {}

    def test_compare_locations_includes_salary_objects(self, sample_salary_data):
        """Test comparar ubicaciones incluye objetos SalaryInfo"""
        mock_client = Mock()

        service = SalaryService(mock_client)
        service.get_estimated_salary = Mock(
            return_value=[SalaryInfo.model_validate(sample_salary_data)]
        )

        comparison = service.compare_locations("Developer", ["Madrid"], "ALL")

        assert "salaries" in comparison["Madrid"]
        assert isinstance(comparison["Madrid"]["salaries"][0], SalaryInfo)
