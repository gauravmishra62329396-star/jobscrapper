#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: test_export_service.py
Descripción: Suite de tests para ExportService incluyendo exportación a CSV/JSON
             de trabajos y salarios, verificación de contenido y múltiples registros.

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
import json
import csv
import pytest
from unittest.mock import mock_open, patch, MagicMock
from src.services.export_service import ExportService


def test_export_jobs_to_csv(sample_job, temp_output_dir):
    """Test exportación de trabajos a CSV"""
    service = ExportService(temp_output_dir)
    jobs = [sample_job]

    filepath = service.export_jobs_to_csv(jobs, "test_jobs")

    # Verificar que el archivo existe
    assert filepath.exists()
    assert filepath.suffix == ".csv"

    # Verificar contenido
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        assert len(rows) == 1
        assert rows[0]['job_id'] == sample_job.job_id
        assert rows[0]['title'] == sample_job.title


def test_export_jobs_to_json(sample_job, temp_output_dir):
    """Test exportación de trabajos a JSON"""
    service = ExportService(temp_output_dir)
    jobs = [sample_job]

    filepath = service.export_jobs_to_json(jobs, "test_jobs")

    # Verificar que el archivo existe
    assert filepath.exists()
    assert filepath.suffix == ".json"

    # Verificar contenido
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

        assert len(data) == 1
        assert data[0]['job_id'] == sample_job.job_id
        assert data[0]['title'] == sample_job.title


def test_export_salaries_to_json(sample_salary, temp_output_dir):
    """Test exportación de salarios a JSON"""
    service = ExportService(temp_output_dir)
    salaries = [sample_salary]

    filepath = service.export_salaries_to_json(salaries, "test_salaries")

    # Verificar que el archivo existe
    assert filepath.exists()

    # Verificar contenido
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

        assert len(data) == 1
        assert data[0]['job_title'] == sample_salary.job_title
        assert data[0]['median_salary'] == sample_salary.median_salary


def test_export_multiple_jobs(sample_job, temp_output_dir):
    """Test exportación de múltiples trabajos"""
    service = ExportService(temp_output_dir)

    # Crear múltiples trabajos
    jobs = [sample_job for _ in range(5)]

    filepath = service.export_jobs_to_csv(jobs, "multiple_jobs")

    # Verificar contenido
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        assert len(rows) == 5


def test_export_service_initialization_default_dir():
    """Test inicialización con directorio por defecto"""
    service = ExportService()

    assert service.output_dir.exists()


def test_export_service_initialization_custom_dir(temp_output_dir):
    """Test inicialización con directorio personalizado"""
    service = ExportService(temp_output_dir)

    assert service.output_dir == temp_output_dir


def test_export_salaries_to_csv(sample_salary, temp_output_dir):
    """Test exportación de salarios a CSV"""
    service = ExportService(temp_output_dir)
    salaries = [sample_salary]

    filepath = service.export_salaries_to_csv(salaries, "test_salaries")

    # Verificar que el archivo existe
    assert filepath.exists()
    assert filepath.suffix == ".csv"

    # Verificar contenido
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        assert len(rows) == 1
        assert rows[0]['job_title'] == sample_salary.job_title
        assert rows[0]['median_salary'] == str(sample_salary.median_salary)


def test_export_jobs_csv_with_lists(sample_job_data, temp_output_dir):
    """Test exportación CSV convierte listas a strings"""
    from src.models.job import Job

    sample_job_data["job_required_skills"] = ["Python", "Django", "SQL"]
    sample_job_data["job_benefits"] = ["Health", "Dental"]
    job = Job.model_validate(sample_job_data)

    service = ExportService(temp_output_dir)
    filepath = service.export_jobs_to_csv([job], "test_lists")

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        row = next(reader)

        assert "Python, Django, SQL" in row['required_skills']
        assert "Health, Dental" in row['benefits']


