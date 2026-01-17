/**
 * FREE-TIER OPTIMIZED: JSON Database Schema
 * All data stored in JSON files instead of MongoDB
 * ✅ No external database cost
 * ✅ GitHub Codespace compatible
 * ✅ Version control friendly
 */

// ============================================================================
// 1. DATA STRUCTURE: data/jobs.json (Primary Job Cache)
// ============================================================================

export interface Job {
  id: string; // unique ID: "job_<timestamp>_<random>"
  external_id: string; // OpenWeb Ninja job ID
  title: string; // "Senior Python Developer"
  company: string; // "Google India"
  location: string; // "Bangalore, Karnataka"
  country: string; // "India"
  
  // Salary Information
  salary_min: number | null; // 500000 (in INR or local currency)
  salary_max: number | null; // 800000
  salary_currency: string; // "INR"
  salary_period: string; // "monthly" | "yearly"
  
  // Job Details
  description: string; // Full job description
  employment_type: string; // "full-time" | "contract" | "freelance"
  experience_level: string; // "entry" | "mid" | "senior"
  experience_years: number | null; // 5
  
  // Skills & Requirements
  skills: string[]; // ["Python", "FastAPI", "PostgreSQL"]
  required_skills: string[];
  preferred_skills: string[];
  education_required: string | null; // "Bachelor's in CS"
  
  // Links & Metadata
  apply_url: string; // Direct link to apply
  company_website: string | null;
  company_logo_url: string | null;
  is_remote: boolean; // true | false
  remote_type: string; // "fully_remote" | "hybrid" | "on_site"
  
  // Tracking Information
  source: string; // "openwebninja" | "manual"
  source_metadata: {
    api_keyword: string; // "python developer bangalore"
    api_request_id: string;
  };
  
  fetched_at: string; // ISO timestamp when this job was fetched
  posted_at: string | null; // When job was posted (if available)
  job_status: string; // "active" | "closed" | "expired" | "pending_verification"
  
  // Deduplication
  is_duplicate: boolean; // false (unless merged with another)
  canonical_id: string | null; // null (or ID of duplicate job if this is duplicate)
  dedup_key: string; // hash of (title + company + location) for deduplication
  
  // Matching & User Interest
  match_score: number | null; // Set by matching engine (0-1)
  user_applications: number; // 0 (incremented when user applies)
  user_saves: number; // 0 (incremented when user bookmarks)
  
  // Admin & Compliance
  is_verified: boolean; // true after manual verification
  is_hidden: boolean; // false (set to true to hide without deleting)
  compliance_flags: string[]; // ["suspicious_salary", "invalid_url"]
}

export interface JobsJSON {
  jobs: Job[];
  metadata: {
    total_jobs: number; // 10234
    last_updated: string; // ISO timestamp
    schema_version: string; // "1.0"
    data_source: string; // "openwebninja"
    monthly_refresh: string; // "2025-01"
  };
  indexes: {
    by_external_id: { [key: string]: string }; // external_id -> id
    by_company: { [key: string]: string[] }; // company -> [id1, id2, ...]
    by_location: { [key: string]: string[] }; // location -> [id1, id2, ...]
    by_skills: { [key: string]: string[] }; // skill -> [id1, id2, ...]
    by_status: { [key: string]: string[] }; // status -> [id1, id2, ...]
  };
}

const exampleJobsJSON: JobsJSON = {
  jobs: [
    {
      id: "job_1705500000_abc123",
      external_id: "jsearch_12345",
      title: "Senior Python Developer",
      company: "Google India",
      location: "Bangalore, Karnataka",
      country: "India",
      salary_min: 500000,
      salary_max: 800000,
      salary_currency: "INR",
      salary_period: "yearly",
      description: "We're looking for...",
      employment_type: "full-time",
      experience_level: "senior",
      experience_years: 5,
      skills: ["Python", "FastAPI", "PostgreSQL", "Docker"],
      required_skills: ["Python", "FastAPI"],
      preferred_skills: ["PostgreSQL", "Docker"],
      education_required: "Bachelor's in Computer Science",
      apply_url: "https://careers.google.com/job/123",
      company_website: "https://google.com",
      company_logo_url: "https://...",
      is_remote: false,
      remote_type: "hybrid",
      source: "openwebninja",
      source_metadata: {
        api_keyword: "python developer bangalore",
        api_request_id: "req_001",
      },
      fetched_at: "2025-01-17T10:30:00Z",
      posted_at: "2025-01-10T09:00:00Z",
      job_status: "active",
      is_duplicate: false,
      canonical_id: null,
      dedup_key: "senior-python-developer_google-india_bangalore-karnataka",
      match_score: 0.92,
      user_applications: 0,
      user_saves: 0,
      is_verified: true,
      is_hidden: false,
      compliance_flags: [],
    },
  ],
  metadata: {
    total_jobs: 10234,
    last_updated: "2025-01-17T10:30:00Z",
    schema_version: "1.0",
    data_source: "openwebninja",
    monthly_refresh: "2025-01",
  },
  indexes: {
    by_external_id: {
      jsearch_12345: "job_1705500000_abc123",
    },
    by_company: {
      "google-india": ["job_1705500000_abc123"],
    },
    by_location: {
      "bangalore-karnataka": ["job_1705500000_abc123"],
    },
    by_skills: {
      python: ["job_1705500000_abc123"],
      fastapi: ["job_1705500000_abc123"],
    },
    by_status: {
      active: ["job_1705500000_abc123"],
    },
  },
};

