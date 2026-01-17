// LinkedIn Job Scraper Dashboard - JavaScript

let currentResults = [];
let pollInterval = null;

// Tab switching
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.dataset.tab;
        
        // Update active button
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        // Update active tab content
        document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
        document.getElementById(`${tabName}-tab`).classList.add('active');
    });
});

// Polling function for search results
async function pollSearchResults(searchId, maxAttempts = 30) {
    let attempts = 0;
    
    return new Promise((resolve, reject) => {
        const poll = async () => {
            attempts++;
            try {
                const response = await fetch(`/api/search/${searchId}`);
                const data = await response.json();
                
                if (data.status === 'searching') {
                    // Still searching, update UI
                    document.getElementById('totalJobs').textContent = '⏳ Searching...';
                    
                    if (attempts < maxAttempts) {
                        // Wait 2 seconds and try again
                        setTimeout(poll, 2000);
                        return;
                    } else {
                        reject(new Error('Search timeout'));
                        return;
                    }
                }
                
                // Results ready
                clearInterval(pollInterval);
                resolve(data);
                
            } catch (error) {
                clearInterval(pollInterval);
                reject(error);
            }
        };
        
        poll();
    });
}

// Search predefined jobs
async function searchPredefined(searchId) {
    showLoading(true);
    hideError();
    
    try {
        // Start async search
        const response = await fetch(`/api/search/${searchId}`);
        const initialData = await response.json();
        
        if (!response.ok) {
            throw new Error(initialData.error || 'Search failed');
        }
        
        // If status is searching, poll for results
        if (initialData.status === 'searching') {
            const data = await pollSearchResults(searchId);
            currentResults = data.jobs || [];
            displayResults(data);
        } else {
            // Results available immediately
            currentResults = initialData.jobs || [];
            displayResults(initialData);
        }
        
    } catch (error) {
        showError(error.message);
    } finally {
        showLoading(false);
    }
}

// Custom search
async function performCustomSearch() {
    showLoading(true);
    hideError();
    
    try {
        const formData = {
            query: document.getElementById('query').value,
            country: document.getElementById('country').value,
            date_posted: document.getElementById('date_posted').value,
            employment_types: document.getElementById('employment_types').value || null,
            work_from_home: document.getElementById('work_from_home').checked,
            num_pages: document.getElementById('num_pages').value
        };
        
        if (!formData.query) {
            throw new Error('Please enter a search query');
        }
        
        const response = await fetch('/api/custom-search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Search failed');
        }
        
        currentResults = data.jobs;
        displayResults(data);
    } catch (error) {
        showError(error.message);
    } finally {
        showLoading(false);
    }
}

// Salary search
async function performSalarySearch() {
    showLoading(true);
    hideError();
    
    try {
        const jobTitle = document.getElementById('salary_job_title').value;
        const location = document.getElementById('salary_location').value;
        const experience = document.getElementById('salary_experience').value;
        
        if (!jobTitle) {
            throw new Error('Please enter a job title');
        }
        
        const params = new URLSearchParams({
            location: location,
            experience: experience
        });
        
        const response = await fetch(`/api/salary/${encodeURIComponent(jobTitle)}?${params}`);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Salary query failed');
        }
        
        displaySalaryResults(jobTitle, data);
    } catch (error) {
        showError(error.message);
    } finally {
        showLoading(false);
    }
}

// Display job results
function displayResults(data) {
    document.getElementById('totalJobs').textContent = data.total;
    document.getElementById('resultsTitle').textContent = data.title;
    document.getElementById('salaryResults').classList.add('hidden');
    
    const grid = document.getElementById('jobsGrid');
    grid.innerHTML = '';
    
    if (data.jobs.length === 0) {
        grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 40px;"><p>No jobs found</p></div>';
    } else {
        data.jobs.forEach(job => {
            const card = createJobCard(job);
            grid.appendChild(card);
        });
    }
    
    document.getElementById('resultsSection').classList.remove('hidden');
    window.scrollTo({ top: document.getElementById('resultsSection').offsetTop - 100, behavior: 'smooth' });
}

