#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nombre del archivo: predefined_searches.py
Descripción: Búsquedas predefinidas para el menú principal del scraper.
             Incluye búsquedas comunes de roles tech en diferentes países y modalidades.

Autor: Hex686f6c61
Repositorio: https://github.com/Hex686f6c61/linkedIN-Scraper
Versión: 3.0.0
Fecha: 2025-12-08
"""
from src.models.search_params import SearchParameters


# Diccionario de búsquedas predefinidas
PREDEFINED_SEARCHES = {
    "2": SearchParameters(
        query="project manager scrum agile",
        country="es",
        employment_types="FULLTIME",
        date_posted="week"
    ),
    "3": SearchParameters(
        query="software engineer",
        country="es",
        employment_types="FULLTIME",
        date_posted="week"
    ),
    "4": SearchParameters(
        query="data scientist python machine learning",
        country="es",
        employment_types="FULLTIME",
        date_posted="week"
    ),
    "5": SearchParameters(
        query="frontend developer react javascript",
        country="es",
        employment_types="FULLTIME",
        date_posted="week"
    ),
    "6": SearchParameters(
        query="backend developer python java",
        country="us",
        employment_types="FULLTIME",
        date_posted="week"
    ),
    "7": SearchParameters(
        query="machine learning engineer tensorflow pytorch",
        country="us",
        employment_types="FULLTIME",
        date_posted="3days"
    ),
    "8": SearchParameters(
        query="full stack developer node react python",
        country="us",
        employment_types="FULLTIME",
        date_posted="week"
    ),
    "9": SearchParameters(
        query="devops engineer kubernetes docker aws",
        country="gb",
        employment_types="FULLTIME",
        date_posted="week"
    ),
    "10": SearchParameters(
        query="senior software engineer remote",
        country="us",
        work_from_home=True,
        employment_types="FULLTIME",
        date_posted="week"
    )
}


# Títulos descriptivos para cada búsqueda
SEARCH_TITLES = {
    "2": "Project Manager en España",
    "3": "Software Engineer en España",
    "4": "Data Scientist en España",
    "5": "Frontend Developer en España",
    "6": "Backend Developer en Estados Unidos",
    "7": "Machine Learning Engineer en Estados Unidos",
    "8": "Full Stack Developer en Estados Unidos",
    "9": "DevOps Engineer en Reino Unido",
    "10": "Senior Software Engineer - Remoto Global"
}
