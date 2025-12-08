#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: test_jsearch_client.py
Descripción: Tests para JSearchClient

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.api.jsearch_client import JSearchClient
from src.api.client import HTTPError
from src.models.search_params import SearchParameters


class TestJSearchClient:
    """Tests para JSearchClient"""

    def test_jsearch_client_initialization(self):
        """Test inicialización del cliente"""
        client = JSearchClient(api_key="test_key", api_host="test.api.com")

        assert client.api_key == "test_key"
        assert client.api_host == "test.api.com"
        assert client.client is not None
        assert client.rate_limiter is not None

    def test_jsearch_client_initialization_with_config(self):
        """Test inicialización con config"""
        mock_config = Mock()
        mock_config.request_timeout = 60
        mock_config.rate_limit_delay = 2.0
        mock_config.max_retries = 5
        mock_config.retry_delay = 3

        client = JSearchClient(api_key="test_key", config=mock_config)

        assert client.client.timeout == 60
        assert client.rate_limiter.delay == 2.0
        assert client.rate_limiter.max_retries == 5
        assert client.rate_limiter.retry_delay == 3

    def test_jsearch_client_default_config(self):
        """Test inicialización sin config"""
        client = JSearchClient(api_key="test_key")

        assert client.client.timeout == 30
        assert client.rate_limiter.delay == 1.0
        assert client.rate_limiter.max_retries == 3

    @patch('src.api.jsearch_client.RateLimiter')
    @patch('src.api.jsearch_client.HTTPClient')
    def test_search_jobs_success(self, mock_http_client, mock_rate_limiter):
        """Test búsqueda exitosa de trabajos"""
        # Mock del cliente HTTP
        mock_client_instance = Mock()
        mock_client_instance.get.return_value = {
            "data": [
                {"job_id": "1", "job_title": "Developer"},
                {"job_id": "2", "job_title": "Engineer"}
            ]
        }
        mock_http_client.return_value = mock_client_instance

        # Mock del rate limiter
        mock_limiter_instance = Mock()
        mock_limiter_instance.with_retry = lambda f: f
        mock_rate_limiter.return_value = mock_limiter_instance

        client = JSearchClient(api_key="test_key")
        params = SearchParameters(query="python", country="us")

        jobs = client.search_jobs(params)

        assert len(jobs) == 2
        assert jobs[0]["job_id"] == "1"
        assert jobs[1]["job_title"] == "Engineer"

    @patch('src.api.jsearch_client.RateLimiter')
    @patch('src.api.jsearch_client.HTTPClient')
    def test_search_jobs_with_error_in_response(self, mock_http_client, mock_rate_limiter):
        """Test búsqueda con error en respuesta"""
        mock_client_instance = Mock()
        mock_client_instance.get.return_value = {
            "error": "Invalid API key"
        }
        mock_http_client.return_value = mock_client_instance

        mock_limiter_instance = Mock()
        mock_limiter_instance.with_retry = lambda f: f
        mock_rate_limiter.return_value = mock_limiter_instance

        client = JSearchClient(api_key="test_key")
        params = SearchParameters(query="python", country="us")

        with pytest.raises(HTTPError) as exc_info:
            client.search_jobs(params)

        assert exc_info.value.status_code == 400

    @patch('src.api.jsearch_client.RateLimiter')
    @patch('src.api.jsearch_client.HTTPClient')
    def test_search_jobs_rate_limit_error(self, mock_http_client, mock_rate_limiter):
        """Test búsqueda con error de rate limit"""
        mock_client_instance = Mock()
        mock_http_client.return_value = mock_client_instance

        # Simular error 429
        def mock_with_retry(func):
            def wrapper(*args, **kwargs):
                raise HTTPError(429, "Rate limit exceeded")
            return wrapper

        mock_limiter_instance = Mock()
        mock_limiter_instance.with_retry = mock_with_retry
        mock_rate_limiter.return_value = mock_limiter_instance

        client = JSearchClient(api_key="test_key")
        params = SearchParameters(query="python", country="us")

        with pytest.raises(HTTPError) as exc_info:
            client.search_jobs(params)

        assert exc_info.value.status_code == 429
        assert "Rate limit" in str(exc_info.value)

    @patch('src.api.jsearch_client.RateLimiter')
    @patch('src.api.jsearch_client.HTTPClient')
    def test_search_jobs_empty_results(self, mock_http_client, mock_rate_limiter):
        """Test búsqueda sin resultados"""
        mock_client_instance = Mock()
        mock_client_instance.get.return_value = {"data": []}
        mock_http_client.return_value = mock_client_instance

        mock_limiter_instance = Mock()
        mock_limiter_instance.with_retry = lambda f: f
        mock_rate_limiter.return_value = mock_limiter_instance

        client = JSearchClient(api_key="test_key")
        params = SearchParameters(query="python", country="us")

        jobs = client.search_jobs(params)
        assert jobs == []

    @patch('src.api.jsearch_client.RateLimiter')
    @patch('src.api.jsearch_client.HTTPClient')
    def test_get_job_details_success(self, mock_http_client, mock_rate_limiter):
        """Test obtener detalles de trabajo exitoso"""
        mock_client_instance = Mock()
        mock_client_instance.get.return_value = {
            "data": [{"job_id": "123", "job_title": "Developer"}]
        }
        mock_http_client.return_value = mock_client_instance

        mock_limiter_instance = Mock()
        mock_limiter_instance.with_retry = lambda f: f
        mock_rate_limiter.return_value = mock_limiter_instance

        client = JSearchClient(api_key="test_key")
        job = client.get_job_details("123", "us")

        assert job["job_id"] == "123"
        assert job["job_title"] == "Developer"

    @patch('src.api.jsearch_client.RateLimiter')
    @patch('src.api.jsearch_client.HTTPClient')
    def test_get_job_details_with_optional_params(self, mock_http_client, mock_rate_limiter):
        """Test obtener detalles con parámetros opcionales"""
        mock_client_instance = Mock()
        mock_client_instance.get.return_value = {
            "data": [{"job_id": "123"}]
        }
        mock_http_client.return_value = mock_client_instance

        mock_limiter_instance = Mock()
        mock_limiter_instance.with_retry = lambda f: f
        mock_rate_limiter.return_value = mock_limiter_instance

        client = JSearchClient(api_key="test_key")
        job = client.get_job_details("123", "us", language="en", fields="id,title")

        # Verificar que se llamó con los parámetros correctos
        call_args = mock_client_instance.get.call_args
        assert call_args[0][0] == "/jsearch/job-details"
        params = call_args[0][1]
        assert params["language"] == "en"
        assert params["fields"] == "id,title"

    @patch('src.api.jsearch_client.RateLimiter')
    @patch('src.api.jsearch_client.HTTPClient')
    def test_get_job_details_not_found(self, mock_http_client, mock_rate_limiter):
        """Test obtener detalles de trabajo no encontrado"""
        mock_client_instance = Mock()
        mock_client_instance.get.return_value = {"data": []}
        mock_http_client.return_value = mock_client_instance

        mock_limiter_instance = Mock()

        def mock_with_retry(func):
            def wrapper(*args, **kwargs):
                raise HTTPError(404, "Trabajo no encontrado")
            return wrapper

        mock_limiter_instance.with_retry = mock_with_retry
        mock_rate_limiter.return_value = mock_limiter_instance

        client = JSearchClient(api_key="test_key")

        with pytest.raises(HTTPError) as exc_info:
            client.get_job_details("nonexistent", "us")

        assert exc_info.value.status_code == 404

    @patch('src.api.jsearch_client.RateLimiter')
    @patch('src.api.jsearch_client.HTTPClient')
    def test_get_estimated_salary_success(self, mock_http_client, mock_rate_limiter):
        """Test obtener estimación salarial exitosa"""
        mock_client_instance = Mock()
        mock_client_instance.get.return_value = {
            "data": [
                {"job_title": "Developer", "median_salary": 50000},
                {"job_title": "Developer", "median_salary": 60000}
            ]
        }
        mock_http_client.return_value = mock_client_instance

        mock_limiter_instance = Mock()
        mock_limiter_instance.with_retry = lambda f: f
        mock_rate_limiter.return_value = mock_limiter_instance

        client = JSearchClient(api_key="test_key")
        salaries = client.get_estimated_salary("Developer", "Madrid, Spain")

        assert len(salaries) == 2
        assert salaries[0]["median_salary"] == 50000

    @patch('src.api.jsearch_client.RateLimiter')
    @patch('src.api.jsearch_client.HTTPClient')
    def test_get_estimated_salary_with_all_params(self, mock_http_client, mock_rate_limiter):
        """Test estimación salarial con todos los parámetros"""
        mock_client_instance = Mock()
        mock_client_instance.get.return_value = {"data": []}
        mock_http_client.return_value = mock_client_instance

        mock_limiter_instance = Mock()
        mock_limiter_instance.with_retry = lambda f: f
        mock_rate_limiter.return_value = mock_limiter_instance

        client = JSearchClient(api_key="test_key")
        salaries = client.get_estimated_salary(
            "Developer",
            "Madrid",
            location_type="CITY",
            years_of_experience="FIVE_TO_SEVEN",
            fields="median"
        )

        # Verificar parámetros
        call_args = mock_client_instance.get.call_args
        params = call_args[0][1]
        assert params["location_type"] == "CITY"
        assert params["years_of_experience"] == "FIVE_TO_SEVEN"
        assert params["fields"] == "median"

    @patch('src.api.jsearch_client.RateLimiter')
    @patch('src.api.jsearch_client.HTTPClient')
    def test_get_estimated_salary_with_error(self, mock_http_client, mock_rate_limiter):
        """Test estimación salarial con error"""
        mock_client_instance = Mock()
        mock_client_instance.get.return_value = {"error": "Invalid location"}
        mock_http_client.return_value = mock_client_instance

        mock_limiter_instance = Mock()
        mock_limiter_instance.with_retry = lambda f: f
        mock_rate_limiter.return_value = mock_limiter_instance

        client = JSearchClient(api_key="test_key")

        with pytest.raises(HTTPError):
            client.get_estimated_salary("Developer", "InvalidLocation")

    @patch('src.api.jsearch_client.RateLimiter')
    @patch('src.api.jsearch_client.HTTPClient')
    def test_get_company_salary_success(self, mock_http_client, mock_rate_limiter):
        """Test obtener salarios de empresa exitoso"""
        mock_client_instance = Mock()
        mock_client_instance.get.return_value = {
            "data": [{"company": "Google", "median_salary": 120000}]
        }
        mock_http_client.return_value = mock_client_instance

        mock_limiter_instance = Mock()
        mock_limiter_instance.with_retry = lambda f: f
        mock_rate_limiter.return_value = mock_limiter_instance

        client = JSearchClient(api_key="test_key")
        salaries = client.get_company_salary("Google", "Software Engineer")

        assert len(salaries) == 1
        assert salaries[0]["company"] == "Google"

    @patch('src.api.jsearch_client.RateLimiter')
    @patch('src.api.jsearch_client.HTTPClient')
    def test_get_company_salary_with_location(self, mock_http_client, mock_rate_limiter):
        """Test salarios de empresa con ubicación"""
        mock_client_instance = Mock()
        mock_client_instance.get.return_value = {"data": []}
        mock_http_client.return_value = mock_client_instance

        mock_limiter_instance = Mock()
        mock_limiter_instance.with_retry = lambda f: f
        mock_rate_limiter.return_value = mock_limiter_instance

        client = JSearchClient(api_key="test_key")
        salaries = client.get_company_salary(
            "Google",
            "Engineer",
            location="Mountain View, CA",
            location_type="CITY",
            years_of_experience="THREE_TO_FIVE"
        )

        # Verificar parámetros
        call_args = mock_client_instance.get.call_args
        params = call_args[0][1]
        assert params["location"] == "Mountain View, CA"
        assert params["location_type"] == "CITY"

    @patch('src.api.jsearch_client.RateLimiter')
    @patch('src.api.jsearch_client.HTTPClient')
    def test_get_company_salary_without_location(self, mock_http_client, mock_rate_limiter):
        """Test salarios de empresa sin ubicación"""
        mock_client_instance = Mock()
        mock_client_instance.get.return_value = {"data": []}
        mock_http_client.return_value = mock_client_instance

        mock_limiter_instance = Mock()
        mock_limiter_instance.with_retry = lambda f: f
        mock_rate_limiter.return_value = mock_limiter_instance

        client = JSearchClient(api_key="test_key")
        salaries = client.get_company_salary("Google", "Engineer", location=None)

        # Verificar que location no está en los parámetros
        call_args = mock_client_instance.get.call_args
        params = call_args[0][1]
        assert "location" not in params

    @patch('src.api.jsearch_client.RateLimiter')
    @patch('src.api.jsearch_client.HTTPClient')
    def test_get_company_salary_with_error(self, mock_http_client, mock_rate_limiter):
        """Test salarios de empresa con error"""
        mock_client_instance = Mock()
        mock_client_instance.get.return_value = {"error": "Company not found"}
        mock_http_client.return_value = mock_client_instance

        mock_limiter_instance = Mock()
        mock_limiter_instance.with_retry = lambda f: f
        mock_rate_limiter.return_value = mock_limiter_instance

        client = JSearchClient(api_key="test_key")

        with pytest.raises(HTTPError):
            client.get_company_salary("NonExistent", "Engineer")


@patch('src.api.jsearch_client.RateLimiter')
@patch('src.api.jsearch_client.HTTPClient')
def test_get_job_details_with_error_response(mock_http_client, mock_rate_limiter):
    """Test detalles de trabajo con respuesta de error"""
    mock_client_instance = Mock()
    mock_client_instance.get.return_value = {"error": "Invalid job ID"}
    mock_http_client.return_value = mock_client_instance

    mock_limiter_instance = Mock()
    mock_limiter_instance.with_retry = lambda f: f
    mock_rate_limiter.return_value = mock_limiter_instance

    client = JSearchClient(api_key="test_key")

    with pytest.raises(HTTPError) as exc_info:
        client.get_job_details("invalid_id")
    assert exc_info.value.status_code == 400


@patch('src.api.jsearch_client.RateLimiter')
@patch('src.api.jsearch_client.HTTPClient')
def test_get_job_details_empty_data(mock_http_client, mock_rate_limiter):
    """Test detalles de trabajo con data vacía"""
    mock_client_instance = Mock()
    mock_client_instance.get.return_value = {"data": []}  # Sin datos
    mock_http_client.return_value = mock_client_instance

    mock_limiter_instance = Mock()
    mock_limiter_instance.with_retry = lambda f: f
    mock_rate_limiter.return_value = mock_limiter_instance

    client = JSearchClient(api_key="test_key")

    with pytest.raises(HTTPError) as exc_info:
        client.get_job_details("not_found_id")
    assert exc_info.value.status_code == 404
    assert "no encontrado" in str(exc_info.value.message).lower()
