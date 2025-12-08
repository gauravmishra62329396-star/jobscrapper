#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: conftest.py
Descripción: Fixtures compartidos para pytest utilizados en todos los tests.
             Proporciona datos de ejemplo para trabajos, salarios y parámetros de búsqueda.

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
import pytest
from pathlib import Path
from src.models.job import Job
from src.models.salary import SalaryInfo
from src.models.search_params import SearchParameters


@pytest.fixture
def sample_job_data():
    """Datos de ejemplo de un trabajo de la API"""
    return {
        "job_id": "abc123xyz",
        "job_title": "Python Developer",
        "employer_name": "Tech Corp",
        "job_city": "Madrid",
        "job_state": "Comunidad de Madrid",
        "job_country": "Spain",
        "job_is_remote": False,
        "job_employment_type": "FULLTIME",
        "job_min_salary": 40000,
        "job_max_salary": 60000,
        "job_salary_currency": "EUR",
        "job_salary_period": "YEAR",
        "job_description": "Buscamos un desarrollador Python con experiencia...",
        "job_apply_link": "https://example.com/apply",
        "job_posted_at_datetime_utc": "2025-12-01T10:00:00Z"
    }


@pytest.fixture
def sample_job(sample_job_data):
    """Objeto Job de ejemplo"""
    return Job.model_validate(sample_job_data)


@pytest.fixture
def sample_salary_data():
    """Datos de ejemplo de salario"""
    return {
        "job_title": "Software Engineer",
        "location": "Madrid, Spain",
        "publisher_name": "Glassdoor",
        "min_salary": 35000,
        "max_salary": 65000,
        "median_salary": 50000,
        "salary_currency": "EUR",
        "salary_period": "YEAR"
    }


@pytest.fixture
def sample_salary(sample_salary_data):
    """Objeto SalaryInfo de ejemplo"""
    return SalaryInfo.model_validate(sample_salary_data)


@pytest.fixture
def sample_search_params():
    """Parámetros de búsqueda de ejemplo"""
    return SearchParameters(
        query="python developer",
        country="es",
        date_posted="week",
        num_pages=1
    )


@pytest.fixture
def temp_output_dir(tmp_path):
    """Directorio temporal para archivos de salida"""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir
