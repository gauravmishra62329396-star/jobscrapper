#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: test_salary.py
Descripción: Suite de tests para el modelo SalaryInfo incluyendo validación,
             formateo de salarios y verificación de datos salariales.

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
from src.models.salary import SalaryInfo


def test_salary_creation(sample_salary_data):
    """Test creación de SalaryInfo"""
    salary = SalaryInfo.model_validate(sample_salary_data)

    assert salary.job_title == "Software Engineer"
    assert salary.median_salary == 50000
    assert salary.salary_currency == "EUR"


def test_salary_formatted_median(sample_salary):
    """Test formateo de salario mediano"""
    formatted = sample_salary.get_formatted_median()

    assert "50,000" in formatted
    assert "EUR" in formatted
    assert "YEAR" in formatted


def test_salary_formatted_range(sample_salary):
    """Test formateo de rango salarial"""
    formatted = sample_salary.get_formatted_range()

    assert "35,000" in formatted
    assert "65,000" in formatted
    assert "EUR" in formatted


def test_salary_has_data(sample_salary):
    """Test verificación de datos salariales"""
    assert sample_salary.has_salary_data() is True


def test_salary_without_data():
    """Test salario sin datos"""
    salary = SalaryInfo(job_title="Test")

    assert salary.has_salary_data() is False
    assert salary.get_formatted_median() == "N/A"
    assert salary.get_formatted_range() == "N/A"


def test_salary_formatted_range_only_min(sample_salary_data):
    """Test formateo de rango con solo mínimo"""
    sample_salary_data["max_salary"] = None
    salary = SalaryInfo.model_validate(sample_salary_data)

    formatted = salary.get_formatted_range()

    assert "35,000+" in formatted
    assert "EUR" in formatted


def test_salary_formatted_range_only_max(sample_salary_data):
    """Test formateo de rango con solo máximo"""
    sample_salary_data["min_salary"] = None
    salary = SalaryInfo.model_validate(sample_salary_data)

    formatted = salary.get_formatted_range()

    assert "Up to" in formatted
    assert "65,000" in formatted


def test_salary_has_data_with_min_only():
    """Test has_salary_data con solo min_salary"""
    salary = SalaryInfo(job_title="Test", min_salary=40000)

    assert salary.has_salary_data() is True


def test_salary_has_data_with_max_only():
    """Test has_salary_data con solo max_salary"""
    salary = SalaryInfo(job_title="Test", max_salary=60000)

    assert salary.has_salary_data() is True


def test_salary_has_data_with_median_only():
    """Test has_salary_data con solo median_salary"""
    salary = SalaryInfo(job_title="Test", median_salary=50000)

    assert salary.has_salary_data() is True


def test_salary_default_currency():
    """Test moneda por defecto"""
    salary = SalaryInfo(job_title="Test", median_salary=50000)

    assert salary.salary_currency == "USD"


def test_salary_default_period():
    """Test período por defecto"""
    salary = SalaryInfo(job_title="Test", median_salary=50000)

    assert salary.salary_period == "YEAR"


def test_salary_optional_fields():
    """Test campos opcionales"""
    salary = SalaryInfo(
        job_title="Test",
        location="Test Location",
        publisher_name="Test Publisher",
        median_salary=50000
    )

    assert salary.job_title == "Test"
    assert salary.location == "Test Location"
    assert salary.publisher_name == "Test Publisher"


def test_salary_with_additional_pay(sample_salary_data):
    """Test con pago adicional"""
    sample_salary_data["additional_pay"] = "$10,000 bonus"
    salary = SalaryInfo.model_validate(sample_salary_data)

    assert salary.additional_pay == "$10,000 bonus"


def test_salary_formatted_range_with_zero_values():
    """Test get_formatted_range con salarios en cero"""
    salary = SalaryInfo(
        job_title="Test",
        min_salary=0,
        max_salary=0,
        median_salary=0
    )

    # Con todos los salarios en 0 (falsy), debería retornar "N/A" (línea 56)
    assert salary.get_formatted_range() == "N/A"
