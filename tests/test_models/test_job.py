#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: test_job.py
Descripción: Suite de tests para el modelo Job incluyendo validación,
             formateo de ubicación, salarios y descripción truncada.

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
import pytest
from pydantic import ValidationError
from src.models.job import Job


def test_job_creation_from_api_data(sample_job_data):
    """Test creación de Job desde datos de API"""
    job = Job.model_validate(sample_job_data)

    assert job.job_id == "abc123xyz"
    assert job.title == "Python Developer"
    assert job.employer_name == "Tech Corp"
    assert job.city == "Madrid"
    assert job.country == "Spain"
    assert job.is_remote is False


def test_job_location_formatting(sample_job):
    """Test formateo de ubicación"""
    location = sample_job.get_location()

    assert "Madrid" in location
    assert "Spain" in location


def test_job_salary_range_formatting(sample_job):
    """Test formateo de rango salarial"""
    salary_range = sample_job.get_salary_range()

    assert salary_range is not None
    assert "40,000" in salary_range
    assert "60,000" in salary_range
    assert "EUR" in salary_range


def test_job_short_description(sample_job):
    """Test descripción truncada"""
    short_desc = sample_job.get_short_description(20)

    assert len(short_desc) <= 23  # 20 + "..."


def test_job_without_salary():
    """Test job sin información salarial"""
    data = {
        "job_id": "test123",
        "job_title": "Developer",
        "job_country": "Spain"
    }
    job = Job.model_validate(data)

    assert job.get_salary_range() is None


def test_job_required_fields():
    """Test campos requeridos"""
    with pytest.raises(ValidationError):
        Job.model_validate({})  # Falta job_id


def test_job_skills_as_list(sample_job_data):
    """Test que required_skills se convierte a lista"""
    sample_job_data["job_required_skills"] = ["Python", "Django", "PostgreSQL"]
    job = Job.model_validate(sample_job_data)

    assert isinstance(job.required_skills, list)
    assert len(job.required_skills) == 3


def test_job_skills_as_string(sample_job_data):
    """Test que required_skills convierte string a lista"""
    sample_job_data["job_required_skills"] = "Python"
    job = Job.model_validate(sample_job_data)

    assert isinstance(job.required_skills, list)
    assert job.required_skills == ["Python"]


def test_job_skills_as_none(sample_job_data):
    """Test que required_skills maneja None"""
    sample_job_data["job_required_skills"] = None
    job = Job.model_validate(sample_job_data)

    assert isinstance(job.required_skills, list)
    assert job.required_skills == []


def test_job_benefits_as_string(sample_job_data):
    """Test que benefits convierte string a lista"""
    sample_job_data["job_benefits"] = "Health Insurance"
    job = Job.model_validate(sample_job_data)

    assert isinstance(job.benefits, list)
    assert job.benefits == ["Health Insurance"]


def test_job_benefits_as_none(sample_job_data):
    """Test que benefits maneja None"""
    sample_job_data["job_benefits"] = None
    job = Job.model_validate(sample_job_data)

    assert job.benefits is None


def test_job_location_city_only(sample_job_data):
    """Test ubicación con solo ciudad"""
    sample_job_data["job_city"] = "Madrid"
    sample_job_data["job_state"] = None
    sample_job_data["job_country"] = None
    job = Job.model_validate(sample_job_data)

    location = job.get_location()
    assert location == "Madrid"


def test_job_location_no_data():
    """Test ubicación sin datos"""
    job = Job.model_validate({"job_id": "test"})

    location = job.get_location()
    assert location == "N/A"


def test_job_salary_range_only_min(sample_job_data):
    """Test rango salarial con solo salario mínimo"""
    sample_job_data["job_min_salary"] = 50000
    sample_job_data["job_max_salary"] = None
    job = Job.model_validate(sample_job_data)

    salary_range = job.get_salary_range()
    assert "50,000+" in salary_range


def test_job_salary_range_only_max(sample_job_data):
    """Test rango salarial con solo salario máximo"""
    sample_job_data["job_min_salary"] = None
    sample_job_data["job_max_salary"] = 80000
    job = Job.model_validate(sample_job_data)

    salary_range = job.get_salary_range()
    assert "Up to" in salary_range
    assert "80,000" in salary_range


def test_job_short_description_exact_length(sample_job_data):
    """Test descripción con longitud exacta"""
    sample_job_data["job_description"] = "X" * 100
    job = Job.model_validate(sample_job_data)

    short_desc = job.get_short_description(100)
    assert len(short_desc) == 100


def test_job_short_description_no_description():
    """Test descripción cuando no hay descripción"""
    job = Job.model_validate({"job_id": "test"})

    short_desc = job.get_short_description()
    assert short_desc == "No disponible"


def test_job_short_description_whitespace_cleanup(sample_job_data):
    """Test que limpia espacios en descripción"""
    sample_job_data["job_description"] = "Test    with   multiple    spaces"
    job = Job.model_validate(sample_job_data)

    short_desc = job.get_short_description(100)
    assert "    " not in short_desc
    assert "Test with multiple spaces" == short_desc


def test_job_populate_by_name():
    """Test que populate_by_name funciona"""
    # Usar nombre de campo sin alias en vez de job_title
    data = {
        "job_id": "test123",
        "title": "Test Title",  # Usando field name en vez de alias
        "employer_name": "Test Corp",
        "city": "Madrid"  # Usando field name en vez de job_city
    }
    job = Job.model_validate(data)

    assert job.title == "Test Title"
    assert job.city == "Madrid"


def test_job_all_optional_fields():
    """Test job con solo campo requerido"""
    job = Job.model_validate({"job_id": "minimal"})

    assert job.job_id == "minimal"
    assert job.title is None
    assert job.employer_name is None
    assert job.is_remote is False


def test_job_salary_range_with_zero_values():
    """Test get_salary_range con salarios en cero"""
    data = {
        "job_id": "test123",
        "job_title": "Developer",
        "job_min_salary": 0,
        "job_max_salary": 0,
        "job_salary_currency": "EUR",
        "job_salary_period": "YEAR"
    }
    job = Job.model_validate(data)

    # Con salarios en 0, debería retornar None (línea 110)
    assert job.get_salary_range() is None