def test_export_jobs_csv_truncates_description(sample_job, temp_output_dir):
    """Test exportación CSV trunca descripción larga"""
    service = ExportService(temp_output_dir)
    filepath = service.export_jobs_to_csv([sample_job], "test_desc")

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        row = next(reader)

        # La descripción debería estar truncada a 500 caracteres
        assert len(row['description']) <= 503  # 500 + "..."


def test_export_jobs_json_preserves_structure(sample_job, temp_output_dir):
    """Test exportación JSON preserva estructura completa"""
    service = ExportService(temp_output_dir)
    filepath = service.export_jobs_to_json([sample_job], "test_structure")

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

        # Verificar que se preservan campos complejos
        assert isinstance(data, list)
        assert 'job_id' in data[0]
        assert 'title' in data[0]


def test_export_empty_jobs_list(temp_output_dir):
    """Test exportación de lista vacía de trabajos"""
    service = ExportService(temp_output_dir)

    filepath_csv = service.export_jobs_to_csv([], "empty_jobs")
    filepath_json = service.export_jobs_to_json([], "empty_jobs")

    # Verificar que los archivos existen pero están vacíos
    assert filepath_csv.exists()
    assert filepath_json.exists()


def test_export_empty_salaries_list(temp_output_dir):
    """Test exportación de lista vacía de salarios"""
    service = ExportService(temp_output_dir)

    filepath_csv = service.export_salaries_to_csv([], "empty_salaries")
    filepath_json = service.export_salaries_to_json([], "empty_salaries")

    assert filepath_csv.exists()
    assert filepath_json.exists()


def test_export_jobs_csv_file_encoding(sample_job_data, temp_output_dir):
    """Test que CSV se exporta con encoding UTF-8"""
    from src.models.job import Job

    # Trabajo con caracteres especiales
    sample_job_data["job_title"] = "Desarrollador Python - España"
    sample_job_data["employer_name"] = "Empresa Española SL"
    job = Job.model_validate(sample_job_data)

    service = ExportService(temp_output_dir)
    filepath = service.export_jobs_to_csv([job], "test_encoding")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "España" in content
        assert "Española" in content


def test_export_salaries_multiple(sample_salary, temp_output_dir):
    """Test exportación de múltiples salarios"""
    service = ExportService(temp_output_dir)
    salaries = [sample_salary for _ in range(3)]

    filepath = service.export_salaries_to_csv(salaries, "multiple_salaries")

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        assert len(rows) == 3


def test_export_jobs_to_csv_error_handling(sample_job, temp_output_dir):
    """Test manejo de errores al exportar trabajos a CSV"""
    service = ExportService(temp_output_dir)
    jobs = [sample_job]

    # Mockear open para que lance excepción
    with patch('builtins.open', side_effect=PermissionError("Access denied")):
        with pytest.raises(PermissionError):
            service.export_jobs_to_csv(jobs, "test_jobs")


def test_export_jobs_to_json_error_handling(sample_job, temp_output_dir):
    """Test manejo de errores al exportar trabajos a JSON"""
    service = ExportService(temp_output_dir)
    jobs = [sample_job]

    # Mockear open para que lance excepción
    with patch('builtins.open', side_effect=IOError("Disk full")):
        with pytest.raises(IOError):
            service.export_jobs_to_json(jobs, "test_jobs")


def test_export_salaries_to_json_error_handling(sample_salary, temp_output_dir):
    """Test manejo de errores al exportar salarios a JSON"""
    service = ExportService(temp_output_dir)
    salaries = [sample_salary]

    # Mockear open para que lance excepción
    with patch('builtins.open', side_effect=OSError("No space left")):
        with pytest.raises(OSError):
            service.export_salaries_to_json(salaries, "test_salaries")


def test_export_salaries_to_csv_error_handling(sample_salary, temp_output_dir):
    """Test manejo de errores al exportar salarios a CSV"""
    service = ExportService(temp_output_dir)
    salaries = [sample_salary]

    # Mockear open para que lance excepción
    with patch('builtins.open', side_effect=PermissionError("Write protected")):
        with pytest.raises(PermissionError):
            service.export_salaries_to_csv(salaries, "test_salaries")
