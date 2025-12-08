#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: search_params.py
Descripción: Modelo Pydantic para validar parámetros de búsqueda de trabajos.
             Incluye validadores para query, país, fecha y conversión a parámetros API.

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class SearchParameters(BaseModel):
    """Parámetros validados para búsqueda de trabajos"""

    query: str = Field(..., min_length=1, description="Query de búsqueda")
    country: str = Field(default="us", description="Código de país (ISO 3166-1 alpha-2)")
    page: int = Field(default=1, ge=1, description="Número de página")
    num_pages: int = Field(default=1, ge=1, le=10, description="Número de páginas a buscar")
    date_posted: str = Field(default="all", description="Período de publicación")
    work_from_home: bool = Field(default=False, description="Solo trabajos remotos")
    employment_types: Optional[str] = Field(None, description="Tipos de empleo separados por coma")
    job_requirements: Optional[str] = Field(None, description="Requisitos del trabajo")
    radius: Optional[int] = Field(None, ge=0, description="Radio de búsqueda en km")
    exclude_job_publishers: Optional[str] = Field(None, description="Publishers a excluir")
    language: Optional[str] = Field(None, description="Código de idioma")

    @field_validator('query')
    @classmethod
    def validate_query(cls, v: str) -> str:
        """Valida que el query no esté vacío"""
        v = v.strip()
        if not v:
            raise ValueError("Query no puede estar vacío")
        return v

    @field_validator('country')
    @classmethod
    def validate_country(cls, v: str) -> str:
        """Valida formato de código de país"""
        v = v.lower().strip()
        if len(v) != 2:
            raise ValueError("Código de país debe ser ISO 3166-1 alpha-2 (2 letras)")
        return v

    @field_validator('date_posted')
    @classmethod
    def validate_date_posted(cls, v: str) -> str:
        """Valida período de publicación"""
        valid_periods = ['all', 'today', '3days', 'week', 'month']
        if v not in valid_periods:
            raise ValueError(f"date_posted debe ser uno de: {', '.join(valid_periods)}")
        return v

    def to_api_params(self) -> dict:
        """Convierte a parámetros para la API"""
        params = {
            'query': self.query,
            'page': str(self.page),
            'num_pages': str(self.num_pages),
            'country': self.country,
            'date_posted': self.date_posted
        }

        # Agregar parámetros opcionales solo si están presentes
        if self.language:
            params['language'] = self.language
        if self.work_from_home:
            params['work_from_home'] = 'true'
        if self.employment_types:
            params['employment_types'] = self.employment_types
        if self.job_requirements:
            params['job_requirements'] = self.job_requirements
        if self.radius is not None:
            params['radius'] = str(self.radius)
        if self.exclude_job_publishers:
            params['exclude_job_publishers'] = self.exclude_job_publishers

        return params
