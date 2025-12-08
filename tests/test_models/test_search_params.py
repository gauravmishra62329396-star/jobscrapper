#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: test_search_params.py
Descripción: Suite de tests para el modelo SearchParameters incluyendo validación
             de parámetros, conversión a API y validación de límites.

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
import pytest
from pydantic import ValidationError
from src.models.search_params import SearchParameters


def test_search_params_creation():
    """Test creación de SearchParameters"""
    params = SearchParameters(
        query="python developer",
        country="es"
    )

    assert params.query == "python developer"
    assert params.country == "es"
    assert params.page == 1  # Default
    assert params.num_pages == 1  # Default


def test_search_params_validation_empty_query():
    """Test validación de query vacío"""
    with pytest.raises(ValidationError):
        SearchParameters(query="", country="es")


def test_search_params_validation_whitespace_query():
    """Test validación de query solo con espacios"""
    with pytest.raises(ValidationError) as exc_info:
        SearchParameters(query="   ", country="es")
    assert "Query no puede estar vacío" in str(exc_info.value)


def test_search_params_validation_country_length():
    """Test validación de longitud de código de país"""
    with pytest.raises(ValidationError):
        SearchParameters(query="test", country="usa")  # Debe ser 2 letras


def test_search_params_validation_date_posted():
    """Test validación de date_posted"""
    # Valor válido
    params = SearchParameters(query="test", country="us", date_posted="week")
    assert params.date_posted == "week"

    # Valor inválido
    with pytest.raises(ValidationError):
        SearchParameters(query="test", country="us", date_posted="invalid")


def test_search_params_to_api_params():
    """Test conversión a parámetros de API"""
    params = SearchParameters(
        query="python",
        country="es",
        date_posted="week",
        work_from_home=True,
        num_pages=2
    )

    api_params = params.to_api_params()

    assert api_params["query"] == "python"
    assert api_params["country"] == "es"
    assert api_params["date_posted"] == "week"
    assert api_params["work_from_home"] == "true"
    assert api_params["num_pages"] == "2"


def test_search_params_optional_fields():
    """Test campos opcionales"""
    params = SearchParameters(
        query="test",
        country="us",
        employment_types="FULLTIME",
        language="en"
    )

    api_params = params.to_api_params()

    assert "employment_types" in api_params
    assert "language" in api_params


def test_search_params_num_pages_limits():
    """Test límites de num_pages"""
    # Valor válido
    params = SearchParameters(query="test", country="us", num_pages=5)
    assert params.num_pages == 5

    # Valor fuera de límites
    with pytest.raises(ValidationError):
        SearchParameters(query="test", country="us", num_pages=11)  # Max 10

    with pytest.raises(ValidationError):
        SearchParameters(query="test", country="us", num_pages=0)  # Min 1


def test_search_params_to_api_params_without_optionals():
    """Test conversión a API params sin campos opcionales"""
    params = SearchParameters(query="test", country="us")

    api_params = params.to_api_params()

    assert "language" not in api_params
    assert "employment_types" not in api_params
    assert "job_requirements" not in api_params
    assert "radius" not in api_params
    assert "exclude_job_publishers" not in api_params
    assert "work_from_home" not in api_params


def test_search_params_to_api_params_with_radius():
    """Test conversión con radius"""
    params = SearchParameters(query="test", country="us", radius=50)

    api_params = params.to_api_params()

    assert "radius" in api_params
    assert api_params["radius"] == "50"


def test_search_params_to_api_params_with_job_requirements():
    """Test conversión con job_requirements"""
    params = SearchParameters(
        query="test",
        country="us",
        job_requirements="degree"
    )

    api_params = params.to_api_params()

    assert "job_requirements" in api_params
    assert api_params["job_requirements"] == "degree"


def test_search_params_to_api_params_with_exclude_publishers():
    """Test conversión con exclude_job_publishers"""
    params = SearchParameters(
        query="test",
        country="us",
        exclude_job_publishers="Indeed,LinkedIn"
    )

    api_params = params.to_api_params()

    assert "exclude_job_publishers" in api_params
    assert api_params["exclude_job_publishers"] == "Indeed,LinkedIn"


def test_search_params_work_from_home_false():
    """Test work_from_home false no se incluye en API params"""
    params = SearchParameters(
        query="test",
        country="us",
        work_from_home=False
    )

    api_params = params.to_api_params()

    # Cuando es False, no se debería incluir
    assert "work_from_home" not in api_params


def test_search_params_radius_zero():
    """Test radius con valor cero"""
    params = SearchParameters(query="test", country="us", radius=0)

    api_params = params.to_api_params()

    # radius=0 es válido y debería incluirse
    assert "radius" in api_params
    assert api_params["radius"] == "0"
