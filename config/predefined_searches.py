#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: predefined_searches.py
Description: Predefined searches for Indian job market.
             Includes common tech role searches across major Indian cities.

Author: Hex686f6c61
Repository: https://github.com/Hex686f6c61/linkedIN-Scraper
Version: 3.0.0
Date: 2025-12-08
"""
from src.models.search_params import SearchParameters


# Dictionary of predefined searches - India focused
PREDEFINED_SEARCHES = {
    "2": SearchParameters(
        query="software engineer india bangalore",
        country="in",
        employment_types="FULLTIME",
        date_posted="week"
    ),
    "3": SearchParameters(
        query="data scientist machine learning india",
        country="in",
        employment_types="FULLTIME",
        date_posted="week"
    ),
    "4": SearchParameters(
        query="frontend developer react angular india",
        country="in",
        employment_types="FULLTIME",
        date_posted="week"
    ),
    "5": SearchParameters(
        query="backend developer python java india",
        country="in",
        employment_types="FULLTIME",
        date_posted="week"
    ),
    "6": SearchParameters(
        query="devops engineer kubernetes docker india",
        country="in",
        employment_types="FULLTIME",
        date_posted="week"
    ),
    "7": SearchParameters(
        query="full stack developer nodejs react india",
        country="in",
        employment_types="FULLTIME",
        date_posted="week"
    ),
    "8": SearchParameters(
        query="machine learning engineer tensorflow india",
        country="in",
        employment_types="FULLTIME",
        date_posted="3days"
    ),
    "9": SearchParameters(
        query="project manager scrum agile india",
        country="in",
        employment_types="FULLTIME",
        date_posted="week"
    ),
    "10": SearchParameters(
        query="cloud engineer aws gcp azure india",
        country="in",
        employment_types="FULLTIME",
        date_posted="week"
    )
}


# Descriptive titles for each search
SEARCH_TITLES = {
    "2": "Software Engineer - India (Bangalore)",
    "3": "Data Scientist - India (Machine Learning)",
    "4": "Frontend Developer - India (React/Angular)",
    "5": "Backend Developer - India (Python/Java)",
    "6": "DevOps Engineer - India (Kubernetes)",
    "7": "Full Stack Developer - India (Node.js)",
    "8": "Machine Learning Engineer - India",
    "9": "Project Manager - India (Scrum/Agile)",
    "10": "Cloud Engineer - India (AWS/GCP/Azure)"
}