// Create job card
function createJobCard(job) {
    const card = document.createElement('div');
    card.className = 'job-card';
    
    const remoteStatus = job.is_remote ? '🌍 Remote' : '📍 On-site';
    const applyButton = job.apply_link && job.apply_link !== '#' 
        ? `<a href="${job.apply_link}" target="_blank" class="btn-apply"><i class="fas fa-external-link-alt"></i> Apply</a>`
        : `<button class="btn-apply" disabled style="opacity: 0.6;"><i class="fas fa-ban"></i> No Link</button>`;
    
    card.innerHTML = `
        <div class="job-header">
            <div class="job-title">${escapeHtml(job.title)}</div>
            <div class="job-company"><i class="fas fa-building"></i> ${escapeHtml(job.company)}</div>
        </div>
        
        <div class="job-body">
            <div class="job-meta">
                <div class="meta-item">
                    <i class="fas fa-map-marker-alt"></i>
                    <span class="meta-label">Location:</span>
                    <span class="meta-value">${escapeHtml(job.location)}</span>
                </div>
                
                <div class="meta-item">
                    <i class="fas fa-dollar-sign"></i>
                    <span class="meta-label">Salary:</span>
                    <span class="meta-value salary">${escapeHtml(job.salary)}</span>
                </div>
                
                <div class="meta-item">
                    <i class="fas fa-briefcase"></i>
                    <span class="meta-label">Type:</span>
                    <span class="meta-value">${escapeHtml(job.employment_type)}</span>
                </div>
                
                <div class="meta-item">
                    <i class="fas fa-globe"></i>
                    <span class="meta-label">Work:</span>
                    <span class="meta-value remote">${remoteStatus}</span>
                </div>
                
                <div class="meta-item">
                    <i class="fas fa-calendar"></i>
                    <span class="meta-label">Posted:</span>
                    <span class="meta-value">${escapeHtml(job.posted_at)}</span>
                </div>
            </div>
            
            <div class="job-description">
                <strong>Description:</strong><br>${escapeHtml(job.description)}
            </div>
            
            <div class="job-meta">
                <div class="meta-item">
                    <i class="fas fa-user"></i>
                    <span class="meta-label">Experience:</span>
                    <span class="meta-value">${escapeHtml(job.required_experience)}</span>
                </div>
                
                <div class="meta-item">
                    <i class="fas fa-graduation-cap"></i>
                    <span class="meta-label">Education:</span>
                    <span class="meta-value">${escapeHtml(job.required_education)}</span>
                </div>
            </div>
        </div>
        
        <div class="job-footer">
            <button class="btn-details" onclick="showJobDetails('${escapeHtml(job.id)}')">
                <i class="fas fa-info-circle"></i> Details
            </button>
            ${applyButton}
        </div>
    `;
    
    return card;
}

// Show job details modal (optional enhancement)
function showJobDetails(jobId) {
    alert(`Job ID: ${jobId}\n\nFull details can be shown in a modal dialog`);
}

// Display salary results
function displaySalaryResults(jobTitle, data) {
    document.getElementById('salaryResults').classList.remove('hidden');
    document.getElementById('jobsGrid').innerHTML = '';
    document.getElementById('resultsTitle').textContent = `Salary Info for ${jobTitle}`;
    
    if (data.salaries.length === 0) {
        document.getElementById('salaryResults').innerHTML = 
            '<div style="padding: 40px; text-align: center;"><p>No salary data found</p></div>';
    } else {
        let table = `
            <table class="salary-table">
                <thead>
                    <tr>
                        <th><i class="fas fa-briefcase"></i> Job Title</th>
                        <th><i class="fas fa-map-marker-alt"></i> Location</th>
                        <th><i class="fas fa-dollar-sign"></i> Median</th>
                        <th><i class="fas fa-chart-bar"></i> Range</th>
                        <th><i class="fas fa-source"></i> Source</th>
                    </tr>
                </thead>
                <tbody>
        `;
        
        data.salaries.forEach(salary => {
            table += `
                <tr>
                    <td>${escapeHtml(salary.job_title)}</td>
                    <td>${escapeHtml(salary.location)}</td>
                    <td><strong>${salary.median_salary}</strong></td>
                    <td>${salary.salary_range}</td>
                    <td>${escapeHtml(salary.publisher)}</td>
                </tr>
            `;
        });
        
        table += `
                </tbody>
            </table>
        `;
        
        document.getElementById('salaryResults').innerHTML = table;
    }
    
    document.getElementById('resultsSection').classList.remove('hidden');
    window.scrollTo({ top: document.getElementById('resultsSection').offsetTop - 100, behavior: 'smooth' });
}

// Export to CSV
function exportToCSV() {
    if (currentResults.length === 0) {
        alert('No results to export');
        return;
    }
    
    let csv = 'Job Title,Company,Location,Salary,Employment Type,Remote,Posted\n';
    
    currentResults.forEach(job => {
        csv += `"${job.title}","${job.company}","${job.location}","${job.salary}","${job.employment_type}","${job.is_remote ? 'Yes' : 'No'}","${job.posted_at}"\n`;
    });
    
    downloadFile(csv, 'jobs.csv', 'text/csv');
}

// Export to JSON
function exportToJSON() {
    if (currentResults.length === 0) {
        alert('No results to export');
        return;
    }
    
    const json = JSON.stringify(currentResults, null, 2);
    downloadFile(json, 'jobs.json', 'application/json');
}

// Download file helper
function downloadFile(content, filename, type) {
    const element = document.createElement('a');
    element.setAttribute('href', `data:${type};charset=utf-8,` + encodeURIComponent(content));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

// Utility functions
function showLoading(show) {
    document.getElementById('loadingSpinner').classList.toggle('hidden', !show);
}

function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = `❌ Error: ${message}`;
    errorDiv.classList.remove('hidden');
}

function hideError() {
    document.getElementById('errorMessage').classList.add('hidden');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Hide loading on page load
window.addEventListener('load', () => {
    showLoading(false);
});
