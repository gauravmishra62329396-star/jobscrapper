# 📊 DATABASE SCHEMAS & DATA MODELS README
**Complete JSON Schema Definitions**

---

## 📋 TABLE OF CONTENTS

1. Jobs Data Model
2. Keywords Data Model
3. Usage Data Model
4. Scraping Logs Model
5. User Data Model (Optional)
6. Schema Evolution & Versioning
7. Validation Rules
8. Migration Guide

---

## 1️⃣ JOBS DATA MODEL (data/jobs.json)

### Complete Schema

```json
{
  "jobs": [
    {
      "id": "job_1705500000_abc123",
      "external_id": "jsearch_12345",
      "title": "Senior Python Developer",
      "company": "Google India",
      "company_website": "https://google.com",
      "company_logo_url": "https://...",
      
      "location": "Bangalore, Karnataka",
      "location_components": {
        "city": "Bangalore",
        "state": "Karnataka",
        "country": "India",
        "country_code": "IN"
      },
      "country": "India",
      "is_remote": false,
      "remote_type": "hybrid",
      
      "salary_min": 500000,
      "salary_max": 800000,
      "salary_currency": "INR",
      "salary_period": "yearly",
      
      "employment_type": "full-time",
      "experience_level": "senior",
      "experience_years": 5,
      
      "description": "We're looking for a Senior Python Developer...",
      "requirements": [
        "5+ years of Python experience",
        "Experience with FastAPI",
        "PostgreSQL knowledge"
      ],
      "skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "Kubernetes"],
      "required_skills": ["Python", "FastAPI"],
      "preferred_skills": ["PostgreSQL", "Docker"],
      "education_required": "Bachelor's in Computer Science",
      
      "apply_url": "https://careers.google.com/job/123",
      "source": "openwebninja",
      "source_metadata": {
        "api_keyword": "python developer bangalore",
        "api_request_id": "req_001",
        "api_response_code": 200,
        "extraction_method": "jsearch_v2.1"
      },
      
      "fetched_at": "2025-01-17T10:30:00Z",
      "posted_at": "2025-01-10T09:00:00Z",
      "job_status": "active",
      
      "is_duplicate": false,
      "canonical_id": null,
      "dedup_key": "senior-python-developer_google-india_bangalore-karnataka",
      "last_seen_active": "2025-01-17T10:30:00Z",
      
      "is_verified": false,
      "is_hidden": false,
      "compliance_flags": [],
      
      "metadata": {
        "views": 0,
        "saves": 0,
        "applications": 0,
        "last_updated": "2025-01-17T10:30:00Z"
      }
    }
  ],
  "metadata": {
    "total_jobs": 10234,
    "last_updated": "2025-01-17T10:30:00Z",
    "schema_version": "1.0",
    "data_source": "openwebninja"
  }
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier (`job_<timestamp>_<random>`) |
| `external_id` | string | Yes | JSearch API job ID |
| `title` | string | Yes | Job title |
| `company` | string | Yes | Company name |
| `location` | string | Yes | Full location string |
| `salary_min` | number | No | Minimum salary (in local currency) |
| `salary_max` | number | No | Maximum salary |
| `employment_type` | string | Yes | full-time, part-time, contract, freelance |
| `skills` | string[] | Yes | Array of required skills |
| `apply_url` | string | Yes | Direct link to apply |
| `source` | string | Yes | Always "openwebninja" |
| `fetched_at` | string | Yes | ISO timestamp of fetch |
| `dedup_key` | string | Yes | Hash for deduplication |
| `job_status` | string | Yes | active, closed, expired |

### Validation Rules

```typescript
// Mandatory fields
- title: must not be empty
- company: must not be empty
- apply_url: must be valid URL
- source: must be "openwebninja"
- fetched_at: must be valid ISO date

// Constraints
- salary_min: if present, must be > 0
- salary_max: if present, must be >= salary_min
- skills: array length >= 1
- dedup_key: unique for each job