// ============================================================================
// 2. DATA STRUCTURE: data/keywords.json (Keyword Tracking & Deduplication)
// ============================================================================

export interface Keyword {
  keyword: string; // "python developer bangalore"
  keyword_normalized: string; // for deduplication
  fetched_at: string; // ISO timestamp of last fetch
  next_refresh_date: string; // When this keyword should be refreshed (7 days later)
  jobs_returned: number; // 245 jobs returned from last fetch
  request_count: number; // 1 (how many times fetched)
  status: string; // "active" | "paused" | "completed"
  notes: string; // "Core keyword for Q1"
  created_at: string;
  updated_at: string;
}

export interface KeywordsJSON {
  keywords: Keyword[];
  metadata: {
    total_keywords: number;
    active_keywords: number;
    last_updated: string;
    refresh_day_of_week: number; // 0-6 (Sunday to Saturday), e.g., 6 = Saturday
    refresh_time_utc: string; // "02:00" for 2:00 AM UTC
  };
}

const exampleKeywordsJSON: KeywordsJSON = {
  keywords: [
    {
      keyword: "python developer bangalore",
      keyword_normalized: "python-developer-bangalore",
      fetched_at: "2025-01-17T10:30:00Z",
      next_refresh_date: "2025-01-24T10:30:00Z",
      jobs_returned: 245,
      request_count: 1,
      status: "active",
      notes: "Core keyword for backend development",
      created_at: "2025-01-17T10:30:00Z",
      updated_at: "2025-01-17T10:30:00Z",
    },
    {
      keyword: "data scientist machine learning india",
      keyword_normalized: "data-scientist-machine-learning-india",
      fetched_at: "2025-01-16T14:15:00Z",
      next_refresh_date: "2025-01-23T14:15:00Z",
      jobs_returned: 189,
      request_count: 1,
      status: "active",
      notes: "Core keyword for AI/ML roles",
      created_at: "2025-01-16T14:15:00Z",
      updated_at: "2025-01-16T14:15:00Z",
    },
  ],
  metadata: {
    total_keywords: 2,
    active_keywords: 2,
    last_updated: "2025-01-17T10:30:00Z",
    refresh_day_of_week: 6, // Saturday
    refresh_time_utc: "02:00", // 2:00 AM
  },
};

// ============================================================================
// 3. DATA STRUCTURE: data/usage.json (API Usage Tracking & Hard Limits)
// ============================================================================

export interface MonthlyUsage {
  month: string; // "2025-01"
  year: number; // 2025
  month_number: number; // 1-12
  
  total_requests: number; // 45 (current usage)
  remaining_requests: number; // 155 (200 - 45)
  max_requests: number; // 200 (free tier limit)
  
  warning_80_percent_triggered: boolean; // true when requests >= 160
  warning_80_percent_triggered_at: string | null; // ISO timestamp
  
  hard_limit_triggered: boolean; // true when requests >= 180
  hard_limit_triggered_at: string | null; // ISO timestamp
  
  requests_by_date: {
    [date: string]: number; // "2025-01-17": 5
  };
  
  requests_by_keyword: {
    [keyword: string]: number; // "python developer bangalore": 1
  };
  
  created_at: string;
  updated_at: string;
}

export interface UsageJSON {
  current_month: MonthlyUsage;
  previous_months: MonthlyUsage[];
  metadata: {
    free_tier_limit: number; // 200
    warning_threshold_percent: number; // 80
    hard_stop_threshold_percent: number; // 90
    hard_stop_request_count: number; // 180
    reset_day: number; // 1 (first day of month)
    reset_utc_hour: number; // 0 (midnight UTC)
  };
}

