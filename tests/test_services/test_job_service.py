#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: test_job_service.py
Descripción: Tests para JobService

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
import pytest
from unittest.mock import Mock, MagicMock
from pydantic import ValidationError
from src.services.job_service import JobService
from src.models.job import Job
from src.models.search_params import SearchParameters


class TestJobService:
    """Tests para JobService"""

    def test_job_service_initialization(self):
        """Test inicialización del servicio"""
        mock_client = Mock()
        service = JobService(mock_client)

        assert service.api_client == mock_client

    def test_search_jobs_success(self, sample_job_data):
        """Test búsqueda exitosa de trabajos"""
        mock_client = Mock()
        mock_client.search_jobs.return_value = [
            sample_job_data,
            sample_job_data.copy()
        ]

        service = JobService(mock_client)
        params = SearchParameters(query="python", country="us")

        jobs = service.search_jobs(params)

        assert len(jobs) == 2
        assert all(isinstance(job, Job) for job in jobs)
        mock_client.search_jobs.assert_called_once_with(params)

    def test_search_jobs_empty_results(self):
        """Test búsqueda sin resultados"""
        mock_client = Mock()
        mock_client.search_jobs.return_value = []

        service = JobService(mock_client)
        params = SearchParameters(query="nonexistent", country="us")

        jobs = service.search_jobs(params)

        assert jobs == []

    def test_search_jobs_with_invalid_data(self, sample_job_data):
        """Test búsqueda con datos inválidos (algunos trabajos fallan validación)"""
        mock_client = Mock()

        # Un trabajo válido y uno inválido
        invalid_job = {"invalid": "data"}  # Falta job_id requerido
        mock_client.search_jobs.return_value = [
            sample_job_data,
            invalid_job,
            sample_job_data.copy()
        ]

        service = JobService(mock_client)
        params = SearchParameters(query="python", country="us")

        jobs = service.search_jobs(params)

        # Solo deberían parsearse los 2 trabajos válidos
        assert len(jobs) == 2
        assert all(isinstance(job, Job) for job in jobs)

    def test_search_jobs_api_error(self):
        """Test búsqueda con error de API"""
        mock_client = Mock()
        mock_client.search_jobs.side_effect = Exception("API Error")

        service = JobService(mock_client)
        params = SearchParameters(query="python", country="us")

        with pytest.raises(Exception) as exc_info:
            service.search_jobs(params)

        assert "API Error" in str(exc_info.value)

    def test_get_job_details_success(self, sample_job_data):
        """Test obtener detalles de trabajo exitoso"""
        mock_client = Mock()
        mock_client.get_job_details.return_value = sample_job_data

        service = JobService(mock_client)
        job = service.get_job_details("abc123", "us")

        assert isinstance(job, Job)
        assert job.job_id == "abc123xyz"
        mock_client.get_job_details.assert_called_once_with("abc123", "us")

    def test_get_job_details_with_country(self, sample_job_data):
        """Test obtener detalles con país específico"""
        mock_client = Mock()
        mock_client.get_job_details.return_value = sample_job_data

        service = JobService(mock_client)
        job = service.get_job_details("abc123", "es")

        mock_client.get_job_details.assert_called_once_with("abc123", "es")

    def test_get_job_details_validation_error(self):
        """Test obtener detalles con datos inválidos"""
        mock_client = Mock()
        mock_client.get_job_details.return_value = {"invalid": "data"}

        service = JobService(mock_client)

        with pytest.raises(ValueError) as exc_info:
            service.get_job_details("invalid", "us")

        assert "inválidos" in str(exc_info.value)

    def test_get_job_details_api_error(self):
        """Test obtener detalles con error de API"""
        mock_client = Mock()
        mock_client.get_job_details.side_effect = Exception("Not found")

        service = JobService(mock_client)

        with pytest.raises(Exception) as exc_info:
            service.get_job_details("notfound", "us")

        assert "Not found" in str(exc_info.value)

    def test_filter_remote_jobs(self, sample_job_data):
        """Test filtrar trabajos remotos"""
        # Crear trabajos remotos y no remotos
        remote_job_data = sample_job_data.copy()
        remote_job_data["job_is_remote"] = True

        non_remote_job_data = sample_job_data.copy()
        non_remote_job_data["job_is_remote"] = False
        non_remote_job_data["job_id"] = "different123"

        jobs = [
            Job.model_validate(remote_job_data),
            Job.model_validate(non_remote_job_data),
            Job.model_validate(remote_job_data)
        ]

        mock_client = Mock()
        service = JobService(mock_client)

        remote_jobs = service.filter_remote_jobs(jobs)

        assert len(remote_jobs) == 2
        assert all(job.is_remote for job in remote_jobs)

    def test_filter_remote_jobs_empty_list(self):
        """Test filtrar trabajos remotos con lista vacía"""
        mock_client = Mock()
        service = JobService(mock_client)

        remote_jobs = service.filter_remote_jobs([])

        assert remote_jobs == []

    def test_filter_remote_jobs_no_remote(self, sample_job_data):
        """Test filtrar cuando no hay trabajos remotos"""
        non_remote_job_data = sample_job_data.copy()
        non_remote_job_data["job_is_remote"] = False

        jobs = [Job.model_validate(non_remote_job_data)]

        mock_client = Mock()
        service = JobService(mock_client)

        remote_jobs = service.filter_remote_jobs(jobs)

        assert remote_jobs == []

    def test_filter_by_salary(self, sample_job_data):
        """Test filtrar por salario mínimo"""
        # Crear trabajos con diferentes salarios
        high_salary_data = sample_job_data.copy()
        high_salary_data["job_min_salary"] = 80000
        high_salary_data["job_id"] = "high123"

        low_salary_data = sample_job_data.copy()
        low_salary_data["job_min_salary"] = 30000
        low_salary_data["job_id"] = "low123"

        jobs = [
            Job.model_validate(high_salary_data),
            Job.model_validate(low_salary_data),
            Job.model_validate(sample_job_data)  # 40000
        ]

        mock_client = Mock()
        service = JobService(mock_client)

        filtered = service.filter_by_salary(jobs, 40000, "EUR")

        assert len(filtered) == 2
        assert all(job.min_salary >= 40000 for job in filtered)

    def test_filter_by_salary_different_currency(self, sample_job_data):
        """Test filtrar por salario con diferente moneda"""
        usd_job_data = sample_job_data.copy()
        usd_job_data["job_salary_currency"] = "USD"
        usd_job_data["job_min_salary"] = 50000

        jobs = [
            Job.model_validate(sample_job_data),  # EUR
            Job.model_validate(usd_job_data)     # USD
        ]

        mock_client = Mock()
        service = JobService(mock_client)

        # Filtrar solo EUR
        filtered = service.filter_by_salary(jobs, 30000, "EUR")

        assert len(filtered) == 1
        assert filtered[0].salary_currency == "EUR"

    def test_filter_by_salary_no_salary_info(self, sample_job_data):
        """Test filtrar cuando trabajos no tienen info salarial"""
        no_salary_data = sample_job_data.copy()
        no_salary_data["job_min_salary"] = None
        no_salary_data["job_max_salary"] = None

        jobs = [Job.model_validate(no_salary_data)]

        mock_client = Mock()
        service = JobService(mock_client)

        filtered = service.filter_by_salary(jobs, 30000, "EUR")

        assert filtered == []

    def test_filter_by_salary_empty_list(self):
        """Test filtrar por salario con lista vacía"""
        mock_client = Mock()
        service = JobService(mock_client)

        filtered = service.filter_by_salary([], 50000, "USD")

        assert filtered == []

    def test_sort_by_salary_descending(self, sample_job_data):
        """Test ordenar por salario descendente"""
        # Crear trabajos con diferentes salarios
        low_job = sample_job_data.copy()
        low_job["job_max_salary"] = 40000
        low_job["job_id"] = "low"

        mid_job = sample_job_data.copy()
        mid_job["job_max_salary"] = 60000
        mid_job["job_id"] = "mid"

        high_job = sample_job_data.copy()
        high_job["job_max_salary"] = 80000
        high_job["job_id"] = "high"

        jobs = [
            Job.model_validate(mid_job),
            Job.model_validate(low_job),
            Job.model_validate(high_job)
        ]

        mock_client = Mock()
        service = JobService(mock_client)

        sorted_jobs = service.sort_by_salary(jobs, descending=True)

        assert sorted_jobs[0].job_id == "high"
        assert sorted_jobs[1].job_id == "mid"
        assert sorted_jobs[2].job_id == "low"

    def test_sort_by_salary_ascending(self, sample_job_data):
        """Test ordenar por salario ascendente"""
        low_job = sample_job_data.copy()
        low_job["job_max_salary"] = 40000
        low_job["job_id"] = "low"

        high_job = sample_job_data.copy()
        high_job["job_max_salary"] = 80000
        high_job["job_id"] = "high"

        jobs = [
            Job.model_validate(high_job),
            Job.model_validate(low_job)
        ]

        mock_client = Mock()
        service = JobService(mock_client)

        sorted_jobs = service.sort_by_salary(jobs, descending=False)

        assert sorted_jobs[0].job_id == "low"
        assert sorted_jobs[1].job_id == "high"

    def test_sort_by_salary_uses_min_when_no_max(self, sample_job_data):
        """Test ordenar usa min_salary cuando no hay max_salary"""
        only_min_job = sample_job_data.copy()
        only_min_job["job_max_salary"] = None
        only_min_job["job_min_salary"] = 50000
        only_min_job["job_id"] = "min_only"

        with_max_job = sample_job_data.copy()
        with_max_job["job_max_salary"] = 60000
        with_max_job["job_id"] = "with_max"

        jobs = [
            Job.model_validate(only_min_job),
            Job.model_validate(with_max_job)
        ]

        mock_client = Mock()
        service = JobService(mock_client)

        sorted_jobs = service.sort_by_salary(jobs, descending=True)

        # with_max (60000) debería estar primero
        assert sorted_jobs[0].job_id == "with_max"

    def test_sort_by_salary_no_salary_info(self, sample_job_data):
        """Test ordenar cuando trabajos no tienen info salarial"""
        no_salary_job = sample_job_data.copy()
        no_salary_job["job_min_salary"] = None
        no_salary_job["job_max_salary"] = None
        no_salary_job["job_id"] = "no_salary"

        with_salary_job = sample_job_data.copy()
        with_salary_job["job_id"] = "with_salary"

        jobs = [
            Job.model_validate(no_salary_job),
            Job.model_validate(with_salary_job)
        ]

        mock_client = Mock()
        service = JobService(mock_client)

        sorted_jobs = service.sort_by_salary(jobs, descending=True)

        # El trabajo con salario debería estar primero
        assert sorted_jobs[0].job_id == "with_salary"
        assert sorted_jobs[1].job_id == "no_salary"

    def test_sort_by_salary_empty_list(self):
        """Test ordenar lista vacía"""
        mock_client = Mock()
        service = JobService(mock_client)

        sorted_jobs = service.sort_by_salary([])

        assert sorted_jobs == []