// Data type validation
- All URLs: must start with http:// or https://
- All currencies: must be 3-letter code (e.g., INR, USD)
- All dates: must be ISO 8601 format
```

### Usage Statistics

```
Size (1,000 jobs):      ~500 KB
Size (10,000 jobs):     ~5 MB
Size (50,000 jobs):     ~25 MB

Read performance:       <50ms for search
Write performance:      Append 100 jobs in <100ms
Memory footprint:       ~8MB for 10,000 jobs
Index memory:           ~2MB additional

Archival size:          5MB / 1000 jobs (compress 50%)
```

---

## 2️⃣ KEYWORDS DATA MODEL (data/keywords.json)

### Complete Schema

```json
{
  "keywords": [
    {
      "keyword": "python developer bangalore",
      "keyword_normalized": "python-developer-bangalore",
      "fetched_at": "2025-01-17T10:30:00Z",
      "next_refresh_date": "2025-01-24T10:30:00Z",
      "jobs_returned": 245,
      "request_count": 1,
      "status": "active",
      "notes": "Core keyword for backend roles",
      "created_at": "2025-01-17T10:30:00Z",
      "updated_at": "2025-01-17T10:30:00Z"
    },
    {
      "keyword": "data scientist machine learning india",
      "keyword_normalized": "data-scientist-machine-learning-india",
      "fetched_at": "2025-01-16T14:15:00Z",
      "next_refresh_date": "2025-01-23T14:15:00Z",
      "jobs_returned": 189,
      "request_count": 1,
      "status": "active",
      "notes": "Core keyword for AI/ML roles",
      "created_at": "2025-01-16T14:15:00Z",
      "updated_at": "2025-01-16T14:15:00Z"
    }
  ],
  "metadata": {
    "total_keywords": 10,
    "active_keywords": 10,
    "paused_keywords": 0,
    "last_updated": "2025-01-17T10:30:00Z"
  }
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `keyword` | string | Original keyword as entered |
| `keyword_normalized` | string | Lowercase, hyphenated (for dedup) |
| `fetched_at` | string | ISO timestamp of last fetch |
| `next_refresh_date` | string | When this keyword should be refreshed (7 days after fetch) |
| `jobs_returned` | number | Number of jobs returned from last fetch |
| `request_count` | number | How many times this keyword has been fetched |
| `status` | string | "active" or "paused" |
| `notes` | string | Admin notes |

### Refresh Schedule Logic

```
Rule 1: New keyword
  ├─ Not in keywords.json
  ├─ Fetch immediately (1 API request)
  └─ Set next_refresh_date = today + 7 days

Rule 2: Recently fetched keyword
  ├─ In keywords.json
  ├─ today < next_refresh_date
  ├─ Skip API call, use cache
  └─ Show "Cached X days ago"

Rule 3: Stale keyword
  ├─ In keywords.json
  ├─ today >= next_refresh_date
  ├─ Fetch on weekly CRON (Sunday 2 AM)
  └─ Set new next_refresh_date

Rule 4: Paused keyword
  ├─ status = "paused"
  ├─ Never refresh automatically
  ├─ Admin can manually refresh
  └─ Use "pause" to stop scraping
```

### Predefined Keywords (Core Set)

```json
[
  "python developer bangalore",
  "data scientist machine learning india",
  "frontend developer react india",
  "backend developer node.js india",
  "devops engineer kubernetes india",
  "qa engineer automation testing india",
  "fullstack developer mern node india",
  "cloud architect aws azure india",
  "ai engineer deep learning india",
  "systems engineer infrastructure india"
]
```

---

## 3️⃣ USAGE DATA MODEL (data/usage.json)

### Complete Schema

```json
{
  "current_month": {
    "month": "2025-01",
    "year": 2025,
    "month_number": 1,
    "total_requests": 45,
    "remaining_requests": 155,
    "max_requests": 200,
    
    "warning_80_percent_triggered": false,
    "warning_80_percent_triggered_at": null,
    
    "hard_limit_triggered": false,
    "hard_limit_triggered_at": null,
    
    "requests_by_date": {
      "2025-01-17": 5,
      "2025-01-16": 3,
      "2025-01-15": 2,
      "2025-01-14": 7,
      "2025-01-10": 10
    },
    
    "requests_by_keyword": {
      "python developer bangalore": 1,
      "data scientist india": 1,
      "frontend developer react": 3,
      "blockchain developer": 1
    },
    
    "requests_by_type": {
      "manual": 15,
      "scheduled": 30,
      "refresh": 0
    },
    
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-17T10:30:00Z"
  },
  
  "previous_months": [
    {
      "month": "2024-12",
      "year": 2024,
      "total_requests": 180,
      "remaining_requests": 20,
      "max_requests": 200
    }
  ],
  
  "metadata": {
    "free_tier_limit": 200,
    "warning_threshold_percent": 80,
    "hard_stop_threshold_percent": 90,
    "hard_stop_request_count": 180,
    "reset_day": 1,
    "reset_utc_hour": 0
  }
}
```

### Field Descriptions

| Field | Type | Purpose |
|-------|------|---------|
| `total_requests` | number | Cumulative API calls this month |
| `remaining_requests` | number | 200 - total_requests |
| `max_requests` | number | Always 200 (free tier) |
| `warning_80_percent_triggered` | boolean | Triggered when total >= 160 |
| `hard_limit_triggered` | boolean | Triggered when total >= 180 |
| `requests_by_date` | object | Daily breakdown |
| `requests_by_keyword` | object | Per-keyword breakdown |

### Enforcement Logic

```typescript
// Before EVERY API call:
if (current_month.total_requests >= 180) {
  return { allowed: false, error: "Hard limit reached" }
}

// Warn at 80%:
if (current_month.total_requests >= 160) {
  logger.warn("⚠️ 80% of budget used")
  // Admin sees warning on dashboard
}

// After successful API call:
current_month.total_requests += 1
current_month.remaining_requests = 200 - total_requests
current_month.requests_by_date[today] += 1
current_month.requests_by_keyword[keyword] += 1
save_to_disk()
```

### Auto-Reset Logic

```
Every month (Feb 1, Mar 1, etc):
  ├─ Archive current_month → previous_months[]
  ├─ Create new current_month:
  │   ├─ month = "2025-02"
  │   ├─ total_requests = 0
  │   ├─ remaining_requests = 200
  │   └─ Clear all request_by_* objects
  ├─ Keep previous_months history (12 months)
  └─ Save to disk

Triggered by:
  ├─ checkMonthBoundary() function
  ├─ Called on every API request
  └─ Also called on app startup
```

---

## 4️⃣ SCRAPING LOGS MODEL (data/scraping-logs.json)

### Complete Schema

```json
{
  "logs": [
    {
      "id": "log_1705500000_abc123",
      "timestamp": "2025-01-17T10:30:00Z",
      "status": "success",
      
      "keyword": "python developer bangalore",
      "request_type": "manual",
      "triggered_by": "admin:user@example.com",
      
      "jobs_fetched": 245,
      "jobs_added": 200,
      "jobs_updated": 45,
      "duplicates_removed": 10,
      
      "error": null,
      "error_code": null,
      "retry_attempt": 0,
      
      "duration_ms": 5432,
      
      "api_requests_used": 1,
      "monthly_usage_after": 46,
      
      "metadata": {
        "api_response_code": 200,
        "api_endpoint": "/jsearch/search",
        "jobs_skipped_reason": ["invalid_url"],
        "location": "Bangalore, Karnataka"
      }
    }
  ],
  
  "metadata": {
    "total_logs": 1234,
    "success_count": 1200,
    "failure_count": 34,
    "last_updated": "2025-01-17T10:30:00Z"
  }
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | success, failure, partial_success, skipped |
| `request_type` | string | manual, scheduled, refresh |
| `triggered_by` | string | admin email or "system" |
| `jobs_fetched` | number | Total jobs returned from API |
| `jobs_added` | number | New jobs (not duplicates) |
| `jobs_updated` | number | Existing jobs that were refreshed |
| `duration_ms` | number | How long the fetch took |
| `error_code` | string | RATE_LIMIT, INVALID_KEYWORD, TIMEOUT, etc |

### Log Entry Examples

```json
// Success case
{
  "id": "log_001",
  "status": "success",
  "keyword": "python developer",
  "jobs_fetched": 245,
  "jobs_added": 200,
  "error": null,
  "duration_ms": 5432,
  "api_requests_used": 1
}

// Failure case
{
  "id": "log_002",
  "status": "failure",
  "keyword": "invalid keyword",
  "jobs_fetched": 0,
  "error": "Invalid keyword format",
  "error_code": "INVALID_KEYWORD",
  "duration_ms": 234,
  "api_requests_used": 0
}

// Duplicate case
{
  "id": "log_003",
  "status": "skipped",
  "keyword": "python developer",
  "error": "Keyword fetched recently (3 days ago)",
  "error_code": "DUPLICATE_KEYWORD",
  "duration_ms": 50,
  "api_requests_used": 0
}

// Rate limit case
{
  "id": "log_004",
  "status": "failure",
  "error": "Rate limit exceeded",
  "error_code": "RATE_LIMIT",
  "retry_attempt": 2,
  "duration_ms": 15000
}
```

### Retention & Cleanup

```
Policy:
  ├─ Keep logs for 30 days
  ├─ Delete logs older than 30 days
  ├─ Keep failed logs for 60 days (for debugging)
  └─ Archive old logs (optional)

Cleanup CRON:
  ├─ Runs: Daily at 2 AM UTC
  ├─ Query: timestamp < (now - 30 days)
  ├─ Delete: All matching logs
  └─ Log: "Deleted 50 logs older than 30 days"

Manual export:
  ├─ Admin can export logs to CSV
  ├─ Format: timestamp, status, keyword, jobs, error
  └─ Keep backups in archives
```

---

## 5️⃣ USER DATA MODEL (Optional - If Using MongoDB)

### User Schema

```typescript
interface User {
  _id: ObjectId
  email: string
  password: string (hashed)
  role: "user" | "admin"
  profile: {
    name: string
    avatar_url: string
    bio: string
  }
  preferences: {
    notification_email: boolean
    notification_push: boolean
    theme: "light" | "dark"
  }
  saved_jobs: ObjectId[]  // Array of Job IDs
  applications: ObjectId[]  // Array of Application IDs
  created_at: Date
  updated_at: Date
  last_login: Date
}
```

### Saved Jobs Schema

```typescript
interface SavedJob {
  _id: ObjectId
  user_id: ObjectId
  job_id: string  // Reference to jobs.json id
  saved_at: Date
  notes: string
}
```

### Applications Schema

```typescript
interface Application {
  _id: ObjectId
  user_id: ObjectId
  job_id: string
  applied_at: Date
  status: "applied" | "interviewing" | "offered" | "rejected"
  notes: string
  follow_up_date: Date
}
```

---

## 6️⃣ SCHEMA EVOLUTION & VERSIONING

### Version History

```
Version 1.0 (Current)
  ├─ Jobs schema with 20+ fields
  ├─ Keywords with 7-day refresh cycle
  ├─ Usage tracking with monthly reset
  ├─ Scraping logs with 30-day retention
  └─ Date: 2025-01-17

Planned changes:
  ├─ Version 1.1: Add "priority_score" to jobs
  ├─ Version 1.2: Add "user_feedback" to jobs
  └─ Version 2.0: Add PostgreSQL option
```

### Migration Steps (Example)

```typescript
// Upgrading from 1.0 to 1.1: Add priority_score

function migrateJobsV1_0toV1_1(jobs: Job[]): Job[] {
  return jobs.map(job => ({
    ...job,
    priority_score: calculatePriorityScore(job)
  }))
}

// Steps:
1. Read jobs.json v1.0
2. Add priority_score field to each job
3. Save as jobs.json v1.1
4. Update schema_version in metadata
5. Log: "Migration complete: 10,234 jobs upgraded"
```

---

## 7️⃣ VALIDATION RULES

### Job Validation

```typescript
// Required fields that must always be present
validateJobRequired(job) {
  assert(job.id, "Missing id")
  assert(job.title, "Missing title")
  assert(job.company, "Missing company")
  assert(job.apply_url, "Missing apply_url")
  assert(job.source === "openwebninja", "Invalid source")
}

// Format validation
validateJobFormat(job) {
  assert(job.apply_url.match(/^https?:\/\//), "Invalid URL")
  assert(job.salary_min <= job.salary_max, "Salary range invalid")
  assert(job.fetched_at.match(/^\d{4}-\d{2}-\d{2}T/), "Invalid date")
  assert(job.dedup_key.length > 0, "Missing dedup_key")
}

// Uniqueness constraints
validateJobUniqueness(job, allJobs) {
  const duplicate = allJobs.find(j => j.dedup_key === job.dedup_key)
  if (duplicate) {
    job.is_duplicate = true
    job.canonical_id = duplicate.id
  }
}
```

### Keyword Validation

```typescript
validateKeyword(keyword) {
  assert(keyword.length > 0, "Keyword cannot be empty")
  assert(keyword.length < 200, "Keyword too long")
  assert(!keyword.includes(":"), "Invalid characters")
  
  const normalized = keyword.toLowerCase().trim()
  return normalized
}
```

### Usage Validation

```typescript
validateUsage(usage) {
  assert(usage.total_requests >= 0, "Invalid request count")
  assert(usage.total_requests <= 200, "Exceeded free tier")
  assert(usage.remaining_requests === 200 - usage.total_requests, "Math error")
  
  if (usage.total_requests >= 180) {
    assert(usage.hard_limit_triggered === true, "Should be triggered")
  }
}
```

---

## 8️⃣ MIGRATION GUIDE

### From MongoDB to JSON (If Migrating)

```typescript
// Step 1: Export MongoDB jobs
const mongoJobs = await Job.find({}).lean()

// Step 2: Transform to JSON format
const jsonJobs = mongoJobs.map(job => ({
  id: `job_${Date.now()}_${Math.random()}`,
  external_id: job.source_metadata?.external_id || null,
  title: job.title,
  // ... map all fields
  source: job.source || "manual",
  fetched_at: job.created_at?.toISOString(),
  dedup_key: createDedup(job)
}))

// Step 3: Save to JSON
await fs.writeFile('./data/jobs.json', 
  JSON.stringify({ jobs: jsonJobs, metadata: {...} })
)

// Step 4: Verify counts
console.log(`Migrated ${jsonJobs.length} jobs`)
```

### Backup & Recovery

```typescript
// Automatic backup (every 6 hours)
const timestamp = new Date().toISOString().split('T')[0]
const backupFile = `./data/backups/jobs.backup.${timestamp}.json`
await fs.copy('./data/jobs.json', backupFile)

// Recovery (if main file corrupted)
const latestBackup = await fs.readdir('./data/backups')
  .sort()
  .pop()
const recovered = await fs.readFile(latestBackup)
await fs.writeFile('./data/jobs.json', recovered)
```

---

## ✅ SCHEMA CHECKLIST

- [ ] All JSON files have metadata.last_updated
- [ ] All dates are ISO 8601 format
- [ ] All URLs start with http:// or https://
- [ ] All IDs are unique within their collection
- [ ] All required fields are non-empty
- [ ] Dedup keys are consistent
- [ ] Usage totals match calculations
- [ ] Logs are properly archived

---

**Next: See API_ENDPOINTS.md for complete API definitions** 🔗
