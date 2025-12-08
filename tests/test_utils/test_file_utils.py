#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: test_file_utils.py
Descripción: Tests para file_utils

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
import pytest
from pathlib import Path
from src.utils.file_utils import (
    clean_filename,
    generate_filename,
    ensure_dir_exists,
    get_file_size,
    format_file_size
)


class TestFileUtils:
    """Tests para utilidades de archivos"""

    def test_clean_filename_basic(self):
        """Test limpieza de nombre de archivo básico"""
        result = clean_filename("test file name")

        assert result == "test_file_name"

    def test_clean_filename_special_chars(self):
        """Test limpieza de caracteres especiales"""
        result = clean_filename("test@file#name$")

        assert "@" not in result
        assert "#" not in result
        assert "$" not in result

    def test_clean_filename_multiple_spaces(self):
        """Test limpieza de espacios múltiples"""
        result = clean_filename("test    file    name")

        assert result == "test_file_name"

    def test_clean_filename_hyphens(self):
        """Test limpieza de guiones"""
        result = clean_filename("test---file---name")

        assert result == "test_file_name"

    def test_clean_filename_mixed_separators(self):
        """Test limpieza de separadores mixtos"""
        result = clean_filename("test - file   name")

        assert result == "test_file_name"

    def test_clean_filename_leading_trailing(self):
        """Test limpieza de guiones al inicio y final"""
        result = clean_filename("-test-file-name-")

        assert not result.startswith("_")
        assert not result.startswith("-")
        assert not result.endswith("_")
        assert not result.endswith("-")

    def test_clean_filename_alphanumeric_only(self):
        """Test que mantiene caracteres alfanuméricos"""
        result = clean_filename("test123_file456")

        assert "test123" in result
        assert "file456" in result

    def test_clean_filename_empty_string(self):
        """Test limpieza de string vacío"""
        result = clean_filename("")

        assert result == ""

    def test_clean_filename_only_special_chars(self):
        """Test limpieza de solo caracteres especiales"""
        result = clean_filename("@#$%&*")

        assert result == ""

    def test_generate_filename_with_timestamp(self):
        """Test generación de nombre con timestamp"""
        result = generate_filename("test", "txt", include_timestamp=True)

        assert result.startswith("test_")
        assert result.endswith(".txt")
        assert len(result) > len("test.txt")

    def test_generate_filename_without_timestamp(self):
        """Test generación de nombre sin timestamp"""
        result = generate_filename("test", "txt", include_timestamp=False)

        assert result == "test.txt"

    def test_generate_filename_different_extensions(self):
        """Test generación con diferentes extensiones"""
        extensions = ["csv", "json", "xml", "html"]

        for ext in extensions:
            result = generate_filename("test", ext, include_timestamp=False)
            assert result.endswith(f".{ext}")

    def test_generate_filename_cleans_base_name(self):
        """Test que genera nombre limpia el base_name"""
        result = generate_filename("test file@name", "txt", include_timestamp=False)

        assert result == "test_filename.txt"

    def test_generate_filename_timestamp_format(self):
        """Test formato del timestamp"""
        result = generate_filename("test", "txt", include_timestamp=True)

        # Debería tener formato: test_YYYYMMDD_HHMMSS.txt
        parts = result.split("_")
        assert len(parts) >= 3  # test, YYYYMMDD, HHMMSS.txt

    def test_ensure_dir_exists_creates_directory(self, tmp_path):
        """Test crear directorio que no existe"""
        new_dir = tmp_path / "new_directory"

        assert not new_dir.exists()

        result = ensure_dir_exists(new_dir)

        assert new_dir.exists()
        assert result == new_dir

    def test_ensure_dir_exists_existing_directory(self, tmp_path):
        """Test con directorio que ya existe"""
        existing_dir = tmp_path / "existing"
        existing_dir.mkdir()

        result = ensure_dir_exists(existing_dir)

        assert existing_dir.exists()
        assert result == existing_dir

    def test_ensure_dir_exists_nested_directories(self, tmp_path):
        """Test crear directorios anidados"""
        nested_dir = tmp_path / "level1" / "level2" / "level3"

        assert not nested_dir.exists()

        result = ensure_dir_exists(nested_dir)

        assert nested_dir.exists()
        assert result == nested_dir

    def test_ensure_dir_exists_from_string(self, tmp_path):
        """Test crear directorio desde string"""
        new_dir = tmp_path / "string_dir"

        result = ensure_dir_exists(str(new_dir))

        assert new_dir.exists()
        assert isinstance(result, Path)

    def test_ensure_dir_exists_returns_path(self, tmp_path):
        """Test que retorna objeto Path"""
        new_dir = tmp_path / "test_dir"

        result = ensure_dir_exists(new_dir)

        assert isinstance(result, Path)

    def test_get_file_size(self, tmp_path):
        """Test obtener tamaño de archivo"""
        test_file = tmp_path / "test.txt"
        test_content = "Hello World!"
        test_file.write_text(test_content)

        size = get_file_size(test_file)

        assert size == len(test_content.encode('utf-8'))

    def test_get_file_size_empty_file(self, tmp_path):
        """Test tamaño de archivo vacío"""
        test_file = tmp_path / "empty.txt"
        test_file.write_text("")

        size = get_file_size(test_file)

        assert size == 0

    def test_get_file_size_large_file(self, tmp_path):
        """Test tamaño de archivo grande"""
        test_file = tmp_path / "large.txt"
        test_content = "X" * 10000
        test_file.write_text(test_content)

        size = get_file_size(test_file)

        assert size == 10000

    def test_get_file_size_from_string_path(self, tmp_path):
        """Test obtener tamaño usando string path"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        size = get_file_size(str(test_file))

        assert size > 0

    def test_format_file_size_bytes(self):
        """Test formatear tamaño en bytes"""
        result = format_file_size(500)

        assert "500" in result
        assert "B" in result

    def test_format_file_size_kilobytes(self):
        """Test formatear tamaño en KB"""
        result = format_file_size(2048)  # 2 KB

        assert "2.0" in result
        assert "KB" in result

    def test_format_file_size_megabytes(self):
        """Test formatear tamaño en MB"""
        result = format_file_size(1024 * 1024 * 5)  # 5 MB

        assert "5.0" in result
        assert "MB" in result

    def test_format_file_size_gigabytes(self):
        """Test formatear tamaño en GB"""
        result = format_file_size(1024 * 1024 * 1024 * 2)  # 2 GB

        assert "2.0" in result
        assert "GB" in result

    def test_format_file_size_terabytes(self):
        """Test formatear tamaño en TB"""
        result = format_file_size(1024 * 1024 * 1024 * 1024 * 1.5)  # 1.5 TB

        assert "1.5" in result
        assert "TB" in result

    def test_format_file_size_zero(self):
        """Test formatear tamaño cero"""
        result = format_file_size(0)

        assert "0.0" in result
        assert "B" in result

    def test_format_file_size_decimal_precision(self):
        """Test precisión decimal en formato"""
        result = format_file_size(1500)  # 1.46 KB

        # Debería tener un decimal
        parts = result.split(".")
        if len(parts) > 1:
            decimal_part = parts[1].split()[0]
            assert len(decimal_part) == 1

    def test_format_file_size_exact_boundaries(self):
        """Test formateo en límites exactos"""
        # Exactamente 1 KB
        result_kb = format_file_size(1024)
        assert "1.0" in result_kb
        assert "KB" in result_kb

        # Exactamente 1 MB
        result_mb = format_file_size(1024 * 1024)
        assert "1.0" in result_mb
        assert "MB" in result_mb

    def test_generate_filename_special_chars_in_base(self):
        """Test generar nombre de archivo con caracteres especiales en base"""
        result = generate_filename("my-test@file#123", "csv", include_timestamp=False)

        assert "@" not in result
        assert "#" not in result
        assert result.endswith(".csv")

    def test_ensure_dir_exists_permission_preserved(self, tmp_path):
        """Test que directorio preserva permisos"""
        new_dir = tmp_path / "perm_test"

        result = ensure_dir_exists(new_dir)

        # El directorio debería ser accesible
        assert result.exists()
        assert result.is_dir()