const exampleUsageJSON: UsageJSON = {
  current_month: {
    month: "2025-01",
    year: 2025,
    month_number: 1,
    total_requests: 45,
    remaining_requests: 155,
    max_requests: 200,
    warning_80_percent_triggered: false,
    warning_80_percent_triggered_at: null,
    hard_limit_triggered: false,
    hard_limit_triggered_at: null,
    requests_by_date: {
      "2025-01-17": 5,
      "2025-01-16": 3,
      "2025-01-15": 2,
    },
    requests_by_keyword: {
      "python developer bangalore": 1,
      "data scientist india": 1,
    },
    created_at: "2025-01-01T00:00:00Z",
    updated_at: "2025-01-17T10:30:00Z",
  },
  previous_months: [],
  metadata: {
    free_tier_limit: 200,
    warning_threshold_percent: 80,
    hard_stop_threshold_percent: 90,
    hard_stop_request_count: 180,
    reset_day: 1,
    reset_utc_hour: 0,
  },
};

// ============================================================================
// 4. DATA STRUCTURE: data/scraping-logs.json (Audit Trail & Debugging)
// ============================================================================

export interface ScrapingLog {
  id: string; // "log_1705500000_abc123"
  timestamp: string; // ISO timestamp
  status: string; // "success" | "failure" | "partial_success" | "skipped"
  
  // Request Details
  keyword: string; // "python developer bangalore"
  request_type: string; // "manual" | "scheduled" | "refresh"
  triggered_by: string; // "admin:john@example.com" | "cron:weekly"
  
  // Results
  jobs_fetched: number; // 245
  jobs_added: number; // 200 (new jobs)
  jobs_updated: number; // 45 (existing jobs refreshed)
  duplicates_removed: number; // 10
  
  // Error Handling
  error: string | null; // null or error message
  error_code: string | null; // "RATE_LIMIT" | "INVALID_KEYWORD" | null
  retry_attempt: number; // 0, 1, 2, etc.
  
  // Duration
  duration_ms: number; // 5432 (milliseconds)
  
  // API Cost
  api_requests_used: number; // 1
  monthly_usage_after: number; // 46
  
  metadata: {
    api_response_code: number; // 200
    jobs_skipped_reason: string[]; // ["invalid_url", "missing_salary"]
  };
}

export interface ScrapingLogsJSON {
  logs: ScrapingLog[];
  metadata: {
    total_logs: number;
    success_count: number;
    failure_count: number;
    last_updated: string;
  };
}

const exampleScrapingLogsJSON: ScrapingLogsJSON = {
  logs: [
    {
      id: "log_1705500000_abc123",
      timestamp: "2025-01-17T10:30:00Z",
      status: "success",
      keyword: "python developer bangalore",
      request_type: "manual",
      triggered_by: "admin:user@example.com",
      jobs_fetched: 245,
      jobs_added: 200,
      jobs_updated: 45,
      duplicates_removed: 10,
      error: null,
      error_code: null,
      retry_attempt: 0,
      duration_ms: 5432,
      api_requests_used: 1,
      monthly_usage_after: 46,
      metadata: {
        api_response_code: 200,
        jobs_skipped_reason: ["invalid_url"],
      },
    },
  ],
  metadata: {
    total_logs: 1,
    success_count: 1,
    failure_count: 0,
    last_updated: "2025-01-17T10:30:00Z",
  },
};

// ============================================================================
// 5. DATA STRUCTURE: data/search-cache.json (In-Memory Search Index)
// ============================================================================

export interface SearchCache {
  timestamp: string; // When this cache was built
  skills_index: {
    [skill: string]: string[]; // "python": ["job_1", "job_2"]
  };
  company_index: {
    [company: string]: string[]; // "google": ["job_1", "job_3"]
  };
  location_index: {
    [location: string]: string[]; // "bangalore": ["job_1", "job_2"]
  };
  combined_index: {
    [combined_key: string]: string[]; // "python_bangalore": ["job_1"]
  };
}

// ============================================================================
// 6. DIRECTORY STRUCTURE
// ============================================================================

/*
jobscrapper/
├── data/
│   ├── jobs.json                 (10,000+ jobs, ~5MB)
│   ├── keywords.json             (10-50 keywords)
│   ├── usage.json                (monthly API usage)
│   ├── scraping-logs.json        (audit trail)
│   ├── search-cache.json         (in-memory index, recreated on startup)
│   └── backups/
│       ├── jobs.backup.2025-01-17.json
│       ├── keywords.backup.2025-01-17.json
│       └── usage.backup.2025-01-17.json
│
├── src/
│   ├── services/
│   │   ├── jsonDatabase.ts       (atomic read/write)
│   │   ├── usageTracker.ts       (monthly limit enforcement)
│   │   ├── keywordDedup.ts       (prevent re-fetching)
│   │   └── jobCache.ts           (in-memory indexing)
│   ├── jobs/
│   │   └── scraperScheduler.ts   (cron with budget awareness)
│   └── controllers/
│       └── searchController.ts   (instant JSON queries)
│
└── .gitignore
    ├── node_modules/
    └── (data/ is committed for version control)
*/

export default {
  exampleJobsJSON,
  exampleKeywordsJSON,
  exampleUsageJSON,
  exampleScrapingLogsJSON,
};
