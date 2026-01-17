#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Dashboard for LinkedIn Job Scraper - FIXED VERSION
"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
from pathlib import Path
import sys
import threading
import time

from src.utils.config import Config
from src.utils.logger import setup_logger
from src.api.jsearch_client import JSearchClient
from src.services.job_service import JobService
from src.services.salary_service import SalaryService
from src.services.export_service import ExportService
from config.predefined_searches import PREDEFINED_SEARCHES, SEARCH_TITLES

app = Flask(__name__)
CORS(app)

# Global cache for API results
search_cache = {}
cache_timestamp = {}

# Initialize services
try:
    config = Config.load()
    logger = setup_logger(
        level=config.log_level,
        log_dir=config.log_dir,
        log_to_file=config.log_to_file,
        log_to_console=False
    )
    
    api_client = JSearchClient(config.api_key, config.api_host, config)
    job_service = JobService(api_client)
    salary_service = SalaryService(api_client)
    export_service = ExportService(config.output_dir)
    
    print("✅ All services initialized successfully")
    
except Exception as e:
    print(f"❌ Error initializing services: {e}")
    sys.exit(1)


def perform_search_background(search_id):
    """Perform search in background to avoid timeout"""
    try:
        if search_id not in PREDEFINED_SEARCHES:
            search_cache[search_id] = {'error': 'Invalid search ID'}
            return
        
        params = PREDEFINED_SEARCHES[search_id]
        print(f"[BG] Starting search for {search_id}: {params.query}")
        
        # Search jobs
        jobs = job_service.search_jobs(params)
        print(f"[BG] Found {len(jobs)} jobs")
        
        # Format jobs
        jobs_data = []
        for job in jobs:
            try:
                job_dict = {
                    'id': job.job_id,
                    'title': job.title or 'N/A',
                    'company': job.employer_name or 'N/A',
                    'location': job.get_location(),
                    'salary': job.get_salary_range() or 'Not specified',
                    'employment_type': job.employment_type or 'N/A',
                    'is_remote': job.is_remote,
                    'posted_at': job.posted_at_datetime or 'N/A',
                    'description': job.get_short_description(500),
                    'required_experience': job.required_experience or 'Not specified',
                    'required_education': job.required_education or 'Not specified',
                    'apply_link': job.apply_link or '#'
                }
                jobs_data.append(job_dict)
            except Exception as e:
                logger.warning(f"Error formatting job: {e}")
                continue
        
        search_cache[search_id] = {
            'success': True,
            'title': SEARCH_TITLES.get(search_id, 'Search Results'),
            'total': len(jobs_data),
            'jobs': jobs_data
        }
        cache_timestamp[search_id] = time.time()
        print(f"[BG] Search complete - cached {len(jobs_data)} jobs")
        
    except Exception as e:
        print(f"[BG] Error in search: {e}")
        search_cache[search_id] = {'success': False, 'error': str(e)}


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html', searches=SEARCH_TITLES)


