#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: salary.py
Descripción: Modelo Pydantic para representar información salarial.
             Incluye rangos salariales, salario mediano y métodos de formateo.

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
from typing import Optional
from pydantic import BaseModel, Field


class SalaryInfo(BaseModel):
    """Modelo que representa información salarial"""

    job_title: Optional[str] = Field(None, description="Título del puesto")
    location: Optional[str] = Field(None, description="Ubicación")
    publisher_name: Optional[str] = Field(None, description="Fuente de los datos")

    # Salary ranges
    min_salary: Optional[float] = Field(None, description="Salario mínimo")
    max_salary: Optional[float] = Field(None, description="Salario máximo")
    median_salary: Optional[float] = Field(None, description="Salario mediano")

    # Salary metadata
    salary_currency: str = Field(default="USD", description="Moneda")
    salary_period: str = Field(default="YEAR", description="Período (YEAR/MONTH/HOUR)")

    # Additional compensation
    additional_pay: Optional[str] = Field(None, description="Pago adicional (bonos, equity)")

    model_config = {"populate_by_name": True}

    def get_formatted_median(self) -> str:
        """Retorna salario mediano formateado"""
        if not self.median_salary:
            return "N/A"
        return f"{self.median_salary:,.0f} {self.salary_currency}/{self.salary_period}"

    def get_formatted_range(self) -> str:
        """Retorna rango salarial formateado"""
        if not self.min_salary and not self.max_salary:
            return "N/A"

        if self.min_salary and self.max_salary:
            return f"{self.min_salary:,.0f} - {self.max_salary:,.0f} {self.salary_currency}/{self.salary_period}"
        elif self.min_salary:
            return f"{self.min_salary:,.0f}+ {self.salary_currency}/{self.salary_period}"
        else:  # self.max_salary
            return f"Up to {self.max_salary:,.0f} {self.salary_currency}/{self.salary_period}"

    def has_salary_data(self) -> bool:
        """Verifica si tiene datos salariales"""
        return bool(self.min_salary or self.max_salary or self.median_salary)
