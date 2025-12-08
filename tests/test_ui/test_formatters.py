#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: test_formatters.py
Descripción: Tests para formatters de jobs y salarios

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
import pytest
from unittest.mock import Mock
from rich.table import Table
from rich.panel import Panel
from src.ui.formatters import JobFormatter, SalaryFormatter
from src.models.job import Job
from src.models.salary import SalaryInfo


class TestJobFormatter:
    """Tests para JobFormatter"""

    def test_format_job_table(self, sample_job):
        """Test formatear tabla de trabajos"""
        jobs = [sample_job, sample_job]

        table = JobFormatter.format_job_table(jobs)

        assert isinstance(table, Table)
        assert "2" in table.title  # Debe mostrar cantidad de trabajos

    def test_format_job_table_empty_list(self):
        """Test formatear tabla vacía"""
        table = JobFormatter.format_job_table([])

        assert isinstance(table, Table)
        assert "0" in table.title

    def test_format_job_table_truncates_long_text(self, sample_job_data):
        """Test que la tabla trunca textos largos"""
        sample_job_data["job_title"] = "A" * 100
        sample_job_data["employer_name"] = "B" * 100
        job = Job.model_validate(sample_job_data)

        table = JobFormatter.format_job_table([job])

        # No debería fallar con textos largos
        assert isinstance(table, Table)

    def test_format_job_details(self, sample_job):
        """Test formatear detalles de trabajo"""
        panel = JobFormatter.format_job_details(sample_job)

        assert isinstance(panel, Panel)

    def test_format_job_details_contains_info(self, sample_job):
        """Test que detalles contienen información del trabajo"""
        panel = JobFormatter.format_job_details(sample_job)

        # El contenido debería estar en panel.renderable
        content = str(panel.renderable)
        assert sample_job.title in content or "Python Developer" in content

    def test_format_job_summary(self, sample_job):
        """Test formatear resumen de trabajos"""
        jobs = [sample_job, sample_job]

        summary = JobFormatter.format_job_summary(jobs)

        assert isinstance(summary, str)
        assert "2 trabajos" in summary
        assert sample_job.title in summary

    def test_format_job_summary_empty_list(self):
        """Test formatear resumen vacío"""
        summary = JobFormatter.format_job_summary([])

        assert isinstance(summary, str)
        assert "0 trabajos" in summary

    def test_format_job_summary_includes_details(self, sample_job):
        """Test que resumen incluye detalles importantes"""
        summary = JobFormatter.format_job_summary([sample_job])

        assert "Python Developer" in summary or sample_job.title in summary
        assert sample_job.employer_name in summary

    def test_format_job_table_handles_none_values(self, sample_job_data):
        """Test tabla maneja valores None"""
        sample_job_data["job_title"] = None
        sample_job_data["employer_name"] = None
        job = Job.model_validate(sample_job_data)

        table = JobFormatter.format_job_table([job])

        # No debería fallar con valores None
        assert isinstance(table, Table)

    def test_format_job_details_handles_none_values(self, sample_job_data):
        """Test detalles manejan valores None"""
        sample_job_data["job_title"] = None
        sample_job_data["employer_name"] = None
        job = Job.model_validate(sample_job_data)

        panel = JobFormatter.format_job_details(job)

        assert isinstance(panel, Panel)

    def test_format_job_summary_handles_none_values(self, sample_job_data):
        """Test resumen maneja valores None"""
        sample_job_data["job_title"] = None
        sample_job_data["employer_name"] = None
        job = Job.model_validate(sample_job_data)

        summary = JobFormatter.format_job_summary([job])

        assert isinstance(summary, str)
        assert "N/A" in summary


class TestSalaryFormatter:
    """Tests para SalaryFormatter"""

    def test_format_salary_table(self, sample_salary):
        """Test formatear tabla de salarios"""
        salaries = [sample_salary, sample_salary]

        table = SalaryFormatter.format_salary_table(salaries)

        assert isinstance(table, Table)

    def test_format_salary_table_empty_list(self):
        """Test formatear tabla vacía"""
        table = SalaryFormatter.format_salary_table([])

        assert isinstance(table, Table)

    def test_format_salary_table_truncates_long_text(self, sample_salary_data):
        """Test tabla trunca textos largos"""
        sample_salary_data["job_title"] = "A" * 100
        sample_salary_data["location"] = "B" * 100
        salary = SalaryInfo.model_validate(sample_salary_data)

        table = SalaryFormatter.format_salary_table([salary])

        assert isinstance(table, Table)

    def test_format_salary_details(self, sample_salary):
        """Test formatear detalles de salarios"""
        salaries = [sample_salary, sample_salary]

        details = SalaryFormatter.format_salary_details(salaries)

        assert isinstance(details, str)
        assert "2 resultados" in details
        assert sample_salary.job_title in details

    def test_format_salary_details_empty_list(self):
        """Test formatear detalles vacíos"""
        details = SalaryFormatter.format_salary_details([])

        assert isinstance(details, str)
        assert "0 resultados" in details

    def test_format_salary_details_includes_info(self, sample_salary):
        """Test que detalles incluyen información salarial"""
        details = SalaryFormatter.format_salary_details([sample_salary])

        assert sample_salary.job_title in details
        # Debería incluir salario formateado
        assert "50,000" in details or sample_salary.location in details

    def test_format_salary_table_handles_none_values(self, sample_salary_data):
        """Test tabla maneja valores None"""
        sample_salary_data["job_title"] = None
        sample_salary_data["location"] = None
        sample_salary_data["publisher_name"] = None
        salary = SalaryInfo.model_validate(sample_salary_data)

        table = SalaryFormatter.format_salary_table([salary])

        assert isinstance(table, Table)

    def test_format_salary_details_handles_none_values(self, sample_salary_data):
        """Test detalles manejan valores None"""
        sample_salary_data["job_title"] = None
        sample_salary_data["location"] = None
        salary = SalaryInfo.model_validate(sample_salary_data)

        details = SalaryFormatter.format_salary_details([salary])

        assert isinstance(details, str)
        assert "N/A" in details

    def test_format_salary_details_with_additional_pay(self, sample_salary_data):
        """Test detalles incluyen pago adicional"""
        sample_salary_data["additional_pay"] = "$5,000 bonus"
        salary = SalaryInfo.model_validate(sample_salary_data)

        details = SalaryFormatter.format_salary_details([salary])

        assert "$5,000 bonus" in details

    def test_format_salary_details_without_additional_pay(self, sample_salary):
        """Test detalles sin pago adicional"""
        details = SalaryFormatter.format_salary_details([sample_salary])

        # No debería causar errores
        assert isinstance(details, str)