@app.route('/api/search/<search_id>', methods=['GET'])
def api_search(search_id):
    """API endpoint for predefined searches"""
    try:
        # If already cached and recent (10 mins), return cached
        if search_id in search_cache:
            if search_id in cache_timestamp and time.time() - cache_timestamp[search_id] < 600:
                print(f"[API] Returning cached results for {search_id}")
                return jsonify(search_cache[search_id])
        
        # Check if search is in progress
        if search_id in search_cache and 'total' in search_cache[search_id]:
            print(f"[API] Returning in-progress results for {search_id}")
            return jsonify(search_cache[search_id])
        
        # Start background search
        if search_id not in search_cache:
            print(f"[API] Starting async search for {search_id}")
            search_cache[search_id] = {'status': 'searching', 'progress': 0}
            
            thread = threading.Thread(target=perform_search_background, args=(search_id,))
            thread.daemon = True
            thread.start()
            
            # Return immediate response
            return jsonify({
                'success': True,
                'status': 'searching',
                'message': 'Search in progress, please wait...',
                'jobs': []
            })
        
        # Return current status
        return jsonify(search_cache.get(search_id, {'status': 'waiting'}))
    
    except Exception as e:
        print(f"[API] Error: {e}")
        logger.error(f"Search error: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/search-status/<search_id>', methods=['GET'])
def api_search_status(search_id):
    """Check status of a search"""
    if search_id in search_cache:
        return jsonify(search_cache[search_id])
    return jsonify({'status': 'not_found'}), 404


@app.route('/api/custom-search', methods=['POST'])
def api_custom_search():
    """API endpoint for custom searches"""
    try:
        data = request.json
        print(f"[API] Custom search: {data}")
        
        from src.models.search_params import SearchParameters
        
        params = SearchParameters(
            query=data.get('query', ''),
            country=data.get('country', 'in'),
            date_posted=data.get('date_posted', 'week'),
            work_from_home=data.get('work_from_home', False),
            employment_types=data.get('employment_types'),
            num_pages=min(int(data.get('num_pages', 1)), 10)
        )
        
        print(f"[API] Searching: {params.query}")
        
        # Search jobs
        jobs = job_service.search_jobs(params)
        print(f"[API] Found {len(jobs)} jobs")
        
        # Format jobs
        jobs_data = []
        for job in jobs:
            try:
                job_dict = {
                    'id': job.job_id,
                    'title': job.title or 'N/A',
                    'company': job.employer_name or 'N/A',
                    'location': job.get_location(),
                    'salary': job.get_salary_range() or 'Not specified',
                    'employment_type': job.employment_type or 'N/A',
                    'is_remote': job.is_remote,
                    'posted_at': job.posted_at_datetime or 'N/A',
                    'description': job.get_short_description(500),
                    'required_experience': job.required_experience or 'Not specified',
                    'required_education': job.required_education or 'Not specified',
                    'apply_link': job.apply_link or '#'
                }
                jobs_data.append(job_dict)
            except Exception as e:
                logger.warning(f"Error formatting job: {e}")
                continue
        
        response = {
            'success': True,
            'title': f'Custom Search: {params.query}',
            'total': len(jobs_data),
            'jobs': jobs_data
        }
        print(f"[API] Returning {len(jobs_data)} jobs")
        return jsonify(response)
    
    except Exception as e:
        print(f"[API] Custom search error: {e}")
        logger.error(f"Custom search error: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/job-details/<job_id>', methods=['GET'])
def api_job_details(job_id):
    """API endpoint for job details"""
    try:
        country = request.args.get('country', 'in')
        job = job_service.get_job_details(job_id, country)
        
        return jsonify({
            'id': job.job_id,
            'title': job.title,
            'company': job.employer_name,
            'location': job.get_location(),
            'salary': job.get_salary_range() or 'Not specified',
            'employment_type': job.employment_type or 'N/A',
            'is_remote': job.is_remote,
            'posted_at': job.posted_at_datetime or 'N/A',
            'description': job.description or 'No description available',
            'required_experience': job.required_experience or 'Not specified',
            'required_education': job.required_education or 'Not specified',
            'apply_link': job.apply_link or '#'
        })
    
    except Exception as e:
        logger.error(f"Job details error: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/salary/<job_title>', methods=['GET'])
def api_salary(job_title):
    """API endpoint for salary information"""
    try:
        country = request.args.get('country', 'in')
        experience = request.args.get('experience', 'ALL')
        
        salary_info = salary_service.get_estimated_salary(
            job_title=job_title,
            country=country,
            experience_level=experience
        )
        
        return jsonify({
            'job_title': job_title,
            'country': country,
            'experience': experience,
            'data': salary_info
        })
    
    except Exception as e:
        logger.error(f"Salary error: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = 5000
    print(f"\n🚀 Starting Flask app on port {port}...")
    print(f"📱 Open browser: http://localhost:{port}")
    print(f"🔍 API Status: http://localhost:{port}/api/search/2\n")
    
    app.run(debug=False, use_reloader=False, port=port, host='0.0.0.0', threaded=True)
