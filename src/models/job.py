#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: job.py
Descripción: Modelo Pydantic para representar ofertas de trabajo de LinkedIn.
             Incluye validación de datos, campos de ubicación, salario y requisitos.

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class Job(BaseModel):
    """Modelo que representa un trabajo de LinkedIn"""

    job_id: str = Field(..., description="ID único del trabajo")
    title: Optional[str] = Field(None, alias="job_title", description="Título del puesto")
    employer_name: Optional[str] = Field(None, description="Nombre de la empresa")
    employer_logo: Optional[str] = Field(None, description="URL del logo")
    job_publisher: Optional[str] = Field(None, description="Publisher del trabajo")

    # Location fields
    city: Optional[str] = Field(None, alias="job_city")
    state: Optional[str] = Field(None, alias="job_state")
    country: Optional[str] = Field(None, alias="job_country")
    latitude: Optional[float] = Field(None, alias="job_latitude")
    longitude: Optional[float] = Field(None, alias="job_longitude")

    # Job details
    is_remote: bool = Field(False, alias="job_is_remote")
    employment_type: Optional[str] = Field(None, alias="job_employment_type")
    description: Optional[str] = Field(None, alias="job_description")
    apply_link: Optional[str] = Field(None, alias="job_apply_link")
    google_link: Optional[str] = Field(None, alias="job_google_link")

    # Salary information
    min_salary: Optional[float] = Field(None, alias="job_min_salary")
    max_salary: Optional[float] = Field(None, alias="job_max_salary")
    salary_currency: Optional[str] = Field(None, alias="job_salary_currency")
    salary_period: Optional[str] = Field(None, alias="job_salary_period")

    # Dates
    posted_at_timestamp: Optional[int] = Field(None, alias="job_posted_at_timestamp")
    posted_at_datetime: Optional[str] = Field(None, alias="job_posted_at_datetime_utc")
    expiration_timestamp: Optional[int] = Field(None, alias="job_offer_expiration_timestamp")
    expiration_datetime: Optional[str] = Field(None, alias="job_offer_expiration_datetime_utc")

    # Requirements
    required_experience: Optional[str] = Field(None, alias="job_required_experience")
    required_skills: List[str] = Field(default_factory=list, alias="job_required_skills")
    required_education: Optional[str] = Field(None, alias="job_required_education")
    experience_in_place_of_education: Optional[bool] = Field(None, alias="job_experience_in_place_of_education")

    # Additional info
    benefits: Optional[List[str]] = Field(None, alias="job_benefits")
    highlights: Optional[dict] = Field(None, alias="job_highlights")

    model_config = {"populate_by_name": True}

    @field_validator('required_skills', mode='before')
    @classmethod
    def validate_skills(cls, v):
        """Asegura que required_skills sea siempre una lista"""
        if v is None:
            return []
        if isinstance(v, str):
            return [v]
        return v

    @field_validator('benefits', mode='before')
    @classmethod
    def validate_benefits(cls, v):
        """Asegura que benefits sea siempre una lista o None"""
        if v is None:
            return None
        if isinstance(v, str):
            return [v]
        return v

    def get_location(self) -> str:
        """Retorna ubicación formateada"""
        parts = []
        if self.city:
            parts.append(self.city)
        if self.state:
            parts.append(self.state)
        if self.country:
            parts.append(self.country)
        return ", ".join(parts) if parts else "N/A"

    def get_salary_range(self) -> Optional[str]:
        """Retorna rango salarial formateado"""
        if not self.min_salary and not self.max_salary:
            return None

        currency = self.salary_currency or "USD"
        period = self.salary_period or "YEAR"

        if self.min_salary and self.max_salary:
            return f"{self.min_salary:,.0f} - {self.max_salary:,.0f} {currency}/{period}"
        elif self.min_salary:
            return f"{self.min_salary:,.0f}+ {currency}/{period}"
        else:  # self.max_salary
            return f"Up to {self.max_salary:,.0f} {currency}/{period}"

    def get_short_description(self, max_length: int = 300) -> str:
        """Retorna descripción truncada"""
        if not self.description:
            return "No disponible"

        desc = ' '.join(self.description.split())  # Limpia espacios
        if len(desc) <= max_length:
            return desc

        return desc[:max_length] + "..."
